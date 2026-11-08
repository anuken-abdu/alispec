# -*- coding: utf-8 -*-
"""Генератор alispec.kz (аренда манипуляторов, Астана): python3 src/build.py → dist/
Скорость: CSS встроен в каждую страницу, шрифты локальные (2 файла в первом экране), фото WebP с srcset,
тег Google грузится после первого действия посетителя."""
import html, json, re, shutil, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from data import *

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"; A = ROOT / "assets"
VER = "0811262000"
TODAY = date.today().isoformat()
NB = re.compile(r"(\d) (т|м|км|тонн|метр|часа|часов|футов)(?=[\s.,;:)]|$)")
def E(s): return NB.sub("\\1&nbsp;\\2", html.escape(str(s), quote=True))
PAGES = []
FL = {f["t"]: f for f in FLEET}
def furl(f): return f"/manipulyatory/{f['slug']}/"
def surl(s): return f"/uslugi/{s['slug']}/"

def wa(text): return f"https://wa.me/{WA_NUMBER}?text=" + re.sub(r"\s", "%20", html.escape(text))
def wa_attr(text): return f'href="{wa(text)}" target="_blank" rel="noopener" data-wa'
PH = json.loads((Path(__file__).parent / "ph_icons.json").read_text(encoding="utf-8"))
def ph(name, cls="ph"): return f'<svg class="{cls}" viewBox="0 0 256 256" aria-hidden="true" focusable="false">{PH[name + "-duotone"]}</svg>'
ICON = {
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "wa": '<path d="M3.5 20.5l1.2-4.3A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 8.5c0 3 2.5 6.3 6 6.8l1.3-1.6-2-1-1 .9c-1-.5-2-1.5-2.4-2.5l.9-1-1-2z"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "up": '<path d="M12 19V5M6 11l6-6 6 6"/>', "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>', "close": '<path d="M6 6l12 12M18 6L6 18"/>', "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>', "send": '<path d="M4 12l16-8-6 16-2.5-6.5z"/>', "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "spark": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}
def ui(n, cls="ui"): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</g></svg>'

# ---------------------------------------------------------------- фото
IMG_W = {p.stem.rsplit("-", 1)[0]: sorted(int(x.stem.rsplit("-", 1)[1]) for x in (A / "img").glob(p.stem.rsplit("-", 1)[0] + "-*.webp")) for p in (A / "img").glob("*.webp")}
RATIO = {"hero": (4, 5)}
def img(name, alt, sizes, cls="", eager=False):
    ws = IMG_W[name]; rw, rh = RATIO.get(name, (4, 3)); w0 = ws[min(1, len(ws) - 1)]
    src = ", ".join(f"/assets/img/{name}-{w}.webp {w}w" for w in ws)
    lazy = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/img/{name}-{w0}.webp" srcset="{src}" sizes="{sizes}" width="{w0}" height="{round(w0 * rh / rw)}" alt="{E(alt)}" {lazy}>')

MSG = "Здравствуйте! Нужен манипулятор в Астане."
def logo(dark=False):
    return (f'<a class="logo{" logo-d" if dark else ""}" href="/"><img src="/assets/logo-mark.svg" alt="" width="42" height="42">'
            f'<span class="logo-t">Ali<i>Spec</i><small>манипуляторы</small></span></a>')

def btns(msg=MSG, call="Позвонить", wtxt="WhatsApp"):
    return (f'<div class="btns"><a class="btn btn-p" href="tel:{PHONE_TEL}" data-call>{ui("phone")}{call}</a>'
            f'<a class="btn btn-w" {wa_attr(msg)}>{ui("wa")}{wtxt}</a></div>')

def sec(title, inner, sub="", alt=False, sid="", link=None, cls=""):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ui("arrow")}</a>' if link else ""
    return (f'<section class="sec{" sec-alt" if alt else ""}{" " + cls if cls else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap">'
            f'<div class="sec-h"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{lk}</div>{inner}</div></section>')

