from flask import Flask, send_file, render_template_string
import os
import random
from fpdf import FPDF
from PIL import Image
import webbrowser

app = Flask(__name__)


# Define function to pick random files
def pick_random_files_from_each_directory(directory):
    selected_files = []
    for root, dirs, files in os.walk(directory):
        if files:
            num_files_to_select = random.randint(1, min(3, len(files)))
            # Check if we're in the specific folder
            if os.path.basename(root) == 'Dispozitii generale':
                num_files_to_select = 1
            if os.path.basename(root) == 'ACORDAREA PRIMULUI AJUTOR':
                num_files_to_select = 1
            if os.path.basename(root) == 'BAZELE COMPORTAMENTULUI iN CONDUCEREA AUTOVEHICULULUI':
                num_files_to_select = 1
            if os.path.basename(root) == 'circulatia in intersectii':
                num_files_to_select = 1
            if os.path.basename(root) == 'conditii tehnice':
                num_files_to_select = 1
            if os.path.basename(root) == 'circulatia vehiculelor':
                num_files_to_select = 1
            if os.path.basename(root) == 'depasirea si trecerea':
                num_files_to_select = 1
            if os.path.basename(root) == 'Drepturi si obligatii':
                num_files_to_select = 1  #
            if os.path.basename(root) == 'iNCEPUTUL DEPLASaRII sI SCHIMBAREA DIRECtIEI DE MERS':
                num_files_to_select = 1  #
            if os.path.basename(root) == 'Indicatoare rutiere':
                num_files_to_select = 3  #
            if os.path.basename(root) == 'Intersectiile drumurilor de semnificatie echivalenta':
                num_files_to_select = 1
            if os.path.basename(root) == 'Intersectiile drumurilor de semnificatie neechivalenta':
                num_files_to_select = 1
            if os.path.basename(root) == 'Intersectiile in care drumul cu prioritate isi schimba directia':
                num_files_to_select = 1
            if os.path.basename(root) == 'Marcaje rutiere':
                num_files_to_select = 1
            if os.path.basename(root) == 'OPRIREA sl STAtIONAREA VOLUNTARa. PARCAREA':
                num_files_to_select = 1
            if os.path.basename(root) == 'remorcarea vehiculelor':
                num_files_to_select = 1
            if os.path.basename(root) == 'Semnale Luminoase':
                num_files_to_select = 1
            if os.path.basename(root) == 'viteza de deplasare':
                num_files_to_select = 1
            if os.path.basename(root) == 'cIRCULAtIA BICICLETELOR, TROTINETELOR, BICICLETELOR sI TROTINETELOR ELECTRICE':
                num_files_to_select = 1
            if os.path.basename(root) == 'Semnalele Conducatorului':
                num_files_to_select = 1
            if os.path.basename(root) == 'REGULI PRIVIND CIRCULAtIA VEHICULELOR CU REGIM PRIORITAR DE CIRCULAtIE sI OBLIGAtIILE CELORLALtI CONDUCaTORI DE VEHICULE':
                num_files_to_select = 1
#
            random_files = random.sample(files, num_files_to_select)
            for file in random_files:
                if len(selected_files) <= 24:
                    selected_files.append(os.path.join(root, file))
                else:
                    break
            if len(selected_files) >= 24:
                break
    return selected_files


# Define PDF class
class PDF(FPDF):
    def get_image_size(self, img_path):
        with Image.open(img_path) as img:
            return img.size

    def scale_image(self, img_w, img_h, max_w, max_h):
        scale_factor = min(max_w / img_w, max_h / img_h)
        return img_w * scale_factor, img_h * scale_factor

    def add_images(self, images, imgs_per_page=6, max_pages=4):
        page_count = 1
        max_w = self.w - 20
        max_h = (self.h - 50) / 6
        y = 0
        if page_count != 1:
            y = 80

        for i, img in enumerate(images):
            if page_count > max_pages:
                break
            if i % imgs_per_page == 0 and i != 0:
                self.add_page()
                page_count += 1
                y = 10
            if page_count > max_pages:
                break
            img_w, img_h = self.get_image_size(img)
            scaled_w, scaled_h = self.scale_image(img_w, img_h, max_w, max_h)
            x = (self.w - scaled_w) / 2
            self.image(img, x=x, y=y, w=scaled_w, h=scaled_h)
            y += scaled_h + 5


@app.route('/')
def index():
    # HTML template with Bootstrap and centered button
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aplicatie pentru scoala auto - Viore Chircu</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-14Kw+xZt8nb7jxLTr24fdr92y0p5Qw1yTqBO8d0R5JHcvfZcIEih8O6mg2q1cExT" crossorigin="anonymous">
        <style>
            body, html {
                height: 100%;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f7f7f7;
                font-family: 'Arial', sans-serif;
            }
            .container {
                text-align: center;
                background-color: #fff;
                padding: 50px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            h1 {
                font-size: 2rem;
                margin-bottom: 30px;
                color: #343a40;
            }
            button {
                padding: 15px 30px;
                font-size: 1.2rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Generare Școala Auto - Viorel Chircu</h1>
            <form action="/download_pdf" method="get">
                <button class="btn btn-primary" type="submit">Descarcǎ PDF</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)


@app.route('/download_pdf')
def download_pdf():
    directory_path = 'scoala'  # Replace with your directory
    random_files = pick_random_files_from_each_directory(directory_path)

    if not random_files:
        return "Error: No files to include in the PDF!"

    # Generate the PDF
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_images(random_files)

    pdf_file = 'generated_pdf.pdf'
    pdf.output(pdf_file)

    # Send the file to the user
    response = send_file(pdf_file, as_attachment=True)

    # Delete the file after sending
    @response.call_on_close
    def delete_file():
        os.remove(pdf_file)

    return response


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == '__main__':
    # Open the web browser when the app starts
    open_browser()

    # Run the Flask app
    app.run(debug=False)