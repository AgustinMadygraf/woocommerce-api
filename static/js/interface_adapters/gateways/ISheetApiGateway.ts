import { SheetData } from '../../types/models';

export interface ISheetApiGateway {
  fetchSheetValues(): Promise<SheetData>;
}
