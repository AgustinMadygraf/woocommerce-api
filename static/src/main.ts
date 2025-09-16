import { ISheetController } from './interface_adapters/controllers/ISheetController';
import { IWoocommerceController } from './interface_adapters/controllers/IWoocommerceController';

// Import actual implementations
import SheetController from './interface_adapters/controllers/SheetController.js';
import WoocommerceController from './interface_adapters/controllers/WoocommerceController.js';

document.addEventListener('DOMContentLoaded', () => {
  const sheetController: ISheetController = new SheetController();
  const wooController: IWoocommerceController = new WoocommerceController();

  // Render inicial (Google Sheets)
  sheetController.renderSheetTable('sheet-table-container');

  // Tab switching
  const sheetTab = document.getElementById('sheet-tab');
  const wooTab = document.getElementById('woo-tab');

  sheetTab?.addEventListener('click', () => {
    sheetController.renderSheetTable('sheet-table-container');
  });

  wooTab?.addEventListener('click', () => {
    wooController.renderWoocommerceTable('woo-table-container');
  });

  // Botón actualizar Google Sheets
  const updateSheetsBtn = document.getElementById('update-sheets-btn');
  if (updateSheetsBtn) {
    updateSheetsBtn.addEventListener('click', async () => {
      console.info('[ACTUALIZACIÓN SHEETS] Botón presionado');
      if (updateSheetsBtn instanceof HTMLButtonElement) {
        updateSheetsBtn.disabled = true;
        updateSheetsBtn.textContent = 'Actualizando...';
      }
      let msg: string;
      try {
        try {
          console.log('[ACTUALIZACIÓN SHEETS] Iniciando fetch real...');
          const res = await fetch('/api/update-from-sheets', { method: 'POST' });
          if (!res.ok) {
            let errorMsg = 'Error al actualizar desde Google Sheets.';
            try {
              const errJson = await res.json();
              if (errJson && errJson.error) errorMsg = errJson.error;
            } catch (e) {
              errorMsg = `Error ${res.status}: ${res.statusText}`;
            }
            throw new Error(errorMsg);
          }
          msg = '<div class="alert alert-success mt-2">Actualización desde Google Sheets completada con éxito.</div>';
          console.info('[ACTUALIZACIÓN SHEETS] Actualización exitosa');
        } catch (fetchErr) {
          console.error('[ACTUALIZACIÓN SHEETS] Error en fetch:', fetchErr);
          msg = `<div class="alert alert-danger mt-2">${fetchErr instanceof Error ? fetchErr.message : 'Error al actualizar desde Google Sheets.'}</div>`;
        }
        try {
          const container = document.getElementById('sheet-table-container');
          container?.insertAdjacentHTML('beforebegin', msg);
          console.log('[ACTUALIZACIÓN SHEETS] Mensaje mostrado al usuario');
        } catch (domErr) {
          console.warn('[ACTUALIZACIÓN SHEETS] Error al actualizar el DOM:', domErr);
        }
      } catch (err) {
        console.error('[ACTUALIZACIÓN SHEETS] Error inesperado:', err);
      } finally {
        if (updateSheetsBtn instanceof HTMLButtonElement) {
          updateSheetsBtn.disabled = false;
          updateSheetsBtn.textContent = 'Actualizar base de datos desde Google Sheets';
        }
        console.log('[ACTUALIZACIÓN SHEETS] Botón reactivado');
      }
    });
  }

  // Botón actualizar WooCommerce
  const updateWooBtn = document.getElementById('update-woo-btn');
  if (updateWooBtn) {
    updateWooBtn.addEventListener('click', async () => {
      console.info('[ACTUALIZACIÓN WOO] Botón presionado');
      if (updateWooBtn instanceof HTMLButtonElement) {
        updateWooBtn.disabled = true;
        updateWooBtn.textContent = 'Actualizando...';
      }
      let msg: string;
      try {
        try {
          console.log('[ACTUALIZACIÓN WOO] Iniciando fetch real...');
          const res = await fetch('/api/update-from-woocommerce', { method: 'POST' });
          if (!res.ok) {
            let errorMsg = 'Error al actualizar desde WooCommerce.';
            try {
              const errJson = await res.json();
              if (errJson && errJson.error) errorMsg = errJson.error;
            } catch (e) {
              errorMsg = `Error ${res.status}: ${res.statusText}`;
            }
            throw new Error(errorMsg);
          }
          msg = '<div class="alert alert-success mt-2">Actualización desde WooCommerce completada con éxito.</div>';
          console.info('[ACTUALIZACIÓN WOO] Actualización exitosa');
        } catch (fetchErr) {
          console.error('[ACTUALIZACIÓN WOO] Error en fetch:', fetchErr);
          msg = `<div class="alert alert-danger mt-2">${fetchErr instanceof Error ? fetchErr.message : 'Error al actualizar desde WooCommerce.'}</div>`;
        }
        try {
          const container = document.getElementById('woo-table-container');
          container?.insertAdjacentHTML('beforebegin', msg);
          console.log('[ACTUALIZACIÓN WOO] Mensaje mostrado al usuario');
        } catch (domErr) {
          console.warn('[ACTUALIZACIÓN WOO] Error al actualizar el DOM:', domErr);
        }
      } catch (err) {
        console.error('[ACTUALIZACIÓN WOO] Error inesperado:', err);
      } finally {
        if (updateWooBtn instanceof HTMLButtonElement) {
          updateWooBtn.disabled = false;
          updateWooBtn.textContent = 'Actualizar base de datos desde WooCommerce';
        }
        console.log('[ACTUALIZACIÓN WOO] Botón reactivado');
      }
    });
  }
});