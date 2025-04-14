import { i as isDefined } from './misc-97rxrklX.js';
import { S as SyntaxKind, p as printIdentifier } from './syntax-utils-DfiQDdeq.js';

function isErrorType(type) {
    return "kind" in type && type.kind === "Intrinsic" && type.name === "ErrorType";
}
function isVoidType(type) {
    return "kind" in type && type.kind === "Intrinsic" && type.name === "void";
}
function isNeverType(type) {
    return "kind" in type && type.kind === "Intrinsic" && type.name === "never";
}
function isUnknownType(type) {
    return "kind" in type && type.kind === "Intrinsic" && type.name === "unknown";
}
function isNullType(type) {
    return "kind" in type && type.kind === "Intrinsic" && type.name === "null";
}
function isType(entity) {
    return entity.entityKind === "Type";
}
function isValue(entity) {
    return entity.entityKind === "Value";
}
/**
 * @param type Model type
 */
function isArrayModelType(program, type) {
    return Boolean(type.indexer && type.indexer.key.name === "integer");
}
/**
 * Check if a model is an array type.
 * @param type Model type
 */
function isRecordModelType(program, type) {
    return Boolean(type.indexer && type.indexer.key.name === "string");
}
/**
 * Lookup and find the node
 * @param node Node
 * @returns Template Parent node if applicable
 */
function getParentTemplateNode(node) {
    switch (node.kind) {
        case SyntaxKind.ModelStatement:
        case SyntaxKind.ScalarStatement:
        case SyntaxKind.OperationStatement:
        case SyntaxKind.UnionStatement:
        case SyntaxKind.InterfaceStatement:
            return node.templateParameters.length > 0 ? node : undefined;
        case SyntaxKind.OperationSignatureDeclaration:
        case SyntaxKind.ModelProperty:
        case SyntaxKind.ModelExpression:
            return node.parent ? getParentTemplateNode(node.parent) : undefined;
        default:
            return undefined;
    }
}
/**
 * Check the given type is a finished template instance.
 */
function isTemplateInstance(type) {
    const maybeTemplateType = type;
    return (maybeTemplateType.templateMapper !== undefined &&
        !maybeTemplateType.templateMapper.partial &&
        maybeTemplateType.isFinished);
}
/**
 * Check if the type is a declared type. This include:
 * - non templated type
 * - template declaration
 */
function isDeclaredType(type) {
    if (type.node === undefined) {
        return false;
    }
    const node = type.node;
    return (node.templateParameters === undefined || type.templateMapper === undefined);
}
/**
 * Resolve if the type is a template type declaration(Non initialized template type).
 */
function isTemplateDeclaration(type) {
    if (type.node === undefined) {
        return false;
    }
    const node = type.node;
    return (node.templateParameters &&
        node.templateParameters.length > 0 &&
        type.templateMapper === undefined);
}
/**
 * Resolve if the type was created from a template type or is a template type declaration.
 */
function isTemplateDeclarationOrInstance(type) {
    if (type.node === undefined) {
        return false;
    }
    const node = type.node;
    return node.templateParameters && node.templateParameters.length > 0;
}
/**
 * Check if the given namespace is the global namespace
 * @param program Program
 * @param namespace Namespace
 * @returns {boolean}
 */
function isGlobalNamespace(program, namespace) {
    return program.getGlobalNamespaceType() === namespace;
}
/**
 * Check if the given type is declared in the specified namespace or, optionally, its child namespaces.
 * @param type Type
 * @param namespace Namespace
 * @returns {boolean}
 */
function isDeclaredInNamespace(type, namespace, options = { recursive: true }) {
    let candidateNs = type.namespace;
    while (candidateNs) {
        if (candidateNs === namespace) {
            return true;
        }
        // Operations can be defined inside of an interface that is defined in the
        // desired namespace
        if (type.kind === "Operation" && type.interface && type.interface.namespace === namespace) {
            return true;
        }
        // If we are allowed to check recursively, walk up the namespace hierarchy
        candidateNs = options.recursive ? candidateNs.namespace : undefined;
    }
    return false;
}
function getFullyQualifiedSymbolName(sym, options) {
    if (!sym)
        return "";
    if (sym.symbolSource)
        sym = sym.symbolSource;
    const parent = sym.parent && !(sym.parent.flags & 32768 /* SymbolFlags.SourceFile */) ? sym.parent : undefined;
    const name = sym.flags & 512 /* SymbolFlags.Decorator */ ? sym.name.slice(1) : sym.name;
    if (parent?.name) {
        return `${getFullyQualifiedSymbolName(parent)}.${name}`;
    }
    else if (options?.useGlobalPrefixAtTopLevel) {
        return `global.${name}`;
    }
    else {
        return name;
    }
}

