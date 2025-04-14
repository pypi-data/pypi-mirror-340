import { b as getAnyExtensionFromPath } from './path-utils-B4zKWudT.js';
import { m as mutate } from './misc-97rxrklX.js';

/**
 * Create a new diagnostics creator.
 * @param diagnostics Map of the potential diagnostics.
 * @param libraryName Optional name of the library if in the scope of a library.
 * @returns @see DiagnosticCreator
 */
function createDiagnosticCreator(diagnostics, libraryName) {
    const errorMessage = libraryName
        ? `It must match one of the code defined in the library '${libraryName}'`
        : "It must match one of the code defined in the compiler.";
    function createDiagnostic(diagnostic) {
        const diagnosticDef = diagnostics[diagnostic.code];
        if (!diagnosticDef) {
            const codeStr = Object.keys(diagnostics)
                .map((x) => ` - ${x}`)
                .join("\n");
            const code = String(diagnostic.code);
            throw new Error(`Unexpected diagnostic code '${code}'. ${errorMessage}. Defined codes:\n${codeStr}`);
        }
        const message = diagnosticDef.messages[diagnostic.messageId ?? "default"];
        if (!message) {
            const codeStr = Object.keys(diagnosticDef.messages)
                .map((x) => ` - ${x}`)
                .join("\n");
            const messageId = String(diagnostic.messageId);
            const code = String(diagnostic.code);
            throw new Error(`Unexpected message id '${messageId}'. ${errorMessage} for code '${code}'. Defined codes:\n${codeStr}`);
        }
        const messageStr = typeof message === "string" ? message : message(diagnostic.format);
        const result = {
            code: libraryName ? `${libraryName}/${String(diagnostic.code)}` : diagnostic.code.toString(),
            severity: diagnosticDef.severity,
            message: messageStr,
            target: diagnostic.target,
        };
        if (diagnosticDef.url) {
            mutate(result).url = diagnosticDef.url;
        }
        if (diagnostic.codefixes) {
            mutate(result).codefixes = diagnostic.codefixes;
        }
        return result;
    }
    function reportDiagnostic(program, diagnostic) {
        const diag = createDiagnostic(diagnostic);
        program.reportDiagnostic(diag);
    }
    return {
        diagnostics,
        createDiagnostic,
        reportDiagnostic,
    };
}

function paramMessage(strings, ...keys) {
    const template = (dict) => {
        const result = [strings[0]];
        keys.forEach((key, i) => {
            const value = dict[key];
            if (value !== undefined) {
                result.push(value);
            }
            result.push(strings[i + 1]);
        });
        return result.join("");
    };
    template.keys = keys;
    return template;
}

// Static assert: this won't compile if one of the entries above is invalid.
const diagnostics = {
    /**
     * Scanner errors.
     */
    "digit-expected": {
        severity: "error",
        messages: {
            default: "Digit expected.",
        },
    },
    "hex-digit-expected": {
        severity: "error",
        messages: {
            default: "Hexadecimal digit expected.",
        },
    },
    "binary-digit-expected": {
        severity: "error",
        messages: {
            default: "Binary digit expected.",
        },
    },
    unterminated: {
        severity: "error",
        messages: {
            default: paramMessage `Unterminated ${"token"}.`,
        },
    },
    "creating-file": {
        severity: "error",
        messages: {
            default: paramMessage `Error creating single file: ${"filename"},  ${"error"}`,
        },
    },
    "invalid-escape-sequence": {
        severity: "error",
        messages: {
            default: "Invalid escape sequence.",
        },
    },
    "no-new-line-start-triple-quote": {
        severity: "error",
        messages: {
            default: "String content in triple quotes must begin on a new line.",
        },
    },
    "no-new-line-end-triple-quote": {
        severity: "error",
        messages: {
            default: "Closing triple quotes must begin on a new line.",
        },
    },
    "triple-quote-indent": {
        severity: "error",
        description: "Report when a triple-quoted string has lines with less indentation as the closing triple quotes.",
        url: "https://typespec.io/docs/standard-library/diags/triple-quote-indent",
        messages: {
            default: "All lines in triple-quoted string lines must have the same indentation as closing triple quotes.",
        },
    },
    "invalid-character": {
        severity: "error",
        messages: {
            default: "Invalid character.",
        },
    },
    /**
     * Utils
     */
    "file-not-found": {
        severity: "error",
        messages: {
            default: paramMessage `File ${"path"} not found.`,
        },
    },
    "file-load": {
        severity: "error",
        messages: {
            default: paramMessage `${"message"}`,
        },
    },
    /**
     * Init templates
     */
    "init-template-invalid-json": {
        severity: "error",
        messages: {
            default: paramMessage `Unable to parse ${"url"}: ${"message"}. Check that the template URL is correct.`,
        },
    },
    "init-template-download-failed": {
        severity: "error",
        messages: {
            default: paramMessage `Failed to download template from ${"url"}: ${"message"}. Check that the template URL is correct.`,
        },
    },
    /**
     * Parser errors.
     */
    "multiple-blockless-namespace": {
        severity: "error",
        messages: {
            default: "Cannot use multiple blockless namespaces.",
        },
    },
    "blockless-namespace-first": {
        severity: "error",
        messages: {
            default: "Blockless namespaces can't follow other declarations.",
            topLevel: "Blockless namespace can only be top-level.",
        },
    },
    "import-first": {
        severity: "error",
        messages: {
            default: "Imports must come prior to namespaces or other declarations.",
            topLevel: "Imports must be top-level and come prior to namespaces or other declarations.",
        },
    },
    "token-expected": {
        severity: "error",
        messages: {
            default: paramMessage `${"token"} expected.`,
            unexpected: paramMessage `Unexpected token ${"token"}`,
            numericOrStringLiteral: "Expected numeric or string literal.",
            identifier: "Identifier expected.",
            expression: "Expression expected.",
            statement: "Statement expected.",
            property: "Property expected.",
            enumMember: "Enum member expected.",
            typeofTarget: "Typeof expects a value literal or value reference.",
        },
    },
    "unknown-directive": {
        severity: "error",
        messages: {
            default: paramMessage `Unknown directive '#${"id"}'`,
        },
    },
    "augment-decorator-target": {
        severity: "error",
        messages: {
            default: `Augment decorator first argument must be a type reference.`,
            noInstance: `Cannot reference template instances.`,
            noModelExpression: `Cannot augment model expressions.`,
            noUnionExpression: `Cannot augment union expressions.`,
        },
    },
    "duplicate-decorator": {
        severity: "warning",
        messages: {
            default: paramMessage `Decorator ${"decoratorName"} cannot be used twice on the same declaration.`,
        },
    },
    "decorator-conflict": {
        severity: "warning",
        messages: {
            default: paramMessage `Decorator ${"decoratorName"} cannot be used with decorator ${"otherDecoratorName"} on the same declaration.`,
        },
    },
    "reserved-identifier": {
        severity: "error",
        messages: {
            default: "Keyword cannot be used as identifier.",
            future: paramMessage `${"name"} is a reserved keyword`,
        },
    },
    "invalid-directive-location": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot place directive on ${"nodeName"}.`,
        },
    },
    "invalid-decorator-location": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot decorate ${"nodeName"}.`,
        },
    },
    "default-required": {
        severity: "error",
        messages: {
            default: "Required template parameters must not follow optional template parameters",
        },
    },
    "invalid-template-argument-name": {
        severity: "error",
        messages: {
            default: "Template parameter argument names must be valid, bare identifiers.",
        },
    },
    "invalid-template-default": {
        severity: "error",
        messages: {
            default: "Template parameter defaults can only reference previously declared type parameters.",
        },
    },
    "required-parameter-first": {
        severity: "error",
        messages: {
            default: "A required parameter cannot follow an optional parameter.",
        },
    },
    "rest-parameter-last": {
        severity: "error",
        messages: {
            default: "A rest parameter must be last in a parameter list.",
        },
    },
    "rest-parameter-required": {
        severity: "error",
        messages: {
            default: "A rest parameter cannot be optional.",
        },
    },
    /**
     * Parser doc comment warnings.
     * Design goal: Malformed doc comments should only produce warnings, not errors.
     */
    "doc-invalid-identifier": {
        severity: "warning",
        messages: {
            default: "Invalid identifier.",
            tag: "Invalid tag name. Use backticks around code if this was not meant to be a tag.",
            param: "Invalid parameter name.",
            prop: "Invalid property name.",
            templateParam: "Invalid template parameter name.",
        },
    },
    /**
     * Checker
     */
    "using-invalid-ref": {
        severity: "error",
        messages: {
            default: "Using must refer to a namespace",
        },
    },
    "invalid-type-ref": {
        severity: "error",
        messages: {
            default: "Invalid type reference",
            decorator: "Can't put a decorator in a type",
            function: "Can't use a function as a type",
        },
    },
    "invalid-template-args": {
        severity: "error",
        messages: {
            default: "Invalid template arguments.",
            notTemplate: "Can't pass template arguments to non-templated type",
            tooMany: "Too many template arguments provided.",
            unknownName: paramMessage `No parameter named '${"name"}' exists in the target template.`,
            positionalAfterNamed: "Positional template arguments cannot follow named arguments in the same argument list.",
            missing: paramMessage `Template argument '${"name"}' is required and not specified.`,
            specifiedAgain: paramMessage `Cannot specify template argument '${"name"}' again.`,
        },
    },
    "intersect-non-model": {
        severity: "error",
        messages: {
            default: "Cannot intersect non-model types (including union types).",
        },
    },
    "intersect-invalid-index": {
        severity: "error",
        messages: {
            default: "Cannot intersect incompatible models.",
            never: "Cannot intersect a model that cannot hold properties.",
            array: "Cannot intersect an array model.",
        },
    },
    "incompatible-indexer": {
        severity: "error",
        messages: {
            default: paramMessage `Property is incompatible with indexer:\n${"message"}`,
        },
    },
    "no-array-properties": {
        severity: "error",
        messages: {
            default: "Array models cannot have any properties.",
        },
    },
    "intersect-duplicate-property": {
        severity: "error",
        messages: {
            default: paramMessage `Intersection contains duplicate property definitions for ${"propName"}`,
        },
    },
    "invalid-decorator": {
        severity: "error",
        messages: {
            default: paramMessage `${"id"} is not a decorator`,
        },
    },
    "invalid-ref": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot resolve ${"id"}`,
            identifier: paramMessage `Unknown identifier ${"id"}`,
            decorator: paramMessage `Unknown decorator @${"id"}`,
            inDecorator: paramMessage `Cannot resolve ${"id"} in decorator`,
            underNamespace: paramMessage `Namespace ${"namespace"} doesn't have member ${"id"}`,
            member: paramMessage `${"kind"} doesn't have member ${"id"}`,
            metaProperty: paramMessage `${"kind"} doesn't have meta property ${"id"}`,
            node: paramMessage `Cannot resolve '${"id"}' in node ${"nodeName"} since it has no members. Did you mean to use "::" instead of "."?`,
        },
    },
    "duplicate-property": {
        severity: "error",
        messages: {
            default: paramMessage `Model already has a property named ${"propName"}`,
        },
    },
    "override-property-mismatch": {
        severity: "error",
        messages: {
            default: paramMessage `Model has an inherited property named ${"propName"} of type ${"propType"} which cannot override type ${"parentType"}`,
            disallowedOptionalOverride: paramMessage `Model has a required inherited property named ${"propName"} which cannot be overridden as optional`,
        },
    },
    "extend-scalar": {
        severity: "error",
        messages: {
            default: "Scalar must extend other scalars.",
        },
    },
    "extend-model": {
        severity: "error",
        messages: {
            default: "Models must extend other models.",
            modelExpression: "Models cannot extend model expressions.",
        },
    },
    "is-model": {
        severity: "error",
        messages: {
            default: "Model `is` must specify another model.",
            modelExpression: "Model `is` cannot specify a model expression.",
        },
    },
    "is-operation": {
        severity: "error",
        messages: {
            default: "Operation can only reuse the signature of another operation.",
        },
    },
    "spread-model": {
        severity: "error",
        messages: {
            default: "Cannot spread properties of non-model type.",
            neverIndex: "Cannot spread type because it cannot hold properties.",
            selfSpread: "Cannot spread type within its own declaration.",
        },
    },
    "unsupported-default": {
        severity: "error",
        messages: {
            default: paramMessage `Default must be have a value type but has type '${"type"}'.`,
        },
    },
    "spread-object": {
        severity: "error",
        messages: {
            default: "Cannot spread properties of non-object type.",
        },
    },
    "expect-value": {
        severity: "error",
        messages: {
            default: paramMessage `${"name"} refers to a type, but is being used as a value here.`,
            model: paramMessage `${"name"} refers to a model type, but is being used as a value here. Use #{} to create an object value.`,
            modelExpression: `Is a model expression type, but is being used as a value here. Use #{} to create an object value.`,
            tuple: `Is a tuple type, but is being used as a value here. Use #[] to create an array value.`,
            templateConstraint: paramMessage `${"name"} template parameter can be a type but is being used as a value here.`,
        },
    },
    "non-callable": {
        severity: "error",
        messages: {
            default: paramMessage `Type ${"type"} is not is not callable.`,
        },
    },
    "named-init-required": {
        severity: "error",
        messages: {
            default: paramMessage `Only scalar deriving from 'string', 'numeric' or 'boolean' can be instantited without a named constructor.`,
        },
    },
    "invalid-primitive-init": {
        severity: "error",
        messages: {
            default: `Instantiating scalar deriving from 'string', 'numeric' or 'boolean' can only take a single argument.`,
            invalidArg: paramMessage `Expected a single argument of type ${"expected"} but got ${"actual"}.`,
        },
    },
    "ambiguous-scalar-type": {
        severity: "error",
        messages: {
            default: paramMessage `Value ${"value"} type is ambiguous between ${"types"}. To resolve be explicit when instantiating this value(e.g. '${"example"}(${"value"})').`,
        },
    },
    unassignable: {
        severity: "error",
        messages: {
            default: paramMessage `Type '${"sourceType"}' is not assignable to type '${"targetType"}'`,
        },
    },
    "property-unassignable": {
        severity: "error",
        messages: {
            default: paramMessage `Types of property '${"propName"}' are incompatible`,
        },
    },
    "property-required": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propName"}' is required in type '${"targetType"}' but here is optional.`,
        },
    },
    "value-in-type": {
        severity: "error",
        messages: {
            default: "A value cannot be used as a type.",
            referenceTemplate: "Template parameter can be passed values but is used as a type.",
            noTemplateConstraint: "Template parameter has no constraint but a value is passed. Add `extends valueof unknown` to accept any value.",
        },
    },
    "no-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propName"}' cannot be defined because model cannot hold properties.`,
        },
    },
    "missing-index": {
        severity: "error",
        messages: {
            default: paramMessage `Index signature for type '${"indexType"}' is missing in type '${"sourceType"}'.`,
        },
    },
    "missing-property": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propertyName"}' is missing on type '${"sourceType"}' but required in '${"targetType"}'`,
        },
    },
    "unexpected-property": {
        severity: "error",
        messages: {
            default: paramMessage `Object value may only specify known properties, and '${"propertyName"}' does not exist in type '${"type"}'.`,
        },
    },
    "extends-interface": {
        severity: "error",
        messages: {
            default: "Interfaces can only extend other interfaces",
        },
    },
    "extends-interface-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Interface extends cannot have duplicate members. The duplicate member is named ${"name"}`,
        },
    },
    "interface-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Interface already has a member named ${"name"}`,
        },
    },
    "union-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Union already has a variant named ${"name"}`,
        },
    },
    "enum-member-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `Enum already has a member named ${"name"}`,
        },
    },
    "constructor-duplicate": {
        severity: "error",
        messages: {
            default: paramMessage `A constructor already exists with name ${"name"}`,
        },
    },
    "spread-enum": {
        severity: "error",
        messages: {
            default: "Cannot spread members of non-enum type.",
        },
    },
    "decorator-fail": {
        severity: "error",
        messages: {
            default: paramMessage `Decorator ${"decoratorName"} failed!\n\n${"error"}`,
        },
    },
    "rest-parameter-array": {
        severity: "error",
        messages: {
            default: "A rest parameter must be of an array type.",
        },
    },
    "decorator-extern": {
        severity: "error",
        messages: {
            default: "A decorator declaration must be prefixed with the 'extern' modifier.",
        },
    },
    "function-extern": {
        severity: "error",
        messages: {
            default: "A function declaration must be prefixed with the 'extern' modifier.",
        },
    },
    "function-unsupported": {
        severity: "error",
        messages: {
            default: "Function are currently not supported.",
        },
    },
    "missing-implementation": {
        severity: "error",
        messages: {
            default: "Extern declaration must have an implementation in JS file.",
        },
    },
    "overload-same-parent": {
        severity: "error",
        messages: {
            default: `Overload must be in the same interface or namespace.`,
        },
    },
    shadow: {
        severity: "warning",
        messages: {
            default: paramMessage `Shadowing parent template parameter with the same name "${"name"}"`,
        },
    },
    "invalid-deprecation-argument": {
        severity: "error",
        messages: {
            default: paramMessage `#deprecation directive is expecting a string literal as the message but got a "${"kind"}"`,
            missing: "#deprecation directive is expecting a message argument but none was provided.",
        },
    },
    "duplicate-deprecation": {
        severity: "warning",
        messages: {
            default: "The #deprecated directive cannot be used more than once on the same declaration.",
        },
    },
    /**
     * Configuration
     */
    "config-invalid-argument": {
        severity: "error",
        messages: {
            default: paramMessage `Argument "${"name"}" is not defined as a parameter in the config.`,
        },
    },
    "config-circular-variable": {
        severity: "error",
        messages: {
            default: paramMessage `There is a circular reference to variable "${"name"}" in the cli configuration or arguments.`,
        },
    },
    "config-path-absolute": {
        severity: "error",
        messages: {
            default: paramMessage `Path "${"path"}" cannot be relative. Use {cwd} or {project-root} to specify what the path should be relative to.`,
        },
    },
    "config-invalid-name": {
        severity: "error",
        messages: {
            default: paramMessage `The configuration name "${"name"}" is invalid because it contains a dot ("."). Using a dot will conflict with using nested configuration values.`,
        },
    },
    "path-unix-style": {
        severity: "warning",
        messages: {
            default: paramMessage `Path should use unix style separators. Use "/" instead of "\\".`,
        },
    },
    "config-path-not-found": {
        severity: "error",
        messages: {
            default: paramMessage `No configuration file found at config path "${"path"}".`,
        },
    },
    /**
     * Program
     */
    "dynamic-import": {
        severity: "error",
        messages: {
            default: "Dynamically generated TypeSpec cannot have imports",
        },
    },
    "invalid-import": {
        severity: "error",
        messages: {
            default: "Import paths must reference either a directory, a .tsp file, or .js file",
        },
    },
    "invalid-main": {
        severity: "error",
        messages: {
            default: "Main file must either be a .tsp file or a .js file.",
        },
    },
    "import-not-found": {
        severity: "error",
        messages: {
            default: paramMessage `Couldn't resolve import "${"path"}"`,
        },
    },
    "library-invalid": {
        severity: "error",
        messages: {
            default: paramMessage `Library "${"path"}" is invalid: ${"message"}`,
        },
    },
    "incompatible-library": {
        severity: "warning",
        messages: {
            default: paramMessage `Multiple versions of "${"name"}" library were loaded:\n${"versionMap"}`,
        },
    },
    "compiler-version-mismatch": {
        severity: "warning",
        messages: {
            default: paramMessage `Current TypeSpec compiler conflicts with local version of @typespec/compiler referenced in ${"basedir"}. \nIf this warning occurs on the command line, try running \`typespec\` with a working directory of ${"basedir"}. \nIf this warning occurs in the IDE, try configuring the \`tsp-server\` path to ${"betterTypeSpecServerPath"}.\n  Expected: ${"expected"}\n  Resolved: ${"actual"}`,
        },
    },
    "duplicate-symbol": {
        severity: "error",
        messages: {
            default: paramMessage `Duplicate name: "${"name"}"`,
        },
    },
    "decorator-decl-target": {
        severity: "error",
        messages: {
            default: "dec must have at least one parameter.",
            required: "dec first parameter must be required.",
        },
    },
    "mixed-string-template": {
        severity: "error",
        messages: {
            default: "String template is interpolating values and types. It must be either all values to produce a string value or or all types for string template type.",
        },
    },
    "non-literal-string-template": {
        severity: "error",
        messages: {
            default: "Value interpolated in this string template cannot be converted to a string. Only literal types can be automatically interpolated.",
        },
    },
    /**
     * Binder
     */
    "ambiguous-symbol": {
        severity: "error",
        messages: {
            default: paramMessage `"${"name"}" is an ambiguous name between ${"duplicateNames"}. Try using fully qualified name instead: ${"duplicateNames"}`,
        },
    },
    "duplicate-using": {
        severity: "error",
        messages: {
            default: paramMessage `duplicate using of "${"usingName"}" namespace`,
        },
    },
    /**
     * Library
     */
    "on-validate-fail": {
        severity: "error",
        messages: {
            default: paramMessage `onValidate failed with errors. ${"error"}`,
        },
    },
    "invalid-emitter": {
        severity: "error",
        messages: {
            default: paramMessage `Requested emitter package ${"emitterPackage"} does not provide an "$onEmit" function.`,
        },
    },
    "js-error": {
        severity: "error",
        messages: {
            default: paramMessage `Failed to load ${"specifier"} due to the following JS error: ${"error"}`,
        },
    },
    "missing-import": {
        severity: "error",
        messages: {
            default: paramMessage `Emitter '${"emitterName"}' requires '${"requiredImport"}' to be imported. Add 'import "${"requiredImport"}".`,
        },
    },
    /**
     * Linter
     */
    "invalid-rule-ref": {
        severity: "error",
        messages: {
            default: paramMessage `Reference "${"ref"}" is not a valid reference to a rule or ruleset. It must be in the following format: "<library-name>:<rule-name>"`,
        },
    },
    "unknown-rule": {
        severity: "error",
        messages: {
            default: paramMessage `Rule "${"ruleName"}" is not found in library "${"libraryName"}"`,
        },
    },
    "unknown-rule-set": {
        severity: "error",
        messages: {
            default: paramMessage `Rule set "${"ruleSetName"}" is not found in library "${"libraryName"}"`,
        },
    },
    "rule-enabled-disabled": {
        severity: "error",
        messages: {
            default: paramMessage `Rule "${"ruleName"}" has been enabled and disabled in the same ruleset.`,
        },
    },
    /**
     * Formatter
     */
    "format-failed": {
        severity: "error",
        messages: {
            default: paramMessage `File '${"file"}' failed to format. ${"details"}`,
        },
    },
    /**
     * Decorator
     */
    "invalid-pattern-regex": {
        severity: "warning",
        messages: {
            default: "@pattern decorator expects a valid regular expression pattern.",
        },
    },
    "decorator-wrong-target": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot apply ${"decorator"} decorator to ${"to"}`,
            withExpected: paramMessage `Cannot apply ${"decorator"} decorator to ${"to"} since it is not assignable to ${"expected"}`,
        },
    },
    "invalid-argument": {
        severity: "error",
        messages: {
            default: paramMessage `Argument of type '${"value"}' is not assignable to parameter of type '${"expected"}'`,
        },
    },
    "invalid-argument-count": {
        severity: "error",
        messages: {
            default: paramMessage `Expected ${"expected"} arguments, but got ${"actual"}.`,
            atLeast: paramMessage `Expected at least ${"expected"} arguments, but got ${"actual"}.`,
        },
    },
    "known-values-invalid-enum": {
        severity: "error",
        messages: {
            default: paramMessage `Enum cannot be used on this type. Member ${"member"} is not assignable to type ${"type"}.`,
        },
    },
    "invalid-value": {
        severity: "error",
        messages: {
            default: paramMessage `Type '${"kind"}' is not a value type.`,
            atPath: paramMessage `Type '${"kind"}' of '${"path"}' is not a value type.`,
        },
    },
    deprecated: {
        severity: "warning",
        messages: {
            default: paramMessage `Deprecated: ${"message"}`,
        },
    },
    "no-optional-key": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propertyName"}' marked as key cannot be optional.`,
        },
    },
    "invalid-discriminated-union": {
        severity: "error",
        messages: {
            default: "",
            noAnonVariants: "Unions with anonymous variants cannot be discriminated",
        },
    },
    "invalid-discriminated-union-variant": {
        severity: "error",
        messages: {
            default: paramMessage `Union variant "${"name"}" must be a model type.`,
            noEnvelopeModel: paramMessage `Union variant "${"name"}" must be a model type when the union has envelope: none.`,
            discriminantMismatch: paramMessage `Variant "${"name"}" explicitly defines the discriminator property "${"discriminant"}" but the value "${"propertyValue"}" do not match the variant name "${"variantName"}".`,
            duplicateDefaultVariant: `Discriminated union only allow a single default variant(Without a variant name).`,
            noDiscriminant: paramMessage `Variant "${"name"}" type is missing the discriminant property "${"discriminant"}".`,
            wrongDiscriminantType: paramMessage `Variant "${"name"}" type's discriminant property "${"discriminant"}" must be a string literal or string enum member.`,
        },
    },
    "missing-discriminator-property": {
        severity: "error",
        messages: {
            default: paramMessage `Each derived model of a discriminated model type should have set the discriminator property("${"discriminator"}") or have a derived model which has. Add \`${"discriminator"}: "<discriminator-value>"\``,
        },
    },
    "invalid-discriminator-value": {
        severity: "error",
        messages: {
            default: paramMessage `Discriminator value should be a string, union of string or string enum but was ${"kind"}.`,
            required: "The discriminator property must be a required property.",
            duplicate: paramMessage `Discriminator value "${"discriminator"}" is already used in another variant.`,
        },
    },
    "invalid-encode": {
        severity: "error",
        messages: {
            default: "Invalid encoding",
            wrongType: paramMessage `Encoding '${"encoding"}' cannot be used on type '${"type"}'. Expected: ${"expected"}.`,
            wrongEncodingType: paramMessage `Encoding '${"encoding"}' on type '${"type"}' is expected to be serialized as '${"expected"}' but got '${"actual"}'.`,
            wrongNumericEncodingType: paramMessage `Encoding '${"encoding"}' on type '${"type"}' is expected to be serialized as '${"expected"}' but got '${"actual"}'. Set '@encode' 2nd parameter to be of type ${"expected"}. e.g. '@encode("${"encoding"}", int32)'`,
            firstArg: `First argument of "@encode" must be the encoding name or the string type when encoding numeric types.`,
        },
    },
    "invalid-mime-type": {
        severity: "error",
        messages: {
            default: paramMessage `Invalid mime type '${"mimeType"}'`,
        },
    },
    "no-mime-type-suffix": {
        severity: "error",
        messages: {
            default: paramMessage `Cannot use mime type '${"mimeType"}' with suffix '${"suffix"}'. Use a simple mime \`type/subtype\` instead.`,
        },
    },
    "encoded-name-conflict": {
        severity: "error",
        messages: {
            default: paramMessage `Encoded name '${"name"}' conflicts with existing member name for mime type '${"mimeType"}'`,
            duplicate: paramMessage `Same encoded name '${"name"}' is used for 2 members '${"mimeType"}'`,
        },
    },
    "incompatible-paging-props": {
        severity: "error",
        messages: {
            default: paramMessage `Paging property has multiple types: '${"kinds"}'`,
        },
    },
    "invalid-paging-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Paging property '${"kind"}' is not valid in this context.`,
            input: paramMessage `Paging property '${"kind"}' cannot be used in the parameters of an operation.`,
            output: paramMessage `Paging property '${"kind"}' cannot be used in the return type of an operation.`,
        },
    },
    "duplicate-paging-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Duplicate property paging '${"kind"}' for operation ${"operationName"}.`,
        },
    },
    "missing-paging-items": {
        severity: "error",
        messages: {
            default: paramMessage `Paged operation '${"operationName"}' return type must have a property annotated with @pageItems.`,
        },
    },
    /**
     * Service
     */
    "service-decorator-duplicate": {
        severity: "error",
        messages: {
            default: `@service can only be set once per TypeSpec document.`,
        },
    },
    "list-type-not-model": {
        severity: "error",
        messages: {
            default: "@list decorator's parameter must be a model type.",
        },
    },
    "invalid-range": {
        severity: "error",
        messages: {
            default: paramMessage `Range "${"start"}..${"end"}" is invalid.`,
        },
    },
    /**
     * Mutator
     */
    "add-response": {
        severity: "error",
        messages: {
            default: "Cannot add a response to anything except an operation statement.",
        },
    },
    "add-parameter": {
        severity: "error",
        messages: {
            default: "Cannot add a parameter to anything except an operation statement.",
        },
    },
    "add-model-property": {
        severity: "error",
        messages: {
            default: "Cannot add a model property to anything except a model statement.",
        },
    },
    "add-model-property-fail": {
        severity: "error",
        messages: {
            default: paramMessage `Could not add property/parameter "${"propertyName"}" of type "${"propertyTypeName"}"`,
        },
    },
    "add-response-type": {
        severity: "error",
        messages: {
            default: paramMessage `Could not add response type "${"responseTypeName"}" to operation ${"operationName"}"`,
        },
    },
    "circular-base-type": {
        severity: "error",
        messages: {
            default: paramMessage `Type '${"typeName"}' recursively references itself as a base type.`,
        },
    },
    "circular-constraint": {
        severity: "error",
        messages: {
            default: paramMessage `Type parameter '${"typeName"}' has a circular constraint.`,
        },
    },
    "circular-op-signature": {
        severity: "error",
        messages: {
            default: paramMessage `Operation '${"typeName"}' recursively references itself.`,
        },
    },
    "circular-alias-type": {
        severity: "error",
        messages: {
            default: paramMessage `Alias type '${"typeName"}' recursively references itself.`,
        },
    },
    "circular-const": {
        severity: "error",
        messages: {
            default: paramMessage `const '${"name"}' recursively references itself.`,
        },
    },
    "circular-prop": {
        severity: "error",
        messages: {
            default: paramMessage `Property '${"propName"}' recursively references itself.`,
        },
    },
    "conflict-marker": {
        severity: "error",
        messages: {
            default: "Conflict marker encountered.",
        },
    },
    // #region Visibility
    "visibility-sealed": {
        severity: "error",
        messages: {
            default: paramMessage `Visibility of property '${"propName"}' is sealed and cannot be changed.`,
        },
    },
    "default-visibility-not-member": {
        severity: "error",
        messages: {
            default: "The default visibility modifiers of a class must be members of the class enum.",
        },
    },
    "operation-visibility-constraint-empty": {
        severity: "error",
        messages: {
            default: "Operation visibility constraints with no arguments are not allowed.",
            returnType: "Return type visibility constraints with no arguments are not allowed.",
            parameter: "Parameter visibility constraints with no arguments are not allowed. To disable effective PATCH optionality, use @patch(#{ implicitOptionality: false }) instead.",
        },
    },
    // #endregion
    // #region CLI
    "no-compatible-vs-installed": {
        severity: "error",
        messages: {
            default: "No compatible version of Visual Studio found.",
        },
    },
    "vs-extension-windows-only": {
        severity: "error",
        messages: {
            default: "Visual Studio extension is not supported on non-Windows.",
        },
    },
    "vscode-in-path": {
        severity: "error",
        messages: {
            default: "Couldn't find VS Code 'code' command in PATH. Make sure you have the VS Code executable added to the system PATH.",
            osx: "Couldn't find VS Code 'code' command in PATH. Make sure you have the VS Code executable added to the system PATH.\nSee instruction for Mac OS here https://code.visualstudio.com/docs/setup/mac",
        },
    },
    // #endregion CLI
};
const { createDiagnostic, reportDiagnostic } = createDiagnosticCreator(diagnostics);

