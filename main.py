import os
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
from fpdf import FPDF
from PIL import Image  # Pillow library to get image dimensions


def pick_random_files_from_each_directory(directory):
    selected_files = []
    # Iterate through each folder
    for root, dirs, files in os.walk(directory):
        if files:
            # Randomly decide how many files to select from this folder (between 1 and min(3, number of files))
            num_files_to_select = random.randint(1, min(3, len(files)))

            # Check if we're in the specific folder
            if os.path.basename(root) == 'Dispozitii generale':
                num_files_to_select = 1
            if os.path.basename(root) == 'Dispozitii generale':
                    num_files_to_select = 1

            # Randomly pick that number of files from the current folder
            random_files = random.sample(files, num_files_to_select)

            # Add the selected files with their full path to the list
            for file in random_files:
                if len(selected_files) <= 24:  # Check if we can still add files
                    selected_files.append(os.path.join(root, file))
                else:
                    break  # Stop if we already have 24 files
            if len(selected_files) >= 24:  # Exit the loop if we've selected 24 files
                break

    return selected_files


# Specify the directory you want to iterate through
directory_path = 'scoala'

# Get the randomly selected files from each directory
random_files = pick_random_files_from_each_directory(directory_path)

class PDF(FPDF):
    def get_image_size(self, img_path):
        with Image.open(img_path) as img:
            return img.size  # returns (width, height)

    def scale_image(self, img_w, img_h, max_w, max_h):
        # Calculate the scaling factor to fit the image within max_w and max_h
        scale_factor = min(max_w / img_w, max_h / img_h)
        return img_w * scale_factor, img_h * scale_factor

    def add_images(self, images, imgs_per_page=6, max_pages=4):
        page_count = 1
        max_w = self.w - 20  # Max width for each image (account for margins)
        max_h = (self.h - 50) / 6  # Max height for each image (6 rows per page)
        y= 0
        if(page_count != 1 ): y = 80 # Starting y-coordinate for placing images

        for i, img in enumerate(images):
            # Stop adding images if we've reached the max number of pages
            if page_count > max_pages:
                break

            # If necessary, start a new page
            if i % imgs_per_page == 0 and i != 0:
                self.add_page()
                page_count += 1
                y = 10  # Reset y for the next page

            if page_count > max_pages:
                break  # Exit the loop if we exceed the max page count

            # Get the original image size
            img_w, img_h = self.get_image_size(img)

            # Scale the image to fit within the available space
            scaled_w, scaled_h = self.scale_image(img_w, img_h, max_w, max_h)

            # Center the image on the page by calculating the x-coordinate
            x = (self.w - scaled_w) / 2  # Center the image horizontally

            # Place the image on the PDF
            self.image(img, x=x, y=y, w=scaled_w, h=scaled_h)
            y += scaled_h + 5  # Move y down for the next image (5 points of spacing)

        # Add spacing between the last image and the bottom of the page for the first page
        if page_count == 1:  # Only for the first page
            y += 15  # Add 15 points of spacing (adjust as needed)


# List of image paths (replace with actual paths)
images = random_files

# Create a PDF object
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Add the images to the PDF, scaled to fit 1 per row and 6 per column (6 per page across 4 pages)
pdf.add_images(images)

# Output the PDF to a file
pdf.output('test.pdf')
