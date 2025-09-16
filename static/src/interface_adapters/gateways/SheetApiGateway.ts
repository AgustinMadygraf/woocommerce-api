import { ISheetApiGateway } from './ISheetApiGateway';

/**
 * Gateway to interact with the Sheets API
 * Implements the ISheetApiGateway interface
 */
export default class SheetApiGateway implements ISheetApiGateway {
  /**
   * Fetches sheet values from the API
   * @returns Promise resolving to a 2D array of sheet data
   */
  async fetchSheetValues(): Promise<string[][]> {
    const res = await fetch('/api/sheet-values');
    if (!res.ok) {
      let errorMsg = 'Error al cargar los datos.';
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
