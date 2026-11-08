# -*- coding: utf-8 -*-
"""Google Ads alispec.kz для веб-интерфейса: Инструменты → Массовые действия → Загрузки (xlsx).
Только рентабельные запросы: 11 ключей, фразовое соответствие, кампания ограничена Астаной. Запуск: python3 src/ads.py → google-ads/"""
import sys
from pathlib import Path
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font
sys.path.insert(0, str(Path(__file__).parent))
from data import SITE_URL, PHONE_DISPLAY

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "google-ads"
CAMP = "AliSpec Манипулятор Поиск"
NEG_LIST = "AliSpec минус-слова"
GEO = "Astana, Kazakhstan"
BUDGET = 10
ERR = []
COMMON_H = ["Подача за 1–2 часа", "Круглосуточно, без выходных", "Манипуляторы 7–25 тонн", "Борт до 13 м, стрела до 17 м", "Операторы с допусками",
            "Астана и пригороды до 100 км", "Контейнеры 20 и 40 футов", "Подача через забор", "Звоните — подберём технику", "AliSpec — манипуляторы"]
COMMON_D = ["Манипуляторы 7, 12, 20 и 25 тонн. Борт до 13 м, стрела до 17 м. Подача за 1–2 часа.",
            "Работаем круглосуточно по Астане и в радиусе 100 км. Операторы с допусками. Звоните!"]
# (группа, URL, ключи-фразы, свои заголовки, 2 описания, path1)
G = [("Аренда манипулятора", "/", ["аренда манипулятора", "услуги манипулятора", "заказать манипулятор", "кран манипулятор аренда", "манипулятор астана"],
      ["Аренда манипулятора в Астане", "Услуги манипулятора", "Заказать манипулятор", "Кран-манипулятор в аренду", "Манипулятор 24/7 в Астане"],
      ["Аренда кран-манипулятора в Астане: перевозка, погрузка, разгрузка и монтаж грузов.",
       "Подберём манипулятор под вес и длину груза. Подача в течение 1–2 часов, круглосуточно."], "манипулятор"),
     ("Кран-борт", "/manipulyatory/", ["кран борт астана", "аренда кран борта"],
      ["Кран-борт в Астане", "Аренда кран-борта", "Кран-борт 7, 12, 20, 25 тонн", "Длинный борт до 13 метров", "Сравните модели на сайте"],
      ["Кран-борт в аренду в Астане: 7, 12, 20 и 25 тонн, борт до 13 м, стрела до 17 м.",
       "Стройматериалы, ЖБИ, металлоконструкции, бытовки и оборудование. Подача 1–2 часа."], "кран-борт"),
     ("Манипулятор 25 тонн", "/manipulyatory/manipulyator-25-tonn/", ["манипулятор 25 тонн"],
      ["Манипулятор 25 тонн в Астане", "Борт 13 м, стрела 17 м", "Для 40-футовых контейнеров", "Негабарит и оборудование", "Монтаж металлоконструкций"],
      ["Манипулятор 25 тонн: борт 13 м, Z-образная стрела 17 м. Контейнеры 40 футов и негабарит.",
       "Тяжёлое оборудование, модульные здания, металлоконструкции. Круглосуточно по Астане."], "25-тонн"),
     ("Контейнеры и бытовки", "/uslugi/perevozka-kontejnerov/", ["перевозка контейнера манипулятором", "перевозка контейнеров астана", "перевозка бытовки"],
      ["Перевозка контейнеров", "Контейнер 40 футов на объект", "Перевозка бытовок в Астане", "Установка на объект краном", "Вагончики и блок-модули"],
      ["Грузим, перевозим и ставим на место контейнеры 20 и 40 футов, бытовки и вагончики.",
       "Манипулятор сам грузит и разгружает — отдельный кран не нужен. Подача 1–2 часа."], "контейнеры")]
NEG = ["вакансия", "вакансии", "работа", "работу", "требуется", "требуются", "резюме", "зарплата", "водитель манипулятора", "машинист",
       "купить", "продажа", "продам", "бу", "б/у", "olx", "крыша", "kaspi", "каспи", "цена нового", "лизинг", "ремонт", "запчасти", "гидравлика",
       "обучение", "курсы", "удостоверение", "своими руками", "чертеж", "чертёж", "схема", "игрушка", "лего", "робот", "промышленный", "медицинский",
       "алматы", "шымкент", "караганда", "кокшетау", "павлодар", "актобе", "атырау", "костанай",
       "автовышка", "эвакуатор", "экскаватор", "погрузчик", "автокран", "газель", "грузчики", "грузчик", "самосвал"]
def chk(t, n, what):
    if len(t) > n: ERR.append(f"{what} >{n}: {t} ({len(t)})")
    return t
def headlines(hs):
    out = []
    for t in hs + COMMON_H:
        if t.lower() not in {x.lower() for x in out}: out.append(t)
    return out[:15]
def xlsx(path, cols, rows):
    wb = Workbook(); ws = wb.active; ws.title = "Upload"; ws.append(cols)
    for c in ws[1]: c.font = Font(bold=True)
    for r in rows: ws.append([r.get(c, "") for c in cols])
    wb.save(path)
