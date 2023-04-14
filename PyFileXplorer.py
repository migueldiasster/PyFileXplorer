import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class FileExplorerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Explorador de Archivos")
        self.create_gui()

    def create_gui(self):
        # Crear el Treeview para mostrar los archivos y carpetas
        self.treeview = ttk.Treeview(self.window)
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear el scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Agregar eventos de doble clic y clic derecho al Treeview
        self.treeview.bind('<Double-1>', self.open_file)
        self.treeview.bind('<Button-3>', self.show_context_menu)

        # Crear el menú contextual para el clic derecho
        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Abrir", command=self.open_file)
        self.context_menu.add_command(label="Eliminar", command=self.delete_file)
        self.context_menu.add_command(label="Copiar", command=self.copy_file)
        self.context_menu.add_command(label="Pegar", command=self.paste_file)

        # Crear el botón de selección de directorio
        self.browse_button = ttk.Button(self.window, text="Seleccionar Directorio", command=self.browse_directory)
        self.browse_button.pack(pady=10)

        self.window.mainloop()

    def browse_directory(self):
        directory_path = filedialog.askdirectory()  # Mostrar el diálogo de selección de directorio
        self.treeview.delete(*self.treeview.get_children())  # Limpiar el Treeview

        if directory_path:
            self.populate_treeview(directory_path)

    def populate_treeview(self, directory_path, parent=''):
        # Recorrer los archivos y carpetas en el directorio y agregarlos al Treeview
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            item_id = self.treeview.insert(parent, 'end', text=item, open=False)

            if os.path.isdir(item_path):
                self.treeview.item(item_id, tags=('directory',))
                self.populate_treeview(item_path, item_id)
            else:
                self.treeview.item(item_id, tags=('file',))

    def open_file(self, event=None):
        selected_item = self.treeview.selection()

        if selected_item:
            item_text = self.treeview.item(selected_item)['text']
            item_tags = self.treeview.item(selected_item)['tags']

            if 'file' in item_tags:
                messagebox.showinfo("Abrir", f"Se seleccionó el archivo: {item_text}")
            else:
                self.treeview.item(selected_item, open=not self.treeview.item(selected_item, 'open'))

    def delete_file(self):
        selected_item = self.treeview.selection()

        if selected_item:
            item_text = self.treeview.item(selected_item)['text']
            item_tags = self.treeview.item(selected_item)['tags']

            if 'file' in item_tags:
                confirm = messagebox.askyesno("Eliminar", f"¿Estás seguro de que quieres eliminar el archivo {item_text}?")

                if confirm:
                    self.treeview.delete(selected_item)
            else:
                confirm = messagebox.askyesno("Eliminar", f"¿Estás seguro de que quieres eliminar la carpeta {item_text}?")

                if confirm:
                    self.treeview.delete(selected_item)

    def copy_file(self):
        selected_item = self.treeview.selection()

        if selected_item:
            self.copied_item = selected_item

    def paste_file(self):
        selected_item = self.treeview.selection()

        if selected_item and self.copied_item:
            copied_item_text = self.treeview.item(self.copied_item)['text']
            copied_item_tags = self.treeview.item(self.copied_item)['tags']

            if 'file' in copied_item_tags:
                self.treeview.insert(selected_item, 'end', text=copied_item_text, tags=copied_item_tags)
            else:
                self.treeview.insert(selected_item, 'end', text=copied_item_text, tags=copied_item_tags, open=False)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

if __name__ == '__main__':
    app = FileExplorerApp()
    