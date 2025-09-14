/*
Path: static/js/main.js
*/

import SheetController from './interface_adapters/controllers/SheetController.js';

document.addEventListener('DOMContentLoaded', () => {
  const controller = new SheetController();
  controller.renderSheetTable('sheet-table-container');
});
