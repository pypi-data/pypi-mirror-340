import { c as compilerAssert } from './syntax-utils-DfiQDdeq.js';
import { g as getTypeName, i as isTemplateDeclaration, C as CustomKeyMap } from './custom-key-map-CsDDh10S.js';
import { j as joinPaths } from './path-utils-B4zKWudT.js';
import { e as emitFile } from './emitter-utils-BS8a3nhl.js';
import './misc-97rxrklX.js';

/**
 * Keeps track of a value we don't know yet because of a circular reference. Use
 * the `onValue` method to provide a callback with how to handle the
 * placeholder's value becoming available. Generally the callback will replace
 * this placeholder with the value in whatever references the placeholder.
 */
class Placeholder {
    #listeners = [];
    setValue(value) {
        for (const listener of this.#listeners) {
            listener(value);
        }
    }
    onValue(cb) {
        this.#listeners.push(cb);
    }
}

function scopeChain(scope) {
    const chain = [];
    while (scope) {
        chain.unshift(scope);
        scope = scope.parentScope;
    }
    return chain;
}
/**
 * Resolve relative scopes between the current scope and the target declaration.
 * @param target The target declaration
 * @param currentScope Current scope
 * @returns
 */
function resolveDeclarationReferenceScope(target, currentScope) {
    const targetScope = target.scope;
    const targetChain = scopeChain(targetScope);
    const currentChain = scopeChain(currentScope);
    let diffStart = 0;
    while (targetChain[diffStart] &&
        currentChain[diffStart] &&
        targetChain[diffStart] === currentChain[diffStart]) {
        diffStart++;
    }
    const pathUp = currentChain.slice(diffStart);
    const pathDown = targetChain.slice(diffStart);
    const commonScope = targetChain[diffStart - 1] ?? null;
    return { pathUp, pathDown, commonScope };
}

/**
 * Represent a reference cycle.
 * The cycle entries will always start with a declaration if there is one in the cycle.
 */