def crumbs_html(cr):
    items = [("Главная", "/")] + cr
    li = "".join(f'<li><a href="{u}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>' for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs" aria-label="Навигация"><ol>{li}</ol></nav>'

def specs_dl(f, kz=None):
    L = kz or {"crane": "Кран", "boom": "Вылет стрелы", "deck": "Длина борта", "board": "Борт везёт", "t": "т", "m": "м"}
    return (f'<dl class="sp"><div><dt>{L["crane"]}</dt><dd>{f["crane"]} {L["t"]}</dd></div><div><dt>{L["boom"]}</dt><dd>{f["boom"]} {L["m"]}</dd></div>'
            f'<div><dt>{L["deck"]}</dt><dd>{f["deck"]} {L["m"]}</dd></div><div><dt>{L["board"]}</dt><dd>{f["board"]} {L["t"]}</dd></div></dl>')

def ph_hero(h1, lead, crumbs, msg=MSG, photo=None, alt=""):
    side = f'<div class="phd-img">{img(photo, alt, "(max-width:767px) 100vw, 480px", eager=True)}</div>' if photo else ""
    return (f'<section class="phd"><div class="wrap">{crumbs_html(crumbs)}<div class="phd-in{" has-img" if photo else ""}"><div><h1>{h1}</h1>'
            f'<p class="lead-t">{lead}</p>{btns(msg)}</div>{side}</div></div></section>')

# ---------------------------------------------------------------- блоки
def perks_html():
    return '<section class="perks"><div class="wrap"><ul>' + "".join(f'<li>{ph(i)}<span><b>{E(t)}</b><small>{E(s)}</small></span></li>' for i, t, s in PERKS) + "</ul></div></section>"

def fleet_cards(items=None):
    out = []
    for f in items or FLEET:
        out.append(f'''<article class="fc"><a class="fc-img" href="{furl(f)}">{img(f["img"], f"Манипулятор {f['t']} тонн в Астане", "(max-width:767px) 100vw, (max-width:1180px) 50vw, 340px")}</a>
<div class="fc-b"><h3><a href="{furl(f)}">Манипулятор <b>{f["t"]}</b> тонн</a></h3>{specs_dl(f)}<p>{E(f["lead"])}</p>
<div class="fc-a"><a class="btn btn-p btn-s" href="tel:{PHONE_TEL}" data-call>{ui("phone")}Заказать</a><a class="lnk" href="{furl(f)}">Подробнее {ui("arrow")}</a></div></div></article>''')
    n = len(out)
    return f'<div class="fcs fcs-{n}">' + "".join(out) + "</div>"

def compare_table(kz=None):
    L = kz or {"crane": "Кран поднимает", "boom": "Вылет стрелы", "deck": "Длина борта", "board": "Борт везёт", "btype": "Тип стрелы", "t": "т", "m": "м"}
    head = "".join(f'<th scope="col"><a href="{furl(f)}">{f["t"]} {L["t"]}</a></th>' if not kz else f'<th scope="col">{f["t"]} {L["t"]}</th>' for f in FLEET)
    def row(k, unit): return f'<tr><th scope="row">{L[k]}</th>' + "".join(f"<td>{f[k]} {unit}</td>" for f in FLEET) + "</tr>"
    bt = f'<tr><th scope="row">{L["btype"]}</th>' + "".join(f'<td>{(kz["z"] if "Z" in f["boom_type"] else kz["tel"]) if kz else f["boom_type"].replace("Телескопическая ", "Телескоп. ")}</td>' for f in FLEET) + "</tr>"
    return (f'<div class="tbl"><table><thead><tr><th scope="col">{"Манипулятор" if not kz else ""}</th>{head}</tr></thead><tbody>'
            f'{row("crane", L["t"])}{row("board", L["t"])}{row("deck", L["m"])}{row("boom", L["m"])}{bt}</tbody></table></div>')

def svc_cards(items=None):
    items = items or SERVICES; n = len(items)
    return f'<div class="scs scs-{n}">' + "".join(f'<a class="scd" href="{surl(s)}">{ph(s["icon"])}<b>{E(s["name"])}</b><span>{E(s["short"])}</span>{ui("arrow")}</a>' for s in items) + "</div>"

def steps_html(st=None):
    return '<ol class="steps">' + "".join(f'<li><span>{i:02d}</span><b>{E(t)}</b><p>{E(d)}</p></li>' for i, (t, d) in enumerate(st or STEPS, 1)) + "</ol>"

def factors_html():
    return '<div class="fac">' + "".join(f'<div><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in PRICE_FACTORS) + "</div>"

def checks(items):
    return '<ul class="chk">' + "".join(f'<li>{ui("check")}<span>{E(x)}</span></li>' for x in items) + "</ul>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}{ui("chev")}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>"

def districts_html(cur=""):
    li = "".join(f'<li><a href="/rayony/{d["slug"]}/"{" aria-current=page" if d["slug"] == cur else ""}>{E(d["short"])}{ui("arrow")}</a></li>' for d in DISTRICTS)
    sub = f'<li><a href="/rayony/prigorody/"{" aria-current=page" if cur == "prigorody" else ""}>Пригороды{ui("arrow")}</a></li>'
    return f'<ul class="dl">{li}{sub}</ul>'

def geo_sec(cur=""):
    return sec("Работаем по всей Астане", districts_html(cur), "Все районы города и пригороды в радиусе до 100 км: " + ", ".join(SUBURBS) + ".", alt=True, sid="rayony")

def article_cards():
    return '<div class="arts">' + "".join(f'<a class="art" href="/stati/{a["slug"]}/"><b>{E(a["title"])}</b><span>{E(a["desc"])}</span>{ui("arrow")}</a>' for a in ARTICLES) + "</div>"

def gallery():
    items = [("g4", "Манипулятор с контейнером на объекте в Астане"), ("g1", "Разгрузка контейнера манипулятором"), ("g2", "Манипулятор с поднятой стрелой"), ("g3", "Кран-манипулятор на базе тягача")]
    return '<div class="gal">' + "".join(f'<figure>{img(n, a, "(max-width:767px) 50vw, 25vw")}</figure>' for n, a in items) + "</div>"

def callout(msg=MSG):
    return f'''<section class="cta"><div class="wrap"><div class="cta-in"><div><b>Опишите груз — подберём манипулятор</b><p>Вес, размеры и адрес. Подача в течение 1–2 часов, круглосуточно.</p></div>{btns(msg)}</div></div></section>'''

def lead_form(title="Заказать манипулятор", t=0):
    opts = '<option>Подберите за меня</option>' + "".join(f'<option{" selected" if f["t"] == t else ""}>Манипулятор {f["t"]} тонн</option>' for f in FLEET)
    return f'''<section class="sec sec-dark" id="zayavka"><div class="wrap lead">
<div><h2>{title}</h2><p>Заполните форму — заявка откроется в WhatsApp. Или позвоните, ответим круглосуточно.</p>
<a class="lead-ph" href="tel:{PHONE_TEL}" data-call>{ui("phone")}{PHONE_DISPLAY}</a><p class="lead-h">{ui("clock")}{HOURS}</p></div>
<form class="form" data-lead novalidate>
<div class="fld"><label for="fN">Имя</label><input id="fN" name="name" autocomplete="name"></div>
<div class="fld"><label for="fP">Телефон</label><input id="fP" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="+7"></div>
<div class="fld"><label for="fV">Техника</label><select id="fV" name="job">{opts}</select></div>
<div class="fld"><label for="fD">Когда</label><select id="fD" name="when"><option>Как можно скорее</option><option>Сегодня</option><option>Завтра</option><option>Другая дата</option></select></div>
<div class="fld fld-w"><label for="fM">Груз и адрес</label><textarea id="fM" name="msg" rows="3" placeholder="Например: 40-футовый контейнер, из Байконыра в Косшы"></textarea></div>
<p class="f-err" hidden>Укажите телефон, чтобы мы могли связаться.</p>
<button class="btn btn-p fld-w" type="submit">{ui("wa")}Отправить в WhatsApp</button>
<p class="f-note fld-w">Нажимая кнопку, вы соглашаетесь с <a href="/privacy-policy/">политикой конфиденциальности</a>.</p></form></div></section>'''

# ---------------------------------------------------------------- schema
ORG = {"@type": "LocalBusiness", "@id": SITE_URL + "/#org", "name": BRAND, "description": "Аренда кран-манипуляторов 7–25 тонн в Астане и в радиусе 100 км",
       "url": SITE_URL + "/", "telephone": PHONE_TEL, "image": SITE_URL + "/assets/og.png", "logo": SITE_URL + "/assets/icon-512.png",
       "address": {"@type": "PostalAddress", "addressLocality": "Астана", "addressCountry": "KZ"}, "geo": {"@type": "GeoCoordinates", "latitude": 51.1282, "longitude": 71.4304},
       "areaServed": [{"@type": "City", "name": "Астана"}, {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": 51.1282, "longitude": 71.4304}, "geoRadius": "100000"}],
       "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}}
def service_schema(name, url, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": "Аренда кран-манипулятора", "url": SITE_URL + url, "description": desc,
            "provider": {"@id": SITE_URL + "/#org"}, "areaServed": {"@type": "City", "name": "Астана"}}
def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def fit(s, n=155): return s if len(s) <= n else s[:n - 1].rsplit(" ", 1)[0].rstrip(",.:;—") + "…"

# ---------------------------------------------------------------- шаблон
CSS = (Path(__file__).parent / "fonts.css").read_text(encoding="utf-8") + (Path(__file__).parent / "styles.css").read_text(encoding="utf-8")
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S); CSS = re.sub(r"\s*\n\s*", "", CSS); CSS = re.sub(r"\s*([{};:,>])\s*", r"\1", CSS).replace(";}", "}")

def nav_html():
    fl = "".join(f'<li><a href="{furl(f)}">Манипулятор {f["t"]} тонн</a></li>' for f in FLEET)
    sv = "".join(f'<li><a href="{surl(s)}">{E(s["name"])}</a></li>' for s in SERVICES)
    return f'''<nav class="nav" id="nav" aria-label="Меню"><ul>
<li class="has"><a href="/manipulyatory/">Техника</a><ul class="sub">{fl}</ul></li><li class="has"><a href="/uslugi/">Услуги</a><ul class="sub">{sv}</ul></li>
<li><a href="/ceny/">Цены</a></li><li><a href="/rayony/">Районы</a></li><li><a href="/kontakty/">Контакты</a></li><li><a class="lang" href="/kz/" hreflang="kk" lang="kk">ҚАЗ</a></li></ul>
<div class="nav-m">{btns()}</div></nav>'''

def page(path, title, desc, body, schemas=(), crumbs=None, prio="0.7", lang="ru", preload=None, alt_kz=False):
    PAGES.append((path, prio))
    desc = fit(desc)
    bc = []
    if crumbs:
        items = [("Главная", "/")] + crumbs
        bc = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}]
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>' for s in [{"@context": "https://schema.org", **ORG}, *schemas, *bc])
    cfg = json.dumps({"ads": GADS_ID, "call": GADS_CALL_LABEL, "wa": GADS_WA_LABEL, "form": GADS_FORM_LABEL, "wan": WA_NUMBER}, ensure_ascii=False)
    hre = ""
    if path in ("/", "/kz/"):
        hre = f'<link rel="alternate" hreflang="ru" href="{SITE_URL}/"><link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/"><link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'
    pre = ""
    if preload:
        n = preload; pre = f'<link rel="preload" as="image" type="image/webp" imagesrcset="{", ".join(f"/assets/img/{n}-{w}.webp {w}w" for w in IMG_W[n])}" imagesizes="(max-width:767px) 100vw, 480px" fetchpriority="high">'
    fl_f = "".join(f'<li><a href="{furl(f)}">Манипулятор {f["t"]} тонн</a></li>' for f in FLEET)
    sv_f = "".join(f'<li><a href="{surl(s)}">{E(s["name"])}</a></li>' for s in SERVICES)
    doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">{hre}
<meta name="robots" content="{"noindex,follow" if path == "/404" else "index,follow,max-image-preview:large"}">
<meta name="geo.region" content="KZ-AST"><meta name="geo.placename" content="Астана"><meta name="geo.position" content="51.1282;71.4304"><meta name="ICBM" content="51.1282, 71.4304">
<meta property="og:type" content="website"><meta property="og:locale" content="{"kk_KZ" if lang == "kk" else "ru_KZ"}"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:image" content="{SITE_URL}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#17181a">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/logo-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/oswald-cyrillic-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/onest-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>{pre}
<style>{CSS}</style>
{ld}
</head>
<body>
<a class="skip" href="#main">{"Мазмұнға өту" if lang == "kk" else "К содержимому"}</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}{nav_html()}
<div class="hdr-c"><a class="hdr-ph" href="tel:{PHONE_TEL}" data-call>{PHONE_DISPLAY}<small>{"тәулік бойы" if lang == "kk" else "круглосуточно"}</small></a>
<a class="hdr-call" href="tel:{PHONE_TEL}" data-call aria-label="Позвонить {PHONE_DISPLAY}">{ui("phone")}</a>
<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">{ui("menu")}{ui("close", "ui ui-x")}</button></div></div></header>
<main id="main">
{body}
</main>
<footer class="ftr"><div class="wrap ftr-g">
<div class="ftr-a">{logo(True)}<p>Аренда кран-манипуляторов 7–25 тонн в Астане и в радиусе 100 км. {HOURS}.</p><a class="ftr-ph" href="tel:{PHONE_TEL}" data-call>{PHONE_DISPLAY}</a><p class="ftr-ad">{ui("pin")}Астана и пригороды до 100 км</p></div>
<div><p class="ftr-h">Техника</p><ul>{fl_f}<li><a href="/manipulyatory/">Сравнить модели</a></li></ul></div>
<div><p class="ftr-h">Услуги</p><ul>{sv_f}</ul></div>
<div><p class="ftr-h">Информация</p><ul><li><a href="/ceny/">Цены</a></li><li><a href="/rayony/">Районы</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/kontakty/">Контакты</a></li><li><a href="/kz/" hreflang="kk">Қазақша</a></li><li><a href="/privacy-policy/">Конфиденциальность</a></li></ul></div>
</div><div class="wrap ftr-b"><span>© {date.today().year} {BRAND}. Информация на сайте не является публичной офертой.</span><a href="{DEV[1]}" target="_blank" rel="noopener">Разработка сайта — {DEV[0]}</a></div></footer>
<div class="fab"><button class="fab-b" type="button" data-back aria-label="Назад" title="Назад">{ui("back")}</button><button class="fab-b" type="button" data-top aria-label="Наверх" title="Наверх">{ui("up")}</button></div>
<button class="chat-o" type="button" data-chat aria-label="ИИ-консультант"><span class="chat-o-i">{ui("spark")}</span><span class="chat-o-t">ИИ-консультант</span></button>
<div class="chat" id="chat" hidden role="dialog" aria-label="ИИ-консультант"><div class="chat-h"><b>{BRAND}<small>ИИ-консультант</small></b><button type="button" data-chat-x aria-label="Закрыть чат">{ui("close")}</button></div>
<div class="chat-l" aria-live="polite"></div><div class="chat-q"></div>
<form class="chat-f"><input name="q" autocomplete="off" placeholder="Напишите вопрос" aria-label="Ваш вопрос"><button type="submit" aria-label="Отправить">{ui("send")}</button></form>
<a class="chat-wa" {wa_attr("Здравствуйте! Пишу с сайта, нужен манипулятор.")}>{ui("wa")}Продолжить в WhatsApp</a></div>
<script>window.CFG={cfg};</script>
<script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''
    out = DIST / "404.html" if path == "/404" else DIST / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding="utf-8")

