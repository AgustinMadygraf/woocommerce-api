/*
Path: static/js/main.js
*/

import SheetController from './interface_adapters/controllers/SheetController.js';
import WoocommerceController from './interface_adapters/controllers/WoocommerceController.js';

document.addEventListener('DOMContentLoaded', () => {
  const sheetController = new SheetController();
  const wooController = new WoocommerceController();

  // Render inicial (Google Sheets)
  sheetController.renderSheetTable('sheet-table-container');

  // Tab switching
  const sheetTab = document.getElementById('sheet-tab');
  const wooTab = document.getElementById('woo-tab');

  sheetTab.addEventListener('click', () => {
    sheetController.renderSheetTable('sheet-table-container');
  });

  wooTab.addEventListener('click', () => {
    wooController.renderWoocommerceTable('woo-table-container');
  });
});
