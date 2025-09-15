import { WoocommerceProductData } from '../../../src/types/models';

export interface IWoocommerceTablePresenter {
  present(data: WoocommerceProductData): string;
}