var browser$1 = {exports: {}};

// shim for using process in browser
var process = browser$1.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ());
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop$1() {}

process.on = noop$1;
process.addListener = noop$1;
process.once = noop$1;
process.off = noop$1;
process.removeListener = noop$1;
process.removeAllListeners = noop$1;
process.emit = noop$1;
process.prependListener = noop$1;
process.prependOnceListener = noop$1;

process.listeners = function (name) { return [] };

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };

function noop() {}
var browser = /** @type {boolean} */browser$1.exports.browser;
var emitWarning = noop;
var binding = /** @type {Function} */browser$1.exports.binding;
var exit = noop;
var pid = 1;
var features = {};
var kill = noop;
var dlopen = noop;
var uptime = noop;
var memoryUsage = noop;
var uvCounters = noop;
var platform = 'browser';
var arch = 'browser';
var execPath = 'browser';
var execArgv = /** @type {string[]} */[];
var api = {
  nextTick: browser$1.exports.nextTick,
  title: browser$1.exports.title,
  browser: browser,
  env: browser$1.exports.env,
  argv: browser$1.exports.argv,
  version: browser$1.exports.version,
  versions: browser$1.exports.versions,
  on: browser$1.exports.on,
  addListener: browser$1.exports.addListener,
  once: browser$1.exports.once,
  off: browser$1.exports.off,
  removeListener: browser$1.exports.removeListener,
  removeAllListeners: browser$1.exports.removeAllListeners,
  emit: browser$1.exports.emit,
  emitWarning: emitWarning,
  prependListener: browser$1.exports.prependListener,
  prependOnceListener: browser$1.exports.prependOnceListener,
  listeners: browser$1.exports.listeners,
  binding: binding,
  cwd: browser$1.exports.cwd,
  chdir: browser$1.exports.chdir,
  umask: browser$1.exports.umask,
  exit: exit,
  pid: pid,
  features: features,
  kill: kill,
  dlopen: dlopen,
  uptime: uptime,
  memoryUsage: memoryUsage,
  uvCounters: uvCounters,
  platform: platform,
  arch: arch,
  execPath: execPath,
  execArgv: execArgv
};

browser$1.exports.addListener;
browser$1.exports.argv;
browser$1.exports.chdir;
browser$1.exports.cwd;
browser$1.exports.emit;
browser$1.exports.env;
browser$1.exports.listeners;
browser$1.exports.nextTick;
browser$1.exports.off;
browser$1.exports.on;
browser$1.exports.once;
browser$1.exports.prependListener;
browser$1.exports.prependOnceListener;
browser$1.exports.removeAllListeners;
browser$1.exports.removeListener;
browser$1.exports.title;
browser$1.exports.umask;
browser$1.exports.version;
browser$1.exports.versions;

// noop logger shouldn't be used in browser
function formatLog(log) {
    return JSON.stringify(log);
}

function createSourceFile(text, path) {
    let lineStarts = undefined;
    return {
        text,
        path,
        getLineStarts,
        getLineAndCharacterOfPosition,
    };
    function getLineStarts() {
        return (lineStarts = lineStarts ?? scanLineStarts(text));
    }
    function getLineAndCharacterOfPosition(position) {
        const starts = getLineStarts();
        let line = binarySearch(starts, position);
        // When binarySearch returns < 0 indicating that the value was not found, it
        // returns the bitwise complement of the index where the value would need to
        // be inserted to keep the array sorted. So flipping the bits back to this
        // positive index tells us what the line number would be if we were to
        // create a new line starting at the given position, and subtracting 1 from
        // that therefore gives us the line number we're after.
        if (line < 0) {
            line = ~line - 1;
        }
        return {
            line,
            character: position - starts[line],
        };
    }
}
function getSourceFileKindFromExt(path) {
    const ext = getAnyExtensionFromPath(path);
    if (ext === ".js" || ext === ".mjs") {
        return "js";
    }
    else if (ext === ".tsp") {
        return "typespec";
    }
    else {
        return undefined;
    }
}
function scanLineStarts(text) {
    const starts = [];
    let start = 0;
    let pos = 0;
    while (pos < text.length) {
        const ch = text.charCodeAt(pos);
        pos++;
        switch (ch) {
            case 13 /* CharCode.CarriageReturn */:
                if (text.charCodeAt(pos) === 10 /* CharCode.LineFeed */) {
                    pos++;
                }
            // fallthrough
            case 10 /* CharCode.LineFeed */:
                starts.push(start);
                start = pos;
                break;
        }
    }
    starts.push(start);
    return starts;
}
/**
 * Search sorted array of numbers for the given value. If found, return index
 * in array where value was found. If not found, return a negative number that
 * is the bitwise complement of the index where value would need to be inserted
 * to keep the array sorted.
 */
