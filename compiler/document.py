# document.py
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Documentacion del Codigo Fuente', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(source_code, output_pdf):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Codigo Fuente:')
    pdf.chapter_body(source_code)
    pdf.output(output_pdf)

def read_source_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()
