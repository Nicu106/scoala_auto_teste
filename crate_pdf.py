from fpdf import FPDF

# Create a PDF document
pdf = FPDF()

# Add a page
pdf.add_page()

# Set font for the PDF (font, style, size)
pdf.set_font("Arial", 'B', 16)

# Add a title
pdf.cell(200, 10, txt="Hello Nicu!", ln=True, align='C')

# Add a subtitle
pdf.set_font("Arial", 'I', 12)
pdf.cell( 200, 10, txt="Test loren dorolor inpus", ln=True, align='C')

# Add some body text
pdf.set_font("Arial", '', 12)
pdf.multi_cell(0, 10, txt="Buna ce mai faci.")

# Save the PDF to a file
pdf.output("Dinu.pdf")

print("PDF created successfully!")