function binarySearch(array, value) {
    let low = 0;
    let high = array.length - 1;
    while (low <= high) {
        const middle = low + ((high - low) >> 1);
        const v = array[middle];
        if (v < value) {
            low = middle + 1;
        }
        else if (v > value) {
            high = middle - 1;
        }
        else {
            return middle;
        }
    }
    return ~low;
}

var ResolutionResultFlags;
(function (ResolutionResultFlags) {
    ResolutionResultFlags[ResolutionResultFlags["None"] = 0] = "None";
    ResolutionResultFlags[ResolutionResultFlags["Resolved"] = 2] = "Resolved";
    ResolutionResultFlags[ResolutionResultFlags["Unknown"] = 4] = "Unknown";
    ResolutionResultFlags[ResolutionResultFlags["Ambiguous"] = 8] = "Ambiguous";
    ResolutionResultFlags[ResolutionResultFlags["NotFound"] = 16] = "NotFound";
    ResolutionResultFlags[ResolutionResultFlags["ResolutionFailed"] = 28] = "ResolutionFailed";
})(ResolutionResultFlags || (ResolutionResultFlags = {}));
/**
 * AST types
 */
var SyntaxKind;
(function (SyntaxKind) {
    SyntaxKind[SyntaxKind["TypeSpecScript"] = 0] = "TypeSpecScript";
    SyntaxKind[SyntaxKind["JsSourceFile"] = 1] = "JsSourceFile";
    SyntaxKind[SyntaxKind["ImportStatement"] = 2] = "ImportStatement";
    SyntaxKind[SyntaxKind["Identifier"] = 3] = "Identifier";
    SyntaxKind[SyntaxKind["AugmentDecoratorStatement"] = 4] = "AugmentDecoratorStatement";
    SyntaxKind[SyntaxKind["DecoratorExpression"] = 5] = "DecoratorExpression";
    SyntaxKind[SyntaxKind["DirectiveExpression"] = 6] = "DirectiveExpression";
    SyntaxKind[SyntaxKind["MemberExpression"] = 7] = "MemberExpression";
    SyntaxKind[SyntaxKind["NamespaceStatement"] = 8] = "NamespaceStatement";
    SyntaxKind[SyntaxKind["UsingStatement"] = 9] = "UsingStatement";
    SyntaxKind[SyntaxKind["OperationStatement"] = 10] = "OperationStatement";
    SyntaxKind[SyntaxKind["OperationSignatureDeclaration"] = 11] = "OperationSignatureDeclaration";
    SyntaxKind[SyntaxKind["OperationSignatureReference"] = 12] = "OperationSignatureReference";
    SyntaxKind[SyntaxKind["ModelStatement"] = 13] = "ModelStatement";
    SyntaxKind[SyntaxKind["ModelExpression"] = 14] = "ModelExpression";
    SyntaxKind[SyntaxKind["ModelProperty"] = 15] = "ModelProperty";
    SyntaxKind[SyntaxKind["ModelSpreadProperty"] = 16] = "ModelSpreadProperty";
    SyntaxKind[SyntaxKind["ScalarStatement"] = 17] = "ScalarStatement";
    SyntaxKind[SyntaxKind["InterfaceStatement"] = 18] = "InterfaceStatement";
    SyntaxKind[SyntaxKind["UnionStatement"] = 19] = "UnionStatement";
    SyntaxKind[SyntaxKind["UnionVariant"] = 20] = "UnionVariant";
    SyntaxKind[SyntaxKind["EnumStatement"] = 21] = "EnumStatement";
    SyntaxKind[SyntaxKind["EnumMember"] = 22] = "EnumMember";
    SyntaxKind[SyntaxKind["EnumSpreadMember"] = 23] = "EnumSpreadMember";
    SyntaxKind[SyntaxKind["AliasStatement"] = 24] = "AliasStatement";
    SyntaxKind[SyntaxKind["DecoratorDeclarationStatement"] = 25] = "DecoratorDeclarationStatement";
    SyntaxKind[SyntaxKind["FunctionDeclarationStatement"] = 26] = "FunctionDeclarationStatement";
    SyntaxKind[SyntaxKind["FunctionParameter"] = 27] = "FunctionParameter";
    SyntaxKind[SyntaxKind["UnionExpression"] = 28] = "UnionExpression";
    SyntaxKind[SyntaxKind["IntersectionExpression"] = 29] = "IntersectionExpression";
    SyntaxKind[SyntaxKind["TupleExpression"] = 30] = "TupleExpression";
    SyntaxKind[SyntaxKind["ArrayExpression"] = 31] = "ArrayExpression";
    SyntaxKind[SyntaxKind["StringLiteral"] = 32] = "StringLiteral";
    SyntaxKind[SyntaxKind["NumericLiteral"] = 33] = "NumericLiteral";
    SyntaxKind[SyntaxKind["BooleanLiteral"] = 34] = "BooleanLiteral";
    SyntaxKind[SyntaxKind["StringTemplateExpression"] = 35] = "StringTemplateExpression";
    SyntaxKind[SyntaxKind["StringTemplateHead"] = 36] = "StringTemplateHead";
    SyntaxKind[SyntaxKind["StringTemplateMiddle"] = 37] = "StringTemplateMiddle";
    SyntaxKind[SyntaxKind["StringTemplateTail"] = 38] = "StringTemplateTail";
    SyntaxKind[SyntaxKind["StringTemplateSpan"] = 39] = "StringTemplateSpan";
    SyntaxKind[SyntaxKind["ExternKeyword"] = 40] = "ExternKeyword";
    SyntaxKind[SyntaxKind["VoidKeyword"] = 41] = "VoidKeyword";
    SyntaxKind[SyntaxKind["NeverKeyword"] = 42] = "NeverKeyword";
    SyntaxKind[SyntaxKind["UnknownKeyword"] = 43] = "UnknownKeyword";
    SyntaxKind[SyntaxKind["ValueOfExpression"] = 44] = "ValueOfExpression";
    SyntaxKind[SyntaxKind["TypeReference"] = 45] = "TypeReference";
    SyntaxKind[SyntaxKind["TemplateParameterDeclaration"] = 46] = "TemplateParameterDeclaration";
    SyntaxKind[SyntaxKind["EmptyStatement"] = 47] = "EmptyStatement";
    SyntaxKind[SyntaxKind["InvalidStatement"] = 48] = "InvalidStatement";
    SyntaxKind[SyntaxKind["LineComment"] = 49] = "LineComment";
    SyntaxKind[SyntaxKind["BlockComment"] = 50] = "BlockComment";
    SyntaxKind[SyntaxKind["Doc"] = 51] = "Doc";
    SyntaxKind[SyntaxKind["DocText"] = 52] = "DocText";
    SyntaxKind[SyntaxKind["DocParamTag"] = 53] = "DocParamTag";
    SyntaxKind[SyntaxKind["DocPropTag"] = 54] = "DocPropTag";
    SyntaxKind[SyntaxKind["DocReturnsTag"] = 55] = "DocReturnsTag";
    SyntaxKind[SyntaxKind["DocErrorsTag"] = 56] = "DocErrorsTag";
    SyntaxKind[SyntaxKind["DocTemplateTag"] = 57] = "DocTemplateTag";
    SyntaxKind[SyntaxKind["DocUnknownTag"] = 58] = "DocUnknownTag";
    SyntaxKind[SyntaxKind["Return"] = 59] = "Return";
    SyntaxKind[SyntaxKind["JsNamespaceDeclaration"] = 60] = "JsNamespaceDeclaration";
    SyntaxKind[SyntaxKind["TemplateArgument"] = 61] = "TemplateArgument";
    SyntaxKind[SyntaxKind["TypeOfExpression"] = 62] = "TypeOfExpression";
    SyntaxKind[SyntaxKind["ObjectLiteral"] = 63] = "ObjectLiteral";
    SyntaxKind[SyntaxKind["ObjectLiteralProperty"] = 64] = "ObjectLiteralProperty";
    SyntaxKind[SyntaxKind["ObjectLiteralSpreadProperty"] = 65] = "ObjectLiteralSpreadProperty";
    SyntaxKind[SyntaxKind["ArrayLiteral"] = 66] = "ArrayLiteral";
    SyntaxKind[SyntaxKind["ConstStatement"] = 67] = "ConstStatement";
    SyntaxKind[SyntaxKind["CallExpression"] = 68] = "CallExpression";
    SyntaxKind[SyntaxKind["ScalarConstructor"] = 69] = "ScalarConstructor";
})(SyntaxKind || (SyntaxKind = {}));
var IdentifierKind;
(function (IdentifierKind) {
    IdentifierKind[IdentifierKind["TypeReference"] = 0] = "TypeReference";
    IdentifierKind[IdentifierKind["TemplateArgument"] = 1] = "TemplateArgument";
    IdentifierKind[IdentifierKind["Decorator"] = 2] = "Decorator";
    IdentifierKind[IdentifierKind["Function"] = 3] = "Function";
    IdentifierKind[IdentifierKind["Using"] = 4] = "Using";
    IdentifierKind[IdentifierKind["Declaration"] = 5] = "Declaration";
    IdentifierKind[IdentifierKind["ModelExpressionProperty"] = 6] = "ModelExpressionProperty";
    IdentifierKind[IdentifierKind["ModelStatementProperty"] = 7] = "ModelStatementProperty";
    IdentifierKind[IdentifierKind["ObjectLiteralProperty"] = 8] = "ObjectLiteralProperty";
    IdentifierKind[IdentifierKind["Other"] = 9] = "Other";
})(IdentifierKind || (IdentifierKind = {}));
/** Used to explicitly specify that a diagnostic has no target. */
const NoTarget = Symbol.for("NoTarget");
var ListenerFlow;
(function (ListenerFlow) {
    /**
     * Do not navigate any containing or referenced type.
     */
    ListenerFlow[ListenerFlow["NoRecursion"] = 1] = "NoRecursion";
})(ListenerFlow || (ListenerFlow = {}));

function logDiagnostics(diagnostics, logger) {
    for (const diagnostic of diagnostics) {
        logger.log({
            level: diagnostic.severity,
            message: diagnostic.message,
            code: diagnostic.code,
            url: diagnostic.url,
            sourceLocation: getSourceLocation(diagnostic.target, { locateId: true }),
            related: getRelatedLocations(diagnostic),
        });
    }
}
function formatDiagnostic(diagnostic, options = {}) {
    return formatLog({
        code: diagnostic.code,
        level: diagnostic.severity,
        message: diagnostic.message,
        url: diagnostic.url,
        sourceLocation: getSourceLocation(diagnostic.target, { locateId: true }),
        related: getRelatedLocations(diagnostic),
    }, { pretty: options?.pretty ?? false, pathRelativeTo: options?.pathRelativeTo });
}
function getRelatedLocations(diagnostic) {
    return getDiagnosticTemplateInstantitationTrace(diagnostic.target).map((x) => {
        return {
            message: "occurred while instantiating template",
            location: getSourceLocation(x),
        };
    });
}
function getSourceLocation(target, options = {}) {
    if (target === NoTarget || target === undefined) {
        return undefined;
    }
    if ("file" in target) {
        return target;
    }
    if (!("kind" in target) && !("entityKind" in target)) {
        // TemplateInstanceTarget
        if (!("declarations" in target)) {
            return getSourceLocationOfNode(target.node, options);
        }
        // symbol
        if (target.flags & 8192 /* SymbolFlags.Using */) {
            target = target.symbolSource;
        }
        if (!target.declarations[0]) {
            return createSyntheticSourceLocation();
        }
        return getSourceLocationOfNode(target.declarations[0], options);
    }
    else if ("kind" in target && typeof target.kind === "number") {
        // node
        return getSourceLocationOfNode(target, options);
    }
    else {
        // type
        const targetNode = target.node;
        if (targetNode) {
            return getSourceLocationOfNode(targetNode, options);
        }
        return createSyntheticSourceLocation();
    }
}
/**
 * @internal
 */
function getDiagnosticTemplateInstantitationTrace(target) {
    if (typeof target !== "object" || !("templateMapper" in target)) {
        return [];
    }
    const result = [];
    let current = target.templateMapper;
    while (current) {
        result.push(current.source.node);
        current = current.source.mapper;
    }
    return result;
}
function createSyntheticSourceLocation(loc = "<unknown location>") {
    return {
        file: createSourceFile("", loc),
        pos: 0,
        end: 0,
        isSynthetic: true,
    };
}
function getSourceLocationOfNode(node, options) {
    let root = node;
    while (root.parent !== undefined) {
        root = root.parent;
    }
    if (root.kind !== SyntaxKind.TypeSpecScript && root.kind !== SyntaxKind.JsSourceFile) {
        return createSyntheticSourceLocation(node.flags & 8 /* NodeFlags.Synthetic */
            ? undefined
            : "<unknown location - cannot obtain source location of unbound node - file bug at https://github.com/microsoft/typespec>");
    }
    if (options.locateId && "id" in node && node.id !== undefined) {
        node = node.id;
    }
    return {
        file: root.file,
        pos: node.pos,
        end: node.end,
    };
}
/**
 * Use this to report bugs in the compiler, and not errors in the source code
 * being compiled.
 *
 * @param condition Throw if this is not true.
 *
 * @param message Error message.
 *
 * @param target Optional location in source code that might give a clue about
 *               what got the compiler off track.
 */
function compilerAssert(condition, message, target) {
    if (condition) {
        return;
    }
    if (target) {
        let location;
        try {
            location = getSourceLocation(target);
        }
        catch (err) { }
        if (location) {
            const pos = location.file.getLineAndCharacterOfPosition(location.pos);
            const file = location.file.path;
            const line = pos.line + 1;
            const col = pos.character + 1;
            message += `\nOccurred while compiling code in ${file} near line ${line}, column ${col}`;
        }
    }
    throw new Error(message);
}
/**
 * Assert that the input type has one of the kinds provided
 */
function assertType(typeDescription, t, ...kinds) {
    if (kinds.indexOf(t.kind) === -1) {
        throw new Error(`Expected ${typeDescription} to be type ${kinds.join(", ")}`);
    }
}
/**
 * Report a deprecated diagnostic.
 * @param program TypeSpec Program.
 * @param message Message describing the deprecation.
 * @param target Target of the deprecation.
 */
function reportDeprecated(program, message, target) {
    program.reportDiagnostic({
        severity: "warning",
        code: "deprecated",
        message: `Deprecated: ${message}`,
        target,
    });
}
/**
 * Create a new instance of the @see DiagnosticCollector.
 */
function createDiagnosticCollector() {
    const diagnostics = [];
    return {
        diagnostics,
        add,
        pipe,
        wrap,
        join,
    };
    function add(diagnostic) {
        diagnostics.push(diagnostic);
    }
    function pipe(result) {
        const [value, diags] = result;
        for (const diag of diags) {
            diagnostics.push(diag);
        }
        return value;
    }
    function wrap(value) {
        return [value, diagnostics];
    }
    function join(result) {
        const [value, diags] = result;
        for (const diag of diags) {
            diagnostics.push(diag);
        }
        return [value, diagnostics];
    }
}
/**
 * Ignore the diagnostics emitted by the diagnostic accessor pattern and just return the actual result.
 * @param result Accessor pattern tuple result including the actual result and the list of diagnostics.
 * @returns Actual result.
 */
function ignoreDiagnostics(result) {
    return result[0];
}
function defineCodeFix(fix) {
    return fix;
}

//
// Generated by scripts/regen-nonascii-map.js
// on node v18.16.0 with unicode 15.0.
//
/**
 * @internal
 *
 * Map of non-ascii characters that are valid in an identifier. Each pair of
 * numbers represents an inclusive range of code points.
 */