# ---------------------------------------------------------------- страницы
def hero_specs(kz=None):
    L = kz or {}
    items = [("25", "т", L.get("c", "грузоподъёмность")), ("13", "м", L.get("d", "длина борта")), ("17", "м", L.get("b", "вылет стрелы")), ("24/7", "", L.get("h", "без выходных"))]
    return '<ul class="hs">' + "".join(f"<li><b>{a}<i>{u}</i></b><span>{t}</span></li>" for a, u, t in items) + "</ul>"

def build_home():
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t">
<h1>Аренда манипулятора в&nbsp;Астане</h1>
<p class="lead-t">Кран-манипуляторы 7, 12, 20 и 25 тонн с бортом до 13&nbsp;м. Перевозка, погрузка, разгрузка и монтаж. Подача за 1–2 часа, круглосуточно.</p>
{btns()}{hero_specs()}</div>
<div class="hero-v">{img("hero", "Манипулятор 25 тонн с 40-футовым контейнером в Астане", "(max-width:767px) 100vw, 480px", eager=True)}</div></div></section>
{perks_html()}
{sec("Наша техника", fleet_cards(), "Подберём манипулятор точно под вес и длину груза.", sid="tekhnika", link=("Сравнить модели", "/manipulyatory/"))}
{sec("Сравнение манипуляторов", compare_table(), "Название модели — по грузоподъёмности борта.", alt=True)}
{sec("Услуги манипулятора", svc_cards(), "Перевозка, погрузка, разгрузка и монтаж по Астане и до 100 км.", sid="uslugi")}
{callout()}
{sec("Как заказать манипулятор", steps_html())}
{sec("Техника на объектах", gallery(), alt=True)}
{sec("От чего зависит цена", factors_html(), "Стоимость называем по телефону, когда уточним груз и адрес.", link=("Подробнее о ценах", "/ceny/"))}
{geo_sec()}
<section class="sec"><div class="wrap"><div class="prose"><h2>Аренда манипулятора в Астане</h2>
<p>Предоставляем кран-манипуляторы в Астане и в радиусе до 100 км. Грузоподъёмность борта — от 7 до 25 тонн, длина борта — до 13 метров, вылет стрелы — до 17 метров. Техника подходит для доставки стройматериалов, перевозки контейнеров, погрузки и разгрузки оборудования и монтажных работ.</p>
<p>Манипулятор 25 тонн с бортом 13 метров перевозит 40-футовые контейнеры, тяжёлое промышленное оборудование и металлоконструкции. Стрела с вылетом до 17 метров подаёт груз через заборы, на крыши и в труднодоступные места.</p></div></div></section>
{sec("Полезно знать", article_cards(), alt=True, link=("Все статьи", "/stati/"))}
{sec("Частые вопросы", faq_html(FAQ))}
{lead_form()}'''
    page("/", f"Аренда манипулятора в Астане — 7, 12, 20, 25 тонн | {BRAND}",
         "Аренда кран-манипулятора в Астане: 7, 12, 20 и 25 тонн, борт до 13 м, стрела до 17 м. Контейнеры, стройматериалы, монтаж. Подача за 1–2 часа, 24/7.",
         body, [service_schema("Аренда манипулятора в Астане", "/", "Кран-манипуляторы 7–25 тонн: перевозка, погрузка, разгрузка и монтаж."), faq_schema(FAQ)], prio="1.0", preload="hero")

def build_kz():
    K = KZ
    L = {"crane": K["crane"], "boom": K["boom"], "deck": K["deck"], "board": K["board"], "btype": K["btype"], "z": K["z"], "tel": K["tel"], "t": K["t"], "m": K["m"]}
    msg = "Сәлеметсіз бе! Астанада манипулятор керек."
    cards = "".join(f'''<article class="fc"><div class="fc-img">{img(f["img"], f"{f['t']} тонна манипулятор, Астана", "(max-width:767px) 100vw, (max-width:1180px) 50vw, 340px")}</div>
