import os
import time
import tkinter as tk
import tkinter.font
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--text_dir', help='folder path')
parser.add_argument('--line_split', help='pause between lines')
parser.add_argument('--word_split', help='pause between words')
args = parser.parse_args()

print(args)
text_dir = os.path.expanduser('~/') if args.text_dir is None else args.text_dir
line_split = 0.1 if args.line_split is None else args.line_split
word_split = 0.08 if args.word_split is None else args.word_split
print("Text Directory", text_dir)
print("Line split {} s".format(str(line_split)))
print("Word split {} s".format(str(word_split)))


def read_text(u):
    with open(os.path.join(text_dir, u), "r") as f:
        for line in f:
            for word in line.split():
                yield(word)
                time.sleep(word_split)
            time.sleep(line_split)
    yield " "


files_in_dir = [u for u in os.listdir(text_dir) if os.path.isfile(os.path.join(text_dir, u))]
for u in files_in_dir:
    print(u)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.minsize(width=300, height=80)
        self.pack()

        self.hi_there = None
        self.it = None
        self.chosen_text = None
        self.text_buttons = None
        self.canvas = None
        self.back = None
        self.end = None
        self.quit = None

        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Start\n(click me)"
        self.hi_there["command"] = self.show_names
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="CLOSE", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def choose(self):
        print("I'm chosen", self.chosen_text)
        self.it = read_text(self.chosen_text)
        for u, v in self.text_buttons.items():
            v.destroy()
        self.display_text()

    def show_names(self):
        print("Showing text names")
        self.hi_there.destroy()
        name_font = tk.font.Font(family='Helvetica', size=10, weight='bold')
        self.text_buttons = {}
        for my_u in files_in_dir:
            s = """def choose_text{0}(self):
                self.chosen_text = "{1}"
                self.choose()
Application.choose_text{0} = choose_text{0}
self.text_buttons[my_u] = tk.Button(self, text=my_u, padx=5, pady=5, height=5, width=20, font=name_font, command=self.choose_text{0})
            
            """.format(''.join([i for i in my_u[:-4] if i.isalpha()]), my_u)
            exec(s)
            self.text_buttons[my_u].pack(expand=True)

    def display_text(self):
        go_on = True

        def stop():
            nonlocal go_on
            go_on = False
            self.canvas.destroy()
            self.back.destroy()
            self.show_names()

        self.back = tk.Button(self, text="BACK", fg="blue",
                              command=stop)
        self.back.pack(side="bottom")
        print("Printing text")
        text_font = tk.font.Font(family='Helvetica', size=50, weight='bold')

        self.canvas = tk.Button(self, text="Words", padx=0, pady=0, height=2, width=20,
                                font=text_font)

        def refresh():
            if not go_on:
                return
            s = next(self.it)
            self.canvas.config(text=s)
            if s != " ":
                self.canvas.after(100, refresh)
            else:
                self.canvas.config(text="END of File\n CLICK ME", fg="BLACK",
                                   command=stop)
        self.canvas.pack(expand=True)
        self.canvas.after(100, refresh)


root = tk.Tk()
root.title('RapidReader')
root.lift()
root.attributes('-topmost', True)
app = Application(master=root)
app.mainloop()