//prettier-ignore
const nonAsciiIdentifierMap = [
    0xa0, 0x377,
    0x37a, 0x37f,
    0x384, 0x38a,
    0x38c, 0x38c,
    0x38e, 0x3a1,
    0x3a3, 0x52f,
    0x531, 0x556,
    0x559, 0x58a,
    0x58d, 0x58f,
    0x591, 0x5c7,
    0x5d0, 0x5ea,
    0x5ef, 0x5f4,
    0x600, 0x70d,
    0x70f, 0x74a,
    0x74d, 0x7b1,
    0x7c0, 0x7fa,
    0x7fd, 0x82d,
    0x830, 0x83e,
    0x840, 0x85b,
    0x85e, 0x85e,
    0x860, 0x86a,
    0x870, 0x88e,
    0x890, 0x891,
    0x898, 0x983,
    0x985, 0x98c,
    0x98f, 0x990,
    0x993, 0x9a8,
    0x9aa, 0x9b0,
    0x9b2, 0x9b2,
    0x9b6, 0x9b9,
    0x9bc, 0x9c4,
    0x9c7, 0x9c8,
    0x9cb, 0x9ce,
    0x9d7, 0x9d7,
    0x9dc, 0x9dd,
    0x9df, 0x9e3,
    0x9e6, 0x9fe,
    0xa01, 0xa03,
    0xa05, 0xa0a,
    0xa0f, 0xa10,
    0xa13, 0xa28,
    0xa2a, 0xa30,
    0xa32, 0xa33,
    0xa35, 0xa36,
    0xa38, 0xa39,
    0xa3c, 0xa3c,
    0xa3e, 0xa42,
    0xa47, 0xa48,
    0xa4b, 0xa4d,
    0xa51, 0xa51,
    0xa59, 0xa5c,
    0xa5e, 0xa5e,
    0xa66, 0xa76,
    0xa81, 0xa83,
    0xa85, 0xa8d,
    0xa8f, 0xa91,
    0xa93, 0xaa8,
    0xaaa, 0xab0,
    0xab2, 0xab3,
    0xab5, 0xab9,
    0xabc, 0xac5,
    0xac7, 0xac9,
    0xacb, 0xacd,
    0xad0, 0xad0,
    0xae0, 0xae3,
    0xae6, 0xaf1,
    0xaf9, 0xaff,
    0xb01, 0xb03,
    0xb05, 0xb0c,
    0xb0f, 0xb10,
    0xb13, 0xb28,
    0xb2a, 0xb30,
    0xb32, 0xb33,
    0xb35, 0xb39,
    0xb3c, 0xb44,
    0xb47, 0xb48,
    0xb4b, 0xb4d,
    0xb55, 0xb57,
    0xb5c, 0xb5d,
    0xb5f, 0xb63,
    0xb66, 0xb77,
    0xb82, 0xb83,
    0xb85, 0xb8a,
    0xb8e, 0xb90,
    0xb92, 0xb95,
    0xb99, 0xb9a,
    0xb9c, 0xb9c,
    0xb9e, 0xb9f,
    0xba3, 0xba4,
    0xba8, 0xbaa,
    0xbae, 0xbb9,
    0xbbe, 0xbc2,
    0xbc6, 0xbc8,
    0xbca, 0xbcd,
    0xbd0, 0xbd0,
    0xbd7, 0xbd7,
    0xbe6, 0xbfa,
    0xc00, 0xc0c,
    0xc0e, 0xc10,
    0xc12, 0xc28,
    0xc2a, 0xc39,
    0xc3c, 0xc44,
    0xc46, 0xc48,
    0xc4a, 0xc4d,
    0xc55, 0xc56,
    0xc58, 0xc5a,
    0xc5d, 0xc5d,
    0xc60, 0xc63,
    0xc66, 0xc6f,
    0xc77, 0xc8c,
    0xc8e, 0xc90,
    0xc92, 0xca8,
    0xcaa, 0xcb3,
    0xcb5, 0xcb9,
    0xcbc, 0xcc4,
    0xcc6, 0xcc8,
    0xcca, 0xccd,
    0xcd5, 0xcd6,
    0xcdd, 0xcde,
    0xce0, 0xce3,
    0xce6, 0xcef,
    0xcf1, 0xcf3,
    0xd00, 0xd0c,
    0xd0e, 0xd10,
    0xd12, 0xd44,
    0xd46, 0xd48,
    0xd4a, 0xd4f,
    0xd54, 0xd63,
    0xd66, 0xd7f,
    0xd81, 0xd83,
    0xd85, 0xd96,
    0xd9a, 0xdb1,
    0xdb3, 0xdbb,
    0xdbd, 0xdbd,
    0xdc0, 0xdc6,
    0xdca, 0xdca,
    0xdcf, 0xdd4,
    0xdd6, 0xdd6,
    0xdd8, 0xddf,
    0xde6, 0xdef,
    0xdf2, 0xdf4,
    0xe01, 0xe3a,
    0xe3f, 0xe5b,
    0xe81, 0xe82,
    0xe84, 0xe84,
    0xe86, 0xe8a,
    0xe8c, 0xea3,
    0xea5, 0xea5,
    0xea7, 0xebd,
    0xec0, 0xec4,
    0xec6, 0xec6,
    0xec8, 0xece,
    0xed0, 0xed9,
    0xedc, 0xedf,
    0xf00, 0xf47,
    0xf49, 0xf6c,
    0xf71, 0xf97,
    0xf99, 0xfbc,
    0xfbe, 0xfcc,
    0xfce, 0xfda,
    0x1000, 0x10c5,
    0x10c7, 0x10c7,
    0x10cd, 0x10cd,
    0x10d0, 0x1248,
    0x124a, 0x124d,
    0x1250, 0x1256,
    0x1258, 0x1258,
    0x125a, 0x125d,
    0x1260, 0x1288,
    0x128a, 0x128d,
    0x1290, 0x12b0,
    0x12b2, 0x12b5,
    0x12b8, 0x12be,
    0x12c0, 0x12c0,
    0x12c2, 0x12c5,
    0x12c8, 0x12d6,
    0x12d8, 0x1310,
    0x1312, 0x1315,
    0x1318, 0x135a,
    0x135d, 0x137c,
    0x1380, 0x1399,
    0x13a0, 0x13f5,
    0x13f8, 0x13fd,
    0x1400, 0x169c,
    0x16a0, 0x16f8,
    0x1700, 0x1715,
    0x171f, 0x1736,
    0x1740, 0x1753,
    0x1760, 0x176c,
    0x176e, 0x1770,
    0x1772, 0x1773,
    0x1780, 0x17dd,
    0x17e0, 0x17e9,
    0x17f0, 0x17f9,
    0x1800, 0x1819,
    0x1820, 0x1878,
    0x1880, 0x18aa,
    0x18b0, 0x18f5,
    0x1900, 0x191e,
    0x1920, 0x192b,
    0x1930, 0x193b,
    0x1940, 0x1940,
    0x1944, 0x196d,
    0x1970, 0x1974,
    0x1980, 0x19ab,
    0x19b0, 0x19c9,
    0x19d0, 0x19da,
    0x19de, 0x1a1b,
    0x1a1e, 0x1a5e,
    0x1a60, 0x1a7c,
    0x1a7f, 0x1a89,
    0x1a90, 0x1a99,
    0x1aa0, 0x1aad,
    0x1ab0, 0x1ace,
    0x1b00, 0x1b4c,
    0x1b50, 0x1b7e,
    0x1b80, 0x1bf3,
    0x1bfc, 0x1c37,
    0x1c3b, 0x1c49,
    0x1c4d, 0x1c88,
    0x1c90, 0x1cba,
    0x1cbd, 0x1cc7,
    0x1cd0, 0x1cfa,
    0x1d00, 0x1f15,
    0x1f18, 0x1f1d,
    0x1f20, 0x1f45,
    0x1f48, 0x1f4d,
    0x1f50, 0x1f57,
    0x1f59, 0x1f59,
    0x1f5b, 0x1f5b,
    0x1f5d, 0x1f5d,
    0x1f5f, 0x1f7d,
    0x1f80, 0x1fb4,
    0x1fb6, 0x1fc4,
    0x1fc6, 0x1fd3,
    0x1fd6, 0x1fdb,
    0x1fdd, 0x1fef,
    0x1ff2, 0x1ff4,
    0x1ff6, 0x1ffe,
    0x2000, 0x200d,
    0x2010, 0x2027,
    0x202a, 0x2064,
    0x2066, 0x2071,
    0x2074, 0x208e,
    0x2090, 0x209c,
    0x20a0, 0x20c0,
    0x20d0, 0x20f0,
    0x2100, 0x218b,
    0x2190, 0x2426,
    0x2440, 0x244a,
    0x2460, 0x2b73,
    0x2b76, 0x2b95,
    0x2b97, 0x2cf3,
    0x2cf9, 0x2d25,
    0x2d27, 0x2d27,
    0x2d2d, 0x2d2d,
    0x2d30, 0x2d67,
    0x2d6f, 0x2d70,
    0x2d7f, 0x2d96,
    0x2da0, 0x2da6,
    0x2da8, 0x2dae,
    0x2db0, 0x2db6,
    0x2db8, 0x2dbe,
    0x2dc0, 0x2dc6,
    0x2dc8, 0x2dce,
    0x2dd0, 0x2dd6,
    0x2dd8, 0x2dde,
    0x2de0, 0x2e5d,
    0x2e80, 0x2e99,
    0x2e9b, 0x2ef3,
    0x2f00, 0x2fd5,
    0x2ff0, 0x2ffb,
    0x3000, 0x303f,
    0x3041, 0x3096,
    0x3099, 0x30ff,
    0x3105, 0x312f,
    0x3131, 0x318e,
    0x3190, 0x31e3,
    0x31f0, 0x321e,
    0x3220, 0xa48c,
    0xa490, 0xa4c6,
    0xa4d0, 0xa62b,
    0xa640, 0xa6f7,
    0xa700, 0xa7ca,
    0xa7d0, 0xa7d1,
    0xa7d3, 0xa7d3,
    0xa7d5, 0xa7d9,
    0xa7f2, 0xa82c,
    0xa830, 0xa839,
    0xa840, 0xa877,
    0xa880, 0xa8c5,
    0xa8ce, 0xa8d9,
    0xa8e0, 0xa953,
    0xa95f, 0xa97c,
    0xa980, 0xa9cd,
    0xa9cf, 0xa9d9,
    0xa9de, 0xa9fe,
    0xaa00, 0xaa36,
    0xaa40, 0xaa4d,
    0xaa50, 0xaa59,
    0xaa5c, 0xaac2,
    0xaadb, 0xaaf6,
    0xab01, 0xab06,
    0xab09, 0xab0e,
    0xab11, 0xab16,
    0xab20, 0xab26,
    0xab28, 0xab2e,
    0xab30, 0xab6b,
    0xab70, 0xabed,
    0xabf0, 0xabf9,
    0xac00, 0xd7a3,
    0xd7b0, 0xd7c6,
    0xd7cb, 0xd7fb,
    0xf900, 0xfa6d,
    0xfa70, 0xfad9,
    0xfb00, 0xfb06,
    0xfb13, 0xfb17,
    0xfb1d, 0xfb36,
    0xfb38, 0xfb3c,
    0xfb3e, 0xfb3e,
    0xfb40, 0xfb41,
    0xfb43, 0xfb44,
    0xfb46, 0xfbc2,
    0xfbd3, 0xfd8f,
    0xfd92, 0xfdc7,
    0xfdcf, 0xfdcf,
    0xfdf0, 0xfe19,
    0xfe20, 0xfe52,
    0xfe54, 0xfe66,
    0xfe68, 0xfe6b,
    0xfe70, 0xfe74,
    0xfe76, 0xfefc,
    0xfeff, 0xfeff,
    0xff01, 0xffbe,
    0xffc2, 0xffc7,
    0xffca, 0xffcf,
    0xffd2, 0xffd7,
    0xffda, 0xffdc,
    0xffe0, 0xffe6,
    0xffe8, 0xffee,
    0xfff9, 0xfffc,
    0x10000, 0x1000b,
    0x1000d, 0x10026,
    0x10028, 0x1003a,
    0x1003c, 0x1003d,
    0x1003f, 0x1004d,
    0x10050, 0x1005d,
    0x10080, 0x100fa,
    0x10100, 0x10102,
    0x10107, 0x10133,
    0x10137, 0x1018e,
    0x10190, 0x1019c,
    0x101a0, 0x101a0,
    0x101d0, 0x101fd,
    0x10280, 0x1029c,
    0x102a0, 0x102d0,
    0x102e0, 0x102fb,
    0x10300, 0x10323,
    0x1032d, 0x1034a,
    0x10350, 0x1037a,
    0x10380, 0x1039d,
    0x1039f, 0x103c3,
    0x103c8, 0x103d5,
    0x10400, 0x1049d,
    0x104a0, 0x104a9,
    0x104b0, 0x104d3,
    0x104d8, 0x104fb,
    0x10500, 0x10527,
    0x10530, 0x10563,
    0x1056f, 0x1057a,
    0x1057c, 0x1058a,
    0x1058c, 0x10592,
    0x10594, 0x10595,
    0x10597, 0x105a1,
    0x105a3, 0x105b1,
    0x105b3, 0x105b9,
    0x105bb, 0x105bc,
    0x10600, 0x10736,
    0x10740, 0x10755,
    0x10760, 0x10767,
    0x10780, 0x10785,
    0x10787, 0x107b0,
    0x107b2, 0x107ba,
    0x10800, 0x10805,
    0x10808, 0x10808,
    0x1080a, 0x10835,
    0x10837, 0x10838,
    0x1083c, 0x1083c,
    0x1083f, 0x10855,
    0x10857, 0x1089e,
    0x108a7, 0x108af,
    0x108e0, 0x108f2,
    0x108f4, 0x108f5,
    0x108fb, 0x1091b,
    0x1091f, 0x10939,
    0x1093f, 0x1093f,
    0x10980, 0x109b7,
    0x109bc, 0x109cf,
    0x109d2, 0x10a03,
    0x10a05, 0x10a06,
    0x10a0c, 0x10a13,
    0x10a15, 0x10a17,
    0x10a19, 0x10a35,
    0x10a38, 0x10a3a,
    0x10a3f, 0x10a48,
    0x10a50, 0x10a58,
    0x10a60, 0x10a9f,
    0x10ac0, 0x10ae6,
    0x10aeb, 0x10af6,
    0x10b00, 0x10b35,
    0x10b39, 0x10b55,
    0x10b58, 0x10b72,
    0x10b78, 0x10b91,
    0x10b99, 0x10b9c,
    0x10ba9, 0x10baf,
    0x10c00, 0x10c48,
    0x10c80, 0x10cb2,
    0x10cc0, 0x10cf2,
    0x10cfa, 0x10d27,
    0x10d30, 0x10d39,
    0x10e60, 0x10e7e,
    0x10e80, 0x10ea9,
    0x10eab, 0x10ead,
    0x10eb0, 0x10eb1,
    0x10efd, 0x10f27,
    0x10f30, 0x10f59,
    0x10f70, 0x10f89,
    0x10fb0, 0x10fcb,
    0x10fe0, 0x10ff6,
    0x11000, 0x1104d,
    0x11052, 0x11075,
    0x1107f, 0x110c2,
    0x110cd, 0x110cd,
    0x110d0, 0x110e8,
    0x110f0, 0x110f9,
    0x11100, 0x11134,
    0x11136, 0x11147,
    0x11150, 0x11176,
    0x11180, 0x111df,
    0x111e1, 0x111f4,
    0x11200, 0x11211,
    0x11213, 0x11241,
    0x11280, 0x11286,
    0x11288, 0x11288,
    0x1128a, 0x1128d,
    0x1128f, 0x1129d,
    0x1129f, 0x112a9,
    0x112b0, 0x112ea,
    0x112f0, 0x112f9,
    0x11300, 0x11303,
    0x11305, 0x1130c,
    0x1130f, 0x11310,
    0x11313, 0x11328,
    0x1132a, 0x11330,
    0x11332, 0x11333,
    0x11335, 0x11339,
    0x1133b, 0x11344,
    0x11347, 0x11348,
    0x1134b, 0x1134d,
    0x11350, 0x11350,
    0x11357, 0x11357,
    0x1135d, 0x11363,
    0x11366, 0x1136c,
    0x11370, 0x11374,
    0x11400, 0x1145b,
    0x1145d, 0x11461,
    0x11480, 0x114c7,
    0x114d0, 0x114d9,
    0x11580, 0x115b5,
    0x115b8, 0x115dd,
    0x11600, 0x11644,
    0x11650, 0x11659,
    0x11660, 0x1166c,
    0x11680, 0x116b9,
    0x116c0, 0x116c9,
    0x11700, 0x1171a,
    0x1171d, 0x1172b,
    0x11730, 0x11746,
    0x11800, 0x1183b,
    0x118a0, 0x118f2,
    0x118ff, 0x11906,
    0x11909, 0x11909,
    0x1190c, 0x11913,
    0x11915, 0x11916,
    0x11918, 0x11935,
    0x11937, 0x11938,
    0x1193b, 0x11946,
    0x11950, 0x11959,
    0x119a0, 0x119a7,
    0x119aa, 0x119d7,
    0x119da, 0x119e4,
    0x11a00, 0x11a47,
    0x11a50, 0x11aa2,
    0x11ab0, 0x11af8,
    0x11b00, 0x11b09,
    0x11c00, 0x11c08,
    0x11c0a, 0x11c36,
    0x11c38, 0x11c45,
    0x11c50, 0x11c6c,
    0x11c70, 0x11c8f,
    0x11c92, 0x11ca7,
    0x11ca9, 0x11cb6,
    0x11d00, 0x11d06,
    0x11d08, 0x11d09,
    0x11d0b, 0x11d36,
    0x11d3a, 0x11d3a,
    0x11d3c, 0x11d3d,
    0x11d3f, 0x11d47,
    0x11d50, 0x11d59,
    0x11d60, 0x11d65,
    0x11d67, 0x11d68,
    0x11d6a, 0x11d8e,
    0x11d90, 0x11d91,
    0x11d93, 0x11d98,
    0x11da0, 0x11da9,
    0x11ee0, 0x11ef8,
    0x11f00, 0x11f10,
    0x11f12, 0x11f3a,
    0x11f3e, 0x11f59,
    0x11fb0, 0x11fb0,
    0x11fc0, 0x11ff1,
    0x11fff, 0x12399,
    0x12400, 0x1246e,
    0x12470, 0x12474,
    0x12480, 0x12543,
    0x12f90, 0x12ff2,
    0x13000, 0x13455,
    0x14400, 0x14646,
    0x16800, 0x16a38,
    0x16a40, 0x16a5e,
    0x16a60, 0x16a69,
    0x16a6e, 0x16abe,
    0x16ac0, 0x16ac9,
    0x16ad0, 0x16aed,
    0x16af0, 0x16af5,
    0x16b00, 0x16b45,
    0x16b50, 0x16b59,
    0x16b5b, 0x16b61,
    0x16b63, 0x16b77,
    0x16b7d, 0x16b8f,
    0x16e40, 0x16e9a,
    0x16f00, 0x16f4a,
    0x16f4f, 0x16f87,
    0x16f8f, 0x16f9f,
    0x16fe0, 0x16fe4,
    0x16ff0, 0x16ff1,
    0x17000, 0x187f7,
    0x18800, 0x18cd5,
    0x18d00, 0x18d08,
    0x1aff0, 0x1aff3,
    0x1aff5, 0x1affb,
    0x1affd, 0x1affe,
    0x1b000, 0x1b122,
    0x1b132, 0x1b132,
    0x1b150, 0x1b152,
    0x1b155, 0x1b155,
    0x1b164, 0x1b167,
    0x1b170, 0x1b2fb,
    0x1bc00, 0x1bc6a,
    0x1bc70, 0x1bc7c,
    0x1bc80, 0x1bc88,
    0x1bc90, 0x1bc99,
    0x1bc9c, 0x1bca3,
    0x1cf00, 0x1cf2d,
    0x1cf30, 0x1cf46,
    0x1cf50, 0x1cfc3,
    0x1d000, 0x1d0f5,
    0x1d100, 0x1d126,
    0x1d129, 0x1d1ea,
    0x1d200, 0x1d245,
    0x1d2c0, 0x1d2d3,
    0x1d2e0, 0x1d2f3,
    0x1d300, 0x1d356,
    0x1d360, 0x1d378,
    0x1d400, 0x1d454,
    0x1d456, 0x1d49c,
    0x1d49e, 0x1d49f,
    0x1d4a2, 0x1d4a2,
    0x1d4a5, 0x1d4a6,
    0x1d4a9, 0x1d4ac,
    0x1d4ae, 0x1d4b9,
    0x1d4bb, 0x1d4bb,
    0x1d4bd, 0x1d4c3,
    0x1d4c5, 0x1d505,
    0x1d507, 0x1d50a,
    0x1d50d, 0x1d514,
    0x1d516, 0x1d51c,
    0x1d51e, 0x1d539,
    0x1d53b, 0x1d53e,
    0x1d540, 0x1d544,
    0x1d546, 0x1d546,
    0x1d54a, 0x1d550,
    0x1d552, 0x1d6a5,
    0x1d6a8, 0x1d7cb,
    0x1d7ce, 0x1da8b,
    0x1da9b, 0x1da9f,
    0x1daa1, 0x1daaf,
    0x1df00, 0x1df1e,
    0x1df25, 0x1df2a,
    0x1e000, 0x1e006,
    0x1e008, 0x1e018,
    0x1e01b, 0x1e021,
    0x1e023, 0x1e024,
    0x1e026, 0x1e02a,
    0x1e030, 0x1e06d,
    0x1e08f, 0x1e08f,
    0x1e100, 0x1e12c,
    0x1e130, 0x1e13d,
    0x1e140, 0x1e149,
    0x1e14e, 0x1e14f,
    0x1e290, 0x1e2ae,
    0x1e2c0, 0x1e2f9,
    0x1e2ff, 0x1e2ff,
    0x1e4d0, 0x1e4f9,
    0x1e7e0, 0x1e7e6,
    0x1e7e8, 0x1e7eb,
    0x1e7ed, 0x1e7ee,
    0x1e7f0, 0x1e7fe,
    0x1e800, 0x1e8c4,
    0x1e8c7, 0x1e8d6,
    0x1e900, 0x1e94b,
    0x1e950, 0x1e959,
    0x1e95e, 0x1e95f,
    0x1ec71, 0x1ecb4,
    0x1ed01, 0x1ed3d,
    0x1ee00, 0x1ee03,
    0x1ee05, 0x1ee1f,
    0x1ee21, 0x1ee22,
    0x1ee24, 0x1ee24,
    0x1ee27, 0x1ee27,
    0x1ee29, 0x1ee32,
    0x1ee34, 0x1ee37,
    0x1ee39, 0x1ee39,
    0x1ee3b, 0x1ee3b,
    0x1ee42, 0x1ee42,
    0x1ee47, 0x1ee47,
    0x1ee49, 0x1ee49,
    0x1ee4b, 0x1ee4b,
    0x1ee4d, 0x1ee4f,
    0x1ee51, 0x1ee52,
    0x1ee54, 0x1ee54,
    0x1ee57, 0x1ee57,
    0x1ee59, 0x1ee59,
    0x1ee5b, 0x1ee5b,
    0x1ee5d, 0x1ee5d,
    0x1ee5f, 0x1ee5f,
    0x1ee61, 0x1ee62,
    0x1ee64, 0x1ee64,
    0x1ee67, 0x1ee6a,
    0x1ee6c, 0x1ee72,
    0x1ee74, 0x1ee77,
    0x1ee79, 0x1ee7c,
    0x1ee7e, 0x1ee7e,
    0x1ee80, 0x1ee89,
    0x1ee8b, 0x1ee9b,
    0x1eea1, 0x1eea3,
    0x1eea5, 0x1eea9,
    0x1eeab, 0x1eebb,
    0x1eef0, 0x1eef1,
    0x1f000, 0x1f02b,
    0x1f030, 0x1f093,
    0x1f0a0, 0x1f0ae,
    0x1f0b1, 0x1f0bf,
    0x1f0c1, 0x1f0cf,
    0x1f0d1, 0x1f0f5,
    0x1f100, 0x1f1ad,
    0x1f1e6, 0x1f202,
    0x1f210, 0x1f23b,
    0x1f240, 0x1f248,
    0x1f250, 0x1f251,
    0x1f260, 0x1f265,
    0x1f300, 0x1f6d7,
    0x1f6dc, 0x1f6ec,
    0x1f6f0, 0x1f6fc,
    0x1f700, 0x1f776,
    0x1f77b, 0x1f7d9,
    0x1f7e0, 0x1f7eb,
    0x1f7f0, 0x1f7f0,
    0x1f800, 0x1f80b,
    0x1f810, 0x1f847,
    0x1f850, 0x1f859,
    0x1f860, 0x1f887,
    0x1f890, 0x1f8ad,
    0x1f8b0, 0x1f8b1,
    0x1f900, 0x1fa53,
    0x1fa60, 0x1fa6d,
    0x1fa70, 0x1fa7c,
    0x1fa80, 0x1fa88,
    0x1fa90, 0x1fabd,
    0x1fabf, 0x1fac5,
    0x1face, 0x1fadb,
    0x1fae0, 0x1fae8,
    0x1faf0, 0x1faf8,
    0x1fb00, 0x1fb92,
    0x1fb94, 0x1fbca,
    0x1fbf0, 0x1fbf9,
    0x20000, 0x2a6df,
    0x2a700, 0x2b739,
    0x2b740, 0x2b81d,
    0x2b820, 0x2cea1,
    0x2ceb0, 0x2ebe0,
    0x2f800, 0x2fa1d,
    0x30000, 0x3134a,
    0x31350, 0x323af,
    0xe0001, 0xe0001,
    0xe0020, 0xe007f,
    0xe0100, 0xe01ef,
];