<div class="fc-b"><h3>{K["model"].format(t=f["t"])}</h3>{specs_dl(f, L)}<p>{E(f["kz_tasks"])}</p><div class="fc-a"><a class="btn btn-p btn-s" href="tel:{PHONE_TEL}" data-call>{ui("phone")}{K["order"]}</a></div></div></article>''' for f in FLEET)
    perks = '<section class="perks"><div class="wrap"><ul>' + "".join(f'<li>{ph(i)}<span><b>{E(t)}</b><small>{E(s)}</small></span></li>' for (i, *_), (t, s) in zip(PERKS, K["perks"])) + "</ul></div></section>"
    svc = '<div class="scs">' + "".join(f'<div class="scd">{ph(s["icon"])}<b>{E(t)}</b><span>{E(d)}</span></div>' for s, (t, d) in zip(SERVICES, K["svc"])) + "</div>"
    why = '<div class="fac">' + "".join(f'<div><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in K["whys"]) + "</div>"
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t"><h1>{K["h1"]}</h1><p class="lead-t">{K["lead"]}</p>
{btns(msg, K["call"], K["wa"])}{hero_specs({"c": "жүккөтергіштік", "d": "борт ұзындығы", "b": "жебе ұзындығы", "h": "демалыссыз"})}</div>
<div class="hero-v">{img("hero", "Астанада 40 футтық контейнері бар 25 тонна манипулятор", "(max-width:767px) 100vw, 480px", eager=True)}</div></div></section>
{perks}
{sec(K["fleet"], '<div class="fcs">' + cards + "</div>", K["fleet_sub"], sid="tekhnika")}
{sec(K["fleet"] + " — " + K["btype"].lower(), compare_table(L), alt=True)}
{sec(K["services"], svc)}
{sec(K["how"], steps_html(K["steps"]), alt=True)}
{sec(K["why"], why)}
<section class="sec sec-alt"><div class="wrap"><div class="prose"><h2>{K["seo_h"]}</h2>{"".join(f"<p>{E(p)}</p>" for p in K["seo"])}<p><a href="/" hreflang="ru">{K["ru"]} →</a></p></div></div></section>
<section class="sec sec-dark" id="zayavka"><div class="wrap lead"><div><h2>{K["contacts"]}</h2><p>{K["area"]}</p>
<a class="lead-ph" href="tel:{PHONE_TEL}" data-call>{ui("phone")}{PHONE_DISPLAY}</a><p class="lead-h">{ui("clock")}{K["hours"]}</p>{btns(msg, K["call"], K["wa"])}</div></div></section>'''
    page("/kz/", K["title"], K["desc"], body, [service_schema("Астанада манипулятор жалдау", "/kz/", K["lead"])], prio="0.8", lang="kk", preload="hero")

