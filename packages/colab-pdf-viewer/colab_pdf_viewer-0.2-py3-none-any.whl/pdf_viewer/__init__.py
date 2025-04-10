import requests
import io
import base64
from pdf2image import convert_from_bytes
from IPython.display import HTML, display

def display_scrollable_pdf_from_url(url, width=800, height=450):
    """
    Display a PDF file from a GitHub raw URL (or any direct PDF URL) inside a scrollable
    fixed-size box within a Jupyter Notebook or Google Colab.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_bytes = response.content

        images = convert_from_bytes(pdf_bytes)

        img_tags = []
        for img in images:
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            img_tag = f'<img src="data:image/png;base64,{img_base64}" style="width:100%; margin-bottom:10px;" />'
            img_tags.append(img_tag)

        html_code = f"""
        <div style="width:{width}px; height:{height}px; overflow:auto; border:1px solid #ccc;
                    padding:10px; border-radius:8px;">
            {''.join(img_tags)}
        </div>
        """
        display(HTML(html_code))

    except Exception as e:
        display(HTML(f"<div style='color:red;'>Error loading PDF: {e}</div>"))