class ReferenceCycle {
    /**
     * If this cycle contains a declaration.
     */
    containsDeclaration;
    #entries;
    constructor(entries) {
        const firstDeclarationIndex = entries.findIndex((entry) => entry.entity.kind === "declaration");
        this.containsDeclaration = firstDeclarationIndex !== -1;
        this.#entries = this.containsDeclaration
            ? [...entries.slice(firstDeclarationIndex), ...entries.slice(0, firstDeclarationIndex)]
            : entries;
    }
    get first() {
        return this.#entries[0];
    }
    [Symbol.iterator]() {
        return this.#entries[Symbol.iterator]();
    }
    [Symbol.toStringTag]() {
        return [...this.#entries, this.#entries[0]].map((x) => getTypeName(x.type)).join(" -> ");
    }
    toString() {
        return this[Symbol.toStringTag]();
    }
}

class EmitterResult {
}
class Declaration extends EmitterResult {
    name;
    scope;
    value;
    kind = "declaration";
    meta = {};
    constructor(name, scope, value) {
        if (value instanceof Placeholder) {
            value.onValue((v) => (this.value = v));
        }
        super();
        this.name = name;
        this.scope = scope;
        this.value = value;
    }
}
class RawCode extends EmitterResult {
    value;
    kind = "code";
    constructor(value) {
        if (value instanceof Placeholder) {
            value.onValue((v) => (this.value = v));
        }
        super();
        this.value = value;
    }
}
class NoEmit extends EmitterResult {
    kind = "none";
}
class CircularEmit extends EmitterResult {
    emitEntityKey;
    kind = "circular";
    constructor(emitEntityKey) {
        super();
        this.emitEntityKey = emitEntityKey;
    }
}

function createAssetEmitter(program, TypeEmitterClass, emitContext) {
    const sourceFiles = [];
    const options = {
        noEmit: program.compilerOptions.dryRun ?? false,
        emitterOutputDir: emitContext.emitterOutputDir,
        ...emitContext.options,
    };
    const typeId = CustomKeyMap.objectKeyer();
    const contextId = CustomKeyMap.objectKeyer();
    const entryId = CustomKeyMap.objectKeyer();
    // This is effectively a seen set, ensuring that we don't emit the same
    // type with the same context twice. So the map stores a triple of:
    //
    // 1. the method of TypeEmitter we would call
    // 2. the tsp type we're emitting.
    // 3. the current context.
    //
    // Note that in order for this to work, context needs to be interned so
    // contexts with the same values inside are treated as identical in the
    // map. See createInterner for more details.
    const typeToEmitEntity = new CustomKeyMap(([method, type, context]) => {
        return `${method}-${typeId.getKey(type)}-${contextId.getKey(context)}`;
    });
    // When we encounter a circular reference, this map will hold a callback
    // that should be called when the circularly referenced type has completed
    // its emit.
    const waitingCircularRefs = new CustomKeyMap(([method, type, context]) => {
        return `${method}-${typeId.getKey(type)}-${contextId.getKey(context)}`;
    });
    // Similar to `typeToEmitEntity`, this ensures we don't recompute context
    // for types that we already have context for. Note that context is
    // dependent on the context of the context call, e.g. if a model is
    // referenced with reference context set we need to get its declaration
    // context again. So we use the context's context as a key. Context must
    // be interned, see createInterner for more details.
    const knownContexts = new CustomKeyMap(([entry, context]) => {
        return `${entryId.getKey(entry)}-${contextId.getKey(context)}`;
    });
    // The stack of types that the currently emitted type is lexically
    // contained in. This gets pushed to when we visit a type that is
    // lexically contained in the current type, and is reset when we jump via
    // reference to another type in a different lexical context. Note that
    // this does not correspond to tsp's lexical nesting, e.g. in the case of
    // an alias to a model expression, the alias is lexically outside the
    // model, but in the type graph we will consider it to be lexically inside
    // whatever references the alias.
    let lexicalTypeStack = [];
    let referenceTypeChain = [];
    // Internally, context is is split between lexicalContext and
    // referenceContext because when a reference is made, we carry over
    // referenceContext but leave lexical context behind. When context is
    // accessed by the user, they are merged by getContext().
    let context = {
        lexicalContext: {},
        referenceContext: {},
    };
    let programContext = null;
    // Incoming reference context is reference context that comes from emitting a
    // type reference. Incoming reference context is only set on the
    // incomingReferenceContextTarget and types lexically contained within it. For
    // example, when referencing a model with reference context set, we may need
    // to get context from the referenced model's namespaces, and such namespaces
    // will not see the reference context. However, the reference context will be
    // available for the model, its properties, and any types nested within it
    // (e.g. anonymous models).
    let incomingReferenceContext = null;
    let incomingReferenceContextTarget = null;
    const stateInterner = createInterner();
    const stackEntryInterner = createInterner();
    const assetEmitter = {
        getContext() {
            return {
                ...context.lexicalContext,
                ...context.referenceContext,
            };
        },
        getOptions() {
            return options;
        },
        getProgram() {
            return program;
        },
        result: {
            declaration(name, value) {
                const scope = currentScope();
                compilerAssert(scope, "Emit context must have a scope set in order to create declarations. Consider setting scope to a new source file's global scope in the `programContext` method of `TypeEmitter`.");
                return new Declaration(name, scope, value);
            },
            rawCode(value) {
                return new RawCode(value);
            },
            none() {
                return new NoEmit();
            },
        },
        createScope(block, name, parentScope = null) {
            let newScope;
            if (!parentScope) {
                // create source file scope
                newScope = {
                    kind: "sourceFile",
                    name,
                    sourceFile: block,
                    parentScope,
                    childScopes: [],
                    declarations: [],
                };
            }
            else {
                newScope = {
                    kind: "namespace",
                    name,
                    namespace: block,
                    childScopes: [],
                    declarations: [],
                    parentScope,
                };
            }
            parentScope?.childScopes.push(newScope);
            return newScope; // the overload of createScope causes type weirdness
        },
        createSourceFile(path) {
            const basePath = options.emitterOutputDir;
            const sourceFile = {
                globalScope: undefined,
                path: joinPaths(basePath, path),
                imports: new Map(),
                meta: {},
            };
            sourceFile.globalScope = this.createScope(sourceFile, "");
            sourceFiles.push(sourceFile);
            return sourceFile;
        },
        emitTypeReference(target, options) {
            return withPatchedReferenceContext(options?.referenceContext, () => {
                const oldIncomingReferenceContext = incomingReferenceContext;
                const oldIncomingReferenceContextTarget = incomingReferenceContextTarget;
                incomingReferenceContext = context.referenceContext ?? null;
                incomingReferenceContextTarget = incomingReferenceContext ? target : null;
                let result;
                if (target.kind === "ModelProperty") {
                    result = invokeTypeEmitter("modelPropertyReference", target);
                }
                else if (target.kind === "EnumMember") {
                    result = invokeTypeEmitter("enumMemberReference", target);
                }
                if (result) {
                    incomingReferenceContext = oldIncomingReferenceContext;
                    incomingReferenceContextTarget = oldIncomingReferenceContextTarget;
                    return result;
                }
                const entity = this.emitType(target);
                incomingReferenceContext = oldIncomingReferenceContext;
                incomingReferenceContextTarget = oldIncomingReferenceContextTarget;
                let placeholder = null;
                if (entity.kind === "circular") {
                    let waiting = waitingCircularRefs.get(entity.emitEntityKey);
                    if (!waiting) {
                        waiting = [];
                        waitingCircularRefs.set(entity.emitEntityKey, waiting);
                    }
                    const typeChainSnapshot = referenceTypeChain;
                    waiting.push({
                        state: {
                            lexicalTypeStack,
                            context,
                        },
                        cb: (resolvedEntity) => invokeReference(this, resolvedEntity, true, resolveReferenceCycle(typeChainSnapshot, entity, typeToEmitEntity)),
                    });
                    placeholder = new Placeholder();
                    return this.result.rawCode(placeholder);
                }
                else {
                    return invokeReference(this, entity, false);
                }
                function invokeReference(assetEmitter, entity, circular, cycle) {
                    let ref;
                    const scope = currentScope();
                    if (circular) {
                        ref = typeEmitter.circularReference(entity, scope, cycle);
                    }
                    else {
                        if (entity.kind !== "declaration") {
                            return entity;
                        }
                        compilerAssert(scope, "Emit context must have a scope set in order to create references to declarations.");
                        const { pathUp, pathDown, commonScope } = resolveDeclarationReferenceScope(entity, scope);
                        ref = typeEmitter.reference(entity, pathUp, pathDown, commonScope);
                    }
                    if (!(ref instanceof EmitterResult)) {
                        ref = assetEmitter.result.rawCode(ref);
                    }
                    if (placeholder) {
                        // this should never happen as this function shouldn't be called until
                        // the target declaration is finished being emitted.
                        compilerAssert(ref.kind !== "circular", "TypeEmitter `reference` returned circular emit");
                        // this could presumably be allowed if we want.
                        compilerAssert(ref.kind === "none" || !(ref.value instanceof Placeholder), "TypeEmitter's `reference` method cannot return a placeholder.");
                        switch (ref.kind) {
                            case "code":
                            case "declaration":
                                placeholder.setValue(ref.value);
                                break;
                            case "none":
                                // this cast is incorrect, think about what should happen
                                // if reference returns noEmit...
                                placeholder.setValue("");
                                break;
                        }
                    }
                    return ref;
                }
            });
        },
        emitDeclarationName(type) {
            return typeEmitter.declarationName(type);
        },
        async writeOutput() {
            return typeEmitter.writeOutput(sourceFiles);
        },
        getSourceFiles() {
            return sourceFiles;
        },
        emitType(type, context) {
            if (context?.referenceContext) {
                incomingReferenceContext = context?.referenceContext ?? incomingReferenceContext;
                incomingReferenceContextTarget = type ?? incomingReferenceContextTarget;
            }
            const declName = isDeclaration(type) && type.kind !== "Namespace" ? typeEmitter.declarationName(type) : null;
            const key = typeEmitterKey(type);
            let args;
            switch (key) {
                case "scalarDeclaration":
                case "scalarInstantiation":
                case "modelDeclaration":
                case "modelInstantiation":
                case "operationDeclaration":
                case "interfaceDeclaration":
                case "interfaceOperationDeclaration":
                case "enumDeclaration":
                case "unionDeclaration":
                case "unionInstantiation":
                    args = [declName];
                    break;
                case "arrayDeclaration":
                    const arrayDeclElement = type.indexer.value;
                    args = [declName, arrayDeclElement];
                    break;
                case "arrayLiteral":
                    const arrayLiteralElement = type.indexer.value;
                    args = [arrayLiteralElement];
                    break;
                case "intrinsic":
                    args = [declName];
                    break;
                default:
                    args = [];
            }
            const result = invokeTypeEmitter(key, type, ...args);
            return result;
        },
        emitProgram(options) {
            const namespace = program.getGlobalNamespaceType();
            if (options?.emitGlobalNamespace) {
                this.emitType(namespace);
                return;
            }
            for (const ns of namespace.namespaces.values()) {
                if (ns.name === "TypeSpec" && !options?.emitTypeSpecNamespace)
                    continue;
                this.emitType(ns);
            }
            for (const model of namespace.models.values()) {
                if (!isTemplateDeclaration(model)) {
                    this.emitType(model);
                }
            }
            for (const operation of namespace.operations.values()) {
                if (!isTemplateDeclaration(operation)) {
                    this.emitType(operation);
                }
            }
            for (const enumeration of namespace.enums.values()) {
                this.emitType(enumeration);
            }
            for (const union of namespace.unions.values()) {
                if (!isTemplateDeclaration(union)) {
                    this.emitType(union);
                }
            }
            for (const iface of namespace.interfaces.values()) {
                if (!isTemplateDeclaration(iface)) {
                    this.emitType(iface);
                }
            }
            for (const scalar of namespace.scalars.values()) {
                this.emitType(scalar);
            }
        },
        emitModelProperties(model) {
            const res = invokeTypeEmitter("modelProperties", model);
            if (res instanceof EmitterResult) {
                return res;
            }
            else {
                return this.result.rawCode(res);
            }
        },
        emitModelProperty(property) {
            return invokeTypeEmitter("modelPropertyLiteral", property);
        },
        emitOperationParameters(operation) {
            return invokeTypeEmitter("operationParameters", operation, operation.parameters);
        },
        emitOperationReturnType(operation) {
            return invokeTypeEmitter("operationReturnType", operation, operation.returnType);
        },
        emitInterfaceOperations(iface) {
            return invokeTypeEmitter("interfaceDeclarationOperations", iface);
        },
        emitInterfaceOperation(operation) {
            const name = typeEmitter.declarationName(operation);
            if (name === undefined) {
                // the general approach of invoking the expression form doesn't work here
                // because TypeSpec doesn't have operation expressions.
                compilerAssert(false, "Unnamed operations are not supported");
            }
            return invokeTypeEmitter("interfaceOperationDeclaration", operation, name);
        },
        emitEnumMembers(en) {
            return invokeTypeEmitter("enumMembers", en);
        },
        emitUnionVariants(union) {
            return invokeTypeEmitter("unionVariants", union);
        },
        emitTupleLiteralValues(tuple) {
            return invokeTypeEmitter("tupleLiteralValues", tuple);
        },
        async emitSourceFile(sourceFile) {
            return await typeEmitter.sourceFile(sourceFile);
        },
    };
    const typeEmitter = new TypeEmitterClass(assetEmitter);
    return assetEmitter;
    /**
     * This function takes care of calling a method on the TypeEmitter to
     * convert it to some emitted output. It will return a cached type if we
     * have seen it before (and the context is the same). It will establish
     * the emit context by calling the appropriate methods before getting the
     * emit result. Also if a type emitter returns just a T or a
     * Placeholder<T>, it will convert that to a RawCode result.
     */
    function invokeTypeEmitter(method, ...args) {
        const type = args[0];
        let entity;
        let emitEntityKey;
        let cached = false;
        withTypeContext(method, args, () => {
            emitEntityKey = [method, type, context];
            const seenEmitEntity = typeToEmitEntity.get(emitEntityKey);
            if (seenEmitEntity) {
                entity = seenEmitEntity;
                cached = true;
                return;
            }
            typeToEmitEntity.set(emitEntityKey, new CircularEmit(emitEntityKey));
            compilerAssert(typeEmitter[method], `TypeEmitter doesn't have a method named ${method}.`);
            entity = liftToRawCode(typeEmitter[method](...args));
        });
        if (cached) {
            return entity;
        }
        if (entity instanceof Placeholder) {
            entity.onValue((v) => handleCompletedEntity(v));
            return entity;
        }
        handleCompletedEntity(entity);
        return entity;
        function handleCompletedEntity(entity) {
            typeToEmitEntity.set(emitEntityKey, entity);
            const waitingRefCbs = waitingCircularRefs.get(emitEntityKey);
            if (waitingRefCbs) {
                for (const record of waitingRefCbs) {
                    withContext(record.state, () => {
                        record.cb(entity);
                    });
                }
                waitingCircularRefs.set(emitEntityKey, []);
            }
            if (entity.kind === "declaration") {
                entity.scope.declarations.push(entity);
            }
        }
        function liftToRawCode(value) {
            if (value instanceof EmitterResult) {
                return value;
            }
            return assetEmitter.result.rawCode(value);
        }
    }
    function isInternalMethod(method) {
        return (method === "interfaceDeclarationOperations" ||
            method === "interfaceOperationDeclaration" ||
            method === "operationParameters" ||
            method === "operationReturnType" ||
            method === "modelProperties" ||
            method === "enumMembers" ||
            method === "tupleLiteralValues" ||
            method === "unionVariants");
    }
    /**
     * This helper takes a type and sets the `context` state to what it should
     * be in order to invoke the type emitter method for that type. This needs
     * to take into account the current context and any incoming reference
     * context.
     */
    function setContextForType(method, args) {
        const type = args[0];
        let newTypeStack;
        // if we've walked into a new declaration, reset the lexical type stack
        // to the lexical containers of the current type.
        if (isDeclaration(type) && type.kind !== "Intrinsic" && !isInternalMethod(method)) {
            newTypeStack = [stackEntryInterner.intern({ method, args: stackEntryInterner.intern(args) })];
            let ns = type.namespace;
            while (ns) {
                if (ns.name === "")
                    break;
                newTypeStack.unshift(stackEntryInterner.intern({ method: "namespace", args: stackEntryInterner.intern([ns]) }));
                ns = ns.namespace;
            }
        }
        else {
            newTypeStack = [
                ...lexicalTypeStack,
                stackEntryInterner.intern({ method, args: stackEntryInterner.intern(args) }),
            ];
        }
        lexicalTypeStack = newTypeStack;
        if (!programContext) {
            programContext = stateInterner.intern({
                lexicalContext: typeEmitter.programContext(program),
                referenceContext: stateInterner.intern({}),
            });
        }
        // Establish our context by starting from program and walking up the type stack
        // and merging in context for each of the lexical containers.
        context = programContext;
        for (const entry of lexicalTypeStack) {
            if (incomingReferenceContext && entry.args[0] === incomingReferenceContextTarget) {
                // bring in any reference context so it is available for any types nested beneath this type.
                context = stateInterner.intern({
                    lexicalContext: context.lexicalContext,
                    referenceContext: stateInterner.intern({
                        ...context.referenceContext,
                        ...incomingReferenceContext,
                    }),
                });
            }
            const seenContext = knownContexts.get([entry, context]);
            if (seenContext) {
                context = seenContext;
                continue;
            }
            const lexicalKey = entry.method + "Context";
            const referenceKey = entry.method + "ReferenceContext";
            if (keyHasContext(entry.method)) {
                compilerAssert(typeEmitter[lexicalKey], `TypeEmitter doesn't have a method named ${lexicalKey}`);
            }
            if (keyHasReferenceContext(entry.method)) {
                compilerAssert(typeEmitter[referenceKey], `TypeEmitter doesn't have a method named ${referenceKey}`);
            }
            const newContext = keyHasContext(entry.method)
                ? typeEmitter[lexicalKey](...entry.args)
                : {};
            const newReferenceContext = keyHasReferenceContext(entry.method)
                ? typeEmitter[referenceKey](...entry.args)
                : {};
            // assemble our new reference and lexical contexts.
            const newContextState = stateInterner.intern({
                lexicalContext: stateInterner.intern({
                    ...context.lexicalContext,
                    ...newContext,
                }),
                referenceContext: stateInterner.intern({
                    ...context.referenceContext,
                    ...newReferenceContext,
                }),
            });
            knownContexts.set([entry, context], newContextState);
            context = newContextState;
        }
        if (!isInternalMethod(method)) {
            referenceTypeChain = [
                ...referenceTypeChain,
                stackEntryInterner.intern({
                    method,
                    type,
                    context,
                }),
            ];
        }
    }
    /**
     * Invoke the callback with the proper context for a given type.
     */
    function withTypeContext(method, args, cb) {
        const oldContext = context;
        const oldTypeStack = lexicalTypeStack;
        const oldRefTypeStack = referenceTypeChain;
        setContextForType(method, args);
        cb();
        context = oldContext;
        lexicalTypeStack = oldTypeStack;
        referenceTypeChain = oldRefTypeStack;
    }
    function withPatchedReferenceContext(referenceContext, cb) {
        if (referenceContext !== undefined) {
            const oldContext = context;
            context = stateInterner.intern({
                lexicalContext: context.lexicalContext,
                referenceContext: stateInterner.intern({
                    ...context.referenceContext,
                    ...referenceContext,
                }),
            });
            const result = cb();
            context = oldContext;
            return result;
        }
        else {
            return cb();
        }
    }
    /**
     * Invoke the callback with the given context.
     */
    function withContext(newContext, cb) {
        const oldContext = context;
        const oldTypeStack = lexicalTypeStack;
        context = newContext.context;
        lexicalTypeStack = newContext.lexicalTypeStack;
        cb();
        context = oldContext;
        lexicalTypeStack = oldTypeStack;
    }
    function typeEmitterKey(type) {
        switch (type.kind) {
            case "Model":
                if (program.checker.isStdType(type) && type.name === "Array") {
                    // likely an array literal, though could be a bare reference to Array maybe?
                    return "arrayLiteral";
                }
                if (type.name === "") {
                    return "modelLiteral";
                }
                if (type.templateMapper) {
                    return "modelInstantiation";
                }
                if (type.indexer && type.indexer.key.name === "integer") {
                    return "arrayDeclaration";
                }
                return "modelDeclaration";
            case "Namespace":
                return "namespace";
            case "ModelProperty":
                return "modelPropertyLiteral";
            case "StringTemplate":
                return "stringTemplate";
            case "Boolean":
                return "booleanLiteral";
            case "String":
                return "stringLiteral";
            case "Number":
                return "numericLiteral";
            case "Operation":
                if (type.interface) {
                    return "interfaceOperationDeclaration";
                }
                else {
                    return "operationDeclaration";
                }
            case "Interface":
                return "interfaceDeclaration";
            case "Enum":
                return "enumDeclaration";
            case "EnumMember":
                return "enumMember";
            case "Union":
                if (!type.name) {
                    return "unionLiteral";
                }
                if (type.templateMapper) {
                    return "unionInstantiation";
                }
                return "unionDeclaration";
            case "UnionVariant":
                return "unionVariant";
            case "Tuple":
                return "tupleLiteral";
            case "Scalar":
                if (type.templateMapper) {
                    return "scalarInstantiation";
                }
                else {
                    return "scalarDeclaration";
                }
            case "Intrinsic":
                return "intrinsic";
            default:
                compilerAssert(false, `Encountered type ${type.kind} which we don't know how to emit.`);
        }
    }
    function currentScope() {
        return context.referenceContext?.scope ?? context.lexicalContext?.scope ?? null;
    }
}
/**
 * Returns true if the given type is a declaration or an instantiation of a declaration.
 * @param type
 * @returns
 */
function isDeclaration(type) {
    switch (type.kind) {
        case "Namespace":
        case "Interface":
        case "Enum":
        case "Operation":
        case "Scalar":
        case "Intrinsic":
            return true;
        case "Model":
            return type.name ? type.name !== "" && type.name !== "Array" : false;
        case "Union":
            return type.name ? type.name !== "" : false;
        default:
            return false;
    }
}
/**
 * An interner takes an object and returns either that same object, or a
 * previously seen object that has the identical shape.
 *
 * This implementation is EXTREMELY non-optimal (O(n*m) where n = number of unique
 * state objects and m = the number of properties a state object contains). This
 * will very quickly be a bottleneck. That said, the common case is no state at
 * all, and also this is essentially implementing records and tuples, so could
 * probably adopt those when they are released. That that said, the records and
 * tuples are presently facing headwinds due to implementations facing exactly
 * these performance characteristics. Regardless, there are optimizations we
 * could consider.
 */
function createInterner() {
    const emptyObject = {};
    const knownKeys = new Map();
    return {
        intern(object) {
            const keys = Object.keys(object);
            const keyLen = keys.length;
            if (keyLen === 0)
                return emptyObject;
            // Find an object set with minimum size by object keys
            let knownObjects = new Set();
            let minSize = Infinity;
            for (const objs of keys.map((key) => knownKeys.get(key))) {
                if (objs && objs.size < minSize) {
                    knownObjects = objs;
                    minSize = objs.size;
                }
            }
            // Now find a known object from the found smallest object set
            for (const ko of knownObjects) {
                const entries = Object.entries(ko);
                if (entries.length !== keyLen)
                    continue;
                let found = true;
                for (const [key, value] of entries) {
                    if (object[key] !== value) {
                        found = false;
                        break;
                    }
                }
                if (found) {
                    return ko;
                }
            }
            // If the object is not known, add all keys as known
            for (const key of keys) {
                const ko = knownKeys.get(key);
                if (ko) {
                    ko.add(object);
                }
                else {
                    knownKeys.set(key, new Set([object]));
                }
            }
            return object;
        },
    };
}
const noContext = new Set(["modelPropertyReference", "enumMemberReference"]);
function keyHasContext(key) {
    return !noContext.has(key);
}
const noReferenceContext = new Set([
    ...noContext,
    "booleanLiteral",
    "stringTemplate",
    "stringLiteral",
    "numericLiteral",
    "scalarInstantiation",
    "enumMember",
    "enumMembers",
    "intrinsic",
]);
function keyHasReferenceContext(key) {
    return !noReferenceContext.has(key);
}
function resolveReferenceCycle(stack, entity, typeToEmitEntity) {
    for (let i = stack.length - 1; i >= 0; i--) {
        if (stack[i].type === entity.emitEntityKey[1]) {
            return new ReferenceCycle(stack.slice(i).map((x) => {
                return {
                    type: x.type,
                    entity: typeToEmitEntity.get([x.method, x.type, x.context]),
                };
            }));
        }
    }
    throw new Error(`Couldn't resolve the circular reference stack for ${getTypeName(entity.emitEntityKey[1])}`);
}

class ArrayBuilder extends Array {
    #setPlaceholderValue(p, value) {
        for (const [i, item] of this.entries()) {
            if (item === p) {
                this[i] = value;
            }
        }
    }
    push(...values) {
        for (const v of values) {
            let toPush;
            if (v instanceof EmitterResult) {
                compilerAssert(v.kind !== "circular", "Can't push a circular emit result.");
                if (v.kind === "none") {
                    toPush = undefined;
                }
                else {
                    toPush = v.value;
                }
            }
            else {
                toPush = v;
            }
            if (toPush instanceof Placeholder) {
                toPush.onValue((v) => this.#setPlaceholderValue(toPush, v));
            }
            super.push(toPush);
        }
        return values.length;
    }
}

const placeholderSym = Symbol("placeholder");
// eslint-disable-next-line @typescript-eslint/no-unsafe-declaration-merging
class ObjectBuilder {
    [placeholderSym];
    constructor(initializer = {}) {
        const copyProperties = (source) => {
            for (const [key, value] of Object.entries(source)) {
                this.set(key, value);
            }
        };
        const registerPlaceholder = (placeholder) => {
            placeholder.onValue(copyProperties);
        };
        if (initializer instanceof ObjectBuilder) {
            if (initializer[placeholderSym]) {
                this[placeholderSym] = initializer[placeholderSym];
                registerPlaceholder(initializer[placeholderSym]);
            }
            copyProperties(initializer);
        }
        else if (initializer instanceof Placeholder) {
            this[placeholderSym] = initializer;
            registerPlaceholder(initializer);
        }
        else {
            copyProperties(initializer);
        }
    }
    set(key, v) {
        let value = v;
        if (v instanceof EmitterResult) {
            compilerAssert(v.kind !== "circular", "Can't set a circular emit result.");
            if (v.kind === "none") {
                this[key] = undefined;
                return;
            }
            else {
                value = v.value;
            }
        }
        if (value instanceof Placeholder) {
            value.onValue((v) => {
                this[key] = v;
            });
        }
        this[key] = value;
    }
}

class StringBuilder extends Placeholder {
    segments = [];
    #placeholders = new Set();
    #notifyComplete() {
        const value = this.segments.join("");
        this.setValue(value);
    }
    #setPlaceholderValue(ph, value) {
        for (const [i, segment] of this.segments.entries()) {
            if (segment === ph) {
                this.segments[i] = value;
            }
        }
        this.#placeholders.delete(ph);
        if (this.#placeholders.size === 0) {
            this.#notifyComplete();
        }
    }
    pushLiteralSegment(segment) {
        if (this.#shouldConcatLiteral()) {
            this.segments[this.segments.length - 1] += segment;
        }
        else {
            this.segments.push(segment);
        }
    }
    pushPlaceholder(ph) {
        this.#placeholders.add(ph);
        ph.onValue((value) => {
            this.#setPlaceholderValue(ph, value);
        });
        this.segments.push(ph);
    }
    pushStringBuilder(builder) {
        for (const segment of builder.segments) {
            this.push(segment);
        }
    }
    push(segment) {
        if (typeof segment === "string") {
            this.pushLiteralSegment(segment);
        }
        else if (segment instanceof StringBuilder) {
            this.pushStringBuilder(segment);
        }
        else {
            this.pushPlaceholder(segment);
        }
    }
    reduce() {
        if (this.#placeholders.size === 0) {
            return this.segments.join("");
        }
        return this;
    }
    #shouldConcatLiteral() {
        return this.segments.length > 0 && typeof this.segments[this.segments.length - 1] === "string";
    }
}
function code(parts, ...substitutions) {
    const builder = new StringBuilder();
    for (const [i, literalPart] of parts.entries()) {
        builder.push(literalPart);
        if (i < substitutions.length) {
            const sub = substitutions[i];
            if (typeof sub === "string") {
                builder.push(sub);
            }
            else if (sub instanceof StringBuilder) {
                builder.pushStringBuilder(sub);
            }
            else if (sub instanceof Placeholder) {
                builder.pushPlaceholder(sub);
            }
            else {
                switch (sub.kind) {
                    case "circular":
                    case "none":
                        builder.pushLiteralSegment("");
                        break;
                    default:
                        builder.push(sub.value);
                }
            }
        }
    }
    return builder.reduce();
}

