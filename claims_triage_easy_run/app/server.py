import csv, io, json, os, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from app.triage_engine import triage_claim

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(ROOT,"data","sample_claims.json")
AUDIT=os.path.join(ROOT,"data","audit_log.jsonl")
LOCK=threading.Lock()

def load_claims():
    with open(DATA,encoding="utf-8") as f: return json.load(f)
def log_event(claim,result):
    with LOCK, open(AUDIT,"a",encoding="utf-8") as f:
        f.write(json.dumps({"input":claim,"result":result})+"\n")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=ROOT,**kwargs)
    def send_json(self,obj,status=200):
        data=json.dumps(obj).encode(); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        p=urlparse(self.path).path
        if p=="/": self.path="/static/index.html"; return super().do_GET()
        if p=="/api/claims":
            rows=[]
            for c in load_claims(): rows.append({**c,"triage":triage_claim(c)})
            return self.send_json(rows)
        if p=="/api/health": return self.send_json({"status":"ok","mode":"local-only","external_apis":False})
        return super().do_GET()
    def do_POST(self):
        p=urlparse(self.path).path
        n=int(self.headers.get("Content-Length",0)); raw=self.rfile.read(n)
        try:
            if p=="/api/triage":
                claim=json.loads(raw or b"{}"); result=triage_claim(claim); log_event(claim,result); return self.send_json(result)
            if p=="/api/bulk":
                rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
                results=[]
                for claim in rows:
                    result=triage_claim(claim); log_event(claim,result); results.append({**claim,**result})
                return self.send_json(results)
            return self.send_json({"error":"not found"},404)
        except Exception as e: return self.send_json({"error":str(e)},400)

if __name__ == "__main__":
    PORT = 53127

    print(f"Claims Triage prototype: http://127.0.0.1:{PORT}")
    print("Press Ctrl+C to stop the application.")

    ThreadingHTTPServer(
        ("127.0.0.1", PORT),
        Handler
    ).serve_forever()
