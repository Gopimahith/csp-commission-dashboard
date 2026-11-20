"""Step 3: read the monthly Excel files (income by service type) and check them against the statements.

Usage:  python scripts/excel_events.py <folder_with_xlsx> <year> [commission_by_month.json]
Files are named like "2025_JAN.xlsx" ... "2025_DEC.xlsx" with columns:
Sr. No., Event Type, Number of Transactions, Commission Amount.
Prints the commission total for each month. If a JSON file {"2025-01": 23879.17, ...} is given,
each month is compared with it (difference should be 0.00). Writes events<year>.json as
[[month, event_type, transactions, amount], ...], the format the dashboard uses.
Needs: openpyxl.
"""
import sys, glob, json, re, os
import openpyxl

folder, year = sys.argv[1], sys.argv[2]
expected = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JULY': 7, 'JUL': 7,
          'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
events, totals = [], {}
for path in sorted(glob.glob(os.path.join(folder, f'*{year}_*.xlsx'))):
    m = MONTHS[re.search(rf'{year}_+([A-Z]+)\.xlsx$', path).group(1)]
    sheet = openpyxl.load_workbook(path, data_only=True).active
    for row in list(sheet.iter_rows(values_only=True))[1:]:
        if row[1] is None:
            continue
        events.append([m, str(row[1]).strip(), row[2], row[3]])
        totals[m] = totals.get(m, 0) + (row[3] or 0)

for m in sorted(totals):
    key = f'{year}-{m:02d}'
    diff = f'  difference vs statement: {totals[m] - expected[key]:.2f}' if key in expected else ''
    print(key, f'{totals[m]:.2f}', diff)
json.dump(events, open(f'events{year}.json', 'w'))
