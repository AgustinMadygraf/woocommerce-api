/**
 * Interface for Google Sheets API Gateway
 * Defines methods for fetching data from Google Sheets
 */
export interface ISheetApiGateway {
  /**
   * Fetches values from Google Sheets API
   * @returns Promise resolving to a 2D array of sheet data
   */
  fetchSheetValues(): Promise<string[][]>;
}
