from typing import Dict

from pandas import DataFrame, ExcelWriter

DEFAULT_DIR: str = '/Users/scvbe/OneDrive/Desktop/psychomterics paper'


class Exporter:
    def __init__(self, filename: str, directory: str = DEFAULT_DIR) -> None:
        self.writer: ExcelWriter = ExcelWriter(f'{directory}/{filename}.xlsx')
        self.directory: str = directory

    def write_multiple_dfs_to_single_sheet(self,
                                           dataframes: Dict[str, DataFrame],
                                           sheet_name: str = 'sheet1',
                                           # *additional_prepending_row: str\
                                           ) -> None:
        with self.writer as writer:
            workbook = writer.book
            # worksheet = workbook.add_worksheet(sheet_name)
            # writer.sheets[sheet_name] = worksheet

            COLUMN: int = 0
            row: int = 0

            # for new_row in additional_prepending_row:
            #     workbook.write_string(row=row, column=COLUMN, string=new_row)
            #     row += 1
            for key in dataframes.keys():
                workbook.write_string(row, COLUMN, key)
                row += 1
                dataframes[key].to_excel(writer, sheet_name=sheet_name, startrow=row, startcol=COLUMN)
                row += dataframes[key].shape[0] + 2
