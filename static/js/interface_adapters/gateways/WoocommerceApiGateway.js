// interface_adapters/gateways/WoocommerceApiGateway.js

export default class WoocommerceApiGateway {
  async fetchWoocommerceProducts() {
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
