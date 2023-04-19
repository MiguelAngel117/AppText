import tkinter as tk
import threading
import time
import re
from colorama import Fore, Back, Style

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x580+400+200")
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
        self.vowel_label = tk.Label(self.root, text="Vocales: 0")
        self.vowel_label.pack(side="right", padx=10)

        # Creación del botón de guardar
        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_document, bg="green")
        self.save_button.pack(pady=10)

        # Creación del botón de convertir a mayúscula
        self.upper_button = tk.Button(self.root, text="Mayúscula", command=self.to_upper, bg="green")
        self.upper_button.pack(pady=10)

        # Hilo para contar las letras
        self.letter_thread = threading.Thread(target=self.count_letters)
        self.letter_thread.daemon = True
        self.letter_thread.start()
        
        # Hilo para contar las palabras
        self.word_thread = threading.Thread(target=self.count_words)
        self.word_thread.daemon = True
        self.word_thread.start()

        # Hilo para contar vocales
        self.vowel_thread = threading.Thread(target=self.count_vowels)
        self.vowel_thread.daemon = True
        self.vowel_thread.start()
        
        # Hilo para auto-guardar
        self.save_thread = threading.Thread(target=self.auto_save)
        self.save_thread.daemon = True
        self.save_thread.start()

        #Hilo para subrayar palabras repetidas
        self.repeat_thread = threading.Thread(target=self.revise_repeated_words)
        self.repeat_thread.daemon = True
        self.repeat_thread.start()
        
        # Hilo para convertir a mayúsculas
        self.upper_thread = threading.Thread(target=self.save_upper_content)
        self.upper_thread.start()

        # Centrar la ventana
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        
    def count_letters(self):
        while True:
            time.sleep(1)
            # Obtener el número de caracteres en el editor de texto
            self.letter_count = sum(not chr.isspace() for chr in self.textbox.get("1.0", tk.END))
            # Actualizar la etiqueta de las letras
            self.letter_label.config(text=f"Letras: {self.letter_count}")
    
    def count_words(self):
        while True:
            time.sleep(1)
            # Obtener el texto en el editor de texto y separarlo por espacios
            words = self.textbox.get("1.0", tk.END).split()
            # Obtener el número de palabras
            self.word_count = len(words)
            # Actualizar la etiqueta de las palabras
            self.word_label.config(text=f"Palabras: {self.word_count}")

    def count_vowels(self):
        while True:
            time.sleep(1)
            # obtenemos el texto que se ha escrito
            text = self.textbox.get("1.0", tk.END)
            # creamos un contador
            count = 0
            # recorremos el texto para encontrar vocales
            for letra in text:
                 # comparamos cada letra en minuscula, con la lista de bocales cobales 
                 if letra.lower() in "aeiou":
                    count = count+1
            # Obtener el número de vocales
            self.vowel_count =  count
            # Actualizar la etiqueta de las vocales
            self.vowel_label.config(text=f"Vocales: {self.vowel_count}")
    
    def revise_repeated_words(self):
        while True:
            time.sleep(1)
            #Se obtiene todo el contenido y se separan las palabras usando los espacios
            text = self.textbox.get("1.0", tk.END)
            words = text.split()
            repeated_words = set([word for word in words
                                  if words.count(word) > 1])
            for word in repeated_words:
                text = re.sub(word, Fore.RED + word + Fore.RESET, text)
            #Actualizar la etiqueta con el numero de palabras repetidas
            self.repeat_label.config(text=f"Palabras repetidas: {len(repeated_words)}")
    
    def auto_save(self):
        while True:
            time.sleep(1)
            # Obtener el contenido del editor de texto
            content = self.textbox.get("1.0", tk.END)
            # Escribir el contenido en un archivo
            with open("autosave.txt", "w") as f:
                f.write(content)
    
    def save_document(self):
        # Obtener el contenido del editor de texto
        content = self.textbox.get("1.0", tk.END)
        # Escribir el contenido en un archivo
        with open("documento.txt", "w") as f:
            f.write(content)

    # Método para guardar el contenido actual del editor
    # convertido a mayúsculas
    def save_upper_content(self):
<<<<<<< HEAD
        while True:   
            time.sleep(1) 
=======
        while True:    
>>>>>>> 1b3c399ed006ea4c2fdaa6b5bdd1a7f304acfb95
            content = self.textbox.get("1.0", tk.END)
            content = content.upper()
            with open("upper.txt", "w") as f:
                f.write(content)

    # Método para mostrar en el editor el contenido
    # convertido a mayúsculas
    def to_upper(self):
        with open("upper.txt", "r") as f:
                content = f.read()
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0",content)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()