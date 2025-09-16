
/**
 * Interface for WooCommerce Table Presenter
 * Defines methods for converting WooCommerce product data into presentable HTML
 */
export interface IWoocommerceTablePresenter {
	/**
	 * Converts product data into an HTML string representation
	 * @param data 2D array of product values
	 * @returns HTML string to be inserted into the DOM
	 */
	present(data: string[][]): string;
}
