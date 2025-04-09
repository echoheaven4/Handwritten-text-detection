import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'])

class TextRecognizer:
    def __init__(self, master):
        self.master = master

        self.canvas = tk.Canvas(master, width=600, height=200, bg='white')
        self.canvas.pack()
        self.canvas.bind('<B1-Motion>', self.paint)

        self.button_predict_draw = tk.Button(master, text='Predict Drawn Input', command=self.predict_drawn_input)
        self.button_predict_draw.pack()

        self.button_insert_image = tk.Button(master, text='Insert Image', command=self.insert_image)
        self.button_insert_image.pack()

        self.button_clear = tk.Button(master, text='Clear', command=self.clear)
        self.button_clear.pack()

        self.button_increase_size = tk.Button(master, text='Increase Marker Size', command=self.increase_marker_size)
        self.button_increase_size.pack()

        self.button_decrease_size = tk.Button(master, text='Decrease Marker Size', command=self.decrease_marker_size)
        self.button_decrease_size.pack()

        self.image = Image.new('L', (600, 200), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.marker_size = 12

        # Text widget to display output
        self.text_output = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=10, font=('Arial', 12))
        self.text_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def paint(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval((x - self.marker_size//2, y - self.marker_size//2,
                                 x + self.marker_size//2, y + self.marker_size//2), 
                                 fill='black', width=0)
        self.draw.ellipse((x - self.marker_size//2, y - self.marker_size//2, 
                           x + self.marker_size//2, y + self.marker_size//2), fill='black')

    def clear(self):
        self.canvas.delete('all')
        self.image = Image.new('L', (600, 200), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def preprocess_image(self, image):
        # Convert image to grayscale and invert colors
        image = image.convert('L')
        image = ImageOps.invert(image)
        image_array = np.array(image).astype('uint8')
        return image_array

    def predict_drawn_input(self):
        try:
            # Preprocess the drawn image
            image_array = self.preprocess_image(self.image)

            # Predict
            result = reader.readtext(image_array)
            text = ' '.join([res[1] for res in result]) if result else "No text detected"

            # Display result in text widget
            self.text_output.delete(1.0, tk.END)  # Clear previous content
            self.text_output.insert(tk.END, f"Predicted text: {text}\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def insert_image(self):
        try:
            # Open file dialog to choose an image
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
            if file_path:
                image = Image.open(file_path).convert('L')
                image_array = self.preprocess_image(image)

                # Predict
                result = reader.readtext(image_array)
                text = ' '.join([res[1] for res in result]) if result else "No text detected"

                # Display result in text widget
                self.text_output.delete(1.0, tk.END)  # Clear previous content
                self.text_output.insert(tk.END, f"Predicted text: {text}\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def increase_marker_size(self):
        self.marker_size += 2

    def decrease_marker_size(self):
        if self.marker_size > 2:
            self.marker_size -= 2

# Initialize Tkinter and the GUI
root = tk.Tk()
root.title('Text Recognizer')
app = TextRecognizer(root)
root.mainloop()
