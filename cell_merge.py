from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment


def merge_same_value(from_source='schedule_t.xlsx', to_source='schedule.xlsx'):
    print(f"merge 시작 - {from_source} -> {to_source}")
    wb = load_workbook(from_source, read_only=False)
    sheets_merge(wb)
    wb.save(to_source)


def sheets_merge(wb):
    for s_name in wb.sheetnames:
        ws = wb[s_name]
        sheet_merge(ws)


def sheet_merge(ws):
    key_columns = [1, 2]  # [대주제(Part), 중주제(Chapter)]
    for key_column in key_columns:
        cell_merge(ws, key_column)


def cell_merge(ws, key_column):
    max_row = ws.max_row
    prev_value = None
    start_row = 2
    for row, row_cells in enumerate(ws.iter_rows(min_col=key_column, min_row=start_row,
                                                 max_col=key_column, max_row=max_row),
                                    start_row):
        if prev_value != row_cells[0].value or row == max_row:
            if prev_value is not None:
                if row == max_row and prev_value == row_cells[0].value:
                    ws.merge_cells(start_row=start_row, start_column=key_column, end_row=row ,
                                   end_column=key_column)
                else:
                    ws.merge_cells(start_row=start_row, start_column=key_column, end_row=row-1,
                                   end_column=key_column)

                ws.cell(row=start_row, column=key_column).alignment = Alignment(horizontal='left',
                                                                                vertical='center')
                start_row = row
            prev_value = row_cells[0].value


if __name__ == '__main__':
    merge_same_value()