def build_fleet():
    body = f'''{ph_hero("Манипуляторы в аренду в Астане", "Четыре модели: борт от 6 до 13 м, стрела от 10 до 17 м. Подберём технику под ваш груз.", [("Техника", "/manipulyatory/")], MSG, "m20", "Манипулятор 20 тонн в Астане")}
{sec("Сравнение моделей", compare_table(), "Название модели — по грузоподъёмности борта.")}
{sec("Модели", fleet_cards(), alt=True)}
{sec("Какой манипулятор выбрать", faq_html(FAQ[:1] + FAQ[4:6]))}{lead_form()}'''
    page("/manipulyatory/", f"Манипуляторы в аренду в Астане: 7–25 тонн | {BRAND}", "Сравнение манипуляторов 7, 12, 20 и 25 тонн: грузоподъёмность крана и борта, длина борта, вылет стрелы. Аренда в Астане круглосуточно.",
         body, crumbs=[("Техника", "/manipulyatory/")], prio="0.9", preload="m20")
    for f in FLEET:
        url = furl(f); others = [x for x in FLEET if x is not f]
        svcs = [s for s in SERVICES if f["t"] in s["fit"]]
        faq = [(f"Сколько стоит аренда манипулятора {f['t']} тонн?", FAQ[1][1]), (f"Сколько поднимает манипулятор {f['t']} тонн?",
                f"Кран поднимает до {f['crane']} т, борт перевозит до {f['board']} т. Длина борта — {f['deck']} м, вылет стрелы — {f['boom']} м."), FAQ[2], FAQ[3]]
        rows = [("Грузоподъёмность крана", f"{f['crane']} т"), ("Грузоподъёмность борта", f"{f['board']} т"), ("Длина борта", f"{f['deck']} м"), ("Вылет стрелы", f"{f['boom']} м"), ("Тип стрелы", f["boom_type"])]
        tbl = '<div class="tbl tbl-s"><table><tbody>' + "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows) + "</tbody></table></div>"
        body = f'''{ph_hero(E(f["h1"]), E(f["lead"]), [("Техника", "/manipulyatory/"), (f["name"], url)], f"Здравствуйте! Нужен манипулятор {f['t']} тонн.", f["img"], f"Манипулятор {f['t']} тонн в Астане")}
<section class="sec"><div class="wrap two"><div><h2>Характеристики</h2>{tbl}</div><div><h2>Для каких задач</h2>{checks(f["tasks"])}</div></div></section>
{sec("Услуги на этой технике", svc_cards(svcs), alt=True)}
{callout(f"Здравствуйте! Нужен манипулятор {f['t']} тонн.")}
{sec("Вопросы", faq_html(faq))}
{sec("Другие модели", fleet_cards(others), alt=True)}
{lead_form(f"Заказать манипулятор {f['t']} тонн", f["t"])}'''
        page(url, f"Манипулятор {f['t']} тонн в Астане — аренда | {BRAND}",
             f"Аренда манипулятора {f['t']} тонн в Астане: кран {f['crane']} т, борт {f['deck']} м, стрела {f['boom']} м. {f['lead']} Подача 1–2 часа, 24/7.",
             body, [service_schema(f"Аренда манипулятора {f['t']} тонн", url, f["lead"]), faq_schema(faq)], crumbs=[("Техника", "/manipulyatory/"), (f["name"], url)], prio="0.9", preload=f["img"])

