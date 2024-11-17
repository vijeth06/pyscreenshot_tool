import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
import os
from datetime import datetime
import pyscreenshot as ImageGrab


def capture_full_screen(save_path):
    """Captures the entire screen and saves the screenshot."""
    screenshot = ImageGrab.grab()
    screenshot.save(save_path)
    print(f"Screenshot saved as {save_path}")
    return screenshot

def capture_region(save_path, bbox):
    """Captures a specific region of the screen and saves the screenshot."""
    screenshot = ImageGrab.grab(bbox=bbox)
    screenshot.save(save_path)
    print(f"Screenshot of region {bbox} saved as {save_path}")
    return screenshot

def get_save_path(custom_name=None):
    """Generates a filename for the screenshot."""
    if not custom_name:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    else:
        filename = f"{custom_name}.png"
    save_path = os.path.join(os.getcwd(), filename)
    return save_path


class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Capture Tool")
        self.root.geometry("500x450")
        self.root.resizable(True, True)  

       
        self.style = ttk.Style()
        self.style.theme_use('clam')  
        
        self.style.configure('GreenButton.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#4CAF50', borderwidth=1)
        self.style.map('GreenButton.TButton', background=[('active', '#388E3C')])  

        self.style.configure('Quit.TButton', font=('Arial', 10, 'bold'), foreground='white', background='red', borderwidth=1)
        self.style.map('Quit.TButton', background=[('active', '#B71C1C')])  

        self.style.configure('ConfirmButton.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#FF9800', borderwidth=1)
        self.style.map('ConfirmButton.TButton', background=[('active', '#F57C00')])  

        self.root.configure(bg='#e0e0e0')  

        self.custom_name = tk.StringVar()

       
        self.title_label = ttk.Label(root, text="Screenshot Capture Tool", font=("Arial", 20, "bold"), background='#e0e0e0', foreground='#37474F')
        self.title_label.pack(pady=15)

        self.custom_name_label = ttk.Label(root, text="Custom Filename (Optional):", background='#e0e0e0', foreground='#37474F')
        self.custom_name_label.pack(pady=5)
        self.custom_name_entry = ttk.Entry(root, textvariable=self.custom_name, width=40)
        self.custom_name_entry.pack(pady=5)

        self.full_screen_button = ttk.Button(root, text="📷 Capture Full Screen", command=self.capture_full_screen_gui, style='GreenButton.TButton')
        self.full_screen_button.pack(pady=12)

        self.region_button = ttk.Button(root, text="📐 Capture Specific Region", command=self.capture_region_gui, style='GreenButton.TButton')
        self.region_button.pack(pady=12)

        self.view_button = ttk.Button(root, text="🖼️ View Last Screenshot", command=self.view_screenshot_gui, style='GreenButton.TButton')
        self.view_button.pack(pady=12)

        self.quit_button = ttk.Button(root, text="❌ Quit", command=root.quit, style='Quit.TButton')
        self.quit_button.pack(pady=15)

        self.last_screenshot_path = None

    def capture_full_screen_gui(self):
        """Handles full screen capture through the GUI."""
        save_path = get_save_path(self.custom_name.get().strip())
        capture_full_screen(save_path)
        self.last_screenshot_path = save_path
        messagebox.showinfo("Screenshot Saved", f"Full screen screenshot saved as {save_path}")
        self.update_view_button()  

    def capture_region_gui(self):
        """Handles region capture through the GUI."""
        try:
            coord_window = tk.Toplevel(self.root)
            coord_window.title("Enter Region Coordinates")
            coord_window.geometry("350x400")
            coord_window.resizable(False, False)
            coord_window.configure(bg='#f5f5f5')

            coord_vars = {
                "left": tk.IntVar(),
                "top": tk.IntVar(),
                "right": tk.IntVar(),
                "bottom": tk.IntVar(),
            }

            ttk.Label(coord_window, text="Left:", background='#f5f5f5').pack(pady=5)
            ttk.Entry(coord_window, textvariable=coord_vars["left"]).pack(pady=5)
            ttk.Label(coord_window, text="Top:", background='#f5f5f5').pack(pady=5)
            ttk.Entry(coord_window, textvariable=coord_vars["top"]).pack(pady=5)
            ttk.Label(coord_window, text="Right:", background='#f5f5f5').pack(pady=5)
            ttk.Entry(coord_window, textvariable=coord_vars["right"]).pack(pady=5)
            ttk.Label(coord_window, text="Bottom:", background='#f5f5f5').pack(pady=5)
            ttk.Entry(coord_window, textvariable=coord_vars["bottom"]).pack(pady=5)

            def on_confirm():
                try:
                    left = coord_vars["left"].get()
                    top = coord_vars["top"].get()
                    right = coord_vars["right"].get()
                    bottom = coord_vars["bottom"].get()

                    if right <= left or bottom <= top:
                        messagebox.showerror("Error", "Invalid coordinates. Please enter valid values.")
                        return

                    bbox = (left, top, right, bottom)
                    save_path = get_save_path(self.custom_name.get().strip())
                    capture_region(save_path, bbox)
                    self.last_screenshot_path = save_path
                    messagebox.showinfo("Screenshot Saved", f"Region screenshot saved as {save_path}")
                    self.update_view_button()  
                    coord_window.destroy()  
                except ValueError:
                    messagebox.showerror("Error", "Please enter numeric values.")

            confirm_button = ttk.Button(coord_window, text="Confirm", command=on_confirm, style='ConfirmButton.TButton')
            confirm_button.pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_screenshot_gui(self):
        """Displays the last captured screenshot if available."""
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            try:
                img = Image.open(self.last_screenshot_path)
                img.show()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display screenshot: {e}")
        else:
            messagebox.showinfo("No Screenshot", "No screenshot is available to view.")

    def update_view_button(self):
        """Update the text of the view button to show if a screenshot is available."""
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            self.view_button.config(text="🖼️ View Last Screenshot")
        else:
            self.view_button.config(text="🖼️ No Screenshot to View")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
