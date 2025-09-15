import { WoocommerceProductData } from '../../types/models';

export interface IWoocommerceTablePresenter {
  present(data: WoocommerceProductData): string;
}
