import { SheetData } from '../../../src/types/models';

export interface ISheetApiGateway {
  fetchSheetValues(): Promise<SheetData>;
}
