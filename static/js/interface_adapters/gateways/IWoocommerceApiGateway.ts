import { WoocommerceProductData } from '../../types/models';

export interface IWoocommerceApiGateway {
  fetchWoocommerceProducts(): Promise<WoocommerceProductData>;
}
