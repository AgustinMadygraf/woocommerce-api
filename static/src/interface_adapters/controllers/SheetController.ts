/*
Path: static/src/interface_adapters/controllers/SheetController.ts
*/

import { ISheetController } from './ISheetController';
import { ISheetApiGateway } from '../gateways/ISheetApiGateway';
import { ISheetTablePresenter } from '../presenters/ISheetTablePresenter';
import SheetApiGateway from '../gateways/SheetApiGateway.js';
import SheetTablePresenter from '../presenters/SheetTablePresenter.js';

export default class SheetController implements ISheetController {
  private gateway: ISheetApiGateway;
  private presenter: ISheetTablePresenter;

  constructor() {
    this.gateway = new SheetApiGateway();
    this.presenter = new SheetTablePresenter();
  }

  async renderSheetTable(containerId: string): Promise<void> {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`[API ERROR] Container with ID '${containerId}' not found`);
      return;
    }
    
    try {
      const data = await this.gateway.fetchSheetValues();
      const html = this.presenter.present(data);
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err instanceof Error ? err.message : 'Error desconocido'}</div>`;
      console.error('[API ERROR]', err);
    }
  }
}