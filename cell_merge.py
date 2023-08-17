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
        max_row = ws.max_row
        key_columns = [1, 2]
        sheet_merge(key_columns, max_row, ws)


def sheet_merge(key_columns, max_row, ws):
    for key_column in key_columns:
        start_row = 2
        prev_value = None
        cell_merge(key_column, max_row, prev_value, start_row, ws)


def cell_merge(key_column, max_row, prev_value, start_row, ws):
    for row, row_cells in enumerate(ws.iter_rows(min_col=key_column, min_row=start_row,
                                                 max_col=key_column, max_row=max_row),
                                    start_row):
        if prev_value != row_cells[0].value or row == max_row:
            if prev_value is not None:
                if row == max_row:
                    end_row = row
                else:
                    end_row = row - 1
                ws.merge_cells(start_row=start_row, start_column=key_column, end_row=end_row,
                               end_column=key_column)

                ws.cell(row=start_row, column=key_column).alignment = Alignment(horizontal='left',
                                                                                vertical='center')
                start_row = row
            prev_value = row_cells[0].value


if __name__ == '__main__':
    merge_same_value()