def build_services():
    body = f'''{ph_hero("Услуги манипулятора в Астане", "Перевозка, погрузка, разгрузка и монтаж — полный спектр работ кран-манипулятора по Астане и до 100 км.", [("Услуги", "/uslugi/")], MSG, "g4", "Манипулятор с контейнером")}
{sec("Все услуги", svc_cards())}{sec("Как заказать", steps_html(), alt=True)}{lead_form()}'''
    page("/uslugi/", f"Услуги манипулятора в Астане | {BRAND}", "Услуги кран-манипулятора в Астане: доставка стройматериалов, перевозка контейнеров, монтаж, погрузка и разгрузка, срочная подача.",
         body, crumbs=[("Услуги", "/uslugi/")], prio="0.9", preload="g4")
    for s in SERVICES:
        url = surl(s); fits = [FL[t] for t in s["fit"]]
        faq = [("Какой манипулятор подходит для этой работы?", "Подходят модели: " + ", ".join(f"{t} т" for t in s["fit"]) + ". Точно подберём по весу и размерам груза."), FAQ[1], FAQ[2], FAQ[3]]
        body = f'''{ph_hero(E(s["h1"]), E(s["short"]), [("Услуги", "/uslugi/"), (s["name"], url)], f"Здравствуйте! Нужен манипулятор: {s['name'].lower()}.", fits[-1]["img"], f"{s['name']} манипулятором в Астане")}
<section class="sec"><div class="wrap two"><div class="prose">{"".join(f"<p>{E(p)}</p>" for p in s["body"])}</div><div><h2>Что делаем</h2>{checks(s["tasks"])}</div></div></section>
{sec("Подходящая техника", fleet_cards(fits), alt=True)}
{sec("Что сообщить при заявке", checks(ORDER_INFO))}
{callout(f"Здравствуйте! Нужен манипулятор: {s['name'].lower()}.")}
{sec("Вопросы", faq_html(faq), alt=True)}
{sec("Другие услуги", svc_cards([x for x in SERVICES if x is not s]))}
{lead_form(f"Заявка: {s['name'].lower()}", fits[0]["t"] if len(fits) == 1 else 0)}'''
        page(url, f"{s['h1']} | {BRAND}", f"{s['h1']}: {s['short']} Манипуляторы 7–25 т, подача 1–2 часа, круглосуточно.",
             body, [service_schema(s["h1"].replace(" в Астане", ""), url, s["short"]), faq_schema(faq)], crumbs=[("Услуги", "/uslugi/"), (s["name"], url)], prio="0.8", preload=fits[-1]["img"])

