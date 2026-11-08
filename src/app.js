(function () {
  "use strict";
  var KB = /*__KB__*/{};
  var CFG = window.CFG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function waUrl(t) { return "https://wa.me/" + CFG.wan + "?text=" + encodeURIComponent(t); }

  /* ---------- тег Google: очередь сразу, сам скрипт — после первого действия посетителя (касание, прокрутка, клавиша) — не мешает скорости загрузки ---------- */
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  if (CFG.ads) {
    window.gtag("js", new Date()); window.gtag("config", CFG.ads);
    var gl = false;
    var loadTag = function () {
      if (gl) return; gl = true;
      var sc = document.createElement("script"); sc.async = true; sc.src = "https://www.googletagmanager.com/gtag/js?id=" + CFG.ads; document.head.appendChild(sc);
    };
    ["pointerdown", "keydown", "scroll", "touchstart"].forEach(function (ev) { window.addEventListener(ev, loadTag, { once: true, passive: true }); });
  }
  /* ---------- конверсии Google Ads ---------- */
  function conv(kind) {
    var label = kind === "call" ? CFG.call : kind === "form" ? (CFG.form || CFG.wa) : CFG.wa;
    if (CFG.ads && label) window.gtag("event", "conversion", { send_to: CFG.ads + "/" + label, value: 1.0, currency: "USD", transport_type: "beacon" });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    var h = a.getAttribute("href") || "";
    if (h.indexOf("tel:") === 0) conv("call");
    else if (h.indexOf("wa.me") > -1) conv("wa");
  });

  /* ---------- меню ---------- */
  var burger = $(".burger"), nav = $("#nav");
  function setNav(o) {
    if (!burger || !nav) return;
    nav.classList.toggle("open", o); burger.setAttribute("aria-expanded", o ? "true" : "false");
    burger.setAttribute("aria-label", o ? "Закрыть меню" : "Открыть меню"); document.body.classList.toggle("lock", o);
  }
  if (burger) burger.addEventListener("click", function () { setNav(!nav.classList.contains("open")); });
  if (nav) nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 1180) setNav(false); });

  /* ---------- назад / наверх ---------- */
  var fab = $(".fab");
  var ftr = $(".ftr");
  function onScroll() {
    if (fab) fab.classList.toggle("on", window.pageYOffset > 500);
    // у самого низа страницы плавающие кнопки становятся полупрозрачными, чтобы не закрывать подвал
    var end = ftr ? ftr.getBoundingClientRect().top < window.innerHeight - 40 : false;
    document.body.classList.toggle("at-end", end);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); requestAnimationFrame(onScroll);
  $$("[data-top]").forEach(function (b) { b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); }); });
  $$("[data-back]").forEach(function (b) {
    b.addEventListener("click", function () {
      var ref = document.referrer, same = ref && ref.indexOf(location.host) > -1;
      if (same && history.length > 1) history.back(); else location.href = "/";
    });
  });

  /* ---------- заявка → WhatsApp (+ расширенные конверсии: телефон передаётся в Google в хешированном виде) ---------- */
  function e164(ph) { var d = ph.replace(/\D/g, ""); if (d.length === 11 && d[0] === "8") d = "7" + d.slice(1); if (d.length === 10) d = "7" + d; return "+" + d; }
  $$("form[data-lead]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ph = (f.elements.phone.value || "").replace(/[^\d+]/g, ""), err = $(".f-err", f);
      if (ph.replace(/\D/g, "").length < 10) { err.hidden = false; f.elements.phone.focus(); return; }
      err.hidden = true;
      var t = "Здравствуйте! Заявка с сайта.\nТехника: " + f.elements.job.value + "\nКогда: " + f.elements.when.value +
        (f.elements.msg.value.trim() ? "\nГруз и адрес: " + f.elements.msg.value.trim() : "") +
        (f.elements.name.value.trim() ? "\nИмя: " + f.elements.name.value.trim() : "") + "\nТелефон: " + ph;
      if (typeof window.gtag === "function") window.gtag("set", "user_data", { phone_number: e164(ph) });
      conv("form");
      window.open(waUrl(t), "_blank", "noopener");
    });
  });

  /* ---------- чат: ИИ через /api/chat, без ключа — встроенный автоответчик ---------- */
  var chat = $("#chat"), list = chat && $(".chat-l", chat), qbox = chat && $(".chat-q", chat), opener = $(".chat-o");
  var hist = [], started = false, busy = false;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function add(text, who, html) {
    var d = document.createElement("div"); d.className = "msg " + (who === "u" ? "msg-u" : "msg-b");
    if (html) d.innerHTML = html; else d.textContent = text;
    list.appendChild(d); list.scrollTop = list.scrollHeight; return d;
  }
  function quick(items) {
    qbox.innerHTML = "";
    items.forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { ask(q); }); qbox.appendChild(b); });
  }
  function low(s) { return s.toLowerCase().replace(/ё/g, "е"); }
  // встроенный автоответчик: работает без ИИ-ключа и при сбое сети
  var INTENTS = [
    [/цен|стоим|сколько стоит|прайс|почем|по чем|тариф|за час|за смену|дорого|расцен/, "Стоимость зависит от модели, времени работы, расстояния и сложности подачи. Назовём цену по телефону " + KB.phone + " или в WhatsApp, когда уточним груз и адрес.", "/ceny/"],
    [/контейнер|40 фут|20 фут|морск/, "Контейнеры 20 и 40 футов перевозим манипулятором 25 тонн: борт 13 м, стрела 17 м. Для 20-футовых подходит и 20 тонн с бортом 10 м.", "/uslugi/perevozka-kontejnerov/"],
    [/срочн|сегодня|сейчас|быстро|когда можете|через сколько|ночь|ночью|выходн|праздн/, "Подаём манипулятор в течение 1–2 часов после заявки. Работаем круглосуточно, без выходных и праздников. Позвоните " + KB.phone + "."],
    [/за город|пригород|косшы|коянды|талапкер|акмол|аршалы|шортанды|область|км/, "Работаем по всей Астане и в радиусе до 100 км: Косшы, Коянды, Талапкер, Акмол, Аршалы, Шортанды, дачи и промзоны.", "/rayony/prigorody/"],
    [/забор|крыш|через|высот|труднодоступ/, "Стрела с вылетом до 17 метров подаёт груз через заборы, на крыши и в труднодоступные места. Опишите место — подберём модель."],
    [/кольц|септик|колод/, "Бетонные кольца и септики привозим и устанавливаем — обычно хватает манипулятора 7 или 12 тонн.", "/uslugi/montazhnye-raboty/"],
    [/кирпич|блок|поддон|плит|стройматер|металлопрокат|арматур/, "Стройматериалы привозим и разгружаем краном прямо на место. Поддоны и кирпич — манипулятор 7 или 12 тонн, плиты и длинномер — 20 или 25 тонн.", "/uslugi/dostavka-strojmaterialov/"],
    [/бытовк|вагончик|модул/, "Бытовки и вагончики перевозим и ставим на место манипулятором 12 или 20 тонн, блок-модули — 25 тонн.", "/uslugi/perevozka-kontejnerov/"],
    [/оборудован|станок|станки|генератор|трансформатор/, "Оборудование и станки грузим, перевозим и разгружаем. Тяжёлое и негабаритное — манипулятор 25 тонн.", "/uslugi/pogruzka-razgruzka/"],
    [/допуск|оператор|водител|безопасн/, "Все водители-операторы имеют допуски и опыт работы с кран-манипуляторами на стройках и промышленных объектах."],
    [/автокран|кран нужен|башенн/, "Манипулятор сам грузит, везёт и разгружает. Если груз очень тяжёлый или нужен подъём на большую высоту — нужен автокран. Опишите задачу, подскажем.", "/stati/manipulyator-ili-avtokran/"],
    [/юр\.|юрлиц|тоо|(^|\s)ип(\s|$)|договор|ндс|счет|счёт|безнал|налич|оплат|kaspi|каспи/, "Условия оплаты и документы для организаций уточнит менеджер по телефону " + KB.phone + "."],
    [/(^|\s)бот|робот|ты кто|живой|человек|оператор/, "Я ИИ-консультант сайта. Диспетчер ответит по телефону или в WhatsApp — кнопка ниже."],
    [/спасиб|рахмет|благодар/, "Пожалуйста! Позвоните или напишите в WhatsApp — подадим технику."],
    [/привет|здравств|салем|сәлем|добрый|ассалам/, "Здравствуйте! Подскажу по аренде манипулятора в Астане. Какой груз нужно перевезти?"]
  ];
  function local(q) {
    var s = low(q);
    if (s.replace(/\D/g, "").length >= 10) return { t: "Спасибо! Чтобы заявка точно дошла, отправьте номер в WhatsApp кнопкой ниже." };
    var m = s.match(/(\d{1,2})\s*(т|тонн|тн)/), fl = KB.fleet || [];
    if (m) {
      var w = +m[1], pick = null;
      for (var i = 0; i < fl.length; i++) if (fl[i][0] === w) pick = fl[i];
      if (!pick) for (var j = 0; j < fl.length; j++) if (fl[j][0] >= w) { pick = fl[j]; }
      if (pick) return { t: "Манипулятор " + pick[0] + " тонн: борт везёт до " + pick[0] + " т (длина " + pick[2] + " м), кран поднимает до " + pick[1] + " т, вылет стрелы " + pick[3] + " м. Если груз нужно поднимать краном целиком — назовите вес и размеры, подберём точнее.", u: pick[4] };
      return { t: "Самый крупный манипулятор в парке — 25 тонн (борт 13 м). Если груз тяжелее, позвоните " + KB.phone + " — подскажем решение." };
    }
    for (var k = 0; k < INTENTS.length; k++) if (INTENTS[k][0].test(s)) return { t: INTENTS[k][1], u: INTENTS[k][2] };
    return { t: "Опишите груз (вес, размеры) и адрес — подберём манипулятор. Или позвоните " + KB.phone + "." };
  }
  function reply(r) {
    var h = esc(r.t) + (r.u ? '<br><a href="' + r.u + '">Открыть страницу</a>' : "");
    add("", "b", h);
  }
  function ask(q) {
    q = String(q || "").trim(); if (!q || busy) return;
    add(q, "u"); hist.push({ role: "user", content: q });
    busy = true; var wait = add("…", "b");
    var done = function (txt) { busy = false; wait.remove(); hist.push({ role: "assistant", content: txt }); add(txt, "b"); };
    var ctrl = window.AbortController ? new AbortController() : null; var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-12), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { clearTimeout(to); if (!r.ok) throw 0; return r.json(); })
      .then(function (d) { if (!d || !d.text) throw 0; done(d.text); })
      .catch(function () { busy = false; wait.remove(); var r = local(q); hist.push({ role: "assistant", content: r.t }); reply(r); if (qbox) qbox.innerHTML = ""; });
  }
  function openChat() {
    chat.hidden = false; if (opener) opener.hidden = true;
    if (!started) { started = true; add("Здравствуйте! Я ИИ-консультант AliSpec. Подскажу, какой манипулятор подойдёт под ваш груз. Что нужно перевезти?", "b"); quick(["Сколько стоит?", "Контейнер 40 футов", "Бетонные кольца", "Как быстро подадите?", "За город", "Какой манипулятор выбрать?"]); }
    setTimeout(function () { var i = $("input", chat); if (i && window.innerWidth > 767) i.focus(); }, 50);
  }
  if (chat) {
    $$("[data-chat]").forEach(function (b) { b.addEventListener("click", openChat); });
    $("[data-chat-x]", chat).addEventListener("click", function () { chat.hidden = true; if (opener) opener.hidden = false; });
    $(".chat-f", chat).addEventListener("submit", function (e) { e.preventDefault(); var i = this.elements.q; ask(i.value); i.value = ""; });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (chat && !chat.hidden) { chat.hidden = true; if (opener) opener.hidden = false; }
    setNav(false);
  });
})();
