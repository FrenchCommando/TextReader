import time
import tkinter as tk
import tkinter.font

line_split = .1
word_split = .08


def set_line_split(t):
    global line_split
    line_split = t

def set_word_split(t):
    global word_split
    word_split = t


class Application(tk.Frame):
    def __init__(self, master=None, library=None):
        super().__init__(master)
        self.master = master
        self.master.minsize(width=300, height=80)
        self.pack()

        self.library = library

        self.start = None
        self.it = None
        self.chosen_text = None
        self.text_buttons = None
        self.canvas = None
        self.pause = None
        self.back = None
        self.end = None
        self.quit = None

        self.create_widgets()

    def read_text(self, u):
        with self.library[u]() as f:
            for line in f:
                time.sleep(line_split)
                for word in line.split():
                    time.sleep(word_split)
                    yield (word)
        yield " "

    def create_widgets(self):
        self.start = tk.Button(self, text="Start\n(click me)", command=self.show_names)
        self.start.pack(side="top")

        self.quit = tk.Button(self, text="CLOSE", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def choose(self, chosen):
        print("I'm chosen: ", chosen)
        self.it = self.read_text(chosen)
        for u, v in self.text_buttons.items():
            v.destroy()
        self.display_text()

    def show_names(self):
        print("Showing text names")
        if self.start is not None:
            self.start.destroy()
        name_font = tk.font.Font(family='Helvetica', size=10, weight='bold')
        self.text_buttons = {}
        for my_u in self.library:
            self.text_buttons[my_u] = tk.Button(self, text=my_u, padx=1, pady=1, font=name_font,
                                                command=lambda u=my_u: self.choose(u))
            self.text_buttons[my_u].pack(expand=True)
        self.winfo_toplevel().wm_geometry("")  # cleans effect of manual resizing

    def display_text(self):
        self.winfo_toplevel().wm_geometry("")  # cleans effect of manual resizing
        go_on = True

        def pause_restart():
            nonlocal go_on
            go_on = not go_on
            if not go_on:
                self.pause["text"] = "RESTART"
            else:
                self.pause["text"] = "PAUSE"
                self.canvas.after(100, refresh)

        self.pause = tk.Button(self, text="PAUSE", fg="green", command=pause_restart)
        self.pause.pack(side="bottom")

        def stop():
            nonlocal go_on
            go_on = False
            self.canvas.destroy()
            self.pause.destroy()
            self.back.destroy()
            self.show_names()

        self.back = tk.Button(self, text="BACK", fg="blue", command=stop)
        self.back.pack(side="bottom")

        print("Printing text")
        text_font = tk.font.Font(family='Helvetica', size=50, weight='bold')
        self.canvas = tk.Button(self, text="---Starting---", padx=0, pady=0, height=2, width=20,
                                font=text_font)

        def refresh():
            nonlocal go_on
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


def run_application(library, name='RapidReader'):
    root = tk.Tk()
    root.title(name)
    root.attributes('-topmost', True)
    app = Application(master=root, library=library)
    app.mainloop()
