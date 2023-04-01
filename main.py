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
        self.filename = filedialog.askopenfilename(title="Select an Image",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.image = Image.open(self.filename)
        self.image_label.configure(text="Image selected: " + os.path.basename(self.filename))
        self.add_button.configure(state=NORMAL)

    def add_watermark(self):
        # Get image dimensions
        global date_time
        width, height = self.image.size

        # Get image exif data
        exif_data = self.image.getexif()

        # Check if image has exif data
        if exif_data:
            try:
                date_time = exif_data[306]
            except:
                date_time = None

        if date_time:
            watermark_text = date_time
            font = ImageFont.truetype("arial.ttf", int(width * 0.03))

            # Create watermark image with appropriate size
            text_bbox = ImageDraw.Draw(self.image).textbbox((0, 0), watermark_text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            watermark = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))

            draw = ImageDraw.Draw(watermark)
            draw.text((0, 0), watermark_text, font=font, fill=(255, 255, 255, 60))

            watermark_pos = (width - text_width, height - 2 * text_height)
            self.image.paste(watermark, watermark_pos, mask=watermark)

            # Save image
            save_file = os.path.join(os.path.dirname(self.filename),
                                     os.path.splitext(os.path.basename(self.filename))[0] + "_watermarked.jpg")
            self.image.save(save_file, "JPEG", quality=95)

            self.add_button.configure(state=DISABLED)
            self.image_label.configure(text="Watermark added. Image saved as: " + os.path.basename(save_file))

        else:
            self.image_label.configure(text="No EXIF data found. Watermark not added.")


root = Tk()
my_gui = WatermarkApp(root)
root.mainloop()
