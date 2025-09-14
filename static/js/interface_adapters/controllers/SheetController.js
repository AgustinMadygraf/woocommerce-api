// interface_adapters/controller/SheetController.js
import SheetApiGateway from '../gateways/SheetApiGateway.js';
import SheetTablePresenter from '../presenters/SheetTablePresenter.js';

export default class SheetController {
  constructor() {
    this.gateway = new SheetApiGateway();
    this.presenter = new SheetTablePresenter();
  }

  async renderSheetTable(containerId) {
    const container = document.getElementById(containerId);
    try {
      const data = await this.gateway.fetchSheetValues();
      const html = this.presenter.present(data);
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
      console.error('[API ERROR]', err);
    }
  }
}
