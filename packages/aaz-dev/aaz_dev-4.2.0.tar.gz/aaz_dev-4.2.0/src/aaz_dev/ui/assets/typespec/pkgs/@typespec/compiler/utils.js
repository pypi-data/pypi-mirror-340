export { Q as Queue, T as TwoLevelMap, n as createRekeyableMap, a as deepClone, f as deepEquals } from './misc-97rxrklX.js';
import './path-utils-B4zKWudT.js';

/**
 * Helper class to track duplicate instance
 */
class DuplicateTracker {
    #entries = new Map();
    /**
     * Track usage of K.
     * @param k key that is being checked for duplicate.
     * @param v value that map to the key
     */
    track(k, v) {
        const existing = this.#entries.get(k);
        if (existing === undefined) {
            this.#entries.set(k, [v]);
        }
        else {
            existing.push(v);
        }
    }
    /**
     * Return iterator of all the duplicate entries.
     */
    *entries() {
        for (const [k, v] of this.#entries.entries()) {
            if (v.length > 1) {
                yield [k, v];
            }
        }
    }
}

function useStateMap(key) {
    const getter = (program, target) => program.stateMap(key).get(target);
    const setter = (program, target, value) => program.stateMap(key).set(target, value);
    const mapGetter = (program) => program.stateMap(key);
    return [getter, setter, mapGetter];
}
function useStateSet(key) {
    const getter = (program, target) => program.stateSet(key).has(target);
    const setter = (program, target) => program.stateSet(key).add(target);
    return [getter, setter];
}

export { DuplicateTracker, useStateMap, useStateSet };
