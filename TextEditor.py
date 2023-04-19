import tkinter as tk
import threading
import re
from colorama import Fore, Back, Style

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500+400+200")
        self.root.title("Procesador de Texto")
        
        # Contadores de letras y palabras
        self.letter_count = 0
        self.word_count = 0
        
        # Creación del editor de texto
        self.textbox = tk.Text(self.root, height=25, width=60)
        self.textbox.pack(pady=20)
        
        # Creación de las etiquetas de los contadores
        self.letter_label = tk.Label(self.root, text="Letras: 0")
        self.letter_label.pack(side="right", padx=10)
        self.word_label = tk.Label(self.root, text="Palabras: 0")
        self.word_label.pack(side="left", padx=10)
        
        self.repeat_label = tk.Label(self.root, text="Palabras repetidas: 0")
        self.repeat_label.pack(side="left", padx=10)

        # Creación del botón de guardar
        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_document, bg="green")
        self.save_button.pack(pady=10)

        # Hilo para contar las letras
        self.letter_thread = threading.Thread(target=self.count_letters)
        self.letter_thread.daemon = True
        self.letter_thread.start()
        
        # Hilo para contar las palabras
        self.word_thread = threading.Thread(target=self.count_words)
        self.word_thread.daemon = True
        self.word_thread.start()
        
        # Hilo para auto-guardar
        self.save_thread = threading.Thread(target=self.auto_save)
        self.save_thread.daemon = True
        self.save_thread.start()
        
        #Hilo para subrayar palabras repetidas
        self.repeat_thread = threading.Thread(target=self.revise_repeated_words)
        self.repeat_thread.daemon = True
        self.repeat_thread.start()
        
        # Centrar la ventana
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        
    def count_letters(self):
        while True:
            # Obtener el número de caracteres en el editor de texto
            self.letter_count = len(self.textbox.get("1.0", tk.END)) - 1
            # Actualizar la etiqueta de las letras
            self.letter_label.config(text=f"Letras: {self.letter_count}")
    
    def count_words(self):
        while True:
            # Obtener el texto en el editor de texto y separarlo por espacios
            words = self.textbox.get("1.0", tk.END).split()
            # Obtener el número de palabras
            self.word_count = len(words)
            # Actualizar la etiqueta de las palabras
            self.word_label.config(text=f"Palabras: {self.word_count}")
    
    def auto_save(self):
        while True:
            # Obtener el contenido del editor de texto
            content = self.textbox.get("1.0", tk.END)
            # Escribir el contenido en un archivo
            with open("autosave.txt", "w") as f:
                f.write(content)
    
    def revise_repeated_words(self):
        while True:
            #Se obtiene todo el contenido y se separan las palabras usando los espacios
            text = self.textbox.get("1.0", tk.END)
            words = text.split()
            repeated_words = set([word for word in words
                                  if words.count(word) > 1])
            for word in repeated_words:
                text = re.sub(word, Fore.RED + word + Fore.RESET, text)
            #Actualizar la etiqueta con el numero de palabras repetidas
            self.repeat_label.config(text=f"Palabras repetidas: {len(repeated_words)}")
    
    def save_document(self):
        # Obtener el contenido del editor de texto
        content = self.textbox.get("1.0", tk.END)
        # Escribir el contenido en un archivo
        with open("documento.txt", "w") as f:
            f.write(content)
if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
