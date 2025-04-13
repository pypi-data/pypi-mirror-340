import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tkinter import messagebox
import qrcode
import os



class QRCodeGenerator:
    def __init__(self, input_widget, save_path_widget, remarks_widget=None):
        self.input_widget = input_widget
        self.save_path_widget = save_path_widget
        self.remarks_widget = remarks_widget

    def generate_qr_code(self):
        input_text = self.input_widget.get("1.0", "end-1c").strip()
        save_path_str = self.save_path_widget.get().strip()
        remarks = self.remarks_widget.get().strip() if self.remarks_widget else ""
        
        if input_text and save_path_str:
            lines = input_text.splitlines()
            remarks_lines = remarks.splitlines() if remarks else []

            for i, line in enumerate(lines):
                # Generate the QR save path for each line
                qr_save_path = os.path.splitext(save_path_str)[0] + f"_image{i + 1}.jpg"
                
                # Determine the remark for the current line
                remark = remarks_lines[min(i, len(remarks_lines) - 1)] if remarks_lines else None

                # Create the combined text for the QR code
                qr_text = f"{line} - Remark: {remark}" if remark else line

                try:
                    # Generate QR Code
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(qr_text)  # Use qr_text here instead of input_text
                    qr.make(fit=True)

                    img = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))  

                    img = img.convert('RGB')

                    # Add space for text below the image
                    width, height = img.size
                    new_img = Image.new('RGB', (width, height + 50), 'white')
                    new_img.paste(img, box=(0, 0, width, height))  
                    draw = ImageDraw.Draw(new_img)

                    # Load font
                    try:
                        font = ImageFont.truetype("arial.ttf", 16)
                    except FileNotFoundError:
                        font = ImageFont.load_default()

                    # For QR code text
                    draw.text((10, height + 5), f'QR Code: {line}', fill='black', font=font)
                    
                    # For remark text
                    draw.text((10, height + 25), f'Remark: {remark}' if remark else 'No Remark', fill='black', font=font)

                    # Save the image
                    if os.path.isdir(save_path_str):
                        qr_save_path = os.path.join(save_path_str, f"image_{i + 1}.png")  

                    new_img.save(qr_save_path)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save QR code for line {i + 1}: {e}")
                    return  # Stop processing on error

            messagebox.showinfo("Success", f'QR Codes saved at: {os.path.dirname(qr_save_path)}')
            self.input_widget.delete("1.0", tk.END)  # Clear multiline entry
            self.remarks_widget.delete(0, tk.END)
            self.save_path_widget.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter text and select a save location for the QR codes.")

 