/**
 * Implement emitter logic by extending this class and passing it to
 * `emitContext.createAssetEmitter`. This class should not be constructed
 * directly.
 *
 * TypeEmitters serve two primary purposes:
 *
 * 1. Handle emitting TypeSpec types into other languages
 * 2. Set emitter context
 *
 * The generic type parameter `T` is the type you expect to produce for each TypeSpec type.
 * In the case of generating source code for a programming language, this is probably `string`
 * (in which case, consider using the `CodeTypeEmitter`) but might also be an AST node. If you
 * are emitting JSON or similar, `T` would likely be `object`.
 *
 * ## Emitting types
 *
 * Emitting TypeSpec types into other languages is accomplished by implementing
 * the AssetEmitter method that corresponds with the TypeSpec type you are
 * emitting. For example, to emit a TypeSpec model declaration, implement the
 * `modelDeclaration` method.
 *
 * TypeSpec types that have both declaration and literal forms like models or
 * unions will have separate methods. For example, models have both
 * `modelDeclaration` and `modelLiteral` methods that can be implemented
 * separately.
 *
 * Also, types which can be instantiated like models or operations have a
 * separate method for the instantiated type. For example, models have a
 * `modelInstantiation` method that gets called with such types. Generally these
 * will be treated either as if they were declarations or literals depending on
 * preference, but may also be treated specially.
 *
 * ## Emitter results
 * There are three kinds of results your methods might return - declarations,
 * raw code, or nothing.
 *
 * ### Declarations
 *
 * Create declarations by calling `this.emitter.result.declaration` passing it a
 * name and the emit output for the declaration. Note that you must have scope
 * in your context or you will get an error. If you want all declarations to be
 * emitted to the same source file, you can create a single scope in
 * `programContext` via something like:
 *
 * ```typescript
 * programContext(program: Program): Context {
 *   const sourceFile = this.emitter.createSourceFile("test.txt");
 *   return {
 *     scope: sourceFile.globalScope,
 *   };
 * }
 * ```
 *
 * ### Raw Code
 *
 * Create raw code, or emitter output that doesn't contribute to a declaration,
 * by calling `this.emitter.result.rawCode` passing it a value. Returning just a
 * value is considered raw code and so you often don't need to call this
 * directly.
 *
 * ### No Emit
 *
 * When a type doesn't contribute anything to the emitted output, return
 * `this.emitter.result.none()`.
 *
 * ## Context
 *
 * The TypeEmitter will often want to keep track of what context a type is found
 * in. There are two kinds of context - lexical context, and reference context.
 *
 * * Lexical context is context that applies to the type and every type
 *   contained inside of it. For example, lexical context for a model will apply
 *   to the model, its properties, and any nested model literals.
 * * Reference context is context that applies to types contained inside of the
 *   type and referenced anywhere inside of it. For example, reference context
 *   set on a model will apply to the model, its properties, any nested model
 *   literals, and any type referenced inside anywhere inside the model and any
 *   of the referenced types' references.
 *
 * In both cases, context is an object. It's strongly recommended that the context
 * object either contain only primitive types, or else only reference immutable
 * objects.
 *
 * Set lexical by implementing the `*Context` methods of the TypeEmitter and
 * returning the context, for example `modelDeclarationContext` sets the context
 * for model declarations and the types contained inside of it.
 *
 * Set reference context by implementing the `*ReferenceContext` methods of the
 * TypeEmitter and returning the context. Note that not all types have reference
 * context methods, because not all types can actually reference anything.
 *
 * When a context method returns some context, it is merged with the current
 * context. It is not possible to remove previous context, but it can be
 * overridden with `undefined`.
 *
 * When emitting types with context, the same type might be emitted multiple
 * times if we come across that type with different contexts. For example, if we
 * have a TypeSpec program like
 *
 * ```typespec
 * model Pet { }
 * model Person {
 *   pet: Pet;
 * }
 * ```
 *
 * And we set reference context for the Person model, Pet will be emitted twice,
 * once without context and once with the reference context.
 */
