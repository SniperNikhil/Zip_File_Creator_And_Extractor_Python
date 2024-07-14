import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
from tkinterdnd2 import DND_FILES, TkinterDnD

class ZipFileCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("ZIP File Creator and Extractor")

        self.files = []
        self.zip_file_path = ""
        self.output_dir = ""
        self.extract_output_dir = ""

        self.create_frames()
        self.create_widgets()
        self.apply_colors()
        self.setup_dnd()

    def create_frames(self):
        # Create a frame for the ZIP File Creator
        self.frame_creator = tk.Frame(self.root, padx=10, pady=10, relief="solid", bd=2, bg="#f0f0f0")
        self.frame_creator.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Create a frame for the ZIP File Extractor
        self.frame_extractor = tk.Frame(self.root, padx=10, pady=10, relief="ridge", bd=2, bg="#f0f0f0")
        self.frame_extractor.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def create_widgets(self):
        # ZIP File Creator Frame
        tk.Label(self.frame_creator, text="ZIP File Creator", font=('Helvetica', 16, 'bold'), bg="#f0f0f0").pack(pady=10)
        
        tk.Label(self.frame_creator, text="Select files or directories to compress:", bg="#f0f0f0").pack(pady=10)
        tk.Button(self.frame_creator, text="Select Files/Directories", command=self.select_files, bg="#d9d9d9", font=('Helvetica', 12)).pack(pady=5)

        self.file_listbox = tk.Listbox(self.frame_creator, width=50, height=10, bg="#ffffff", font=('Helvetica', 12))
        self.file_listbox.pack(pady=10)

        tk.Label(self.frame_creator, text="Output Directory:", bg="#f0f0f0").pack(pady=10)
        self.output_label = tk.Label(self.frame_creator, text="No directory selected", bg="#f0f0f0", font=('Helvetica', 12))
        self.output_label.pack(pady=5)

        tk.Button(self.frame_creator, text="Select Output Directory", command=self.select_output_directory, bg="#d9d9d9", font=('Helvetica', 12)).pack(pady=5)

        tk.Label(self.frame_creator, text="Compression Level:", bg="#f0f0f0").pack(pady=10)
        self.compression_var = tk.StringVar(value="ZIP_DEFLATED")
        self.compression_menu = tk.OptionMenu(self.frame_creator, self.compression_var, "ZIP_STORED", "ZIP_DEFLATED", "ZIP_BZIP2", "ZIP_LZMA")
        self.compression_menu.config(bg="#ffffff", font=('Helvetica', 12))
        self.compression_menu.pack(pady=5)

        tk.Button(self.frame_creator, text="Create ZIP", command=self.create_zip, bg="#4CAF50", fg="#ffffff", font=('Helvetica', 12, 'bold')).pack(pady=20)

        # ZIP File Extractor Frame
        tk.Label(self.frame_extractor, text="ZIP File Extractor", font=('Helvetica', 16, 'bold'), bg="#f0f0f0").pack(pady=10)

        tk.Label(self.frame_extractor, text="Select ZIP file to extract:", bg="#f0f0f0").pack(pady=10)
        tk.Button(self.frame_extractor, text="Select ZIP File", command=self.select_zip_file, bg="#d9d9d9", font=('Helvetica', 12)).pack(pady=5)

        self.extract_label = tk.Label(self.frame_extractor, text="Selected ZIP File: None", bg="#f0f0f0", font=('Helvetica', 12))
        self.extract_label.pack(pady=10)

        tk.Label(self.frame_extractor, text="Select Extraction Directory:", bg="#f0f0f0").pack(pady=10)
        self.extract_output_label = tk.Label(self.frame_extractor, text="Extraction Directory: None", bg="#f0f0f0", font=('Helvetica', 12))
        self.extract_output_label.pack(pady=5)
        tk.Button(self.frame_extractor, text="Select Extraction Directory", command=self.select_extract_output_directory, bg="#d9d9d9", font=('Helvetica', 12)).pack(pady=5)

        tk.Button(self.frame_extractor, text="Extract ZIP", command=self.extract_zip, bg="#2196F3", fg="#ffffff", font=('Helvetica', 12, 'bold')).pack(pady=20)

        # Reset Button
        tk.Button(self.frame_extractor, text="Reset", command=self.reset_all, bg="#FF5722", fg="#ffffff", font=('Helvetica', 12, 'bold')).pack(pady=20)
        tk.Button(self.frame_creator, text="Reset", command=self.reset_all, bg="#FF5722", fg="#ffffff", font=('Helvetica', 12, 'bold')).pack(pady=10)

    def apply_colors(self):
        self.root.configure(bg="#e6e6e6")

    def setup_dnd(self):
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            self.files.append(file)
            self.file_listbox.insert(tk.END, file)

    def select_files(self):
        selected_files = filedialog.askopenfilenames()  # Or use askdirectory for directories
        for file in selected_files:
            self.files.append(file)
            self.file_listbox.insert(tk.END, file)

    def select_output_directory(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_label.config(text=f"Output Directory: {self.output_dir}")

    def create_zip(self):
        if not self.output_dir:
            messagebox.showwarning("Warning", "No output directory selected.")
            return

        output_filename = os.path.join(self.output_dir, "output.zip")
        compression = self.get_compression()

        with zipfile.ZipFile(output_filename, 'w', compression=compression) as zipf:
            for file in self.files:
                if os.path.isdir(file):
                    self.zipdir(file, zipf)
                else:
                    zipf.write(file, os.path.basename(file))

        messagebox.showinfo("Success", f"ZIP file '{output_filename}' created successfully!")
        self.reset_form()

    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                           os.path.join(path, '..')))

    def get_compression(self):
        compression_dict = {
            "ZIP_STORED": zipfile.ZIP_STORED,
            "ZIP_DEFLATED": zipfile.ZIP_DEFLATED,
            "ZIP_BZIP2": zipfile.ZIP_BZIP2,
            "ZIP_LZMA": zipfile.ZIP_LZMA
        }
        return compression_dict.get(self.compression_var.get(), zipfile.ZIP_DEFLATED)

    def reset_form(self):
        self.files = []
        self.file_listbox.delete(0, tk.END)
        self.output_dir = ""
        self.output_label.config(text="No directory selected")
        self.compression_var.set("ZIP_DEFLATED")

    def select_zip_file(self):
        self.zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if self.zip_file_path:
            self.extract_label.config(text=f"Selected ZIP File: {self.zip_file_path}")

    def select_extract_output_directory(self):
        self.extract_output_dir = filedialog.askdirectory()
        if self.extract_output_dir:
            self.extract_output_label.config(text=f"Extraction Directory: {self.extract_output_dir}")

    def extract_zip(self):
        if not self.zip_file_path:
            messagebox.showwarning("Warning", "No ZIP file selected.")
            return

        if not self.extract_output_dir:
            messagebox.showwarning("Warning", "No extraction directory selected.")
            return

        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_output_dir)

        messagebox.showinfo("Success", f"ZIP file extracted to '{self.extract_output_dir}' successfully!")
        self.reset_extract_form()

    def reset_extract_form(self):
        self.zip_file_path = ""
        self.extract_output_dir = ""
        self.extract_label.config(text="Select ZIP file to extract:")
        self.extract_output_label.config(text="Select Extraction Directory:")

    def reset_all(self):
        self.reset_form()
        self.reset_extract_form()
        self.files = []
        self.zip_file_path = ""
        self.output_dir = ""
        self.extract_output_dir = ""
        self.file_listbox.delete(0, tk.END)
        self.output_label.config(text="No directory selected")
        self.extract_label.config(text="Selected ZIP File: None")
        self.extract_output_label.config(text="Extraction Directory: None")
        self.compression_var.set("ZIP_DEFLATED")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ZipFileCreator(root)
    root.mainloop()
