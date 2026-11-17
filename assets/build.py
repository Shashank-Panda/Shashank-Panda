"""Generates the profile SVGs (light + dark). Run: python assets/build.py"""
from pathlib import Path

OUT = Path(__file__).parent

THEMES = {
    "dark": dict(bg="#0F1A2E", panel="#16243D", grid="#22334F", ink="#E8EEF7",
                 muted="#8FA1BD", root="#5B6E8F", violet="#9B8CFF", amber="#F2B544",
                 teal="#3CC4B4", blue="#5AA2FF", rose="#FF6F7D", lock="#2A3B5A"),
    "light": dict(bg="#F6F8FC", panel="#FFFFFF", grid="#DCE3EE", ink="#14213A",
                  muted="#5A6B86", root="#8796B0", violet="#6A55E8", amber="#C9860F",
                  teal="#13897C", blue="#2369D6", rose="#D93A4B", lock="#E7ECF4"),
}

SANS = "-apple-system,'Segoe UI Variable Display','Segoe UI',system-ui,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'Cascadia Code','SF Mono',Menlo,Consolas,monospace"


def banner(t):
    W, H = 1200, 440
    names_x, bar_x0, bar_x1 = 56, 404, 1144
    span = bar_x1 - bar_x0
    top = 196
    row_h = 36
    # (name, detail, color, start%, width%, duration label)
    rows = [
        ("GET /shashank-panda", "", "root", 0.00, 1.00),
        ("relay.route", "cheapest model above the quality floor", "violet", 0.02, 0.38),
        ("booking.lock", "seat × 15 min, unique index", "amber", 0.11, 0.33),
        ("wallet.hold", "authorise now, capture once", "teal", 0.34, 0.29),
        ("outbox.dispatch", "claim, backoff, dead-letter", "blue", 0.49, 0.29),
        ("kiosk.alert", "spoken if the game is fullscreen", "rose", 0.59, 0.33),
    ]
    ticks = "".join(
        f'<line x1="{bar_x0 + span*i/4:.1f}" y1="{top-14}" x2="{bar_x0 + span*i/4:.1f}" '
        f'y2="{top + row_h*len(rows) - 6}" stroke="{t["grid"]}" stroke-width="1"/>'
        + (f'<text x="{bar_x0 + span*i/4 + 6:.1f}" y="{top-20}" class="tick">{60*i} ms</text>' if i < 4 else
         f'<text x="{bar_x0 + span*i/4 - 6:.1f}" y="{top-20}" class="tick" text-anchor="end">{60*i} ms</text>')
        for i in range(5)
    )
    body = []
    for i, (name, detail, col, s, w) in enumerate(rows):
        dur = f"{round(w*240)} ms"
        y = top + i * row_h
        x = bar_x0 + span * s
        bw = span * w
        delay = 0.35 + i * 0.22
        indent = 0 if i == 0 else 18
        c = t[col]
        dur_el = (f'<text x="{x + bw - 10:.1f}" y="{y + 14.5}" class="inbar" text-anchor="end" style="animation-delay:{delay + 0.35:.2f}s">{dur}</text>'
                  if i == 0 else
                  f'<text x="{x + bw + 8:.1f}" y="{y + 14.5}" class="dur" style="animation-delay:{delay + 0.35:.2f}s">{dur}</text>')
        guide = "" if i == 0 else (
            f'<path d="M{names_x+6} {top+20} V{y+10} H{names_x+14}" fill="none" '
            f'stroke="{t["grid"]}" stroke-width="1.5"/>')
        body.append(f'''
  <g class="row" style="animation-delay:{delay - 0.15:.2f}s">
    {guide}
    <text x="{names_x + indent}" y="{y + 15}" class="span">{name}</text>
    <rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="20" rx="4" fill="{c}" class="bar" style="animation-delay:{delay:.2f}s;transform-origin:{x:.1f}px {y+10}px"/>
    <text x="{x + 10:.1f}" y="{y + 14.5}" class="inbar" style="animation-delay:{delay + 0.35:.2f}s">{detail}</text>
    {dur_el}
  </g>''')
    sweep_end = top + row_h * len(rows) - 6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Shashank Shekhar Panda, backend and platform engineer. A trace waterfall listing things Shashank builds: LLM routing, booking locks, wallet holds, an outbox dispatcher and kiosk alerts.">
