/*
Path: static/src/interface_adapters/controllers/SheetController.ts
*/
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import SheetApiGateway from '../gateways/SheetApiGateway.js';
import SheetTablePresenter from '../presenters/SheetTablePresenter.js';
export default class SheetController {
    constructor() {
        this.gateway = new SheetApiGateway();
        this.presenter = new SheetTablePresenter();
    }
    renderSheetTable(containerId) {
        return __awaiter(this, void 0, void 0, function* () {
            const container = document.getElementById(containerId);
            if (!container) {
                console.error(`[API ERROR] Container with ID '${containerId}' not found`);
                return;
            }
            try {
                const data = yield this.gateway.fetchSheetValues();
                const html = this.presenter.present(data);
                container.innerHTML = html;
            }
            catch (err) {
                container.innerHTML = `<div class="alert alert-danger">${err instanceof Error ? err.message : 'Error desconocido'}</div>`;
                console.error('[API ERROR]', err);
            }
        });
    }
}
