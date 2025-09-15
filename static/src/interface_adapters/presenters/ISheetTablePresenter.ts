import { SheetData } from '../../../src/types/models';

export interface ISheetTablePresenter {
  present(data: SheetData): string;
}