def build_districts():
    body = f'''{ph_hero("Манипулятор по районам Астаны", "Все районы города и пригороды в радиусе до 100 км.", [("Районы", "/rayony/")], MSG)}
{sec("Районы и пригороды", districts_html())}{lead_form()}'''
    page("/rayony/", f"Аренда манипулятора по районам Астаны | {BRAND}", "Манипулятор в районах Алматы, Байконыр, Есиль, Нура, Сарыарка, Сарайшык и в пригородах Астаны до 100 км.", body, crumbs=[("Районы", "/rayony/")], prio="0.7")
    for d in DISTRICTS + [dict(slug="prigorody", short="Пригороды", name="пригороды Астаны", loc="в пригородах Астаны",
                              about="Работаем в радиусе до 100 км от Астаны: " + ", ".join(SUBURBS) + ", дачные массивы и промзоны Акмолинской области.")]:
        url = f"/rayony/{d['slug']}/"
        faq = [(f"Работаете {d['loc']}?", "Да. Подача в течение 1–2 часов, круглосуточно." if d["slug"] != "prigorody" else "Да, в радиусе до 100 км от Астаны. Время подачи зависит от расстояния — уточним по телефону."), FAQ[0], FAQ[1]]
        body = f'''{ph_hero(f"Манипулятор {E(d['loc'])}", E(d["about"]), [("Районы", "/rayony/"), (d["short"], url)], f"Здравствуйте! Нужен манипулятор, {d['name']}.")}
{sec("Техника", fleet_cards())}{sec("Услуги", svc_cards(), alt=True)}{sec("Вопросы", faq_html(faq))}{sec("Другие районы", districts_html(d["slug"]), alt=True)}
{lead_form(f"Заказать манипулятор — {d['short']}")}'''
        page(url, f"Манипулятор {d['loc']} — аренда в Астане | {BRAND}", f"Аренда манипулятора {d['loc']}: 7–25 тонн, борт до 13 м. {d['about']}",
             body, [service_schema(f"Аренда манипулятора {d['loc']}", url, d["about"]), faq_schema(faq)], crumbs=[("Районы", "/rayony/"), (d["short"], url)], prio="0.6")

def build_articles():
    for a in ARTICLES:
        url = f"/stati/{a['slug']}/"
        parts = ["<ul>" + "".join(f"<li>{E(i)}</li>" for i in x) + "</ul>" if t == "ul" else f"<{t}>{E(x)}</{t}>" for t, x in a["body"]]
        body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Статьи", "/stati/"), (a["title"], url)])}<h1>{E(a["title"])}</h1><p class="lead-t">{E(a["desc"])}</p></div></section>
<section class="sec"><div class="wrap"><article class="prose">{"".join(parts)}{btns()}</article></div></section>
{sec("Другие статьи", article_cards(), alt=True)}{lead_form()}'''
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": TODAY, "dateModified": TODAY,
               "author": {"@id": SITE_URL + "/#org"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": SITE_URL + url, "inLanguage": "ru"}
        page(url, f"{a['title']} | {BRAND}", a["desc"], body, [sch], crumbs=[("Статьи", "/stati/"), (a["title"], url)], prio="0.5")
    body = f'''{ph_hero("Статьи", "Как выбрать манипулятор, подготовиться к заказу и чем манипулятор отличается от автокрана.", [("Статьи", "/stati/")])}{sec("Все статьи", article_cards())}'''
    page("/stati/", f"Статьи о манипуляторах | {BRAND}", "Как выбрать манипулятор по грузу, что подготовить перед заказом, манипулятор или автокран.", body, crumbs=[("Статьи", "/stati/")], prio="0.5")

def build_misc():
    body = f'''{ph_hero("Цены на аренду манипулятора", "Стоимость зависит от модели, времени работы, расстояния и сложности подачи. Назовём цену по телефону, когда уточним груз и адрес.", [("Цены", "/ceny/")], "Здравствуйте! Хочу узнать стоимость аренды манипулятора.")}
{sec("От чего зависит цена", factors_html())}{sec("Модели", compare_table(), alt=True)}{sec("Что сообщить для расчёта", checks(ORDER_INFO))}
{sec("Вопросы", faq_html(FAQ[:4]), alt=True)}{lead_form("Узнать стоимость")}'''
    page("/ceny/", f"Цены на аренду манипулятора в Астане | {BRAND}", "Стоимость аренды манипулятора в Астане: от чего зависит цена, модели 7–25 тонн. Расчёт по телефону и WhatsApp, круглосуточно.",
         body, [faq_schema(FAQ[:4])], crumbs=[("Цены", "/ceny/")], prio="0.8")
    body = f'''{ph_hero("Контакты", "Звоните или пишите в WhatsApp — отвечаем круглосуточно.", [("Контакты", "/kontakty/")])}
