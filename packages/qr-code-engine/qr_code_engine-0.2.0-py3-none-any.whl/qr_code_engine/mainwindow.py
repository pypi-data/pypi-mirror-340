import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from tkinter import ttk

from .subwindow.multitextwindow import MultiTextWindow
from .logic.qrcodegenerator import QRCodeGenerator

#Custom Tkinter Theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MainWindow(ctk.CTk):
	def __init__(self, title:str, size, minsize):
		super().__init__()
		self.title(title)  
		self.geometry(f"{size[0]}x{size[1]}")  
		self.minsize(minsize[0], minsize[1])
		self.maingui()
		self.footer()
		self.mainloop()
	
	# Main Widget
	def maingui(self):
		# Row 0
		label_scan = ctk.CTkLabel(self, text="ENTER QR CODE :")
		label_scan.grid(row=0, column=0, padx=20, pady=20, sticky='w')
		self.entry_qr_code = ctk.CTkTextbox(self, width=300, height=80, bg_color="transparent", border_width=2)
		self.entry_qr_code.grid(row=0, column=1, padx=10, pady=20)

		# MultiText Window Class instance creation
		self.multitext_editor = MultiTextWindow(self, self.entry_qr_code)

		# Bind the double-click event to the TextEditor's open_editor method
		self.entry_qr_code.bind("<Double-1>", self.multitext_editor.open_editor)

		# Row 1
		label_remark = ctk.CTkLabel(self, text="REMARK ( OPTIONAL ) :")
		label_remark.grid(row=1, column=0, padx=20, pady=10, sticky='w')
		self.entry_remark = ctk.CTkEntry(self, width=300)
		self.entry_remark.grid(row=1, column=1, padx=20, pady=10)

		# Row 3
		self.savelocation()

	def savelocation(self):
		self.output_location_path = ""  
		browse_button = ctk.CTkButton(self, text="Browse Location", command=lambda: self.browse_folder())
		browse_button.grid(row=2, column=0, padx=20, pady=10, sticky='w')

		self.save_entry = ctk.CTkEntry(self, width=300, font=("Arial", 12))
		self.save_entry.grid(row=2, column=1, padx=20, pady=10, sticky='e')

	def browse_folder(self):
		selected_folder = filedialog.askdirectory()
		if selected_folder:
			self.output_location_path = selected_folder  
			self.save_entry.delete(0, tk.END)
			self.save_entry.insert(0, selected_folder)
			print(f"output location is {self.output_location_path}") 
			

	def get_output_location(self): 
		return self.output_location_path

	def footer(self):			
		# Generate 

		self.logic_add = QRCodeGenerator(self.entry_qr_code, self.save_entry, self.entry_remark)

		
		generate = ctk.CTkButton(self, text="GENERATE", width=300, height=40, command=self.logic_add.generate_qr_code)
		generate.grid(row=3, column=1, padx=10, pady=20)

		footer_label = ctk.CTkLabel(self, text="github.com/abyshergill/QR_Code_Generator")
		footer_label.grid(row=4, column=1, padx=20, pady=20, sticky='nsew')


def run_app():
    app = MainWindow("QR Code Engine", (530,300), (100,200) )
    app.mainloop()
		

	