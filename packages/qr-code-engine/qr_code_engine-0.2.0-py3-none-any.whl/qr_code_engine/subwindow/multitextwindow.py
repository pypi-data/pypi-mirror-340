import tkinter as tk
import customtkinter as ctk


class MultiTextWindow:
    def __init__(self, root, target):
        self.root = root
        self.target = target
        self.editor_window = None

    def open_editor(self, event=None):
        if self.editor_window is not None and self.editor_window.winfo_exists():
            self.editor_window.lift()
            return
       
        self.editor_window = ctk.CTkToplevel(self.root)
        self.editor_window.title("Enter Text for QR Code")
        self.editor_window.geometry("360x320")
        self.editor_window.resizable(False, False)
        self.editor_window.configure(bg="#E6F7FF")

        text_editor = ctk.CTkTextbox(self.editor_window, width=320, height=250, border_width=2)
        text_editor.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
		
		# Freeze the main window
        self.editor_window.grab_set()  
        def on_ok():
            text = text_editor.get("1.0", tk.END).strip()
            if text:
                self.target.delete("1.0", ctk.END) 
                self.target.insert(ctk.END, text)
			#Unfreeze the main window	
            self.editor_window.grab_release() 
            self.editor_window.destroy()
            
            #self.root.deiconify()  # Show the main window again
        
        def on_cancel():
			#Unfreeze the main window
            self.editor_window.grab_release() 
            self.editor_window.destroy()

			
        ok_button = ctk.CTkButton(self.editor_window, text="OK", command=on_ok)
        ok_button.grid(row=1, column=0, padx=20, pady=20)

        cancel_button = ctk.CTkButton(self.editor_window, text="Cancel", command=on_cancel)
        cancel_button.grid(row=1, column=1, padx=20, pady=20)
        self.editor_window.protocol("WM_DELETE_WINDOW", on_cancel)