<style>
  .name {{ font: 700 46px {SANS}; fill: {t["ink"]}; letter-spacing: -0.5px; }}
  .role {{ font: 400 21px {SANS}; fill: {t["muted"]}; }}
  .span {{ font: 500 15px {MONO}; fill: {t["ink"]}; }}
  .tick {{ font: 400 12px {MONO}; fill: {t["muted"]}; }}
  .inbar {{ font: 600 12.5px {SANS}; fill: {t["bg"]}; animation: fade .4s ease-out both; }}
  .dur {{ font: 400 12.5px {MONO}; fill: {t["muted"]}; animation: fade .4s ease-out both; }}
  .row {{ animation: fade .3s ease-out both; }}
  .bar {{ animation: grow .7s cubic-bezier(.2,.8,.2,1) both; }}
  .cursor {{ animation: sweep 2.1s cubic-bezier(.45,0,.2,1) .3s forwards; opacity: 0; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  @keyframes sweep {{ 0% {{ opacity: .9; transform: translateX(0); }} 90% {{ opacity: .9; }} 100% {{ opacity: 0; transform: translateX({span}px); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .row, .inbar, .dur {{ animation: none; }}
    .bar {{ animation: none; }}
    .cursor {{ display: none; }}
  }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<text x="{names_x}" y="92" class="name">Shashank Shekhar Panda</text>
<text x="{names_x}" y="130" class="role">Backend &amp; platform engineer. I build the parts that have to be right: money, time and messages.</text>
<rect x="{names_x - 20}" y="{top - 44}" width="{W - 2*(names_x-20)}" height="{row_h*len(rows) + 64}" rx="12" fill="{t["panel"]}"/>
{ticks}
{"".join(body)}
<line x1="{bar_x0}" y1="{top-14}" x2="{bar_x0}" y2="{sweep_end}" stroke="{t["ink"]}" stroke-width="1.5" class="cursor"/>
</svg>
'''


def card_frame(t, title, blurb_lines, inner, label):
    W, H = 600, 330
    blurb = "".join(
        f'<text x="32" y="{88 + 22*i}" class="blurb">{line}</text>' for i, line in enumerate(blurb_lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
<style>
  .title {{ font: 700 26px {SANS}; fill: {t["ink"]}; }}
  .blurb {{ font: 400 15px {SANS}; fill: {t["muted"]}; }}
  .lbl {{ font: 500 13px {MONO}; fill: {t["ink"]}; }}
  .sm {{ font: 400 12px {MONO}; fill: {t["muted"]}; }}
  .on {{ font: 600 12px {SANS}; fill: {t["bg"]}; }}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{t["panel"]}" stroke="{t["grid"]}" stroke-width="1.5"/>
<text x="32" y="54" class="title">{title}</text>
{blurb}
{inner}
</svg>
'''


def relay_card(t):
    # app -> relay -> providers; one chosen route highlighted, ledger strip below
    v, g = t["violet"], t["grid"]
    providers = [("ollama/llama3", 154, False), ("openai/gpt-mini", 196, True), ("anthropic/opus", 238, False)]
    paths = "".join(
        f'<path d="M308 196 C 345 196, 345 {y}, 382 {y}" fill="none" stroke="{v if on else g}" '
        f'stroke-width="{2.5 if on else 1.5}"/>'
        f'<rect x="382" y="{y-15}" width="186" height="30" rx="6" fill="{v if on else t["bg"]}" '
        f'stroke="{v if on else g}" stroke-width="1.5"/>'
        f'<text x="396" y="{y+5}" class="{"on" if on else "lbl"}">{name}</text>'
        for name, y, on in providers)
    inner = f'''
<rect x="32" y="181" width="96" height="30" rx="6" fill="{t["bg"]}" stroke="{g}" stroke-width="1.5"/>
<text x="46" y="201" class="lbl">your app</text>
<path d="M128 196 H176" stroke="{v}" stroke-width="2.5"/>
<rect x="176" y="170" width="132" height="52" rx="8" fill="{t["bg"]}" stroke="{v}" stroke-width="2"/>
<text x="192" y="193" class="lbl">relay</text>
<text x="192" y="211" class="sm">classify, route</text>
{paths}
<line x1="32" y1="270" x2="568" y2="270" stroke="{g}"/>
<text x="32" y="296" class="sm">Every swap is disclosed in a header. Shadow mode logs what it would</text>
<text x="32" y="314" class="sm">have saved before you let it change anything.</text>'''
    return card_frame(t, "LLM-Relay", [
        "An OpenAI-compatible gateway in Go. It finds the cheapest model",
        "that still clears your quality floor, and proves the saving first."], inner,
        "LLM-Relay: an app calls Relay, which routes to the cheapest of Ollama, OpenAI or Anthropic that meets the quality floor.")


def rushbee_card(t):
    # seat x 15-min bucket lock grid with one rejected double-booking
    a, g = t["amber"], t["grid"]
    cols = ["18:00", "18:15", "18:30", "18:45", "19:00"]
    seats = ["PC-01", "PC-02", "PC-03"]
    booked = {(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1)}
    x0, y0, cw, ch = 104, 168, 70, 26
    cells = []
    for c, label in enumerate(cols):
        cells.append(f'<text x="{x0 + c*cw + 6}" y="{y0 - 10}" class="sm">{label}</text>')
    for r, seat in enumerate(seats):
        cells.append(f'<text x="32" y="{y0 + r*(ch+8) + 18}" class="lbl">{seat}</text>')
        for c in range(len(cols)):
            on = (r, c) in booked
            cells.append(
                f'<rect x="{x0 + c*cw}" y="{y0 + r*(ch+8)}" width="{cw-6}" height="{ch}" rx="5" '
                f'fill="{a if on else t["lock"]}"/>')
    # rejected attempt on PC-02 18:45
    rx, ry = x0 + 4*cw, y0 + 1*(ch+8)
    cells.append(
        f'<rect x="{rx-3}" y="{ry-3}" width="{cw}" height="{ch+6}" rx="7" fill="none" '
        f'stroke="{t["rose"]}" stroke-width="2.5" stroke-dasharray="5 4"/>'
        f'<text x="{rx + cw + 8}" y="{ry + 12}" class="lbl" style="fill:{t["rose"]}">409 conflict</text>'
        f'<text x="{rx + cw + 8}" y="{ry + 28}" class="sm">second booking</text>')
    inner = "".join(cells) + f'''
<line x1="32" y1="270" x2="568" y2="270" stroke="{g}"/>
<text x="32" y="296" class="sm">One lock row per seat per 15 minutes under a unique index, so a</text>
<text x="32" y="314" class="sm">second booking for the same slot fails in the database itself.</text>'''
    return card_frame(t, "RushBee", [
        "Software that runs gaming cafés: live sessions, wallets, bookings,",
        "food orders and a kiosk on every gaming PC."], inner,
        "RushBee: a grid of seats by 15-minute buckets; a second booking for a taken slot is rejected with 409.")


for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t), encoding="utf-8")
    (OUT / f"relay-{name}.svg").write_text(relay_card(t), encoding="utf-8")
    (OUT / f"rushbee-{name}.svg").write_text(rushbee_card(t), encoding="utf-8")
print("ok")
