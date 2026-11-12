from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT=Path("/Users/USER/Library/Application Support/Open Design/namespaces/release-stable/data/projects/3c99ff72-0aaa-4654-b7b0-b06c20233d75")
ALLOWED_DIRS={"assets","solutions","industries","delivery","cases"}
EXT={".html",".css",".js",".svg",".jpg",".jpeg",".png",".webp",".gif",".mp4",".webm",".ico",".woff",".woff2",".ttf"}
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def do_GET(self):
  rel=Path(unquote(urlsplit(self.path).path).lstrip("/") or "index.html")
  if any(p.startswith(".") or p in {"..","backups","docs"} for p in rel.parts):return self.send_error(404)
  if len(rel.parts)>1 and rel.parts[0] not in ALLOWED_DIRS:return self.send_error(404)
  current=ROOT
  for p in rel.parts:
   current=current/p
   if current.is_symlink():return self.send_error(404)
  if not current.resolve().is_relative_to(ROOT.resolve()) or not current.is_file() or current.suffix.lower() not in EXT:return self.send_error(404)
  return super().do_GET()
 def do_HEAD(self):return self.send_error(405)
 def end_headers(self):
  self.send_header("Cache-Control","no-store")
  super().end_headers()
ThreadingHTTPServer(("127.0.0.1",3201),Handler).serve_forever()
