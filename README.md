# CSP Commission Dashboard

An interactive, single-file dashboard that turns years of bank **customer service point (CSP)** commission statements into clear trends: monthly commission, year-over-year totals, best months, income by service type and monthly deductions.

> **About the data:** the figures in this repository are **sample data**. Real statements were read and analysed privately; for this public demo every amount was multiplied by a fixed factor and all names and IDs were removed. Trends are realistic, amounts are not real.

## What it shows

- KPI cards: total commission, deductions, paid out, average per month, best and lowest month
- Financial-year filter (Apr to Mar) and a "compare with another year" card
- Monthly commission bars with an average line, and year-by-year commission, deductions and paid
- Which calendar months earn the most
- 2024 income by service type (AePS withdrawal, balance maintenance, money transfer, insurance schemes and more)
- Monthly TDS, GST and SAVE deductions (from Apr 2023)

## How it was built

1. The statements were scanned images, so `scripts/ocr_statements.py` cleans each page (removes table lines) and runs Tesseract OCR.
2. `scripts/parse_statements.py` parses commission, deduction and payment rows, then **checks the sum of every year against the total printed on the statement**.
3. Monthly commission matched the printed totals for every year. Digit misreads that broke a total were found this way and corrected against the page image.
4. The dashboard is plain HTML, CSS and JavaScript with inline SVG charts, so it opens in any browser with no install.

## Run it

Open `index.html` in a browser. To run the extraction yourself you need `tesseract`, `poppler-utils` and `pip install opencv-python pandas`, and your own statement PDFs.

## Tech

Python, Tesseract OCR, OpenCV, JavaScript, SVG