class TypeEmitter {
    emitter;
    /**
     * @private
     *
     * Constructs a TypeEmitter. Do not use this constructor directly, instead
     * call `createAssetEmitter` on the emitter context object.
     * @param emitter The asset emitter
     */
    constructor(emitter) {
        this.emitter = emitter;
    }
    /**
     * Context shared by the entire program. In cases where you are emitting to a
     * single file, use this method to establish your main source file and set the
     * `scope` property to that source file's `globalScope`.
     * @param program
     * @returns Context
     */
    programContext(program) {
        return {};
    }
    /**
     * Emit a namespace
     *
     * @param namespace
     * @returns Emitter output
     */
    namespace(namespace) {
        for (const ns of namespace.namespaces.values()) {
            this.emitter.emitType(ns);
        }
        for (const model of namespace.models.values()) {
            if (!isTemplateDeclaration(model)) {
                this.emitter.emitType(model);
            }
        }
        for (const operation of namespace.operations.values()) {
            if (!isTemplateDeclaration(operation)) {
                this.emitter.emitType(operation);
            }
        }
        for (const enumeration of namespace.enums.values()) {
            this.emitter.emitType(enumeration);
        }
        for (const union of namespace.unions.values()) {
            if (!isTemplateDeclaration(union)) {
                this.emitter.emitType(union);
            }
        }
        for (const iface of namespace.interfaces.values()) {
            if (!isTemplateDeclaration(iface)) {
                this.emitter.emitType(iface);
            }
        }
        for (const scalar of namespace.scalars.values()) {
            this.emitter.emitType(scalar);
        }
        return this.emitter.result.none();
    }
    /**
     * Set lexical context for a namespace
     *
     * @param namespace
     */
    namespaceContext(namespace) {
        return {};
    }
    /**
     * Set reference context for a namespace.
     *
     * @param namespace
     */
    namespaceReferenceContext(namespace) {
        return {};
    }
    /**
     * Emit a model literal (e.g. as created by `{}` syntax in TypeSpec).
     *
     * @param model
     */
    modelLiteral(model) {
        if (model.baseModel) {
            this.emitter.emitType(model.baseModel);
        }
        this.emitter.emitModelProperties(model);
        return this.emitter.result.none();
    }
    /**
     * Set lexical context for a model literal.
     * @param model
     */
    modelLiteralContext(model) {
        return {};
    }
    /**
     * Set reference context for a model literal.
     * @param model
     */
    modelLiteralReferenceContext(model) {
        return {};
    }
    /**
     * Emit a model declaration (e.g. as created by `model Foo { }` syntax in
     * TypeSpec).
     *
     * @param model
     */
    modelDeclaration(model, name) {
        if (model.baseModel) {
            this.emitter.emitType(model.baseModel);
        }
        this.emitter.emitModelProperties(model);
        return this.emitter.result.none();
    }
    /**
     * Set lexical context for a model declaration.
     *
     * @param model
     * @param name the model's declaration name as retrieved from the
     * `declarationName` method.
     */
    modelDeclarationContext(model, name) {
        return {};
    }
    /**
     * Set reference context for a model declaration.
     * @param model
     */
    modelDeclarationReferenceContext(model, name) {
        return {};
    }
    /**
     * Emit a model instantiation (e.g. as created by `Box<string>` syntax in
     * TypeSpec). In some cases, `name` is undefined because a good name could
     * not be found for the instantiation. This often occurs with for instantiations
     * involving type expressions like `Box<string | int32>`.
     *
     * @param model
     * @param name The name of the instantiation as retrieved from the
     * `declarationName` method.
     */
    modelInstantiation(model, name) {
        if (model.baseModel) {
            this.emitter.emitType(model.baseModel);
        }
        this.emitter.emitModelProperties(model);
        return this.emitter.result.none();
    }
    /**
     * Set lexical context for a model instantiation.
     * @param model
     */
    modelInstantiationContext(model, name) {
        return {};
    }
    /**
     * Set reference context for a model declaration.
     * @param model
     */
    modelInstantiationReferenceContext(model, name) {
        return {};
    }
    /**
     * Emit a model's properties. Unless overridden, this method will emit each of
     * the model's properties and return a no emit result.
     *
     * @param model
     */
    modelProperties(model) {
        for (const prop of model.properties.values()) {
            this.emitter.emitModelProperty(prop);
        }
        return this.emitter.result.none();
    }
    modelPropertiesContext(model) {
        return {};
    }
    modelPropertiesReferenceContext(model) {
        return {};
    }
    /**
     * Emit a property of a model.
     *
     * @param property
     */
    modelPropertyLiteral(property) {
        this.emitter.emitTypeReference(property.type);
        return this.emitter.result.none();
    }
    /**
     * Set lexical context for a property of a model.
     *
     * @param property
     */
    modelPropertyLiteralContext(property) {
        return {};
    }
    /**
     * Set reference context for a property of a model.
     *
     * @param property
     */
    modelPropertyLiteralReferenceContext(property) {
        return {};
    }
    /**
     * Emit a model property reference (e.g. as created by the `SomeModel.prop`
     * syntax in TypeSpec). By default, this will emit the type of the referenced
     * property and return that result. In other words, the emit will look as if
     * `SomeModel.prop` were replaced with the type of `prop`.
     *
     * @param property
     */
    modelPropertyReference(property) {
        return this.emitter.emitTypeReference(property.type);
    }
    /**
     * Emit an enum member reference (e.g. as created by the `SomeEnum.member` syntax
     * in TypeSpec). By default, this will emit nothing.
     *
     * @param property the enum member
     */
    enumMemberReference(member) {
        return this.emitter.result.none();
    }
    arrayDeclaration(array, name, elementType) {
        this.emitter.emitType(array.indexer.value);
        return this.emitter.result.none();
    }
    arrayDeclarationContext(array, name, elementType) {
        return {};
    }
    arrayDeclarationReferenceContext(array, name, elementType) {
        return {};
    }
    arrayLiteral(array, elementType) {
        return this.emitter.result.none();
    }
    arrayLiteralContext(array, elementType) {
        return {};
    }
    arrayLiteralReferenceContext(array, elementType) {
        return {};
    }
    scalarDeclaration(scalar, name) {
        if (scalar.baseScalar) {
            this.emitter.emitType(scalar.baseScalar);
        }
        return this.emitter.result.none();
    }
    scalarDeclarationContext(scalar, name) {
        return {};
    }
    scalarDeclarationReferenceContext(scalar, name) {
        return {};
    }
    scalarInstantiation(scalar, name) {
        return this.emitter.result.none();
    }
    scalarInstantiationContext(scalar, name) {
        return {};
    }
    intrinsic(intrinsic, name) {
        return this.emitter.result.none();
    }
    intrinsicContext(intrinsic, name) {
        return {};
    }
    booleanLiteralContext(boolean) {
        return {};
    }
    booleanLiteral(boolean) {
        return this.emitter.result.none();
    }
    stringTemplateContext(string) {
        return {};
    }
    stringTemplate(stringTemplate) {
        return this.emitter.result.none();
    }
    stringLiteralContext(string) {
        return {};
    }
    stringLiteral(string) {
        return this.emitter.result.none();
    }
    numericLiteralContext(number) {
        return {};
    }
    numericLiteral(number) {
        return this.emitter.result.none();
    }
    operationDeclaration(operation, name) {
        this.emitter.emitOperationParameters(operation);
        this.emitter.emitOperationReturnType(operation);
        return this.emitter.result.none();
    }
    operationDeclarationContext(operation, name) {
        return {};
    }
    operationDeclarationReferenceContext(operation, name) {
        return {};
    }
    interfaceDeclarationOperationsContext(iface) {
        return {};
    }
    interfaceDeclarationOperationsReferenceContext(iface) {
        return {};
    }
    interfaceOperationDeclarationContext(operation, name) {
        return {};
    }
    interfaceOperationDeclarationReferenceContext(operation, name) {
        return {};
    }
    operationParameters(operation, parameters) {
        return this.emitter.result.none();
    }
    operationParametersContext(operation, parameters) {
        return {};
    }
    operationParametersReferenceContext(operation, parameters) {
        return {};
    }
    operationReturnType(operation, returnType) {
        return this.emitter.result.none();
    }
    operationReturnTypeContext(operation, returnType) {
        return {};
    }
    operationReturnTypeReferenceContext(operation, returnType) {
        return {};
    }
    interfaceDeclaration(iface, name) {
        this.emitter.emitInterfaceOperations(iface);
        return this.emitter.result.none();
    }
    interfaceDeclarationContext(iface, name) {
        return {};
    }
    interfaceDeclarationReferenceContext(iface, name) {
        return {};
    }
    interfaceDeclarationOperations(iface) {
        for (const op of iface.operations.values()) {
            this.emitter.emitInterfaceOperation(op);
        }
        return this.emitter.result.none();
    }
    interfaceOperationDeclaration(operation, name) {
        this.emitter.emitOperationParameters(operation);
        this.emitter.emitOperationReturnType(operation);
        return this.emitter.result.none();
    }
    enumDeclaration(en, name) {
        this.emitter.emitEnumMembers(en);
        return this.emitter.result.none();
    }
    enumDeclarationContext(en, name) {
        return {};
    }
    enumDeclarationReferenceContext(en, name) {
        return {};
    }
    enumMembers(en) {
        for (const member of en.members.values()) {
            this.emitter.emitType(member);
        }
        return this.emitter.result.none();
    }
    enumMembersContext(en) {
        return {};
    }
    enumMember(member) {
        return this.emitter.result.none();
    }
    enumMemberContext(member) {
        return {};
    }
    unionDeclaration(union, name) {
        this.emitter.emitUnionVariants(union);
        return this.emitter.result.none();
    }
    unionDeclarationContext(union) {
        return {};
    }
    unionDeclarationReferenceContext(union) {
        return {};
    }
    unionInstantiation(union, name) {
        this.emitter.emitUnionVariants(union);
        return this.emitter.result.none();
    }
    unionInstantiationContext(union, name) {
        return {};
    }
    unionInstantiationReferenceContext(union, name) {
        return {};
    }
    unionLiteral(union) {
        this.emitter.emitUnionVariants(union);
        return this.emitter.result.none();
    }
    unionLiteralContext(union) {
        return {};
    }
    unionLiteralReferenceContext(union) {
        return {};
    }
    unionVariants(union) {
        for (const variant of union.variants.values()) {
            this.emitter.emitType(variant);
        }
        return this.emitter.result.none();
    }
    unionVariantsContext() {
        return {};
    }
    unionVariantsReferenceContext() {
        return {};
    }
    unionVariant(variant) {
        this.emitter.emitTypeReference(variant.type);
        return this.emitter.result.none();
    }
    unionVariantContext(union) {
        return {};
    }
    unionVariantReferenceContext(union) {
        return {};
    }
    tupleLiteral(tuple) {
        this.emitter.emitTupleLiteralValues(tuple);
        return this.emitter.result.none();
    }
    tupleLiteralContext(tuple) {
        return {};
    }
    tupleLiteralValues(tuple) {
        for (const value of tuple.values.values()) {
            this.emitter.emitType(value);
        }
        return this.emitter.result.none();
    }
    tupleLiteralValuesContext(tuple) {
        return {};
    }
    tupleLiteralValuesReferenceContext(tuple) {
        return {};
    }
    tupleLiteralReferenceContext(tuple) {
        return {};
    }
    sourceFile(sourceFile) {
        const emittedSourceFile = {
            path: sourceFile.path,
            contents: "",
        };
        for (const decl of sourceFile.globalScope.declarations) {
            emittedSourceFile.contents += decl.value + "\n";
        }
        return emittedSourceFile;
    }
    async writeOutput(sourceFiles) {
        for (const file of sourceFiles) {
            const outputFile = await this.emitter.emitSourceFile(file);
            await emitFile(this.emitter.getProgram(), {
                path: outputFile.path,
                content: outputFile.contents,
            });
        }
    }
    reference(targetDeclaration, pathUp, pathDown, commonScope) {
        return this.emitter.result.none();
    }
    /**
     * Handle circular references. When this method is called it means we are resolving a circular reference.
     * By default if the target is a declaration it will call to {@link reference} otherwise it means we have an inline reference
     * @param target Reference target.
     * @param scope Current scope.
     * @returns Resolved reference entity.
     */
    circularReference(target, scope, cycle) {
        if (!cycle.containsDeclaration) {
            throw new Error(`Circular references to non-declarations are not supported by this emitter. Cycle:\n${cycle}`);
        }
        if (target.kind !== "declaration") {
            return target;
        }
        compilerAssert(scope, "Emit context must have a scope set in order to create references to declarations.");
        const { pathUp, pathDown, commonScope } = resolveDeclarationReferenceScope(target, scope);
        return this.reference(target, pathUp, pathDown, commonScope);
    }
    declarationName(declarationType) {
        compilerAssert(declarationType.name !== undefined, "Can't emit a declaration that doesn't have a name.");
        if (declarationType.kind === "Enum" || declarationType.kind === "Intrinsic") {
            return declarationType.name;
        }
        // for operations inside interfaces, we don't want to do the fancy thing because it will make
        // operations inside instantiated interfaces get weird names
        if (declarationType.kind === "Operation" && declarationType.interface) {
            return declarationType.name;
        }
        if (!declarationType.templateMapper) {
            return declarationType.name;
        }
        let unspeakable = false;
        const parameterNames = declarationType.templateMapper.args.map((t) => {
            if (t.entityKind === "Indeterminate") {
                t = t.type;
            }
            if (!("kind" in t)) {
                return undefined;
            }
            switch (t.kind) {
                case "Model":
                case "Scalar":
                case "Interface":
                case "Operation":
                case "Enum":
                case "Union":
                case "Intrinsic":
                    if (!t.name) {
                        unspeakable = true;
                        return undefined;
                    }
                    const declName = this.emitter.emitDeclarationName(t);
                    if (declName === undefined) {
                        unspeakable = true;
                        return undefined;
                    }
                    return declName[0].toUpperCase() + declName.slice(1);
                default:
                    unspeakable = true;
                    return undefined;
            }
        });
        if (unspeakable) {
            return undefined;
        }
        return declarationType.name + parameterNames.join("");
    }
}
/**
 * A subclass of `TypeEmitter<string>` that makes working with strings a bit easier.
 * In particular, when emitting members of a type (`modelProperties`, `enumMembers`, etc.),
 * instead of returning no result, it returns the value of each of the members concatenated
 * by commas. It will also construct references by concatenating namespace elements together
 * with `.` which should work nicely in many object oriented languages.
 */
