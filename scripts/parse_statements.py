"""Step 2: parse the OCR text and check every year against the totals printed on the statement.

Usage:  python scripts/parse_statements.py [folder_with_ocr_text]
Reads xc<year>-*.txt (from ocr_statements.py), prints one reconciliation line per year
(parsed sum vs printed total for commission, deductions and paid) and writes parsed.json.
A year whose parsed sum differs from the printed total has an OCR misread: fix it against the page image.
"""
import re,glob,json,collections,os,sys
folder=sys.argv[1] if len(sys.argv)>1 else '.'
years=sorted({int(re.search(r'xc(\d{4})-',f).group(1)) for f in glob.glob(os.path.join(folder,'xc20*-*.txt'))})
out={}
for y in years:
    txt="\n".join(open(f).read() for f in sorted(glob.glob(os.path.join(folder,f'xc{y}-*.txt'))))
    com=[];ded=[];paid=[];stated={}
    section=None
    for ln in txt.splitlines():
        s=ln.strip()
        if re.match(r'^Commission\b',s): section='c'
        elif re.match(r'^Deducation\b',s): section='d'
        elif re.match(r'^Paid\b',s): section='p'
        m=re.search(r'Total Commission\s+([\d.]+)$',s)
        if m and section=='c': stated['com']=float(m.group(1))
        m=re.search(r'Total Deducation\s+([\d.]+)$',s)
        if m and section=='d': stated['ded']=float(m.group(1))
        if section=='c':
            m=re.match(r'^\S{1,3}\s+(\d\d/20\d\d)\s+(Monthly|[A-Za-z ]+?)\s+\S*?([\d]+\.\d\d)$',s)
            if m: com.append((m.group(1),m.group(2),float(m.group(3))))
        elif section=='d':
            m=re.match(r'^\S{1,3}\s+(\d\d/20\d\d)\s+(TDS|GST|SAVE|[A-Za-z ]+?)\s+\S*?([\d]+\.\d+)$',s)
            if m: ded.append((m.group(1),m.group(2).strip(),float(m.group(3))))
        elif section=='p':
            m=re.match(r'^\S{1,3}\s+(\d\d/20\d\d)\s+(.+?)\s+(\d\d/\d\d/\d\d(?:\d\d)?)\b.*?\s\S*?([\d]+\.\d\d)$',s)
            if m: paid.append((m.group(1),m.group(2),m.group(3),float(m.group(4))))
            m=re.search(r'Total\s+([\d.]+)$',s)
            if m and 'Commission' not in s and 'Deducation' not in s: stated['paid']=float(m.group(1))
    out[y]=dict(com=com,ded=ded,paid=paid,stated=stated)
    print(y,'com',len(com),round(sum(c[2] for c in com),2),stated.get('com'),'| ded',len(ded),round(sum(d[2] for d in ded),2),stated.get('ded'),'| paid',len(paid),round(sum(p[3] for p in paid),2),stated.get('paid'))
json.dump(out,open(os.path.join(folder,'parsed.json'),'w'))
