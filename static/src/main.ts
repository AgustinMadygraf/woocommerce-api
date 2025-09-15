import { ISheetController } from './interface_adapters/controllers/ISheetController';
import { IWoocommerceController } from './interface_adapters/controllers/IWoocommerceController';

// Esta función se ejecutará cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  console.log('Aplicación inicializada');
  
  // Evento para el botón de actualizar datos de Google Sheets
  const updateSheetsBtn = document.getElementById('update-sheets-btn');
  updateSheetsBtn?.addEventListener('click', () => {
    console.log('Actualizando datos desde Google Sheets');
    // Aquí llamarás a la función correspondiente cuando implementes los controladores
  });
  
  // Evento para el botón de actualizar datos de WooCommerce
  const updateWooBtn = document.getElementById('update-woo-btn');
  updateWooBtn?.addEventListener('click', () => {
    console.log('Actualizando datos desde WooCommerce');
    // Aquí llamarás a la función correspondiente cuando implementes los controladores
  });
  
  // Inicialización de tablas
  initializeApp();
});

// Función para inicializar la aplicación
async function initializeApp() {
  try {
    console.log('Cargando datos iniciales...');
    // Aquí cargarás los datos cuando implementes los controladores
    
    // Por ejemplo:
    // const sheetController = new SheetController();
    // await sheetController.renderSheetTable('sheet-table-container');
    
    // const wooController = new WooCommerceController();
    // await wooController.renderWoocommerceTable('woo-table-container');
    
  } catch (error) {
    console.error('Error al inicializar la aplicación:', error);
  }
}