# -*- coding: utf-8 -*-
"""Иконки и OG-картинка: python3 src/og.py (нужен dist/), затем снова python3 src/build.py."""
import http.server, socketserver, threading, functools, sys, re
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import build as B
ROOT = Path(__file__).resolve().parent.parent; DIST = ROOT / "dist"; A = ROOT / "assets"
OG = f'''<!doctype html><html><head><meta charset="utf-8"><style>{B.CSS}
html,body{{margin:0}}.og{{position:relative;width:1200px;height:630px;overflow:hidden;color:#fff;background:linear-gradient(105deg,var(--ink) 60%,#26272b 60%)}}
.og::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:14px;background:var(--haz)}}
.og-t{{position:absolute;left:64px;top:60px;width:640px}}.og h1{{font-size:70px;line-height:1.02;margin-top:40px}}
.og p{{margin-top:22px;font-size:26px;color:rgba(255,255,255,.8)}}.og .logo-t{{font-size:32px}}.og .logo img{{width:56px;height:56px}}
.og .hs{{max-width:600px;margin-top:34px}}.og .hs b{{font-size:44px}}
.og-i{{position:absolute;right:64px;top:56px;width:400px;height:500px;border-radius:10px;object-fit:cover;box-shadow:14px 14px 0 var(--r1)}}
</style></head><body><div class="og"><div class="og-t">{B.logo(True)}<h1>Аренда манипулятора в&nbsp;Астане</h1><p>7, 12, 20 и 25 тонн · подача за 1–2 часа</p>{B.hero_specs()}</div>
<img class="og-i" src="/assets/img/hero-800.webp"></div></body></html>'''
ICON = '''<!doctype html><html><body style="margin:0;background:transparent"><div style="width:%dpx;height:%dpx;display:grid;place-items:center;background:%s"><img src="/assets/logo-mark.svg" style="width:%d%%;height:%d%%"></div></body></html>'''
h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST)); http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
with socketserver.TCPServer(("127.0.0.1", 0), h) as srv:
    port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        def shot(html, w, h, out, tr=False):
            (DIST / "_x.html").write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(f"http://127.0.0.1:{port}/_x.html"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
            pg.screenshot(path=str(out), omit_background=tr); pg.close()
        shot(OG, 1200, 630, A / "og.png")
        shot(ICON % (512, 512, "transparent", 100, 100), 512, 512, A / "_mark.png", True)
        shot(ICON % (180, 180, "#e1251b", 100, 100), 180, 180, A / "apple-touch-icon.png")
        shot(ICON % (512, 512, "#e1251b", 100, 100), 512, 512, A / "icon-512.png")
        b.close()
    srv.shutdown()
(DIST / "_x.html").unlink(missing_ok=True)
m = Image.open(A / "_mark.png").convert("RGBA")
Image.open(A / "icon-512.png").resize((192, 192), Image.LANCZOS).save(A / "icon-192.png")
m.save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)]); (A / "_mark.png").unlink()
Image.open(A / "og.png").convert("RGB").save(A / "og.png", optimize=True)
print("ok")