<section class="sec"><div class="wrap cont"><div><span>Телефон и WhatsApp</span><a href="tel:{PHONE_TEL}" data-call>{PHONE_DISPLAY}</a></div><div><span>Режим работы</span><b>{HOURS}</b></div><div><span>Где работаем</span><b>Астана и до 100 км</b></div></div></section>
{geo_sec()}{lead_form()}'''
    page("/kontakty/", f"Контакты — {BRAND}, аренда манипуляторов в Астане", f"Телефон и WhatsApp {PHONE_DISPLAY}. Аренда манипуляторов в Астане и в радиусе 100 км, круглосуточно.", body, crumbs=[("Контакты", "/kontakty/")], prio="0.6")
    body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Политика конфиденциальности", "/privacy-policy/")])}<h1>Политика конфиденциальности</h1></div></section>
<section class="sec"><div class="wrap"><div class="prose"><p>Сайт не хранит персональные данные на своих серверах. Имя, телефон и описание груза из формы передаются в WhatsApp только после того, как вы сами нажмёте кнопку отправки.</p>
<p>Вопросы в чате на сайте обрабатываются ИИ-консультантом для ответа и не используются для рекламы.</p>
<p>Для оценки рекламы используется Google Ads. Вопросы о данных можно задать по телефону {PHONE_DISPLAY}.</p></div></div></section>'''
    page("/privacy-policy/", f"Политика конфиденциальности — {BRAND}", "Как сайт обрабатывает данные формы заявки и чата.", body, crumbs=[("Политика конфиденциальности", "/privacy-policy/")], prio="0.2")
    body = f'''<section class="phd"><div class="wrap"><div class="phd-in"><h1>Страница не найдена</h1><p class="lead-t">Возможно, адрес изменился. Перейдите на главную или выберите технику.</p><div class="btns"><a class="btn btn-p" href="/">На главную</a><a class="btn btn-w" href="/manipulyatory/">Техника</a></div></div></div></section>'''
    page("/404", f"Страница не найдена — {BRAND}", "Страница не найдена.", body, prio="0")

def build_files():
    PAGES[:] = [p for p in PAGES if p[0] != "/404"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u, p in PAGES:
        alt = (f'<xhtml:link rel="alternate" hreflang="ru" href="{SITE_URL}/"/><xhtml:link rel="alternate" hreflang="kk" href="{SITE_URL}/kz/"/>' if u in ("/", "/kz/") else "")
        sm.append(f"<url><loc>{SITE_URL}{u}</loc>{alt}<lastmod>{TODAY}</lastmod><priority>{p}</priority></url>")
    (DIST / "sitemap.xml").write_text("\n".join(sm + ["</urlset>"]), encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "YandexBot", "Bingbot"]
    (DIST / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    ll = [f"# {BRAND} — {BRAND_SUB}", "", "> Аренда кран-манипуляторов 7, 12, 20 и 25 тонн в Астане и в радиусе до 100 км. Круглосуточно, без выходных. Подача в течение 1–2 часов.", "",
          f"- Телефон и WhatsApp: {PHONE_DISPLAY}", f"- Сайт: {SITE_URL}/ (казахская версия: {SITE_URL}/kz/)", "- Цена: рассчитывается по телефону после уточнения груза и адреса.", "", "## Техника (название — по грузоподъёмности борта)"]
    ll += [f"- Манипулятор {f['t']} т: кран {f['crane']} т, борт {f['deck']} м, вылет стрелы {f['boom']} м, стрела — {f['boom_type'][0].lower() + f['boom_type'][1:]}. {SITE_URL}{furl(f)}" for f in FLEET]
    ll += ["", "## Услуги"] + [f"- {s['name']}: {s['short']} {SITE_URL}{surl(s)}" for s in SERVICES]
    ll += ["", "## География", "- Районы Астаны: " + ", ".join(d["short"] for d in DISTRICTS), "- Пригороды до 100 км: " + ", ".join(SUBURBS), "", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ]
    ll += ["", "## Статьи"] + [f"- {a['title']}: {SITE_URL}/stati/{a['slug']}/" for a in ARTICLES]
    (DIST / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": f"{BRAND} — {BRAND_SUB}", "short_name": BRAND, "start_url": "/", "display": "standalone", "background_color": "#17181a", "theme_color": "#17181a",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    shutil.copytree(A, DIST / "assets", dirs_exist_ok=True)
    kb = {"phone": PHONE_DISPLAY, "fleet": [[f["t"], f["crane"], f["deck"], f["boom"], furl(f)] for f in FLEET], "svc": [[s["name"], surl(s)] for s in SERVICES]}
    js = (ROOT / "src" / "app.js").read_text(encoding="utf-8").replace("/*__KB__*/{}", json.dumps(kb, ensure_ascii=False))
    (DIST / "assets" / "app.js").write_text(js, encoding="utf-8")
    if (A / "favicon.ico").exists(): shutil.copy(A / "favicon.ico", DIST / "favicon.ico")

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_home(); build_kz(); build_fleet(); build_services(); build_districts(); build_articles(); build_misc(); build_files()
    print("pages:", len(PAGES))