function utf16CodeUnits(codePoint) {
    return codePoint >= 0x10000 ? 2 : 1;
}
function isHighSurrogate(ch) {
    return ch >= 0xd800 && ch <= 0xdbff;
}
function isLowSurrogate(ch) {
    return ch >= 0xdc00 && ch <= 0xdfff;
}
function isLineBreak(ch) {
    return ch === 10 /* CharCode.LineFeed */ || ch === 13 /* CharCode.CarriageReturn */;
}
function isAsciiWhiteSpaceSingleLine(ch) {
    return (ch === 32 /* CharCode.Space */ ||
        ch === 9 /* CharCode.Tab */ ||
        ch === 11 /* CharCode.VerticalTab */ ||
        ch === 12 /* CharCode.FormFeed */);
}
function isNonAsciiWhiteSpaceSingleLine(ch) {
    return (ch === 133 /* CharCode.NextLine */ || // not considered a line break
        ch === 8206 /* CharCode.LeftToRightMark */ ||
        ch === 8207 /* CharCode.RightToLeftMark */ ||
        ch === 8232 /* CharCode.LineSeparator */ ||
        ch === 8233 /* CharCode.ParagraphSeparator */);
}
function isWhiteSpace(ch) {
    return isWhiteSpaceSingleLine(ch) || isLineBreak(ch);
}
function isWhiteSpaceSingleLine(ch) {
    return (isAsciiWhiteSpaceSingleLine(ch) ||
        (ch > 127 /* CharCode.MaxAscii */ && isNonAsciiWhiteSpaceSingleLine(ch)));
}
function trim(str) {
    let start = 0;
    let end = str.length - 1;
    if (!isWhiteSpace(str.charCodeAt(start)) && !isWhiteSpace(str.charCodeAt(end))) {
        return str;
    }
    while (isWhiteSpace(str.charCodeAt(start))) {
        start++;
    }
    while (isWhiteSpace(str.charCodeAt(end))) {
        end--;
    }
    return str.substring(start, end + 1);
}
function isDigit(ch) {
    return ch >= 48 /* CharCode._0 */ && ch <= 57 /* CharCode._9 */;
}
function isHexDigit(ch) {
    return (isDigit(ch) || (ch >= 65 /* CharCode.A */ && ch <= 70 /* CharCode.F */) || (ch >= 97 /* CharCode.a */ && ch <= 102 /* CharCode.f */));
}
function isBinaryDigit(ch) {
    return ch === 48 /* CharCode._0 */ || ch === 49 /* CharCode._1 */;
}
function isLowercaseAsciiLetter(ch) {
    return ch >= 97 /* CharCode.a */ && ch <= 122 /* CharCode.z */;
}
function isAsciiIdentifierStart(ch) {
    return ((ch >= 65 /* CharCode.A */ && ch <= 90 /* CharCode.Z */) ||
        (ch >= 97 /* CharCode.a */ && ch <= 122 /* CharCode.z */) ||
        ch === 36 /* CharCode.$ */ ||
        ch === 95 /* CharCode._ */);
}
function isAsciiIdentifierContinue(ch) {
    return ((ch >= 65 /* CharCode.A */ && ch <= 90 /* CharCode.Z */) ||
        (ch >= 97 /* CharCode.a */ && ch <= 122 /* CharCode.z */) ||
        (ch >= 48 /* CharCode._0 */ && ch <= 57 /* CharCode._9 */) ||
        ch === 36 /* CharCode.$ */ ||
        ch === 95 /* CharCode._ */);
}
function isIdentifierStart(codePoint) {
    return (isAsciiIdentifierStart(codePoint) ||
        (codePoint > 127 /* CharCode.MaxAscii */ && isNonAsciiIdentifierCharacter(codePoint)));
}
function isIdentifierContinue(codePoint) {
    return (isAsciiIdentifierContinue(codePoint) ||
        (codePoint > 127 /* CharCode.MaxAscii */ && isNonAsciiIdentifierCharacter(codePoint)));
}
function isNonAsciiIdentifierCharacter(codePoint) {
    return lookupInNonAsciiMap(codePoint, nonAsciiIdentifierMap);
}
function codePointBefore(text, pos) {
    if (pos <= 0 || pos > text.length) {
        return { char: undefined, size: 0 };
    }
    const ch = text.charCodeAt(pos - 1);
    if (!isLowSurrogate(ch) || !isHighSurrogate(text.charCodeAt(pos - 2))) {
        return { char: ch, size: 1 };
    }
    return { char: text.codePointAt(pos - 2), size: 2 };
}
function lookupInNonAsciiMap(codePoint, map) {
    // Perform binary search in one of the Unicode range maps
    let lo = 0;
    let hi = map.length;
    let mid;
    while (lo + 1 < hi) {
        mid = lo + (hi - lo) / 2;
        // mid has to be even to catch a range's beginning
        mid -= mid % 2;
        if (map[mid] <= codePoint && codePoint <= map[mid + 1]) {
            return true;
        }
        if (codePoint < map[mid]) {
            hi = mid;
        }
        else {
            lo = mid + 2;
        }
    }
    return false;
}

function createTripleQuoteIndentCodeFix(location) {
    return defineCodeFix({
        id: "triple-quote-indent",
        label: "Format triple-quote-indent",
        fix: (context) => {
            const splitStr = "\n";
            const tripleQuote = '"""';
            const tripleQuoteLen = tripleQuote.length;
            const text = location.file.text.slice(location.pos + tripleQuoteLen, location.end - tripleQuoteLen);
            const lines = splitLines(text);
            if (lines.length === 0) {
                return;
            }
            if (lines.length === 1) {
                const indentNumb = getIndentNumbInLine(lines[0]);
                const prefix = " ".repeat(indentNumb);
                return context.replaceText(location, [tripleQuote, lines[0], `${prefix}${tripleQuote}`].join(splitStr));
            }
            if (lines[0].trim() === "") {
                lines.shift();
            }
            const lastLine = lines[lines.length - 1];
            if (lastLine.trim() === "") {
                lines.pop();
            }
            let prefix = "";
            const minIndentNumb = Math.min(...lines.map((line) => getIndentNumbInLine(line)));
            const lastLineIndentNumb = getIndentNumbInLine(lastLine);
            if (minIndentNumb < lastLineIndentNumb) {
                const indentDiff = lastLineIndentNumb - minIndentNumb;
                prefix = " ".repeat(indentDiff);
            }
            const middle = lines.map((line) => `${prefix}${line}`).join(splitStr);
            return context.replaceText(location, `${tripleQuote}${splitStr}${middle}${splitStr}${" ".repeat(lastLineIndentNumb)}${tripleQuote}`);
            function getIndentNumbInLine(lineText) {
                let curStart = 0;
                while (curStart < lineText.length &&
                    isWhiteSpaceSingleLine(lineText.charCodeAt(curStart))) {
                    curStart++;
                }
                return curStart;
            }
        },
    });
}

/**
 * Find the comment that is at given position, if any.
 *
 * A comment is at the given position if {@link Comment.pos} <= position <
 * {@link Comment.end}. Unlike {@link getNodeAtPosition}, the end node is
 * not included since comments can be adjacent to each other with no trivia
 * or punctuation between them.
 *
 * @internal
 */
function getCommentAtPosition(script, pos) {
    if (!script.parseOptions.comments) {
        // Not an assert since we might make this public and it would be external caller's responsibility.
        throw new Error("ParseOptions.comments must be enabled to use getCommentAtPosition.");
    }
    // Comments are ordered by increasing position, use binary search
    let low = 0;
    let high = script.comments.length - 1;
    while (low <= high) {
        const middle = low + ((high - low) >> 1);
        const candidate = script.comments[middle];
        if (pos >= candidate.end) {
            low = middle + 1;
        }
        else if (pos < candidate.pos) {
            high = middle - 1;
        }
        else {
            return candidate;
        }
    }
    return undefined;
}
/**
 * Adjust the given postion backwards before any trivia.
 */
function getPositionBeforeTrivia(script, pos) {
    if (!script.parseOptions.comments) {
        // Not an assert since we might make this public and it would be external caller's responsibility.
        throw new Error("ParseOptions.comments must be enabled to use getPositionBeforeTrivia.");
    }
    let comment;
    while (pos > 0) {
        if (isWhiteSpace(script.file.text.charCodeAt(pos - 1))) {
            do {
                pos--;
            } while (isWhiteSpace(script.file.text.charCodeAt(pos - 1)));
        }
        else if ((comment = getCommentAtPosition(script, pos - 1))) {
            pos = comment.pos;
        }
        else {
            // note at whitespace or comment
            break;
        }
    }
    return pos;
}

