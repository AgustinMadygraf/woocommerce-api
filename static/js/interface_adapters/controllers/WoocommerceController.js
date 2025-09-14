// interface_adapters/controllers/WoocommerceController.js
import WoocommerceApiGateway from '../gateways/WoocommerceApiGateway.js';
import WoocommerceTablePresenter from '../presenters/WoocommerceTablePresenter.js';

export default class WoocommerceController {
  constructor() {
    this.gateway = new WoocommerceApiGateway();
    this.presenter = new WoocommerceTablePresenter();
  }

  async renderWoocommerceTable(containerId) {
    const container = document.getElementById(containerId);
    try {
      const data = await this.gateway.fetchWoocommerceProducts();
      const html = this.presenter.present(data);
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
      console.error('[API ERROR]', err);
    }
  }
}