function getTypeName(type, options) {
    switch (type.kind) {
        case "Namespace":
            return getNamespaceFullName(type, options);
        case "TemplateParameter":
            return getIdentifierName(type.node.id.sv, options);
        case "Scalar":
            return getScalarName(type, options);
        case "Model":
            return getModelName(type, options);
        case "ModelProperty":
            return getModelPropertyName(type, options);
        case "Interface":
            return getInterfaceName(type, options);
        case "Operation":
            return getOperationName(type, options);
        case "Enum":
            return getEnumName(type, options);
        case "EnumMember":
            return `${getEnumName(type.enum, options)}.${getIdentifierName(type.name, options)}`;
        case "Union":
            return getUnionName(type, options);
        case "UnionVariant":
            return getTypeName(type.type, options);
        case "Tuple":
            return "[" + type.values.map((x) => getTypeName(x, options)).join(", ") + "]";
        case "StringTemplate":
            return getStringTemplateName(type);
        case "String":
            return `"${type.value}"`;
        case "Number":
            return type.valueAsString;
        case "Boolean":
            return type.value.toString();
        case "Intrinsic":
            return type.name;
        default:
            return `(unnamed type)`;
    }
}
function getValuePreview(value, options) {
    switch (value.valueKind) {
        case "ObjectValue":
            return `#{${[...value.properties.entries()].map(([name, value]) => `${name}: ${getValuePreview(value.value, options)}`).join(", ")}}`;
        case "ArrayValue":
            return `#[${value.values.map((x) => getValuePreview(x, options)).join(", ")}]`;
        case "StringValue":
            return `"${value.value}"`;
        case "BooleanValue":
            return `${value.value}`;
        case "NumericValue":
            return `${value.value.toString()}`;
        case "EnumValue":
            return getTypeName(value.value);
        case "NullValue":
            return "null";
        case "ScalarValue":
            return `${getTypeName(value.type, options)}.${value.value.name}(${value.value.args.map((x) => getValuePreview(x, options)).join(", ")}})`;
    }
}
function getEntityName(entity, options) {
    if (isValue(entity)) {
        return getValuePreview(entity, options);
    }
    else if (isType(entity)) {
        return getTypeName(entity, options);
    }
    else {
        switch (entity.entityKind) {
            case "MixedParameterConstraint":
                return [
                    entity.type && getEntityName(entity.type),
                    entity.valueType && `valueof ${getEntityName(entity.valueType)}`,
                ]
                    .filter(isDefined)
                    .join(" | ");
            case "Indeterminate":
                return getTypeName(entity.type, options);
        }
    }
}
function isStdNamespace(namespace) {
    return ((namespace.name === "TypeSpec" && namespace.namespace?.name === "") ||
        (namespace.name === "Reflection" &&
            namespace.namespace?.name === "TypeSpec" &&
            namespace.namespace?.namespace?.name === ""));
}
/**
 * Return the full name of the namespace(e.g. "Foo.Bar")
 * @param type namespace type
 * @param options
 * @returns
 */
function getNamespaceFullName(type, options) {
    const filter = options?.namespaceFilter;
    const segments = [];
    let current = type;
    while (current && current.name !== "") {
        if (filter && !filter(current)) {
            break;
        }
        segments.unshift(getIdentifierName(current.name, options));
        current = current.namespace;
    }
    return segments.join(".");
}
function getNamespacePrefix(type, options) {
    if (type === undefined || isStdNamespace(type)) {
        return "";
    }
    const namespaceFullName = getNamespaceFullName(type, options);
    return namespaceFullName !== "" ? namespaceFullName + "." : "";
}
function getEnumName(e, options) {
    return `${getNamespacePrefix(e.namespace, options)}${getIdentifierName(e.name, options)}`;
}
function getScalarName(scalar, options) {
    return `${getNamespacePrefix(scalar.namespace, options)}${getIdentifierName(scalar.name, options)}`;
}
function getModelName(model, options) {
    const nsPrefix = getNamespacePrefix(model.namespace, options);
    if (model.name === "" && model.properties.size === 0) {
        return "{}";
    }
    if (model.indexer && model.indexer.key.kind === "Scalar") {
        if (model.name === "Array" && isInTypeSpecNamespace(model)) {
            return `${getTypeName(model.indexer.value, options)}[]`;
        }
    }
    if (model.name === "") {
        return (nsPrefix +
            `{ ${[...model.properties.values()].map((prop) => `${prop.name}: ${getTypeName(prop.type, options)}`).join(", ")} }`);
    }
    const modelName = nsPrefix + getIdentifierName(model.name, options);
    if (isTemplateInstance(model)) {
        // template instantiation
        const args = model.templateMapper.args.map((x) => getEntityName(x, options));
        return `${modelName}<${args.join(", ")}>`;
    }
    else if (model.node?.templateParameters?.length > 0) {
        // template
        const params = model.node.templateParameters.map((t) => getIdentifierName(t.id.sv, options));
        return `${modelName}<${params.join(", ")}>`;
    }
    else {
        // regular old model.
        return modelName;
    }
}
function getUnionName(type, options) {
    const nsPrefix = getNamespacePrefix(type.namespace, options);
    const typeName = type.name
        ? getIdentifierName(type.name, options)
        : [...type.variants.values()].map((x) => getTypeName(x.type, options)).join(" | ");
    return nsPrefix + typeName;
}
/**
 * Check if the given namespace is the standard library `TypeSpec` namespace.
 */
