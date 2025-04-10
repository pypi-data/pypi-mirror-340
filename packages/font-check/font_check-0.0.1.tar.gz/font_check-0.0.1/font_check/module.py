import os
import shutil
import sys
from PIL import Image, ImageDraw, ImageFont
import pkg_resources

class FontRendererKh:
    def __init__(self, font_path, data_file="data/data.txt", output_folder="performance",
                 image_width=800, image_height=100, font_size=48, columns=2):
        self.font_path = font_path  # Keep the real font path passed in
        self.data_file = pkg_resources.resource_filename('font_check', data_file)
        self.output_folder = output_folder
        self.image_width = image_width
        self.image_height = image_height
        self.font_size = font_size
        self.columns = min(columns, 5)  # Allow up to 5 columns
        if columns > 5:
            print("Warning: Maximum allowed columns is 5. Setting columns = 5.")
        self.font = self.load_font()
        self.image_cache = []  # Keep images in memory (no saving small files)

    def load_font(self):
        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
            return font
        except Exception as e:
            print(f"Error loading font: {e}")
            sys.exit(1)

    def create_image(self, text):
        image = Image.new("RGB", (self.image_width, self.image_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Use textbbox to calculate width and height
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (self.image_width - text_width) / 2
        y = (self.image_height - text_height) / 2

        # Draw the text
        draw.text((x, y), text, font=self.font, fill=(0, 0, 0))

        # Add a border
        border_color = (0, 0, 0)  # Black
        border_thickness = 2
        for i in range(border_thickness):
            draw.rectangle(
                [i, i, self.image_width - 1 - i, self.image_height - 1 - i],
                outline=border_color
            )

        return image

    def combine_images(self):
        if not self.image_cache:
            print("No images to combine.")
            return

        count = len(self.image_cache)
        columns = self.columns
        rows = (count + columns - 1) // columns  # ceil(count / columns)

        # Assume all images same size
        cell_width = self.image_width
        cell_height = self.image_height

        combined_width = columns * cell_width
        combined_height = rows * cell_height
        combined_image = Image.new('RGB', (combined_width, combined_height), color=(255, 255, 255))

        for idx, img in enumerate(self.image_cache):
            row = idx // columns
            col = idx % columns
            x = col * cell_width
            y = row * cell_height
            combined_image.paste(img, (x, y))

        # Save combined image
        output_path = os.path.join(self.output_folder, "img_render_visualize.jpg")
        combined_image.save(output_path)
        print(f"Combined image saved at: {output_path}")

    def render_all(self):
        print(f"Reading from: {self.data_file}")
        if not os.path.exists(self.data_file):
            print(f"{self.data_file} not found.")
            sys.exit(1)

        os.makedirs(self.output_folder, exist_ok=True)

        # Copy data.txt into performance/
        target_data_file = os.path.join(self.output_folder, "data.txt")
        shutil.copy(self.data_file, target_data_file)
        print(f"Copied data.txt to {target_data_file}")

        with open(self.data_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            text = line.strip()
            if text:
                img = self.create_image(text)
                self.image_cache.append(img)

        # After all images are created, combine and save
        self.combine_images()
