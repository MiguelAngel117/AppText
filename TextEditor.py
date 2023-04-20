import tkinter as tk
import threading
import time
import re
from colorama import Fore, Back, Style

class TextEditor:
    def __init__(self, root):
        """This method is the constructor of the class, it defines the elements 
            that will be in the graphic interface and the variables that 
            the program will have, it also has the instance of root 
            that allows to initialize the graphic component.

        Args:
            root (Object Tk): Return a new top level widget on screen SCREENNAME. A new Tcl interpreter will be created
        """
        self.root = root
        self.root.geometry("500x580+400+200")
        self.root.title("Procesador de Texto")
        
        # Letter and word counters
        self.letter_count = 0
        self.word_count = 0
        
        # Creation of the text editor
        self.textbox = tk.Text(self.root, height=25, width=60)
        self.textbox.pack(pady=20)
        
        # Creation of counter labels
        self.letter_label = tk.Label(self.root, text="Letras: 0")
        self.letter_label.pack(side="right", padx=10)
        self.word_label = tk.Label(self.root, text="Palabras: 0")
        self.word_label.pack(side="left", padx=10)
        self.repeat_label = tk.Label(self.root, text="Palabras repetidas: 0")
        self.repeat_label.pack(side="left", padx=10)
        self.vowel_label = tk.Label(self.root, text="Vocales: 0")
        self.vowel_label.pack(side="right", padx=10)

        # Creation of the save button
        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_document, bg="green")
        self.save_button.pack(pady=10)

        # Button to convert to uppercase
        self.upper_button = tk.Button(self.root, text="Mayúscula", command=self.to_upper, bg="green")
        self.upper_button.pack(pady=10)

        # Thread to count the letters
        self.letter_thread = threading.Thread(target=self.count_letters)
        self.letter_thread.daemon = True
        self.letter_thread.start()
        
        # Word count thread
        self.word_thread = threading.Thread(target=self.count_words)
        self.word_thread.daemon = True
        self.word_thread.start()

        # vowel count thread
        self.vowel_thread = threading.Thread(target=self.count_vowels)
        self.vowel_thread.daemon = True
        self.vowel_thread.start()
        
        # Thread to count the Thread to auto-save
        self.save_thread = threading.Thread(target=self.auto_save)
        self.save_thread.daemon = True
        self.save_thread.start()

        # Thread to underline repeated words
        self.repeat_thread = threading.Thread(target=self.revise_repeated_words)
        self.repeat_thread.daemon = True
        self.repeat_thread.start()
        
        # Thread to convert to uppercase
        self.upper_thread = threading.Thread(target=self.save_upper_content)
        self.upper_thread.start()

        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        
    def count_letters(self):
        while True:
            time.sleep(1)
            # Get the number of characters in the text editor
            self.letter_count = sum(not chr.isspace() for chr in self.textbox.get("1.0", tk.END))
            # Update the letter label
            self.letter_label.config(text=f"Letras: {self.letter_count}")
    
    def count_words(self):
        while True:
            time.sleep(1)
            # Get the text in the text editor and separate it by spaces
            words = self.textbox.get("1.0", tk.END).split()
            # Obtain the number of words
            self.word_count = len(words)
            # Update the word label
            self.word_label.config(text=f"Palabras: {self.word_count}")

    def count_vowels(self):
        while True:
            time.sleep(1)
            # we obtain the text that has been written
            text = self.textbox.get("1.0", tk.END)
            count = 0
            # we scroll through the text to find vowels
            for letra in text:
                 # Each lowercase letter is compared with the list of vowels.
                 if letra.lower() in "aeiou":
                    count = count+1
            # Obtain the number of vowels
            self.vowel_count =  count
            # Update the vowel label
            self.vowel_label.config(text=f"Vocales: {self.vowel_count}")
    
    def revise_repeated_words(self):
        while True:
            time.sleep(1)
            # All the content is obtained and the words are separated using spaces
            text = self.textbox.get("1.0", tk.END)
            words = text.split()
            repeated_words = set([word for word in words
                                  if words.count(word) > 1])
            for word in repeated_words:
                text = re.sub(word, Fore.RED + word + Fore.RESET, text)
            # Update tag with number of repeated words
            self.repeat_label.config(text=f"Palabras repetidas: {len(repeated_words)}")
    
    def auto_save(self):
        while True:
            time.sleep(1)
            # Get the contents of the text editor
            content = self.textbox.get("1.0", tk.END)
            # Write the content to a file
            with open("document.txt", "w") as f:
                f.write(content)
    
    def save_document(self):
        # Get the contents of the text editor
        content = self.textbox.get("1.0", tk.END)
        # Write the content to a file
        with open("document.txt", "w") as f:
            f.write(content)

    # Method to save the current contents of the editor
    # converted to uppercase
    def save_upper_content(self):
        while True:   
            time.sleep(1) 
            content = self.textbox.get("1.0", tk.END)
            content = content.upper()
            with open("documentUpper.txt", "w") as f:
                f.write(content)

    # Method to show in the editor the content
    # converted to uppercase
    def to_upper(self):
        with open("upper.txt", "r") as f:
                content = f.read()
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0",content)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()