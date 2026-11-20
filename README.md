# CSP Commission Dashboard

An interactive, single-file dashboard that turns **8 years of scanned bank customer service point (CSP) commission statements** into clear trends: monthly commission, year-over-year totals, income by service type, and a month-by-month view of what was deducted (GST, SAVE, TDS) before payout.

![Dashboard preview](dashboard.png)

> **About the data:** the figures in this repository are **sample data**. Real statements were read and analysed privately. For this public demo every amount was multiplied by a fixed factor and all names and IDs were removed. Trends and percentages are realistic; the rupee amounts are not real.

## Why I built it

A CSP is a small bank outlet that serves customers who have no branch nearby (withdrawals, deposits, money transfers, account opening). The operator's income is a monthly commission on those transactions. The statements arrive as scanned PDFs and Excel files, so there was no easy way to see how that income moved over the years. This dashboard answers that.

## What it shows

- KPI cards for any financial year (Apr to Mar): total commission, deductions, paid out, average per month, best and lowest month, plus a "compare with another year" card
- Monthly commission bars with an average line, year-by-year totals and a seasonality view
- **Income by service type** for 2024, 2025 and 2026 (year and month selectors)
- **Monthly commission and deductions** with its own year selector: total commission, total deducted, and GST, SAVE and TDS amounts and shares, as cards and bar graphs
- **Before and after deductions**: for each year, commission, deductions and paid out in a bar view and a table

## Key findings

- Deductions settled at **35% of commission** from 2023-24 onward (about 15% GST, 19% SAVE, under 1% TDS). Before that they were roughly 39%.
- Average monthly commission fell to about **one sixth of its 2019-20 level in 2022-23**, then recovered to about three times that low point.
- In 2024, three sources made up about 79% of income: average balance maintenance (35%), AePS withdrawals (29%) and cash withdrawals (14%).
- **February 2026 was the lowest month.** The monthly file for that month has no "Average Balance Maintenance" line, which made up roughly 40 to 50% of monthly income in 2026.

## How it was built

1. `scripts/ocr_statements.py`: the statements were scanned images, so each page is rendered, table lines are removed (they confuse OCR) and Tesseract reads the text.
2. `scripts/parse_statements.py`: parses the commission, deduction and payment rows and **compares each year's sum with the total printed on the statement**. Where they disagreed (for example a digit misread as a symbol), the row was corrected by hand against the page image.
3. `scripts/excel_events.py`: reads the monthly Excel files (income by service type) and checks every month against the statement total. All months of 2024, 2025 and 2026 (Jan to Oct) match to the paisa.
4. The dashboard is plain HTML, CSS and JavaScript with inline SVG charts, so it opens in any browser with no install.

## Run it

Open `index.html` in a browser. To run the extraction yourself you need `tesseract`, `poppler-utils` and `pip install opencv-python numpy openpyxl`, plus your own statement files:

```
python scripts/ocr_statements.py statements/ ocr_out/
python scripts/parse_statements.py ocr_out/
python scripts/excel_events.py monthly_files/ 2025
```

## Notes and limits

- Monthly deduction detail exists only from April 2023. Earlier statements show yearly totals only.
- 2026-27 covers April to October.
- May 2022 has no commission line on the statement.

## Tech

Python, Tesseract OCR, OpenCV, openpyxl, JavaScript, SVG
