import fitz

def extract_highlights(pdf_path):
    doc = fitz.open(pdf_path)
    highlights = []

    for page_num, page in enumerate(doc):
        for annot in page.annots():
            if annot.type[0] == 8:  # Highlight
                text = annot.info.get("content", "").strip() or page.get_textbox(annot.rect).strip()
                color = annot.colors.get("stroke", (1, 1, 0))  # default yellow
                highlights.append({
                    "page": page_num + 1,
                    "text": text,
                    "color": color
                })
    return highlights