// All conflict markers consist of the same character repeated seven times.  If it is
// a <<<<<<< or >>>>>>> marker then it is also followed by a space.
const mergeConflictMarkerLength = 7;
var Token;
(function (Token) {
    Token[Token["None"] = 0] = "None";
    Token[Token["Invalid"] = 1] = "Invalid";
    Token[Token["EndOfFile"] = 2] = "EndOfFile";
    Token[Token["Identifier"] = 3] = "Identifier";
    Token[Token["NumericLiteral"] = 4] = "NumericLiteral";
    Token[Token["StringLiteral"] = 5] = "StringLiteral";
    Token[Token["StringTemplateHead"] = 6] = "StringTemplateHead";
    Token[Token["StringTemplateMiddle"] = 7] = "StringTemplateMiddle";
    Token[Token["StringTemplateTail"] = 8] = "StringTemplateTail";
    // Add new tokens above if they don't fit any of the categories below
    ///////////////////////////////////////////////////////////////
    // Trivia
    /** @internal */ Token[Token["__StartTrivia"] = 9] = "__StartTrivia";
    Token[Token["SingleLineComment"] = 9] = "SingleLineComment";
    Token[Token["MultiLineComment"] = 10] = "MultiLineComment";
    Token[Token["NewLine"] = 11] = "NewLine";
    Token[Token["Whitespace"] = 12] = "Whitespace";
    Token[Token["ConflictMarker"] = 13] = "ConflictMarker";
    // Add new trivia above
    /** @internal */ Token[Token["__EndTrivia"] = 14] = "__EndTrivia";
    ///////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////
    // Doc comment content
    /** @internal */ Token[Token["__StartDocComment"] = 14] = "__StartDocComment";
    Token[Token["DocText"] = 14] = "DocText";
    Token[Token["DocCodeSpan"] = 15] = "DocCodeSpan";
    Token[Token["DocCodeFenceDelimiter"] = 16] = "DocCodeFenceDelimiter";
    /** @internal */ Token[Token["__EndDocComment"] = 17] = "__EndDocComment";
    ///////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////
    // Punctuation
    /** @internal */ Token[Token["__StartPunctuation"] = 17] = "__StartPunctuation";
    Token[Token["OpenBrace"] = 17] = "OpenBrace";
    Token[Token["CloseBrace"] = 18] = "CloseBrace";
    Token[Token["OpenParen"] = 19] = "OpenParen";
    Token[Token["CloseParen"] = 20] = "CloseParen";
    Token[Token["OpenBracket"] = 21] = "OpenBracket";
    Token[Token["CloseBracket"] = 22] = "CloseBracket";
    Token[Token["Dot"] = 23] = "Dot";
    Token[Token["Ellipsis"] = 24] = "Ellipsis";
    Token[Token["Semicolon"] = 25] = "Semicolon";
    Token[Token["Comma"] = 26] = "Comma";
    Token[Token["LessThan"] = 27] = "LessThan";
    Token[Token["GreaterThan"] = 28] = "GreaterThan";
    Token[Token["Equals"] = 29] = "Equals";
    Token[Token["Ampersand"] = 30] = "Ampersand";
    Token[Token["Bar"] = 31] = "Bar";
    Token[Token["Question"] = 32] = "Question";
    Token[Token["Colon"] = 33] = "Colon";
    Token[Token["ColonColon"] = 34] = "ColonColon";
    Token[Token["At"] = 35] = "At";
    Token[Token["AtAt"] = 36] = "AtAt";
    Token[Token["Hash"] = 37] = "Hash";
    Token[Token["HashBrace"] = 38] = "HashBrace";
    Token[Token["HashBracket"] = 39] = "HashBracket";
    Token[Token["Star"] = 40] = "Star";
    Token[Token["ForwardSlash"] = 41] = "ForwardSlash";
    Token[Token["Plus"] = 42] = "Plus";
    Token[Token["Hyphen"] = 43] = "Hyphen";
    Token[Token["Exclamation"] = 44] = "Exclamation";
    Token[Token["LessThanEquals"] = 45] = "LessThanEquals";
    Token[Token["GreaterThanEquals"] = 46] = "GreaterThanEquals";
    Token[Token["AmpsersandAmpersand"] = 47] = "AmpsersandAmpersand";
    Token[Token["BarBar"] = 48] = "BarBar";
    Token[Token["EqualsEquals"] = 49] = "EqualsEquals";
    Token[Token["ExclamationEquals"] = 50] = "ExclamationEquals";
    Token[Token["EqualsGreaterThan"] = 51] = "EqualsGreaterThan";
    // Add new punctuation above
    /** @internal */ Token[Token["__EndPunctuation"] = 52] = "__EndPunctuation";
    ///////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////
    // Statement keywords
    /** @internal */ Token[Token["__StartKeyword"] = 52] = "__StartKeyword";
    /** @internal */ Token[Token["__StartStatementKeyword"] = 52] = "__StartStatementKeyword";
    Token[Token["ImportKeyword"] = 52] = "ImportKeyword";
    Token[Token["ModelKeyword"] = 53] = "ModelKeyword";
    Token[Token["ScalarKeyword"] = 54] = "ScalarKeyword";
    Token[Token["NamespaceKeyword"] = 55] = "NamespaceKeyword";
    Token[Token["UsingKeyword"] = 56] = "UsingKeyword";
    Token[Token["OpKeyword"] = 57] = "OpKeyword";
    Token[Token["EnumKeyword"] = 58] = "EnumKeyword";
    Token[Token["AliasKeyword"] = 59] = "AliasKeyword";
    Token[Token["IsKeyword"] = 60] = "IsKeyword";
    Token[Token["InterfaceKeyword"] = 61] = "InterfaceKeyword";
    Token[Token["UnionKeyword"] = 62] = "UnionKeyword";
    Token[Token["ProjectionKeyword"] = 63] = "ProjectionKeyword";
    Token[Token["ElseKeyword"] = 64] = "ElseKeyword";
    Token[Token["IfKeyword"] = 65] = "IfKeyword";
    Token[Token["DecKeyword"] = 66] = "DecKeyword";
    Token[Token["FnKeyword"] = 67] = "FnKeyword";
    Token[Token["ConstKeyword"] = 68] = "ConstKeyword";
    Token[Token["InitKeyword"] = 69] = "InitKeyword";
    // Add new statement keyword above
    /** @internal */ Token[Token["__EndStatementKeyword"] = 70] = "__EndStatementKeyword";
    ///////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////
    /** @internal */ Token[Token["__StartModifierKeyword"] = 70] = "__StartModifierKeyword";
    Token[Token["ExternKeyword"] = 70] = "ExternKeyword";
    /** @internal */ Token[Token["__EndModifierKeyword"] = 71] = "__EndModifierKeyword";
    ///////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////
    // Other keywords
    Token[Token["ExtendsKeyword"] = 71] = "ExtendsKeyword";
    Token[Token["TrueKeyword"] = 72] = "TrueKeyword";
    Token[Token["FalseKeyword"] = 73] = "FalseKeyword";
    Token[Token["ReturnKeyword"] = 74] = "ReturnKeyword";
    Token[Token["VoidKeyword"] = 75] = "VoidKeyword";
    Token[Token["NeverKeyword"] = 76] = "NeverKeyword";
    Token[Token["UnknownKeyword"] = 77] = "UnknownKeyword";
    Token[Token["ValueOfKeyword"] = 78] = "ValueOfKeyword";
    Token[Token["TypeOfKeyword"] = 79] = "TypeOfKeyword";
    // Add new non-statement keyword above
    /** @internal */ Token[Token["__EndKeyword"] = 80] = "__EndKeyword";
    ///////////////////////////////////////////////////////////////
    /** @internal */ Token[Token["__StartReservedKeyword"] = 80] = "__StartReservedKeyword";
    ///////////////////////////////////////////////////////////////
    // List of keywords that have special meaning in the language but are reserved for future use
    Token[Token["StatemachineKeyword"] = 80] = "StatemachineKeyword";
    Token[Token["MacroKeyword"] = 81] = "MacroKeyword";
    Token[Token["PackageKeyword"] = 82] = "PackageKeyword";
    Token[Token["MetadataKeyword"] = 83] = "MetadataKeyword";
    Token[Token["EnvKeyword"] = 84] = "EnvKeyword";
    Token[Token["ArgKeyword"] = 85] = "ArgKeyword";
    Token[Token["DeclareKeyword"] = 86] = "DeclareKeyword";
    Token[Token["ArrayKeyword"] = 87] = "ArrayKeyword";
    Token[Token["StructKeyword"] = 88] = "StructKeyword";
    Token[Token["RecordKeyword"] = 89] = "RecordKeyword";
    Token[Token["ModuleKeyword"] = 90] = "ModuleKeyword";
    Token[Token["ModKeyword"] = 91] = "ModKeyword";
    Token[Token["PubKeyword"] = 92] = "PubKeyword";
    Token[Token["SubKeyword"] = 93] = "SubKeyword";
    Token[Token["TypeRefKeyword"] = 94] = "TypeRefKeyword";
    Token[Token["TraitKeyword"] = 95] = "TraitKeyword";
    Token[Token["ThisKeyword"] = 96] = "ThisKeyword";
    Token[Token["SelfKeyword"] = 97] = "SelfKeyword";
    Token[Token["SuperKeyword"] = 98] = "SuperKeyword";
    Token[Token["KeyofKeyword"] = 99] = "KeyofKeyword";
    Token[Token["WithKeyword"] = 100] = "WithKeyword";
    Token[Token["ImplementsKeyword"] = 101] = "ImplementsKeyword";
    Token[Token["ImplKeyword"] = 102] = "ImplKeyword";
    Token[Token["SatisfiesKeyword"] = 103] = "SatisfiesKeyword";
    Token[Token["FlagKeyword"] = 104] = "FlagKeyword";
    Token[Token["AutoKeyword"] = 105] = "AutoKeyword";
    Token[Token["PartialKeyword"] = 106] = "PartialKeyword";
    Token[Token["PrivateKeyword"] = 107] = "PrivateKeyword";
    Token[Token["PublicKeyword"] = 108] = "PublicKeyword";
    Token[Token["ProtectedKeyword"] = 109] = "ProtectedKeyword";
    Token[Token["InternalKeyword"] = 110] = "InternalKeyword";
    Token[Token["SealedKeyword"] = 111] = "SealedKeyword";
    Token[Token["LocalKeyword"] = 112] = "LocalKeyword";
    Token[Token["AsyncKeyword"] = 113] = "AsyncKeyword";
    /** @internal */ Token[Token["__EndReservedKeyword"] = 114] = "__EndReservedKeyword";
    ///////////////////////////////////////////////////////////////
    /** @internal */ Token[Token["__Count"] = 114] = "__Count";
})(Token || (Token = {}));
/** @internal */
const TokenDisplay = getTokenDisplayTable([
    [Token.None, "none"],
    [Token.Invalid, "invalid"],
    [Token.EndOfFile, "end of file"],
    [Token.SingleLineComment, "single-line comment"],
    [Token.MultiLineComment, "multi-line comment"],
    [Token.ConflictMarker, "conflict marker"],
    [Token.NumericLiteral, "numeric literal"],
    [Token.StringLiteral, "string literal"],
    [Token.StringTemplateHead, "string template head"],
    [Token.StringTemplateMiddle, "string template middle"],
    [Token.StringTemplateTail, "string template tail"],
    [Token.NewLine, "newline"],
    [Token.Whitespace, "whitespace"],
    [Token.DocCodeFenceDelimiter, "doc code fence delimiter"],
    [Token.DocCodeSpan, "doc code span"],
    [Token.DocText, "doc text"],
    [Token.OpenBrace, "'{'"],
    [Token.CloseBrace, "'}'"],
    [Token.OpenParen, "'('"],
    [Token.CloseParen, "')'"],
    [Token.OpenBracket, "'['"],
    [Token.CloseBracket, "']'"],
    [Token.Dot, "'.'"],
    [Token.Ellipsis, "'...'"],
    [Token.Semicolon, "';'"],
    [Token.Comma, "','"],
    [Token.LessThan, "'<'"],
    [Token.GreaterThan, "'>'"],
    [Token.Equals, "'='"],
    [Token.Ampersand, "'&'"],
    [Token.Bar, "'|'"],
    [Token.Question, "'?'"],
    [Token.Colon, "':'"],
    [Token.ColonColon, "'::'"],
    [Token.At, "'@'"],
    [Token.AtAt, "'@@'"],
    [Token.Hash, "'#'"],
    [Token.HashBrace, "'#{'"],
    [Token.HashBracket, "'#['"],
    [Token.Star, "'*'"],
    [Token.ForwardSlash, "'/'"],
    [Token.Plus, "'+'"],
    [Token.Hyphen, "'-'"],
    [Token.Exclamation, "'!'"],
    [Token.LessThanEquals, "'<='"],
    [Token.GreaterThanEquals, "'>='"],
    [Token.AmpsersandAmpersand, "'&&'"],
    [Token.BarBar, "'||'"],
    [Token.EqualsEquals, "'=='"],
    [Token.ExclamationEquals, "'!='"],
    [Token.EqualsGreaterThan, "'=>'"],
    [Token.Identifier, "identifier"],
    [Token.ImportKeyword, "'import'"],
    [Token.ModelKeyword, "'model'"],
    [Token.ScalarKeyword, "'scalar'"],
    [Token.NamespaceKeyword, "'namespace'"],
    [Token.UsingKeyword, "'using'"],
    [Token.OpKeyword, "'op'"],
    [Token.EnumKeyword, "'enum'"],
    [Token.AliasKeyword, "'alias'"],
    [Token.IsKeyword, "'is'"],
    [Token.InterfaceKeyword, "'interface'"],
    [Token.UnionKeyword, "'union'"],
    [Token.ProjectionKeyword, "'projection'"],
    [Token.ElseKeyword, "'else'"],
    [Token.IfKeyword, "'if'"],
    [Token.DecKeyword, "'dec'"],
    [Token.FnKeyword, "'fn'"],
    [Token.ValueOfKeyword, "'valueof'"],
    [Token.TypeOfKeyword, "'typeof'"],
    [Token.ConstKeyword, "'const'"],
    [Token.InitKeyword, "'init'"],
    [Token.ExtendsKeyword, "'extends'"],
    [Token.TrueKeyword, "'true'"],
    [Token.FalseKeyword, "'false'"],
    [Token.ReturnKeyword, "'return'"],
    [Token.VoidKeyword, "'void'"],
    [Token.NeverKeyword, "'never'"],
    [Token.UnknownKeyword, "'unknown'"],
    [Token.ExternKeyword, "'extern'"],
    // Reserved keywords
    [Token.StatemachineKeyword, "'statemachine'"],
    [Token.MacroKeyword, "'macro'"],
    [Token.PackageKeyword, "'package'"],
    [Token.MetadataKeyword, "'metadata'"],
    [Token.EnvKeyword, "'env'"],
    [Token.ArgKeyword, "'arg'"],
    [Token.DeclareKeyword, "'declare'"],
    [Token.ArrayKeyword, "'array'"],
    [Token.StructKeyword, "'struct'"],
    [Token.RecordKeyword, "'record'"],
    [Token.ModuleKeyword, "'module'"],
    [Token.ModKeyword, "'mod'"],
    [Token.PubKeyword, "'pub'"],
    [Token.SubKeyword, "'sub'"],
    [Token.TypeRefKeyword, "'typeref'"],
    [Token.TraitKeyword, "'trait'"],
    [Token.ThisKeyword, "'this'"],
    [Token.SelfKeyword, "'self'"],
    [Token.SuperKeyword, "'super'"],
    [Token.KeyofKeyword, "'keyof'"],
    [Token.WithKeyword, "'with'"],
    [Token.ImplementsKeyword, "'implements'"],
    [Token.ImplKeyword, "'impl'"],
    [Token.SatisfiesKeyword, "'satisfies'"],
    [Token.FlagKeyword, "'flag'"],
    [Token.AutoKeyword, "'auto'"],
    [Token.PartialKeyword, "'partial'"],
    [Token.PrivateKeyword, "'private'"],
    [Token.PublicKeyword, "'public'"],
    [Token.ProtectedKeyword, "'protected'"],
    [Token.InternalKeyword, "'internal'"],
    [Token.SealedKeyword, "'sealed'"],
    [Token.LocalKeyword, "'local'"],
    [Token.AsyncKeyword, "'async'"],
]);
/** @internal */
const Keywords = new Map([
    ["import", Token.ImportKeyword],
    ["model", Token.ModelKeyword],
    ["scalar", Token.ScalarKeyword],
    ["namespace", Token.NamespaceKeyword],
    ["interface", Token.InterfaceKeyword],
    ["union", Token.UnionKeyword],
    ["if", Token.IfKeyword],
    ["else", Token.ElseKeyword],
    ["projection", Token.ProjectionKeyword],
    ["using", Token.UsingKeyword],
    ["op", Token.OpKeyword],
    ["extends", Token.ExtendsKeyword],
    ["is", Token.IsKeyword],
    ["enum", Token.EnumKeyword],
    ["alias", Token.AliasKeyword],
    ["dec", Token.DecKeyword],
    ["fn", Token.FnKeyword],
    ["valueof", Token.ValueOfKeyword],
    ["typeof", Token.TypeOfKeyword],
    ["const", Token.ConstKeyword],
    ["init", Token.InitKeyword],
    ["true", Token.TrueKeyword],
    ["false", Token.FalseKeyword],
    ["return", Token.ReturnKeyword],
    ["void", Token.VoidKeyword],
    ["never", Token.NeverKeyword],
    ["unknown", Token.UnknownKeyword],
    ["extern", Token.ExternKeyword],
    // Reserved keywords
    ["statemachine", Token.StatemachineKeyword],
    ["macro", Token.MacroKeyword],
    ["package", Token.PackageKeyword],
    ["metadata", Token.MetadataKeyword],
    ["env", Token.EnvKeyword],
    ["arg", Token.ArgKeyword],
    ["declare", Token.DeclareKeyword],
    ["array", Token.ArrayKeyword],
    ["struct", Token.StructKeyword],
    ["record", Token.RecordKeyword],
    ["module", Token.ModuleKeyword],
    ["mod", Token.ModKeyword],
    ["pub", Token.PubKeyword],
    ["sub", Token.SubKeyword],
    ["typeref", Token.TypeRefKeyword],
    ["trait", Token.TraitKeyword],
    ["this", Token.ThisKeyword],
    ["self", Token.SelfKeyword],
    ["super", Token.SuperKeyword],
    ["keyof", Token.KeyofKeyword],
    ["with", Token.WithKeyword],
    ["implements", Token.ImplementsKeyword],
    ["impl", Token.ImplKeyword],
    ["satisfies", Token.SatisfiesKeyword],
    ["flag", Token.FlagKeyword],
    ["auto", Token.AutoKeyword],
    ["partial", Token.PartialKeyword],
    ["private", Token.PrivateKeyword],
    ["public", Token.PublicKeyword],
    ["protected", Token.ProtectedKeyword],
    ["internal", Token.InternalKeyword],
    ["sealed", Token.SealedKeyword],
    ["local", Token.LocalKeyword],
    ["async", Token.AsyncKeyword],
]);
/** @internal */
const ReservedKeywords = new Map([
    // Reserved keywords
    ["statemachine", Token.StatemachineKeyword],
    ["macro", Token.MacroKeyword],
    ["package", Token.PackageKeyword],
    ["metadata", Token.MetadataKeyword],
    ["env", Token.EnvKeyword],
    ["arg", Token.ArgKeyword],
    ["declare", Token.DeclareKeyword],
    ["array", Token.ArrayKeyword],
    ["struct", Token.StructKeyword],
    ["record", Token.RecordKeyword],
    ["module", Token.ModuleKeyword],
    ["trait", Token.TraitKeyword],
    ["this", Token.ThisKeyword],
    ["self", Token.SelfKeyword],
    ["super", Token.SuperKeyword],
    ["keyof", Token.KeyofKeyword],
    ["with", Token.WithKeyword],
    ["implements", Token.ImplementsKeyword],
    ["impl", Token.ImplKeyword],
    ["satisfies", Token.SatisfiesKeyword],
    ["flag", Token.FlagKeyword],
    ["auto", Token.AutoKeyword],
    ["partial", Token.PartialKeyword],
    ["private", Token.PrivateKeyword],
    ["public", Token.PublicKeyword],
    ["protected", Token.ProtectedKeyword],
    ["internal", Token.InternalKeyword],
    ["sealed", Token.SealedKeyword],
    ["local", Token.LocalKeyword],
    ["async", Token.AsyncKeyword],
]);
var TokenFlags;
(function (TokenFlags) {
    TokenFlags[TokenFlags["None"] = 0] = "None";
    TokenFlags[TokenFlags["Escaped"] = 1] = "Escaped";
    TokenFlags[TokenFlags["TripleQuoted"] = 2] = "TripleQuoted";
    TokenFlags[TokenFlags["Unterminated"] = 4] = "Unterminated";
    TokenFlags[TokenFlags["NonAscii"] = 8] = "NonAscii";
    TokenFlags[TokenFlags["DocComment"] = 16] = "DocComment";
    TokenFlags[TokenFlags["Backticked"] = 32] = "Backticked";
})(TokenFlags || (TokenFlags = {}));
function isTrivia(token) {
    return token >= Token.__StartTrivia && token < Token.__EndTrivia;
}
function isComment(token) {
    return token === Token.SingleLineComment || token === Token.MultiLineComment;
}
function isKeyword(token) {
    return token >= Token.__StartKeyword && token < Token.__EndKeyword;
}
/** If is a keyword with no actual use right now but will be in the future. */
function isReservedKeyword(token) {
    return token >= Token.__StartReservedKeyword && token < Token.__EndReservedKeyword;
}
function isPunctuation(token) {
    return token >= Token.__StartPunctuation && token < Token.__EndPunctuation;
}
function isStatementKeyword(token) {
    return token >= Token.__StartStatementKeyword && token < Token.__EndStatementKeyword;
}
function createScanner(source, diagnosticHandler) {
    const file = typeof source === "string" ? createSourceFile(source, "<anonymous file>") : source;
    const input = file.text;
    let position = 0;
    let endPosition = input.length;
    let token = Token.None;
    let tokenPosition = -1;
    let tokenFlags = TokenFlags.None;
    // Skip BOM
    if (position < endPosition && input.charCodeAt(position) === 65279 /* CharCode.ByteOrderMark */) {
        position++;
    }
    return {
        get position() {
            return position;
        },
        get token() {
            return token;
        },
        get tokenPosition() {
            return tokenPosition;
        },
        get tokenFlags() {
            return tokenFlags;
        },
        file,
        scan,
        scanRange,
        scanDoc,
        reScanStringTemplate,
        findTripleQuotedStringIndent,
        unindentAndUnescapeTripleQuotedString,
        eof,
        getTokenText,
        getTokenValue,
    };
    function eof() {
        return position >= endPosition;
    }
    function getTokenText() {
        return input.substring(tokenPosition, position);
    }
    function getTokenValue() {
        switch (token) {
            case Token.StringLiteral:
            case Token.StringTemplateHead:
            case Token.StringTemplateMiddle:
            case Token.StringTemplateTail:
                return getStringTokenValue(token, tokenFlags);
            case Token.Identifier:
                return getIdentifierTokenValue();
            case Token.DocText:
                return getDocTextValue();
            default:
                return getTokenText();
        }
    }
    function lookAhead(offset) {
        const p = position + offset;
        if (p >= endPosition) {
            return Number.NaN;
        }
        return input.charCodeAt(p);
    }
    function scan() {
        tokenPosition = position;
        tokenFlags = TokenFlags.None;
        if (!eof()) {
            const ch = input.charCodeAt(position);
            switch (ch) {
                case 13 /* CharCode.CarriageReturn */:
                    if (lookAhead(1) === 10 /* CharCode.LineFeed */) {
                        position++;
                    }
                // fallthrough
                case 10 /* CharCode.LineFeed */:
                    return next(Token.NewLine);
                case 32 /* CharCode.Space */:
                case 9 /* CharCode.Tab */:
                case 11 /* CharCode.VerticalTab */:
                case 12 /* CharCode.FormFeed */:
                    return scanWhitespace();
                case 40 /* CharCode.OpenParen */:
                    return next(Token.OpenParen);
                case 41 /* CharCode.CloseParen */:
                    return next(Token.CloseParen);
                case 44 /* CharCode.Comma */:
                    return next(Token.Comma);
                case 58 /* CharCode.Colon */:
                    return lookAhead(1) === 58 /* CharCode.Colon */ ? next(Token.ColonColon, 2) : next(Token.Colon);
                case 59 /* CharCode.Semicolon */:
                    return next(Token.Semicolon);
                case 91 /* CharCode.OpenBracket */:
                    return next(Token.OpenBracket);
                case 93 /* CharCode.CloseBracket */:
                    return next(Token.CloseBracket);
                case 123 /* CharCode.OpenBrace */:
                    return next(Token.OpenBrace);
                case 125 /* CharCode.CloseBrace */:
                    return next(Token.CloseBrace);
                case 64 /* CharCode.At */:
                    return lookAhead(1) === 64 /* CharCode.At */ ? next(Token.AtAt, 2) : next(Token.At);
                case 35 /* CharCode.Hash */:
                    const ahead = lookAhead(1);
                    switch (ahead) {
                        case 123 /* CharCode.OpenBrace */:
                            return next(Token.HashBrace, 2);
                        case 91 /* CharCode.OpenBracket */:
                            return next(Token.HashBracket, 2);
                        default:
                            return next(Token.Hash);
                    }
                case 43 /* CharCode.Plus */:
                    return isDigit(lookAhead(1)) ? scanSignedNumber() : next(Token.Plus);
                case 45 /* CharCode.Minus */:
                    return isDigit(lookAhead(1)) ? scanSignedNumber() : next(Token.Hyphen);
                case 42 /* CharCode.Asterisk */:
                    return next(Token.Star);
                case 63 /* CharCode.Question */:
                    return next(Token.Question);
                case 38 /* CharCode.Ampersand */:
                    return lookAhead(1) === 38 /* CharCode.Ampersand */
                        ? next(Token.AmpsersandAmpersand, 2)
                        : next(Token.Ampersand);
                case 46 /* CharCode.Dot */:
                    return lookAhead(1) === 46 /* CharCode.Dot */ && lookAhead(2) === 46 /* CharCode.Dot */
                        ? next(Token.Ellipsis, 3)
                        : next(Token.Dot);
                case 47 /* CharCode.Slash */:
                    switch (lookAhead(1)) {
                        case 47 /* CharCode.Slash */:
                            return scanSingleLineComment();
                        case 42 /* CharCode.Asterisk */:
                            return scanMultiLineComment();
                    }
                    return next(Token.ForwardSlash);
                case 48 /* CharCode._0 */:
                    switch (lookAhead(1)) {
                        case 120 /* CharCode.x */:
                            return scanHexNumber();
                        case 98 /* CharCode.b */:
                            return scanBinaryNumber();
                    }
                // fallthrough
                case 49 /* CharCode._1 */:
                case 50 /* CharCode._2 */:
                case 51 /* CharCode._3 */:
                case 52 /* CharCode._4 */:
                case 53 /* CharCode._5 */:
                case 54 /* CharCode._6 */:
                case 55 /* CharCode._7 */:
                case 56 /* CharCode._8 */:
                case 57 /* CharCode._9 */:
                    return scanNumber();
                case 60 /* CharCode.LessThan */:
                    if (atConflictMarker())
                        return scanConflictMarker();
                    return lookAhead(1) === 61 /* CharCode.Equals */
                        ? next(Token.LessThanEquals, 2)
                        : next(Token.LessThan);
                case 62 /* CharCode.GreaterThan */:
                    if (atConflictMarker())
                        return scanConflictMarker();
                    return lookAhead(1) === 61 /* CharCode.Equals */
                        ? next(Token.GreaterThanEquals, 2)
                        : next(Token.GreaterThan);
                case 61 /* CharCode.Equals */:
                    if (atConflictMarker())
                        return scanConflictMarker();
                    switch (lookAhead(1)) {
                        case 61 /* CharCode.Equals */:
                            return next(Token.EqualsEquals, 2);
                        case 62 /* CharCode.GreaterThan */:
                            return next(Token.EqualsGreaterThan, 2);
                    }
                    return next(Token.Equals);
                case 124 /* CharCode.Bar */:
                    if (atConflictMarker())
                        return scanConflictMarker();
                    return lookAhead(1) === 124 /* CharCode.Bar */ ? next(Token.BarBar, 2) : next(Token.Bar);
                case 34 /* CharCode.DoubleQuote */:
                    return lookAhead(1) === 34 /* CharCode.DoubleQuote */ && lookAhead(2) === 34 /* CharCode.DoubleQuote */
                        ? scanString(TokenFlags.TripleQuoted)
                        : scanString(TokenFlags.None);
                case 33 /* CharCode.Exclamation */:
                    return lookAhead(1) === 61 /* CharCode.Equals */
                        ? next(Token.ExclamationEquals, 2)
                        : next(Token.Exclamation);
                case 96 /* CharCode.Backtick */:
                    return scanBacktickedIdentifier();
                default:
                    if (isLowercaseAsciiLetter(ch)) {
                        return scanIdentifierOrKeyword();
                    }
                    if (isAsciiIdentifierStart(ch)) {
                        return scanIdentifier();
                    }
                    if (ch <= 127 /* CharCode.MaxAscii */) {
                        return scanInvalidCharacter();
                    }
                    return scanNonAsciiToken();
            }
        }
        return (token = Token.EndOfFile);
    }
    function scanDoc() {
        tokenPosition = position;
        tokenFlags = TokenFlags.None;
        if (!eof()) {
            const ch = input.charCodeAt(position);
            switch (ch) {
                case 13 /* CharCode.CarriageReturn */:
                    if (lookAhead(1) === 10 /* CharCode.LineFeed */) {
                        position++;
                    }
                // fallthrough
                case 10 /* CharCode.LineFeed */:
                    return next(Token.NewLine);
                case 92 /* CharCode.Backslash */:
                    if (lookAhead(1) === 64 /* CharCode.At */) {
                        tokenFlags |= TokenFlags.Escaped;
                        return next(Token.DocText, 2);
                    }
                    return next(Token.DocText);
                case 32 /* CharCode.Space */:
                case 9 /* CharCode.Tab */:
                case 11 /* CharCode.VerticalTab */:
                case 12 /* CharCode.FormFeed */:
                    return scanWhitespace();
                case 125 /* CharCode.CloseBrace */:
                    return next(Token.CloseBrace);
                case 64 /* CharCode.At */:
                    return next(Token.At);
                case 42 /* CharCode.Asterisk */:
                    return next(Token.Star);
                case 96 /* CharCode.Backtick */:
                    return lookAhead(1) === 96 /* CharCode.Backtick */ && lookAhead(2) === 96 /* CharCode.Backtick */
                        ? next(Token.DocCodeFenceDelimiter, 3)
                        : scanDocCodeSpan();
                case 60 /* CharCode.LessThan */:
                case 62 /* CharCode.GreaterThan */:
                case 61 /* CharCode.Equals */:
                case 124 /* CharCode.Bar */:
                    if (atConflictMarker())
                        return scanConflictMarker();
                    return next(Token.DocText);
                case 45 /* CharCode.Minus */:
                    return next(Token.Hyphen);
            }
            if (isAsciiIdentifierStart(ch)) {
                return scanIdentifier();
            }
            if (ch <= 127 /* CharCode.MaxAscii */) {
                return next(Token.DocText);
            }
            const cp = input.codePointAt(position);
            if (isIdentifierStart(cp)) {
                return scanNonAsciiIdentifier(cp);
            }
            return scanUnknown(Token.DocText);
        }
        return (token = Token.EndOfFile);
    }
    function reScanStringTemplate(lastTokenFlags) {
        position = tokenPosition;
        tokenFlags = TokenFlags.None;
        return scanStringTemplateSpan(lastTokenFlags);
    }
    function scanRange(range, callback) {
        const savedPosition = position;
        const savedEndPosition = endPosition;
        const savedToken = token;
        const savedTokenPosition = tokenPosition;
        const savedTokenFlags = tokenFlags;
        position = range.pos;
        endPosition = range.end;
        token = Token.None;
        tokenPosition = -1;
        tokenFlags = TokenFlags.None;
        const result = callback();
        position = savedPosition;
        endPosition = savedEndPosition;
        token = savedToken;
        tokenPosition = savedTokenPosition;
        tokenFlags = savedTokenFlags;
        return result;
    }
    function next(t, count = 1) {
        position += count;
        return (token = t);
    }
    function unterminated(t) {
        tokenFlags |= TokenFlags.Unterminated;
        error({ code: "unterminated", format: { token: TokenDisplay[t] } });
        return (token = t);
    }
    function scanNonAsciiToken() {
        tokenFlags |= TokenFlags.NonAscii;
        const ch = input.charCodeAt(position);
        if (isNonAsciiWhiteSpaceSingleLine(ch)) {
            return scanWhitespace();
        }
        const cp = input.codePointAt(position);
        if (isNonAsciiIdentifierCharacter(cp)) {
            return scanNonAsciiIdentifier(cp);
        }
        return scanInvalidCharacter();
    }
    function scanInvalidCharacter() {
        token = scanUnknown(Token.Invalid);
        error({ code: "invalid-character" });
        return token;
    }
    function scanUnknown(t) {
        const codePoint = input.codePointAt(position);
        return (token = next(t, utf16CodeUnits(codePoint)));
    }
    function error(report, pos, end) {
        const diagnostic = createDiagnostic({
            ...report,
            target: { file, pos: pos ?? tokenPosition, end: end ?? position },
        });
        diagnosticHandler(diagnostic);
    }
    function scanWhitespace() {
        do {
            position++;
        } while (!eof() && isWhiteSpaceSingleLine(input.charCodeAt(position)));
        return (token = Token.Whitespace);
    }
    function scanSignedNumber() {
        position++; // consume '+/-'
        return scanNumber();
    }
    function scanNumber() {
        scanKnownDigits();
        if (!eof() && input.charCodeAt(position) === 46 /* CharCode.Dot */) {
            position++;
            scanRequiredDigits();
        }
        if (!eof() && input.charCodeAt(position) === 101 /* CharCode.e */) {
            position++;
            const ch = input.charCodeAt(position);
            if (ch === 43 /* CharCode.Plus */ || ch === 45 /* CharCode.Minus */) {
                position++;
            }
            scanRequiredDigits();
        }
        return (token = Token.NumericLiteral);
    }
    function scanKnownDigits() {
        do {
            position++;
        } while (!eof() && isDigit(input.charCodeAt(position)));
    }
    function scanRequiredDigits() {
        if (eof() || !isDigit(input.charCodeAt(position))) {
            error({ code: "digit-expected" });
            return;
        }
        scanKnownDigits();
    }
    function scanHexNumber() {
        position += 2; // consume '0x'
        if (eof() || !isHexDigit(input.charCodeAt(position))) {
            error({ code: "hex-digit-expected" });
            return (token = Token.NumericLiteral);
        }
        do {
            position++;
        } while (!eof() && isHexDigit(input.charCodeAt(position)));
        return (token = Token.NumericLiteral);
    }
    function scanBinaryNumber() {
        position += 2; // consume '0b'
        if (eof() || !isBinaryDigit(input.charCodeAt(position))) {
            error({ code: "binary-digit-expected" });
            return (token = Token.NumericLiteral);
        }
        do {
            position++;
        } while (!eof() && isBinaryDigit(input.charCodeAt(position)));
        return (token = Token.NumericLiteral);
    }
    function scanSingleLineComment() {
        position = skipSingleLineComment(input, position, endPosition);
        return (token = Token.SingleLineComment);
    }
    function scanMultiLineComment() {
        token = Token.MultiLineComment;
        if (lookAhead(2) === 42 /* CharCode.Asterisk */) {
            tokenFlags |= TokenFlags.DocComment;
        }
        const [newPosition, terminated] = skipMultiLineComment(input, position);
        position = newPosition;
        return terminated ? token : unterminated(token);
    }
    function scanDocCodeSpan() {
        position++; // consume '`'
        loop: for (; !eof(); position++) {
            const ch = input.charCodeAt(position);
            switch (ch) {
                case 96 /* CharCode.Backtick */:
                    position++;
                    return (token = Token.DocCodeSpan);
                case 13 /* CharCode.CarriageReturn */:
                case 10 /* CharCode.LineFeed */:
                    break loop;
            }
        }
        return unterminated(Token.DocCodeSpan);
    }
    function scanString(tokenFlags) {
        if (tokenFlags & TokenFlags.TripleQuoted) {
            position += 3; // consume '"""'
        }
        else {
            position++; // consume '"'
        }
        return scanStringLiteralLike(tokenFlags, Token.StringTemplateHead, Token.StringLiteral);
    }
    function scanStringTemplateSpan(tokenFlags) {
        position++; // consume '{'
        return scanStringLiteralLike(tokenFlags, Token.StringTemplateMiddle, Token.StringTemplateTail);
    }
    function scanStringLiteralLike(requestedTokenFlags, template, tail) {
        const multiLine = requestedTokenFlags & TokenFlags.TripleQuoted;
        tokenFlags = requestedTokenFlags;
        loop: for (; !eof(); position++) {
            const ch = input.charCodeAt(position);
            switch (ch) {
                case 92 /* CharCode.Backslash */:
                    tokenFlags |= TokenFlags.Escaped;
                    position++;
                    if (eof()) {
                        break loop;
                    }
                    continue;
                case 34 /* CharCode.DoubleQuote */:
                    if (multiLine) {
                        if (lookAhead(1) === 34 /* CharCode.DoubleQuote */ && lookAhead(2) === 34 /* CharCode.DoubleQuote */) {
                            position += 3;
                            token = tail;
                            return tail;
                        }
                        else {
                            continue;
                        }
                    }
                    else {
                        position++;
                        token = tail;
                        return tail;
                    }
                case 36 /* CharCode.$ */:
                    if (lookAhead(1) === 123 /* CharCode.OpenBrace */) {
                        position += 2;
                        token = template;
                        return template;
                    }
                    continue;
                case 13 /* CharCode.CarriageReturn */:
                case 10 /* CharCode.LineFeed */:
                    if (multiLine) {
                        continue;
                    }
                    else {
                        break loop;
                    }
            }
        }
        return unterminated(tail);
    }
    function getStringLiteralOffsetStart(token, tokenFlags) {
        switch (token) {
            case Token.StringLiteral:
            case Token.StringTemplateHead:
                return tokenFlags & TokenFlags.TripleQuoted ? 3 : 1; // """ or "
            default:
                return 1; // {
        }
    }
    function getStringLiteralOffsetEnd(token, tokenFlags) {
        switch (token) {
            case Token.StringLiteral:
            case Token.StringTemplateTail:
                return tokenFlags & TokenFlags.TripleQuoted ? 3 : 1; // """ or "
            default:
                return 2; // ${
        }
    }
    function getStringTokenValue(token, tokenFlags) {
        if (tokenFlags & TokenFlags.TripleQuoted) {
            const start = tokenPosition;
            const end = position;
            const [indentationStart, indentationEnd] = findTripleQuotedStringIndent(start, end);
            return unindentAndUnescapeTripleQuotedString(start, end, indentationStart, indentationEnd, token, tokenFlags);
        }
        const startOffset = getStringLiteralOffsetStart(token, tokenFlags);
        const endOffset = getStringLiteralOffsetEnd(token, tokenFlags);
        const start = tokenPosition + startOffset;
        const end = tokenFlags & TokenFlags.Unterminated ? position : position - endOffset;
        if (tokenFlags & TokenFlags.Escaped) {
            return unescapeString(start, end);
        }
        return input.substring(start, end);
    }
    function getIdentifierTokenValue() {
        const start = tokenFlags & TokenFlags.Backticked ? tokenPosition + 1 : tokenPosition;
        const end = tokenFlags & TokenFlags.Backticked && !(tokenFlags & TokenFlags.Unterminated)
            ? position - 1
            : position;
        const text = tokenFlags & TokenFlags.Escaped ? unescapeString(start, end) : input.substring(start, end);
        if (tokenFlags & TokenFlags.NonAscii) {
            return text.normalize("NFC");
        }
        return text;
    }
    function getDocTextValue() {
        if (tokenFlags & TokenFlags.Escaped) {
            let start = tokenPosition;
            const end = position;
            let result = "";
            let pos = start;
            while (pos < end) {
                const ch = input.charCodeAt(pos);
                if (ch !== 92 /* CharCode.Backslash */) {
                    pos++;
                    continue;
                }
                if (pos === end - 1) {
                    break;
                }
                result += input.substring(start, pos);
                switch (input.charCodeAt(pos + 1)) {
                    case 64 /* CharCode.At */:
                        result += "@";
                        break;
                    default:
                        result += input.substring(pos, pos + 2);
                }
                pos += 2;
                start = pos;
            }
            result += input.substring(start, end);
            return result;
        }
        else {
            return input.substring(tokenPosition, position);
        }
    }
    function findTripleQuotedStringIndent(start, end) {
        end = end - 3; // Remove the """
        // remove whitespace before closing delimiter and record it as required
        // indentation for all lines
        const indentationEnd = end;
        while (end > start && isWhiteSpaceSingleLine(input.charCodeAt(end - 1))) {
            end--;
        }
        const indentationStart = end;
        // remove required final line break
        if (isLineBreak(input.charCodeAt(end - 1))) {
            if (isCrlf(end - 2, 0, end)) {
                end--;
            }
            end--;
        }
        return [indentationStart, indentationEnd];
    }
    function unindentAndUnescapeTripleQuotedString(start, end, indentationStart, indentationEnd, token, tokenFlags) {
        const startOffset = getStringLiteralOffsetStart(token, tokenFlags);
        const endOffset = getStringLiteralOffsetEnd(token, tokenFlags);
        start = start + startOffset;
        end = tokenFlags & TokenFlags.Unterminated ? end : end - endOffset;
        if (token === Token.StringLiteral || token === Token.StringTemplateHead) {
            // ignore leading whitespace before required initial line break
            while (start < end && isWhiteSpaceSingleLine(input.charCodeAt(start))) {
                start++;
            }
            // remove required initial line break
            if (isLineBreak(input.charCodeAt(start))) {
                if (isCrlf(start, start, end)) {
                    start++;
                }
                start++;
            }
            else {
                error({
                    code: "no-new-line-start-triple-quote",
                    codefixes: [createTripleQuoteIndentCodeFix({ file, pos: tokenPosition, end: position })],
                });
            }
        }
        if (token === Token.StringLiteral || token === Token.StringTemplateTail) {
            while (end > start && isWhiteSpaceSingleLine(input.charCodeAt(end - 1))) {
                end--;
            }
            // remove required final line break
            if (isLineBreak(input.charCodeAt(end - 1))) {
                if (isCrlf(end - 2, start, end)) {
                    end--;
                }
                end--;
            }
            else {
                error({
                    code: "no-new-line-end-triple-quote",
                    codefixes: [createTripleQuoteIndentCodeFix({ file, pos: tokenPosition, end: position })],
                });
            }
        }
        let skipUnindentOnce = false;
        // We are resuming from the middle of a line so we want to keep text as it is from there.
        if (token === Token.StringTemplateMiddle || token === Token.StringTemplateTail) {
            skipUnindentOnce = true;
        }
        // remove required matching indentation from each line and unescape in the
        // process of doing so
        let result = "";
        let pos = start;
        while (pos < end) {
            if (skipUnindentOnce) {
                skipUnindentOnce = false;
            }
            else {
                // skip indentation at start of line
                start = skipMatchingIndentation(pos, end, indentationStart, indentationEnd);
            }
            let ch;
            while (pos < end && !isLineBreak((ch = input.charCodeAt(pos)))) {
                if (ch !== 92 /* CharCode.Backslash */) {
                    pos++;
                    continue;
                }
                result += input.substring(start, pos);
                if (pos === end - 1) {
                    error({ code: "invalid-escape-sequence" }, pos, pos);
                    pos++;
                }
                else {
                    result += unescapeOne(pos);
                    pos += 2;
                }
                start = pos;
            }
            if (pos < end) {
                if (isCrlf(pos, start, end)) {
                    // CRLF in multi-line string is normalized to LF in string value.
                    // This keeps program behavior unchanged by line-ending conversion.
                    result += input.substring(start, pos);
                    result += "\n";
                    pos += 2;
                }
                else {
                    pos++; // include non-CRLF newline
                    result += input.substring(start, pos);
                }
                start = pos;
            }
        }
        result += input.substring(start, pos);
        return result;
    }
    function isCrlf(pos, start, end) {
        return (pos >= start &&
            pos < end - 1 &&
            input.charCodeAt(pos) === 13 /* CharCode.CarriageReturn */ &&
            input.charCodeAt(pos + 1) === 10 /* CharCode.LineFeed */);
    }
    function skipMatchingIndentation(pos, end, indentationStart, indentationEnd) {
        let indentationPos = indentationStart;
        end = Math.min(end, pos + (indentationEnd - indentationStart));
        while (pos < end) {
            const ch = input.charCodeAt(pos);
            if (isLineBreak(ch)) {
                // allow subset of indentation if line has only whitespace
                break;
            }
            if (ch !== input.charCodeAt(indentationPos)) {
                error({
                    code: "triple-quote-indent",
                    codefixes: [createTripleQuoteIndentCodeFix({ file, pos: tokenPosition, end: position })],
                });
                break;
            }
            indentationPos++;
            pos++;
        }
        return pos;
    }
    function unescapeString(start, end) {
        let result = "";
        let pos = start;
        while (pos < end) {
            const ch = input.charCodeAt(pos);
            if (ch !== 92 /* CharCode.Backslash */) {
                pos++;
                continue;
            }
            if (pos === end - 1) {
                error({ code: "invalid-escape-sequence" }, pos, pos);
                break;
            }
            result += input.substring(start, pos);
            result += unescapeOne(pos);
            pos += 2;
            start = pos;
        }
        result += input.substring(start, pos);
        return result;
    }
    function unescapeOne(pos) {
        const ch = input.charCodeAt(pos + 1);
        switch (ch) {
            case 114 /* CharCode.r */:
                return "\r";
            case 110 /* CharCode.n */:
                return "\n";
            case 116 /* CharCode.t */:
                return "\t";
            case 34 /* CharCode.DoubleQuote */:
                return '"';
            case 92 /* CharCode.Backslash */:
                return "\\";
            case 36 /* CharCode.$ */:
                return "$";
            case 64 /* CharCode.At */:
                return "@";
            case 96 /* CharCode.Backtick */:
                return "`";
            default:
                error({ code: "invalid-escape-sequence" }, pos, pos + 2);
                return String.fromCharCode(ch);
        }
    }
    function scanIdentifierOrKeyword() {
        let count = 0;
        let ch = input.charCodeAt(position);
        while (true) {
            position++;
            count++;
            if (eof()) {
                break;
            }
            ch = input.charCodeAt(position);
            if (count < 12 /* KeywordLimit.MaxLength */ && isLowercaseAsciiLetter(ch)) {
                continue;
            }
            if (isAsciiIdentifierContinue(ch)) {
                return scanIdentifier();
            }
            if (ch > 127 /* CharCode.MaxAscii */) {
                const cp = input.codePointAt(position);
                if (isNonAsciiIdentifierCharacter(cp)) {
                    return scanNonAsciiIdentifier(cp);
                }
            }
            break;
        }
        if (count >= 2 /* KeywordLimit.MinLength */ && count <= 12 /* KeywordLimit.MaxLength */) {
            const keyword = Keywords.get(getTokenText());
            if (keyword) {
                return (token = keyword);
            }
        }
        return (token = Token.Identifier);
    }
    function scanIdentifier() {
        let ch;
        do {
            position++;
            if (eof()) {
                return (token = Token.Identifier);
            }
        } while (isAsciiIdentifierContinue((ch = input.charCodeAt(position))));
        if (ch > 127 /* CharCode.MaxAscii */) {
            const cp = input.codePointAt(position);
            if (isNonAsciiIdentifierCharacter(cp)) {
                return scanNonAsciiIdentifier(cp);
            }
        }
        return (token = Token.Identifier);
    }
    function scanBacktickedIdentifier() {
        position++; // consume '`'
        tokenFlags |= TokenFlags.Backticked;
        loop: for (; !eof(); position++) {
            const ch = input.charCodeAt(position);
            switch (ch) {
                case 92 /* CharCode.Backslash */:
                    position++;
                    tokenFlags |= TokenFlags.Escaped;
                    continue;
                case 96 /* CharCode.Backtick */:
                    position++;
                    return (token = Token.Identifier);
                case 13 /* CharCode.CarriageReturn */:
                case 10 /* CharCode.LineFeed */:
                    break loop;
                default:
                    if (ch > 127 /* CharCode.MaxAscii */) {
                        tokenFlags |= TokenFlags.NonAscii;
                    }
            }
        }
        return unterminated(Token.Identifier);
    }
    function scanNonAsciiIdentifier(startCodePoint) {
        tokenFlags |= TokenFlags.NonAscii;
        let cp = startCodePoint;
        do {
            position += utf16CodeUnits(cp);
        } while (!eof() && isIdentifierContinue((cp = input.codePointAt(position))));
        return (token = Token.Identifier);
    }
    function atConflictMarker() {
        return isConflictMarker(input, position, endPosition);
    }
    function scanConflictMarker() {
        const marker = input.charCodeAt(position);
        position += mergeConflictMarkerLength;
        error({ code: "conflict-marker" });
        if (marker === 60 /* CharCode.LessThan */ || marker === 62 /* CharCode.GreaterThan */) {
            // Consume everything from >>>>>>> or <<<<<<< to the end of the line.
            while (position < endPosition && !isLineBreak(input.charCodeAt(position))) {
                position++;
            }
        }
        else {
            // Consume everything from the start of a ||||||| or =======
            // marker to the start of the next ======= or >>>>>>> marker.
            while (position < endPosition) {
                const ch = input.charCodeAt(position);
                if ((ch === 61 /* CharCode.Equals */ || ch === 62 /* CharCode.GreaterThan */) &&
                    ch !== marker &&
                    isConflictMarker(input, position, endPosition)) {
                    break;
                }
                position++;
            }
        }
        return (token = Token.ConflictMarker);
    }
}
/**
 *
 * @param script
 * @param position
 * @param endPosition exclude
 * @returns return === endPosition (or -1) means not found non-trivia until endPosition + 1
 */
