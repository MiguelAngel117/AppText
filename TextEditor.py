import threading
import time
import tkinter as tk

class TextEditor:
    def __init__(self):
        self.text = ""
        self.num_letters = 0
        self.num_words = 0
        self.auto_save_interval = 10  # tiempo en segundos

    def add_text(self, new_text):
        self.text += new_text
        self.num_letters += len(new_text)
        self.num_words = len(self.text.split())

    def auto_save(self):
        while True:
            with open("autosaved.txt", "w") as f:
                f.write(self.text)
            time.sleep(self.auto_save_interval)

class TextEditorGUI:
    def __init__(self, text_editor):
        self.text_editor = text_editor

        self.root = tk.Tk()
        self.root.geometry("400x400")

        self.text_area = tk.Text(self.root, height=10)
        self.text_area.pack()

        self.letter_count_label = tk.Label(self.root, text="Número de letras: 0")
        self.letter_count_label.pack()

        self.word_count_label = tk.Label(self.root, text="Número de palabras: 0")
        self.word_count_label.pack()

        self.auto_save_thread = threading.Thread(target=self.text_editor.auto_save, daemon=True)
        self.auto_save_thread.start()

        self.letter_count_thread = threading.Thread(target=self.update_letter_count, daemon=True)
        self.letter_count_thread.start()

        self.word_count_thread = threading.Thread(target=self.update_word_count, daemon=True)
        self.word_count_thread.start()

        self.text_area.bind("<Key>", self.on_text_change)

    def start(self):
        self.root.mainloop()

    def on_text_change(self, event):
        new_text = event.char
        self.text_editor.add_text(new_text)

    def update_letter_count(self):
        while True:
            self.letter_count_label.config(text=f"Número de letras: {self.text_editor.num_letters}")
            time.sleep(1)

    def update_word_count(self):
        while True:
            self.word_count_label.config(text=f"Número de palabras: {self.text_editor.num_words}")
            time.sleep(1)

def main():
    text_editor = TextEditor()
    gui = TextEditorGUI(text_editor)
    gui.start()

if __name__ == '__main__':
    main()
