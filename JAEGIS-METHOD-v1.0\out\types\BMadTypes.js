"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BMadError = void 0;
// Error Types
class BMadError extends Error {
    code;
    category;
    constructor(message, code, category = 'execution') {
        super(message);
        this.code = code;
        this.category = category;
        $1this_name$3;
    }
}
exports.BMadError = BMadError;
//# sourceMappingURL=BMadTypes.js.map