function skipTriviaBackward(script, position, endPosition = -1) {
    endPosition = endPosition < -1 ? -1 : endPosition;
    const input = script.file.text;
    if (position === input.length) {
        // it's possible if the pos is at the end of the file, just treat it as trivia
        position--;
    }
    else if (position > input.length) {
        compilerAssert(false, "position out of range");
    }
    while (position > endPosition) {
        const ch = input.charCodeAt(position);
        if (isWhiteSpace(ch)) {
            position--;
        }
        else {
            const comment = getCommentAtPosition(script, position);
            if (comment) {
                position = comment.pos - 1;
            }
            else {
                break;
            }
        }
    }
    return position;
}
/**
 *
 * @param input
 * @param position
 * @param endPosition exclude
 * @returns return === endPosition (or input.length) means not found non-trivia until endPosition - 1
 */
function skipTrivia(input, position, endPosition = input.length) {
    endPosition = endPosition > input.length ? input.length : endPosition;
    while (position < endPosition) {
        const ch = input.charCodeAt(position);
        if (isWhiteSpace(ch)) {
            position++;
            continue;
        }
        if (ch === 47 /* CharCode.Slash */) {
            switch (input.charCodeAt(position + 1)) {
                case 47 /* CharCode.Slash */:
                    position = skipSingleLineComment(input, position, endPosition);
                    continue;
                case 42 /* CharCode.Asterisk */:
                    position = skipMultiLineComment(input, position, endPosition)[0];
                    continue;
            }
        }
        break;
    }
    return position;
}
function skipWhiteSpace(input, position, endPosition = input.length) {
    while (position < endPosition) {
        const ch = input.charCodeAt(position);
        if (!isWhiteSpace(ch)) {
            break;
        }
        position++;
    }
    return position;
}
function skipSingleLineComment(input, position, endPosition = input.length) {
    position += 2; // consume '//'
    for (; position < endPosition; position++) {
        if (isLineBreak(input.charCodeAt(position))) {
            break;
        }
    }
    return position;
}
function skipMultiLineComment(input, position, endPosition = input.length) {
    position += 2; // consume '/*'
    for (; position < endPosition; position++) {
        if (input.charCodeAt(position) === 42 /* CharCode.Asterisk */ &&
            input.charCodeAt(position + 1) === 47 /* CharCode.Slash */) {
            return [position + 2, true];
        }
    }
    return [position, false];
}
function skipContinuousIdentifier(input, position, isBackward = false) {
    let cur = position;
    const direction = isBackward ? -1 : 1;
    const bar = isBackward ? (p) => p >= 0 : (p) => p < input.length;
    while (bar(cur)) {
        const { char: cp, size } = codePointBefore(input, cur);
        cur += direction * size;
        if (!cp || !isIdentifierContinue(cp)) {
            break;
        }
    }
    return cur;
}
function isConflictMarker(input, position, endPosition = input.length) {
    // Conflict markers must be at the start of a line.
    const ch = input.charCodeAt(position);
    if (position === 0 || isLineBreak(input.charCodeAt(position - 1))) {
        if (position + mergeConflictMarkerLength < endPosition) {
            for (let i = 0; i < mergeConflictMarkerLength; i++) {
                if (input.charCodeAt(position + i) !== ch) {
                    return false;
                }
            }
            return (ch === 61 /* CharCode.Equals */ ||
                input.charCodeAt(position + mergeConflictMarkerLength) === 32 /* CharCode.Space */);
        }
    }
    return false;
}
function getTokenDisplayTable(entries) {
    const table = new Array(entries.length);
    for (const [token, display] of entries) {
        compilerAssert(token >= 0 && token < Token.__Count, `Invalid entry in token display table, ${token}, ${Token[token]}, ${display}`);
        compilerAssert(!table[token], `Duplicate entry in token display table for: ${token}, ${Token[token]}, ${display}`);
        table[token] = display;
    }
    for (let token = 0; token < Token.__Count; token++) {
        compilerAssert(table[token], `Missing entry in token display table: ${token}, ${Token[token]}`);
    }
    return table;
}

