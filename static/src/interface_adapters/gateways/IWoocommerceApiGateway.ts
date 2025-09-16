/**
 * Interface for WooCommerce API Gateway
 * Defines methods for fetching WooCommerce products
 */
export interface IWoocommerceApiGateway {
  /**
   * Fetches products from WooCommerce API
   * @returns Promise resolving to a 2D array of product data
   */
  fetchWoocommerceProducts(): Promise<string[][]>;
}