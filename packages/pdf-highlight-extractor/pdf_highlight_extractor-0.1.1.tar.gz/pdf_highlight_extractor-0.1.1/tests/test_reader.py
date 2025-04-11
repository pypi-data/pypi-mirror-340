import fitz  # PyMuPDF

def extract_highlights(pdf_path):
    """
    Extract highlights from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list[dict]: List of highlight dictionaries with keys:
                    - 'page': Page number (1-indexed)
                    - 'text': Highlighted text
                    - 'color': RGB color tuple
    """
    doc = fitz.open(pdf_path)
    highlights = []

    for page_num, page in enumerate(doc):
        if page.annots():
            for annot in page.annots():
                if annot.type[0] == 8:  # 8 = Highlight annotation
                    text = annot.info.get("content", "").strip()

                    # If no text content stored in the annotation, try extracting it from the rect
                    if not text:
                        quadpoints = annot.vertices
                        quads = [quadpoints[i:i+4] for i in range(0, len(quadpoints), 4)]
                        text_fragments = [page.get_textbox(fitz.Quad(quad).rect) for quad in quads]
                        text = " ".join(t.strip() for t in text_fragments if t.strip())

                    # Get color; default to yellow if not available
                    color = annot.colors.get("stroke", (1.0, 1.0, 0.0))

                    highlights.append({
                        "page": page_num + 1,
                        "text": text,
                        "color": tuple(round(c, 3) for c in color)  # rounding for consistency
                    })

    doc.close()
    return highlights

print(extract_highlights("sample.pdf"))