class CodeTypeEmitter extends TypeEmitter {
    modelProperties(model) {
        const builder = new StringBuilder();
        let i = 0;
        for (const prop of model.properties.values()) {
            i++;
            const propVal = this.emitter.emitModelProperty(prop);
            builder.push(code `${propVal}${i < model.properties.size ? "," : ""}`);
        }
        return this.emitter.result.rawCode(builder.reduce());
    }
    interfaceDeclarationOperations(iface) {
        const builder = new StringBuilder();
        let i = 0;
        for (const op of iface.operations.values()) {
            i++;
            builder.push(code `${this.emitter.emitInterfaceOperation(op)}${i < iface.operations.size ? "," : ""}`);
        }
        return builder.reduce();
    }
    enumMembers(en) {
        const builder = new StringBuilder();
        let i = 0;
        for (const enumMember of en.members.values()) {
            i++;
            builder.push(code `${this.emitter.emitType(enumMember)}${i < en.members.size ? "," : ""}`);
        }
        return builder.reduce();
    }
    unionVariants(union) {
        const builder = new StringBuilder();
        let i = 0;
        for (const v of union.variants.values()) {
            i++;
            builder.push(code `${this.emitter.emitType(v)}${i < union.variants.size ? "," : ""}`);
        }
        return builder.reduce();
    }
    tupleLiteralValues(tuple) {
        const builder = new StringBuilder();
        let i = 0;
        for (const v of tuple.values) {
            i++;
            builder.push(code `${this.emitter.emitTypeReference(v)}${i < tuple.values.length ? "," : ""}`);
        }
        return builder.reduce();
    }
    reference(targetDeclaration, pathUp, pathDown, commonScope) {
        const basePath = pathDown.map((s) => s.name).join(".");
        return basePath
            ? this.emitter.result.rawCode(basePath + "." + targetDeclaration.name)
            : this.emitter.result.rawCode(targetDeclaration.name);
    }
}

export { ArrayBuilder, CircularEmit, CodeTypeEmitter, Declaration, EmitterResult, NoEmit, ObjectBuilder, Placeholder, RawCode, ReferenceCycle, StringBuilder, TypeEmitter, code, createAssetEmitter };
