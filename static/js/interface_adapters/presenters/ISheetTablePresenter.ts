import { SheetData } from '../../types/models';

export interface ISheetTablePresenter {
  present(data: SheetData): string;
}