function isTypeSpecNamespace(namespace) {
    return namespace.name === "TypeSpec" && namespace.namespace?.name === "";
}
/**
 * Check if the given type is defined right in the TypeSpec namespace.
 */
function isInTypeSpecNamespace(type) {
    return Boolean(type.namespace && isTypeSpecNamespace(type.namespace));
}
function getModelPropertyName(prop, options) {
    const modelName = prop.model ? getModelName(prop.model, options) : undefined;
    return `${modelName ?? "(anonymous model)"}.${prop.name}`;
}
function getInterfaceName(iface, options) {
    let interfaceName = getIdentifierName(iface.name, options);
    if (isTemplateInstance(iface)) {
        interfaceName += `<${iface.templateMapper.args
            .map((x) => getEntityName(x, options))
            .join(", ")}>`;
    }
    return `${getNamespacePrefix(iface.namespace, options)}${interfaceName}`;
}
function getOperationName(op, options) {
    let opName = getIdentifierName(op.name, options);
    if (op.node.templateParameters.length > 0) {
        // template
        const params = op.node.templateParameters.map((t) => getIdentifierName(t.id.sv, options));
        opName += `<${params.join(", ")}>`;
    }
    const prefix = op.interface
        ? getInterfaceName(op.interface, options) + "."
        : getNamespacePrefix(op.namespace, options);
    return `${prefix}${opName}`;
}
function getIdentifierName(name, options) {
    return options?.printable ? printIdentifier(name) : name;
}
function getStringTemplateName(type) {
    if (type.stringValue) {
        return `"${type.stringValue}"`;
    }
    return "string";
}

/**
 * This is a map type that allows providing a custom keyer function. The keyer
 * function returns a string that is used to look up in the map. This is useful
 * for implementing maps that look up based on an arbitrary number of keys.
 *
 * For example, to look up in a map with a [ObjA, ObjB)] tuple, such that tuples
 * with identical values (but not necessarily identical tuples!) create an
 * object keyer for each of the objects:
 *
 *     const aKeyer = CustomKeyMap.objectKeyer();
 *     const bKeyer = CUstomKeyMap.objectKeyer();
 *
 * And compose these into a tuple keyer to use when instantiating the custom key
 * map:
 *
 *     const tupleKeyer = ([a, b]) => `${aKeyer.getKey(a)}-${bKeyer.getKey(b)}`;
 *     const map = new CustomKeyMap(tupleKeyer);
 *
 */
class CustomKeyMap {
    #items = new Map();
    #keyer;
    constructor(keyer) {
        this.#keyer = keyer;
    }
    get(items) {
        return this.#items.get(this.#keyer(items));
    }
    set(items, value) {
        const key = this.#keyer(items);
        this.#items.set(key, value);
    }
    static objectKeyer() {
        const knownKeys = new WeakMap();
        let count = 0;
        return {
            getKey(o) {
                if (knownKeys.has(o)) {
                    return knownKeys.get(o);
                }
                const key = count;
                count++;
                knownKeys.set(o, key);
                return key;
            },
        };
    }
}

export { CustomKeyMap as C, isArrayModelType as a, isUnknownType as b, isTemplateDeclarationOrInstance as c, getFullyQualifiedSymbolName as d, getEntityName as e, isStdNamespace as f, getTypeName as g, isType as h, isTemplateDeclaration as i, getNamespaceFullName as j, isDeclaredInNamespace as k, isDeclaredType as l, isErrorType as m, isGlobalNamespace as n, isNeverType as o, isNullType as p, isRecordModelType as q, isTemplateInstance as r, isValue as s, isVoidType as t, getParentTemplateNode as u };
