import tkinter as tk
from hangman import HangmanSpiel, SpielStatus


class HangmanGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title("Hangman")

        self.frame_wort = tk.Frame(self)
        self.frame_wort.pack(side=tk.TOP)
        label_wort = tk.Label(self.frame_wort, text='Gesuchtes Wort:')
        label_wort.pack(side=tk.LEFT)

        self.entry_word = tk.Entry(self.frame_wort, show='*')
        self.entry_word.pack(side=tk.RIGHT)
        self.raetselwort = tk.StringVar()
        self.entry_word["textvariable"] = self.raetselwort
        self.entry_word.bind('<Key-Return>', self.print_contents)
        self.entry_word.focus()

    def print_contents(self, event):
        self.entry_word.config(state='disabled')

        self.hangman = HangmanSpiel(self.raetselwort.get())
        print("Hi. The current entry content is:", self.raetselwort.get())

        self.frame_raetsel = tk.Frame(self)
        self.frame_raetsel.pack(side=tk.TOP)
        label_tipp = tk.Label(self.frame_raetsel, text='Tipp:')
        label_tipp.pack(side=tk.LEFT)

        self.entry_tipp = tk.Entry(self.frame_raetsel)
        self.entry_tipp.pack(side=tk.RIGHT)
        self.tipp = tk.StringVar()
        self.entry_tipp['textvariable'] = self.tipp
        self.entry_tipp.bind('<Key-Return>', self.raten)
        self.entry_tipp.focus()

        self.frame_status = tk.Frame(self)
        self.frame_status.pack(side=tk.TOP)
        self.label_status = tk.Label(self.frame_status, text=self.hangman.status_als_text())
        self.label_status.pack(side=tk.RIGHT)

    def raten(self, event):
        spielstand = self.hangman.raten(self.tipp.get())
        self.label_status['text'] = spielstand
        self.tipp.set('')

        if self.hangman.status() == SpielStatus.LAUFEND:
            self.entry_tipp.focus()
        else:
            button_text = "Gewonnen" if self.hangman.status() == SpielStatus.GEWONNEN else "Knapp verloren!"
            button_schliessen = tk.Button(self, text=button_text, command=self.master.destroy)
            button_schliessen.pack(side=tk.TOP)


root = tk.Tk()
app = HangmanGui(master=root)
app.mainloop()

