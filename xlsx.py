from collections import deque
import csv
import xlsxwriter


class XLSX:

    def write_line(self, worksheet, row_number, items):
        for i in range(len(items)):
            worksheet.write(row_number, i, items[i])

    def write_xlsx_row(self, key_list, worksheet, row_number, row_title, row_data):
        cells = deque([row_title])
        for k in key_list:
            if k in row_data:
                cells.append(row_data[k])
            else:
                cells.append('')
        self.write_line(worksheet, row_number, cells)

    def write_statements(self, worksheet, statements):
        headers = csv.default_key_list()
        self.write_line(worksheet, 0, ['line_type'] + headers)
        row_number = 1
        for r in range(len(statements)):
            statement = statements[r]
            line_title = 'statement ' + str(r) + ' header'
            self.write_xlsx_row(headers, worksheet, row_number, line_title, statement.header)
            row_number+=1
            lines = statement.lines
            for i in range(0, len(lines)):
                line_title = 'statement ' + str(r) + ' line ' + str(i)
                self.write_xlsx_row(headers, worksheet, row_number, line_title, lines[i])
                row_number+=1
            line_title = 'statement ' + str(r) + ' footer'
            self.write_xlsx_row(headers, worksheet, row_number, line_title, statement.footer)
            row_number+=1

    def write_xlsx(self, filename, statements):
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        self.write_statements(worksheet, statements)
        workbook.close()