/**
 * Print a string as a TypeSpec identifier. If the string is a valid identifier, return it as is otherwise wrap it into backticks.
 * @param sv Identifier string value.
 * @returns Identifier string as it would be represented in a TypeSpec file.
 *
 * @example
 * ```ts
 * printIdentifier("foo") // foo
 * printIdentifier("foo bar") // `foo bar`
 * ```
 */
function printIdentifier(sv, 
/** @internal */ context = "disallow-reserved") {
    if (needBacktick(sv, context)) {
        const escapedString = sv
            .replace(/\\/g, "\\\\")
            .replace(/\n/g, "\\n")
            .replace(/\r/g, "\\r")
            .replace(/\t/g, "\\t")
            .replace(/`/g, "\\`");
        return `\`${escapedString}\``;
    }
    else {
        return sv;
    }
}
function needBacktick(sv, context) {
    if (sv.length === 0) {
        return false;
    }
    if (context === "allow-reserved" && ReservedKeywords.has(sv)) {
        return false;
    }
    if (Keywords.has(sv)) {
        return true;
    }
    let cp = sv.codePointAt(0);
    if (!isIdentifierStart(cp)) {
        return true;
    }
    let pos = 0;
    do {
        pos += utf16CodeUnits(cp);
    } while (pos < sv.length && isIdentifierContinue((cp = sv.codePointAt(pos))));
    return pos < sv.length;
}
function typeReferenceToString(node) {
    switch (node.kind) {
        case SyntaxKind.MemberExpression:
            return `${typeReferenceToString(node.base)}${node.selector}${typeReferenceToString(node.id)}`;
        case SyntaxKind.TypeReference:
            return typeReferenceToString(node.target);
        case SyntaxKind.Identifier:
            return node.sv;
    }
}
function splitLines(text) {
    const lines = [];
    let start = 0;
    let pos = 0;
    while (pos < text.length) {
        const ch = text.charCodeAt(pos);
        switch (ch) {
            case 13 /* CharCode.CarriageReturn */:
                if (text.charCodeAt(pos + 1) === 10 /* CharCode.LineFeed */) {
                    lines.push(text.slice(start, pos));
                    start = pos + 2;
                    pos++;
                }
                else {
                    lines.push(text.slice(start, pos));
                    start = pos + 1;
                }
                break;
            case 10 /* CharCode.LineFeed */:
                lines.push(text.slice(start, pos));
                start = pos + 1;
                break;
        }
        pos++;
    }
    lines.push(text.slice(start));
    return lines;
}

export { reportDeprecated as A, codePointBefore as B, isIdentifierContinue as C, skipTriviaBackward as D, skipContinuousIdentifier as E, isReservedKeyword as F, isTrivia as G, isComment as H, IdentifierKind as I, isStatementKeyword as J, TokenDisplay as K, ListenerFlow as L, trim as M, NoTarget as N, reportDiagnostic as O, typeReferenceToString as P, ResolutionResultFlags as R, SyntaxKind as S, Token as T, createDiagnostic as a, createSourceFile as b, compilerAssert as c, createDiagnosticCollector as d, createDiagnosticCreator as e, defineCodeFix as f, getSourceLocation as g, paramMessage as h, ignoreDiagnostics as i, createScanner as j, TokenFlags as k, isKeyword as l, isPunctuation as m, isWhiteSpace as n, formatDiagnostic as o, printIdentifier as p, getDiagnosticTemplateInstantitationTrace as q, api as r, splitLines as s, skipWhiteSpace as t, formatLog as u, getSourceFileKindFromExt as v, skipTrivia as w, getPositionBeforeTrivia as x, assertType as y, logDiagnostics as z };
