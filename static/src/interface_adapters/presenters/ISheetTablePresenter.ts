/**
 * Interface for Sheet Table Presenter
 * Defines methods for converting raw sheet data into presentable HTML
 */
export interface ISheetTablePresenter {
  /**
   * Converts sheet data into an HTML string representation
   * @param data 2D array of sheet values
   * @returns HTML string to be inserted into the DOM
   */
  present(data: string[][]): string;
}
