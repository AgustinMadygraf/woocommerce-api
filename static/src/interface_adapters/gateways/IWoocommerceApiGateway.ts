import { WoocommerceProductData } from '../../../src/types/models';

export interface IWoocommerceApiGateway {
  fetchWoocommerceProducts(): Promise<WoocommerceProductData>;
}
