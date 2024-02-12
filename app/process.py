from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  

# HTML-tiedosto PDF-tiedostoksi
def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     if html is not None:
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding='utf-8')
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf; charset=utf-8')
        return None