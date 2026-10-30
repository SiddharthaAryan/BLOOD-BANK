"""Single-computer demonstration. Run: python server.py. Synthetic data only."""
import csv, io, json, os, re, sqlite3, subprocess, tempfile, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parent
DB=ROOT/'demo-records.sqlite3'
FIELDS=['name','age','phone','city','donation','last_donation','health','medicine','procedure','private_discussion','notes']
def connection():
 c=sqlite3.connect(DB); c.execute('CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, created TEXT DEFAULT CURRENT_TIMESTAMP, data TEXT NOT NULL)');return c
class Handler(BaseHTTPRequestHandler):
 def reply(self,code,data,typ='application/json'):
  self.send_response(code);self.send_header('Content-Type',typ);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def jout(self,code,obj):self.reply(code,json.dumps(obj).encode())
 def do_GET(self):
  path=urlsplit(self.path).path
  if path=='/':return self.reply(200,(ROOT/'scan-local.html').read_bytes(),'text/html; charset=utf-8')
  if path=='/api/records':
   with connection() as c: rows=c.execute('SELECT id,created,data FROM records ORDER BY created DESC').fetchall()
   return self.jout(200,[{'id':i,'created':d,**json.loads(v)} for i,d,v in rows])
  if path in ('/export.csv','/export.xlsx'):
   with connection() as c: rows=c.execute('SELECT id,created,data FROM records ORDER BY created DESC').fetchall()
   headers=['Reference','Saved (UTC)']+FIELDS
   def safe(x):
    x=str(x or '');return "'"+x if re.match(r'^\s*[=+@\-\t\r]',x) else x
   values=[[safe(i),safe(d)]+[safe(json.loads(v).get(k,'')) for k in FIELDS] for i,d,v in rows]
   if path.endswith('.csv'):
    out=io.StringIO(newline=''); w=csv.writer(out);w.writerow(headers);w.writerows(values);return self.reply(200,('\ufeff'+out.getvalue()).encode(),'text/csv; charset=utf-8')
   try:
    from openpyxl import Workbook
    book=Workbook(); sheet=book.active;sheet.title='Reviewed records';sheet.append(headers)
    for row in values:sheet.append(row)
    out=io.BytesIO();book.save(out);return self.reply(200,out.getvalue(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
   except ImportError:return self.jout(503,{'error':'Excel export needs openpyxl installed. CSV export is still available.'})
  self.jout(404,{'error':'Not found'})
 def do_POST(self):
  if self.headers.get('Origin') not in (None,'http://127.0.0.1:8765','http://localhost:8765') or self.headers.get('X-Demo-Request')!='yes':return self.jout(403,{'error':'Request rejected'})
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n<1 or n>16000000:return self.jout(413,{'error':'File too large (limit 12 MB per image)'})
   payload=json.loads(self.rfile.read(n));path=urlsplit(self.path).path
   if path=='/api/ocr':
    import base64
    image=base64.b64decode(payload['image'],validate=True)
    if len(image)>12000000:raise ValueError('Image exceeds 12 MB')
    with tempfile.TemporaryDirectory() as temp:
     src=Path(temp)/'image';src.write_bytes(image)
     p=subprocess.run(['tesseract',str(src),'stdout','-l','eng','tsv'],capture_output=True,timeout=90)
     if p.returncode:raise ValueError('OCR could not read this image. Use a supported image or enter data manually.')
     rows=list(csv.DictReader(io.StringIO(p.stdout.decode('utf-8',errors='replace')),delimiter='\t')); lines={};scores=[]
     for r in rows:
      word=r.get('text','').strip()
      try: score=float(r['conf'])
      except (ValueError,KeyError):continue
      if word and score>=0:
       key=(r['block_num'],r['par_num'],r['line_num']);lines.setdefault(key,[]).append(word);scores.append(score)
     text='\n'.join(' '.join(words) for words in lines.values())
     return self.jout(200,{'text':text,'score':round(sum(scores)/len(scores),1) if scores else None,'words':len(scores)})
   if path=='/api/records':
    if payload.get('verified') is not True:raise ValueError('Review confirmation required')
    data=payload.get('fields',{})
    if not isinstance(data,dict):raise ValueError('Invalid fields')
    data={k:str(data.get(k,'')).strip()[:2000] for k in FIELDS}
    if not any(data.values()):raise ValueError('Enter at least one field')
    ident='DEMO-'+uuid.uuid4().hex[:10].upper()
    with connection() as c:c.execute('INSERT INTO records(id,data) VALUES (?,?)',(ident,json.dumps(data)))
    return self.jout(201,{'id':ident})
   self.jout(404,{'error':'Not found'})
  except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:self.jout(400,{'error':str(e)})
  except FileNotFoundError:self.jout(503,{'error':'Tesseract OCR not installed. Install it or enter fields manually.'})
  except subprocess.TimeoutExpired:self.jout(504,{'error':'OCR timed out. Try a smaller, clearer image.'})
 def log_message(self,format,*args):pass
if __name__=='__main__':
 connection().close();print('Demo ready: http://127.0.0.1:8765 (fictional data only)',flush=True);ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
