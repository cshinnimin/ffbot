import { JsonExpectedError } from '../types/Error';

export const JsonUtils = {
    parse(str: string) {
        try {
            return JSON.parse(str);
        } catch {
            throw new JsonExpectedError('I need to recall my training.');
        }
    },
};