import PyPDF2

# Open the PDF file
with open('./assets/mit-lesson-plan-template-fillable.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    fields = reader.get_form_text_fields()
    print(fields)
