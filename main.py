from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ExifTags
import os
import datetime


class WatermarkApp:
    def __init__(self, master):
        self.master = master
        master.title("Watermark App")

        self.image_label = Label(master, text="No image selected.")
        self.image_label.pack(pady=10)

        self.select_button = Button(master, text="Select Image", command=self.upload_image)
        self.select_button.pack(pady=10)

        self.add_button = Button(master, text="Add Watermark", state=DISABLED, command=self.add_watermark)
        self.add_button.pack(pady=10)

    def upload_image(self):
        self.directory = filedialog.askdirectory(title="Select a Directory")
        self.image_label.configure(text="Directory selected: " + self.directory)
        self.add_button.configure(state=NORMAL)

    def add_watermark(self):
        # Define font size based on screen resolution
        font_size = 30

        # Loop through all files in directory and subdirectories
        for subdir, dirs, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(subdir, file)

                # Check if file is an image
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image = Image.open(file_path)

                    # Get image dimensions
                    width, height = image.size

                    # Get image exif data
                    exif_data = image.getexif()

                    # Check if image has exif data
                    if exif_data:
                        try:
                            date_time = exif_data[306]
                        except:
                            date_time = None

                    if date_time:
                        watermark_text = date_time
                        font = ImageFont.truetype("arial.ttf", font_size)

                        draw = ImageDraw.Draw(image)
                        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
                        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

                        watermark = Image.new('RGBA', (text_width + font_size, text_height + font_size), (255, 255, 255, 0))
                        draw = ImageDraw.Draw(watermark)

                        draw.text((-text_bbox[0], -text_bbox[1]), watermark_text, font=font, fill=(255, 255, 255, 60))

                        watermark_pos = (width - text_width - font_size, height - text_height - font_size)
                        image.paste(watermark, watermark_pos, mask=watermark)

                        # Save image
                        save_file = os.path.join(subdir, os.path.splitext(file)[0] + "_watermarked.jpg")
                        image.save(save_file, "JPEG", quality=95)

                        self.image_label.configure(text="Watermark added. Image saved as: " + os.path.basename(save_file))

                    else:
                        self.image_label.configure(text="No EXIF data found. Watermark not added.")

        self.add_button.configure(state=DISABLED)


root = Tk()
my_gui = WatermarkApp(root)
root.mainloop()
