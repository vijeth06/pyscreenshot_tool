import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageGrab, Image
import os
from datetime import datetime
import time


def sanitize_filename(filename):
    """Sanitize filename by removing invalid characters."""
    import re
    return re.sub(r'[\\/*?:"<>|]', "", filename)


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
        filename = sanitize_filename(f"{custom_name}.png")
    return os.path.join(os.getcwd(), filename)


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
        self.selection_box = None

    def capture_full_screen_gui(self):
        """Handles full screen capture through the GUI."""
        try:
            self.root.withdraw() 
            time.sleep(0.5)  
            save_path = get_save_path(self.custom_name.get().strip())
            capture_full_screen(save_path)
            self.root.deiconify()  
            self.last_screenshot_path = save_path
            messagebox.showinfo("Screenshot Saved", f"Full screen screenshot saved as {save_path}")
            self.update_view_button()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot: {e}")
            self.root.deiconify()

    def capture_region_gui(self):
        """Handles region capture through the GUI using mouse drag."""
        try:
            self.root.withdraw()  
            self.root.after(500, self.start_capture_region)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.root.deiconify()

    def start_capture_region(self):
        """Starts the region capture using a transparent overlay."""
        self.selection_box = None
        self.capture_window = tk.Toplevel(self.root)
        self.capture_window.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.capture_window.attributes("-topmost", True)
        self.capture_window.overrideredirect(True)
        self.capture_window.attributes("-alpha", 0.3)  
        self.capture_window.configure(bg='black')

        self.canvas = tk.Canvas(self.capture_window, cursor="cross", bg='black', bd=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        """Handles mouse press to start selecting region."""
        self.start_x = event.x
        self.start_y = event.y
        self.selection_box = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_drag(self, event):
        """Handles mouse drag to resize the selection rectangle."""
        self.canvas.coords(self.selection_box, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        """Handles mouse release to finalize region selection and capture screenshot."""
        end_x = event.x
        end_y = event.y
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        right = max(self.start_x, end_x)
        bottom = max(self.start_y, end_y)

        self.capture_window.destroy()  

        if right <= left or bottom <= top:
            messagebox.showerror("Error", "Invalid coordinates. Please select a valid region.")
            self.root.deiconify()
            return

        save_path = get_save_path(self.custom_name.get().strip())
        capture_region(save_path, (left, top, right, bottom))
        self.last_screenshot_path = save_path
        messagebox.showinfo("Screenshot Saved", f"Region screenshot saved as {save_path}")
        self.update_view_button()

        self.root.deiconify()  

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
