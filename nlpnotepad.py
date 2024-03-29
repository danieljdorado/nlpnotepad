import spacy
import tkinter as tk
from collections import Counter
from tkinter import filedialog
from tkinter import messagebox

class Menubar:

    def __init__(self, parent):

        font_specs = ("Calibri", 14)
        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New",
                                    accelerator='Ctrl+N',
                                    command=parent.new_file)
        file_dropdown.add_command(label="Open",
                                    accelerator='Ctrl+O',
                                    command=parent.open_file)
        file_dropdown.add_command(label="Save",
                                    accelerator='Ctrl+S',
                                    command=parent.save)
        file_dropdown.add_command(label="Save As",
                                    accelerator='Ctrl+Shift+S',
                                    command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit",
                                    command=parent.master.destroy)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label='Release Notes',
                                   command=self.show_release_notes)
        about_dropdown.add_command(label='About',
                                   command=self.show_about_message)


        nlp_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        nlp_dropdown.add_command(label='Report',
                                        command=parent.generate_report)

        menubar.add_cascade(label = "File", menu=file_dropdown)
        menubar.add_cascade(label = "NLP", menu=nlp_dropdown)
        menubar.add_cascade(label = "About", menu=about_dropdown)

    def show_about_message(self):
        box_title = 'About NLP Notepad'
        box_message = 'A Simple Text Analyzer and Editor'
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = 'Release Notes'
        box_message = 'Version 0.1'
        messagebox.showinfo(box_title, box_message)

    def process_report(self):
        box_title = 'Release Notes'
        box_message = 'Version 0.1'
        messagebox.showinfo(box_title, box_message)


class Report:
    "Creates NLP reports from the active window text"

    def __init__(self, parent, processed_text):
        self.processed_text = processed_text

        # Lemma tokens.
        self.tokens = [token.lemma_ for token in self.processed_text if token.pos_ != 'PUNCT']
        self.token_counter = Counter(self.tokens)

        # POS tokens.
        self.pos_tokens = [token.pos_ for token in self.processed_text]
        self.pos_counter = Counter(self.pos_tokens)

    def get_report(self):
        message_title = 'NLP Report'

        reports = [
            self.get_type_token_ratio(),
            self.get_pos_count()
        ]

        report = ''

        for report_message in reports:
            report += report_message + '\n' * 2
        messagebox.showinfo(message_title, report)

    def get_type_token_ratio(self):
        "Return Type-Text Ratio message"
        types = len(list(self.token_counter))
        token_count = sum(self.token_counter.values())
        ttr = round(types / token_count * 100, 2)
        ttr_message = f'Unique Tokens: {types}\nTotal Tokens: {token_count}\nTTR: {ttr}%'
        return ttr_message

    def get_pos_count(self):
        "Return Parts of Speech count message"
        pos_message  = 'Parts of Speech Counts:\n'
        for pos, count in self.pos_counter.most_common():
            pos_message += f'{pos}: {count}\n'
        return pos_message


class Statusbar:
    def __init__(self, parent):
        
        font_specs = ('Colibri', 9)

        self.status = tk.StringVar()
        self.status.set('NLP Notepad - 0.1')

        label = tk.Label(parent.textarea, textvariable=self.status, fg='black',
                         bg='lightgrey', anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set('Your File Has Been Saved!')
        else:
            self.status.set('NLP Notepad - 0.1')


class NlpNotebook:
    def __init__(self, master):
        master.title("Untitled - NLP Notepad")
        master.geometry("1200x700")

        font_specs = ("Comic Sans MS", 15)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

        self.bind_shortcuts()
        
        self.nlp = spacy.load("en_core_web_sm")

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + ' - NLP Notepad')
        else:
            self.master.title('Untitled - NLP Notepad')

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension = '.txt',
            filetypes=[('All Files', '*.*'),
                        ('Text Files', '*.txt')]
        )
        if self.filename: 
            self.textarea.delete(1.0, tk.END)
            with open(self.filename,'r') as f:
                self.textarea.insert(1.0, f.read())
            self.set_window_title(self.filename)

    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_content)
                    self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()
    
    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile='Untitled.txt',
                defaultextension = '.txt',
                filetypes=[('All Files', '*.*'),
                        ('Text Files', '*.txt')])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, 'w') as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def generate_report(self):
        textarea_content = self.textarea.get(1.0, tk.END).strip()

        if textarea_content:
            processed_text = self.nlp(textarea_content)
            self.report = Report(self, processed_text)
            self.report.get_report()
        else:
            message_title = 'Report Error'
            error_message = 'No text to analyze.'
            messagebox.showwarning(message_title, error_message)

    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.update_status)

if __name__ == "__main__":
    master = tk.Tk()
    notepad = NlpNotebook(master)
    master.mainloop()