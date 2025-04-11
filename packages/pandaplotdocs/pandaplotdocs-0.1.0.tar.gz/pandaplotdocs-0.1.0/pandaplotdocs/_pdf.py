import textwrap

FPDF_AVAILABLE = False
try:
    from fpdf import FPDF, HTMLMixin
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

#generate pdf
class PDF(FPDF):
    """Custom PDF class with header and footer."""
    def header(self):
        self.set_font('helvetica', 'B', 12)
        title = 'Essential Pandas & Matplotlib Reference'
        title_w = self.get_string_width(title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.cell(title_w, 10, title, border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, ln=1, fill=1, align='L')
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 10)
        self.multi_cell(0, 5, text)
        self.ln()

    def add_entry_heading(self, text):
        self.set_font('courier', 'B', 11)
        self.cell(0, 6, text, ln=1)
        self.ln(1)

    def add_entry_section_title(self, text):
         self.set_font('helvetica', 'B', 10)
         self.cell(0, 5, text, ln=1)

    def add_entry_code(self, text):
         self.set_font('courier', '', 9)
         self.set_fill_color(245, 245, 245)
         self.multi_cell(0, 4.5, text, border=0, fill=1)
         self.ln(1)

    def add_entry_desc(self, text):
        self.set_font('helvetica', '', 9)
        lines = text.split('\n')
        for line in lines:
            wrapped_lines = textwrap.wrap(line, width=110)
            if not wrapped_lines:
                self.ln(3)
                continue
            for wrapped_line in wrapped_lines:
                 self.cell(5)
                 self.cell(0, 4.5, wrapped_line, ln=1)
        self.ln(1)


#PDF Formatting

def add_doc_entry_pdf(pdf, entry):
    """
    Formats and writes a single documentation entry to the PDF object.

    Args:
        pdf: The FPDF object.
        entry: A dictionary containing 'name', 'prefix', 'sig', 'desc', 'example'.
    """
    #Handle cases where entry incomplete
    name = entry.get('name', 'Unknown Function')
    prefix = entry.get('prefix', '')
    sig_hint = entry.get('sig', '(...)')
    desc = entry.get('desc', 'No description available.')
    example = entry.get('example', None)

    full_name = f"{prefix}{name}"

    y_before = pdf.get_y()
    est_height = 10 # Heading
    est_height += (len(f"{prefix}{sig_hint}") // 80 + 1) * 5 + 5 # Signature
    est_height += (len(desc) // 100 + desc.count('\n') + 1) * 5 + 5 # Description
    if example:
        est_height += (len(example) // 80 + example.count('\n') + 1) * 5 + 5 # Example

    # Check if fits on page
    if y_before + est_height > pdf.h - pdf.b_margin:
        pdf.add_page()

    #Write Heading
    pdf.add_entry_heading(full_name)

    #Write Signature Hint
    pdf.add_entry_section_title("Usage:")
    # Use textwrap for longer signatures
    wrapped_sig = textwrap.fill(
        f"{prefix}{sig_hint}",
        width=85, initial_indent="", subsequent_indent="  " # Indent subsequent lines
    )
    pdf.add_entry_code(wrapped_sig)

    #Write Description
    pdf.add_entry_section_title("Description:")
    pdf.add_entry_desc(desc)

    # Write Example
    if example: # Check if example exists
        pdf.add_entry_section_title("Example:")
        pdf.add_entry_code(example)

    # Add spacing between the entries
    pdf.ln(5) 