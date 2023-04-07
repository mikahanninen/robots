import pdfkit

def html2pdf(filename, outfile):
    options = {
        "enable-local-file-access": None
    }
    pdfkit.from_file(filename, outfile, options=options)