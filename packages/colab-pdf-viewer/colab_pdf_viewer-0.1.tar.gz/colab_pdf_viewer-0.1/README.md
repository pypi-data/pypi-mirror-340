# colab-pdf-viewer

A simple utility to display PDFs as scrollable images inside a fixed-size box in Google Colab or Jupyter Notebook.

## Install (future pip)

Coming soon...

## Usage (inside Colab)

```python
from pdf_viewer import display_scrollable_pdf_from_url

display_scrollable_pdf_from_url(
    "https://raw.githubusercontent.com/your_username/your_repo/main/example.pdf",
    width=800,
    height=450
)

---

### 4. Commit 初始內容

```bash
git add .
git commit -m "Initial commit: PDF viewer module"
