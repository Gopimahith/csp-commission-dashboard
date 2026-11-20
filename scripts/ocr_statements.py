"""Step 1: turn scanned commission-statement PDFs into text.

Usage:  python scripts/ocr_statements.py <folder_with_pdfs> [output_folder]

Expects files named like "<anything>-2019.pdf" (one PDF per financial-year session).
For every page it: renders the PDF to an image, removes the table lines (they confuse OCR),
and runs Tesseract. Output text files are named xc<year>-<page>.txt.
Needs: poppler-utils (pdftoppm), tesseract, opencv-python, numpy.
"""
import cv2, sys, glob, subprocess, os
import numpy as np

src = sys.argv[1] if len(sys.argv) > 1 else '.'
out = sys.argv[2] if len(sys.argv) > 2 else '.'
os.makedirs(out, exist_ok=True)

for pdf in sorted(glob.glob(os.path.join(src, '*-20[12][0-9].pdf'))):
    year = os.path.basename(pdf).split('-')[-1][:4]
    subprocess.run(['pdftoppm', '-r', '300', '-png', pdf, os.path.join(out, f'c{year}')], check=True)

for page in sorted(glob.glob(os.path.join(out, 'c20*.png'))):
    gray = cv2.imread(page, 0)
    bw = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    horiz = cv2.morphologyEx(bw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (80, 1)))
    vert = cv2.morphologyEx(bw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40)))
    lines = cv2.dilate(cv2.bitwise_or(horiz, vert), np.ones((3, 3), np.uint8))
    clean = cv2.bitwise_not(cv2.bitwise_and(bw, cv2.bitwise_not(lines)))   # text only, no table lines
    name = os.path.join(out, 'x' + os.path.basename(page))
    cv2.imwrite(name, clean)
    subprocess.run(['tesseract', name, name[:-4], '--psm', '6', '-c', 'preserve_interword_spaces=1'],
                   capture_output=True)