def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*"):
        if f.is_file(): f.unlink()
    H = [f"Headline {i}" for i in range(1, 16)]; D = [f"Description {i}" for i in range(1, 5)]
    grp, kws, ads, txt = [], [], [], []
    for name, path, base, hs, ds, p1 in G:
        grp.append({"Action": "Add", "Campaign": CAMP, "Ad group": name, "Ad group state": "Enabled"})
        for b in base:
            kws.append({"Action": "Add", "Campaign": CAMP, "Ad group": name, "Keyword": f'"{b}"'})
            for n in NEG:
                if f" {n} " in f" {b} ": ERR.append(f"минус «{n}» режет «{b}»")
        heads = headlines(hs); descs = ds + COMMON_D
        if len(heads) != 15: ERR.append(f"{name}: заголовков {len(heads)}")
        r = {"Action": "Add", "Campaign": CAMP, "Ad group": name, "Ad type": "Responsive search ad", "Final URL": SITE_URL + path, "Path 1": chk(p1, 15, "path"), "Path 2": "астана"}
        for i, h in enumerate(heads): r[H[i]] = chk(h, 30, "headline")
        for i, d in enumerate(descs): r[D[i]] = chk(d, 90, "description")
        ads.append(r)
        txt += [f"Группа: {name}", f"URL: {SITE_URL}{path}", "Ключи: " + ", ".join(f'"{b}"' for b in base), "Заголовки: " + " | ".join(heads), "Описания: " + " | ".join(descs), ""]
    if len(kws) > 15: ERR.append("больше 15 ключей")
    if ERR: print("\n".join(ERR)); raise SystemExit(1)
    wb = openpyxl.load_workbook(ROOT / "src" / "templates" / "Create_New_Campaigns.xlsx")
    for n in list(wb.sheetnames):
        if n.startswith("(Example)"): del wb[n]
    ws = wb[wb.sheetnames[0]]; hdr = [c.value for c in ws[2]]
    if "EU political ads" not in hdr:
        ws.cell(1, len(hdr) + 1, "#Required: EU political ads"); ws.cell(2, len(hdr) + 1, "EU political ads"); hdr.append("EU political ads")
    r = {"Action": "Add", "Campaign status": "Paused", "Campaign": CAMP, "Campaign type": "Search", "Networks": "Google search", "Budget": BUDGET,
         "Budget type": "Daily", "Bid strategy type": "Maximize clicks", "Location": GEO, "EU political ads": "No"}
    ws.append([r.get(h) for h in hdr]); wb.save(OUT / "0-sozdat-kampaniyu.xlsx")
    xlsx(OUT / "1-gruppy.xlsx", ["Action", "Campaign", "Ad group", "Ad group state"], grp)
    xlsx(OUT / "2-klyuchevye-slova.xlsx", ["Action", "Campaign", "Ad group", "Keyword"], kws)
    xlsx(OUT / "3-obyavleniya.xlsx", ["Action", "Campaign", "Ad group", "Ad type"] + H + D + ["Path 1", "Path 2", "Final URL"], ads)
    xlsx(OUT / "4-minus-slova-v-spisok.xlsx", ["Action", "Negative keyword list name", "Negative keyword", "Keyword or list", "Match type"],
         [{"Action": "Add", "Negative keyword list name": NEG_LIST, "Negative keyword": n, "Keyword or list": "Keyword", "Match type": "Phrase Match"} for n in NEG])
    xlsx(OUT / "5-privyazat-spisok-k-kampanii.xlsx", ["Action", "Negative keyword", "Keyword or list", "Campaign"], [{"Action": "Add", "Negative keyword": NEG_LIST, "Keyword or list": "List", "Campaign": CAMP}])
    head = [f"КАМПАНИЯ: {CAMP} (файл 0, на паузе). Местоположение: Астана, «Присутствие». Бюджет: {BUDGET} в день.", f"Групп: {len(grp)}, ключей: {len(kws)} (фраза), минус-слов: {len(NEG)}.", ""]
    ext = ["РЕСУРСЫ (вручную): уточнения — Подача за 1–2 часа · Круглосуточно · Борт до 13 м · Стрела до 17 м · Операторы с допусками · Астана и до 100 км",
           "Быстрые ссылки: Манипулятор 25 т — /manipulyatory/manipulyator-25-tonn/ · Сравнить модели — /manipulyatory/ · Перевозка контейнеров — /uslugi/perevozka-kontejnerov/ · Цены — /ceny/",
           f"Звонок: {PHONE_DISPLAY}", "", "НАСТРОЙКИ: только Google Поиск (без партнёров и КМС); AI Max и широкое соответствие — выкл.; через 2–3 дня чистить поисковые запросы."]
    (OUT / "6-teksty-i-nastroyki.txt").write_text("\n".join(head + txt + ext) + "\n", encoding="utf-8")
    print("групп", len(grp), "ключей", len(kws), "минус", len(NEG))
if __name__ == "__main__":
    main()
