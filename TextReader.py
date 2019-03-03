import os
import time
import tkinter as tk
import tkinter.font


text_dir = os.path.expanduser('~/Text/')
line_split = 0.1
word_split = 0.08


def read_text(u):
    with open(os.path.join(text_dir, u), "r") as f:
        for line in f:
            for word in line.split():
                yield(word)
                time.sleep(word_split)
            time.sleep(line_split)


for u in os.listdir(text_dir):
    print(u)

# it = read_text("quantum.txt")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.show_names
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def choose(self, u):
        print("I'm chosen", u)
        self.it = read_text(u)
        for u, v in self.text_buttons.items():
            v.destroy()
        self.display_text()

    def show_names(self):
        print("Showing text names")
        name_font = tk.font.Font(family='Helvetica', size=10, weight='bold')
        self.text_buttons = {}
        for u in os.listdir(text_dir):
            self.text_buttons[u] = tk.Button(self, text=u, padx=5, pady=5, height=5, width=20,
                                             font=name_font,
                                             command=lambda: self.choose(u))
            self.text_buttons[u].pack()
        self.hi_there.destroy()

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
        print("hi there, everyone!")
        helv36 = tk.font.Font(family='Helvetica', size=50, weight='bold')

        self.canvas = tk.Button(self, text="TOTO", padx=10, pady=10, height=100, width=100,
                                font=helv36)

        def refresh():
            if not go_on:
                return
            s = next(self.it)
            self.canvas.config(text=s)
            if s != " ":
                self.canvas.after(100, refresh)
        self.canvas.pack()
        self.canvas.after(100, refresh)
        self.hi_there.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()