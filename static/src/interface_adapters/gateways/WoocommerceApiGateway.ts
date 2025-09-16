import { IWoocommerceApiGateway } from './IWoocommerceApiGateway';

/**
 * Gateway to interact with the WooCommerce API
 * Implements the IWoocommerceApiGateway interface
 */
export default class WoocommerceApiGateway implements IWoocommerceApiGateway {
  /**
   * Fetches WooCommerce products from the API
   * @returns Promise resolving to a 2D array of product data
   */
  async fetchWoocommerceProducts(): Promise<string[][]> {
    const res = await fetch('/api/woocommerce-products');
    if (!res.ok) {
      let errorMsg = 'Error al cargar los productos WooCommerce.';
      try {
        const errJson = await res.json();
        if (errJson && errJson.error) errorMsg = errJson.error;
      } catch (e) {
        errorMsg = `Error ${res.status}: ${res.statusText}`;
      }
      throw new Error(errorMsg);
    }
    return res.json();
  }
}

