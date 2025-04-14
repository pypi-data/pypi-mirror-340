export { D as unsafe_DefaultRouteProducer, g as unsafe_getRouteProducer, s as unsafe_setRouteOptionsForNamespace, a as unsafe_setRouteProducer } from './auth-BW4o-1d0.js';
import '@typespec/compiler/utils';
import '@typespec/compiler';
import '@typespec/compiler/ast';

let getStreamOf;
try {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    getStreamOf = (await import('@typespec/streams')).getStreamOf;
}
catch {
    getStreamOf = () => {
        throw new Error("@typespec/streams was not found");
    };
}
/**
 * Gets stream metadata for a given `HttpOperationParameters` or `HttpOperationResponseContent`.
 */
function getStreamMetadata(program, httpParametersOrResponse) {
    const body = httpParametersOrResponse.body;
    if (!body)
        return;
    const contentTypes = body.contentTypes;
    if (!contentTypes.length)
        return;
    // @body is always explicitly set by HttpStream, so body.property will be defined.
    const bodyProperty = body.property;
    if (!bodyProperty)
        return;
    const streamData = getStreamFromBodyProperty(program, bodyProperty);
    if (!streamData)
        return;
    return {
        bodyType: body.type,
        originalType: streamData.model,
        streamType: streamData.streamOf,
        contentTypes: contentTypes,
    };
}
function getStreamFromBodyProperty(program, bodyProperty) {
    // Check the model first, then if we can't find it, fallback to the sourceProperty model.
    const streamOf = bodyProperty.model ? getStreamOf(program, bodyProperty.model) : undefined;
    if (streamOf) {
        // if `streamOf` is defined, then we know that `bodyProperty.model` is defined.
        return { model: bodyProperty.model, streamOf };
    }
    if (bodyProperty.sourceProperty) {
        return getStreamFromBodyProperty(program, bodyProperty.sourceProperty);
    }
    return;
}

export { getStreamMetadata };
