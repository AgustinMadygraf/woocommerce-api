/*
Path: static/src/interface_adapters/controllers/WoocommerceController.ts
*/

import { IWoocommerceController } from './IWoocommerceController';
import { IWoocommerceApiGateway } from '../gateways/IWoocommerceApiGateway';
import { IWoocommerceTablePresenter } from '../presenters/IWoocommerceTablePresenter';
import WoocommerceApiGateway from '../gateways/WoocommerceApiGateway.js';
import WoocommerceTablePresenter from '../presenters/WoocommerceTablePresenter.js';

export default class WoocommerceController implements IWoocommerceController {
  private gateway: IWoocommerceApiGateway;
  private presenter: IWoocommerceTablePresenter;

  constructor() {
    this.gateway = new WoocommerceApiGateway();
    this.presenter = new WoocommerceTablePresenter();
  }

  async renderWoocommerceTable(containerId: string): Promise<void> {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`[API ERROR] Container with ID '${containerId}' not found`);
      return;
    }
    
    try {
      const data = await this.gateway.fetchWoocommerceProducts();
      const html = this.presenter.present(data);
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err instanceof Error ? err.message : 'Error desconocido'}</div>`;
      console.error('[API ERROR]', err);
    }
  }
}