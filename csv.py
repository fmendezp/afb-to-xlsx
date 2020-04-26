from collections import deque

def short_key_list():
    key_list = ['record_code', 'bank_code', 'account_nb', 'purpose', 'internal_code', 'end2end_identification', '_1', '_2', '_3', '_4', '_5', 'desk_code', 'currency_code', 'nb_of_dec', 'account_nb', 'operation_code', 'operation_date', 'value_date', 'exempt_code', 'reject_code', 'creditor_name', 'debtor_name', 'remittance_information_1', 'label', 'label_1', 'label_2', 'reference', 'prev_date', 'prev_amount', 'next_date', 'next_amount', 'amount']
    return key_list

def default_key_list():
    key_list = ['record_code', 'bank_code', 'account_nb', 'purpose', 'internal_code', 'end2end_identification', '_', '_1', '_2', '_3', '_4', '_5', 'desk_code', 'currency_code', 'nb_of_dec', 'nb_of_dec_amount', 'equivalent_amount', 'nb_of_dec_exchange_rate', 'exchange_rate', 'account_nb', 'operation_code', 'operation_date', 'value_date', 'exempt_code', 'reject_code', 'creditor_account', 'creditor_name', 'creditor_id', 'creditor_id_type', 'creditor_ref_information', 'ultimate_creditor_name', 'ultimate_creditor_id', 'ultimate_creditor_type', 'debtor_account', 'debtor_name', 'debtor_id', 'debtor_id_type', 'ultimate_debtor_name', 'ultimate_debtor_id', 'ultimate_debtor_id_type', 'remittance_information_1', 'remittance_information_2', 'payment_infor_id', 'instruction_id', 'mandate_identification', 'sequence_type', 'label', 'label_1', 'label_2', 'reference', 'prev_date', 'prev_amount', 'next_date', 'next_amount', 'amount', 'qualifier', 'additional_info']
    return key_list

def format_csv_line(string_delimiter, separator, items):
    infix = string_delimiter + separator + ' ' + string_delimiter
    return string_delimiter + (infix.join(list(map(str, items)))) + string_delimiter

class CSVFormat:
    def __init__(self, string_delimiter, separator, key_list = default_key_list()):
        self.string_delimiter = string_delimiter
        self.separator = separator
        self.key_list = key_list

    def build_csv_header(self):
        headers = ['line_type'] + self.key_list
        return format_csv_line(self.string_delimiter, self.separator, headers)

    def build_csv_row(self, row_title, row):
        cells = deque([row_title])
        for k in self.key_list:
            if k in row:
                cells.append(row[k])
            else:
                cells.append('')
        return format_csv_line(self.string_delimiter, self.separator, cells)

    def convert_to_csv_string(self, statements):
        outputstring = ''
        outputstring += self.build_csv_header() + '\n'
        for r in range(len(statements)):
            statement = statements[r]
            lines = statement.lines
            outputstring += self.build_csv_row('statement ' + str(r) + ' header', statement.header) + '\n'
            for i in range(len(lines)):
                outputstring += self.build_csv_row('statement ' + str(r) + ' line ' + str(i), lines[i]) + '\n'
            outputstring += self.build_csv_row('statement ' + str(r) + ' footer', statement.footer) + '\n'
        return outputstring
