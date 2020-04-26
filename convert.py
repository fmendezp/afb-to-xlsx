import uuid
import os
import config
from cfonb import StatementReader
from csv import *
from xlsx import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

class App():

    def __init__(self):
        self.inputfile = ''
        self.outputfile = ''

    def parsefile(self, filename):
        original_file = open(filename, 'r')
        raw_data = original_file.read()
        tmp_file_name = 'tmp_' + uuid.uuid1().hex + '.afb'
        file_with_newlines = open(tmp_file_name, 'w')
        for pos in range(0, len(raw_data), 120):
            file_with_newlines.write(raw_data[pos:pos + 120])
            file_with_newlines.write('\n')
        file_with_newlines.flush()
        file_with_newlines.close()
        original_file.close()

        statement_file = open(tmp_file_name)
        reader = StatementReader()
        result = reader.parse(statement_file)
        statement_file.close()
        os.remove(tmp_file_name)
        self.statements = result

    def convert_to_csv(self):
        if not hasattr(self, 'statements'): return ""
        csvformat = CSVFormat(string_delimiter = self.delimiter_entry.get(), separator = self.separator_entry.get())
        return csvformat.convert_to_csv_string(self.statements)

    def save_csv_format_to_config(self):
        config.set_delimiter(self.delimiter_entry.get())
        config.set_separator(self.separator_entry.get())
        config.save()

    def update_csv_preview(self):
        self.csvresult = self.convert_to_csv()
        self.text.delete(1.0, END)
        self.text.insert(END, self.csvresult)
        self.save_csv_format_to_config()

    def update_csv_preview_callback(self, _a, _b, _c):
        self.update_csv_preview()

    def askopenfile(self):
        self.inputfile = filedialog.askopenfilename(initialdir = config.get_source_path(), title = "Select file", filetypes = (("AFB", ".AFB .afb .CFONB .cfonb"), ("all files", "*.*")))
        self.parsefile(self.inputfile)
        self.update_csv_preview()
        config.set_source_path(os.path.dirname(self.inputfile))
        config.save()
        self.save_button.configure(state=NORMAL)
        self.save_xlsx_button.configure(state=NORMAL)

    def savecsv(self):
        filename =  filedialog.asksaveasfilename(initialdir = config.get_target_path(), title = "Select file", filetypes = (("CSV",".csv"), ("all files","*.*")))
        with open(filename, 'w') as csv_file:
            csv_file.write(self.convert_to_csv())
            csv_file.close()
        config.set_target_path(os.path.dirname(filename))
        config.save()

    def savexlsx(self):
        if not hasattr(self, 'statements') : return
        filename =  filedialog.asksaveasfilename(initialdir = config.get_target_path(), title = "Select file", filetypes = (("XLSX",".xlsx"), ("all files","*.*")))
        XLSX().write_xlsx(filename, self.statements)
        config.set_target_path(os.path.dirname(filename))
        config.save()

    def start(self):
        root = Tk()
        root.title("Convert CFONB to CSV")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        load_button = ttk.Button(mainframe, text="Open AFB/CFONB", command=self.askopenfile, state=DISABLED)
        load_button.configure(state=NORMAL)
        load_button.grid(column=1, row=1, sticky=W)

        ttk.Label(mainframe, text="CSV field separator").grid(column=1, row=2, sticky=E)
        csv_separator = StringVar(value = config.get_separator())
        csv_separator.trace('w', self.update_csv_preview_callback)
        self.separator_entry = ttk.Entry(mainframe, width=3, textvariable=csv_separator)
        self.separator_entry.grid(column=2, row=2, sticky=(W))

        ttk.Label(mainframe, text="CSV string delimiter").grid(column=1, row=3, sticky=E)
        csv_string_delimiter = StringVar(value = config.get_delimiter())
        csv_string_delimiter.trace('w', self.update_csv_preview_callback)
        self.delimiter_entry = ttk.Entry(mainframe, width=3, textvariable=csv_string_delimiter)
        self.delimiter_entry.grid(column=2, row=3, sticky=(W))

        ttk.Label(mainframe, text="Preview").grid(column=1, row=4, sticky=W)

        self.text = ScrolledText(master = mainframe, width = 180, height = 20, wrap = NONE)
        self.text.grid(column=1, columnspan=2, row=5, sticky=W)

        self.save_button = ttk.Button(mainframe, text="Export CSV", command=self.savecsv, state=DISABLED)
        self.save_button.grid(column=1, row=6, sticky=E)

        self.save_xlsx_button = ttk.Button(mainframe, text="Export XLSX", command=self.savexlsx, state=DISABLED)
        self.save_xlsx_button.grid(column=2, row=6, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        load_button.focus()
        root.mainloop()

App().start()
