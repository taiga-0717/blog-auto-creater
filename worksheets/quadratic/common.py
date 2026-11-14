"""ページ共通の HTML 部品"""
from qlib import fr, num, bl, R

CSS = """
<style>
  body { font-size: 11.2pt; }
  .vt { border-collapse: collapse; margin: 1mm 0; font-size: 11.5pt; }
  .vt td, .vt th { border: .35mm solid #222; height: 9mm; min-width: 11.5mm; text-align: center; padding: 0 1mm; }
  .vt th { background: #ececec; font-weight: 700; min-width: 9mm; }
  .vt td.blank { background: #fff; }
  .vt td.ans { font-weight: 700; text-decoration: underline; }
  .expl { border: .45mm solid #222; border-radius: 2mm; padding: 2.5mm 4mm; background: #f6f6f6; }
  .expl h3 { margin: 0 0 1.2mm; font-size: 12.5pt; }
  .key { border: .5mm solid #222; background: #fff; border-radius: 1.5mm; padding: 1.5mm 3mm; margin: 1.5mm 0; font-size: 11.5pt; }
  .key b.big { font-size: 15pt; letter-spacing: .03em; }
  .warn { border: .35mm dashed #222; border-radius: 1.5mm; padding: 1mm 2.5mm; margin-top: 1.5mm; font-size: 10.3pt; background: #fff; }
  .warn::before { content: "⚠ 注意"; font-weight: 700; margin-right: 2mm; }
  .stp { display: inline-block; background: #222; color: #fff; border-radius: 1mm; padding: 0 1.8mm; font-size: 9.5pt; font-weight: 700; margin-right: 1.5mm; }
  .qg { display: grid; gap: 2.5mm; }
  .qg2 { grid-template-columns: repeat(2, 1fr); }
  .qg3 { grid-template-columns: repeat(3, 1fr); }
  .qg4 { grid-template-columns: repeat(4, 1fr); }
  .qc { border: .3mm solid #777; border-radius: 1.5mm; padding: 1.2mm 2mm; display: flex; flex-direction: column; min-height: 0; }
  .qc .t { font-size: 10.6pt; line-height: 1.4; }
  .qc .sp { flex: 1; min-height: 6mm; font-size: 7.8pt; color: #888; }
  .qc .ansbox { align-self: flex-end; height: 9mm; min-width: 34mm; }
  .grow { flex: 1; min-height: 0; }
  .q > .grow:not(.row):not(.qg) { display: flex; flex-direction: column; }
  .lead { font-size: 10.4pt; color: #222; margin-bottom: 1.5mm; }
  .tiny { font-size: 9pt; color: #555; }
  .center { display: flex; justify-content: center; align-items: center; }
  .cmp { border-collapse: collapse; width: 100%; font-size: 10.5pt; }
  .cmp td, .cmp th { border: .3mm solid #444; padding: 1mm 2mm; text-align: center; }
  .cmp th { background: #222; color: #fff; }
  .ans .q { padding: 2.2mm 3.5mm; }
  .ans .pf p { margin: .2mm 0; }
  .aline { margin: .6mm 0; }
  .aline b.no { display: inline-block; min-width: 8mm; }
  .eq { font-size: 11.5pt; letter-spacing: .02em; }
  .ag { display: grid; gap: 2mm 4mm; }
  .ag2 { grid-template-columns: 1fr 1fr; }
  .ag3 { grid-template-columns: 1fr 1fr 1fr; }
  .abox { border: .3mm solid #888; border-radius: 1.5mm; padding: 1.2mm 2.2mm; font-size: 10pt; line-height: 1.5; }
  .abox .h { font-weight: 700; font-size: 10.6pt; }
  .figrow { display: flex; gap: 3mm; align-items: flex-start; }
  .note { font-size: 9.6pt; }
  sup { font-size: .7em; }
  section.ans { font-size: 11.2pt; }
  .ans .note, .ans .abox, .ans .pt { font-size: 10.9pt; line-height: 1.6; }
  .ans .abox .h { font-size: 11.5pt; }
  .ans .qh { font-size: 12.5pt; }
</style>
"""

HEAD = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="style.css">""" + CSS + "</head><body>\n"

NAME = """<div class="name"><div>組<span class="w1"></span></div><div>番<span class="w1"></span></div>
      <div>名前<span class="w2"></span></div>{score}</div>"""


def page(no, title, tag, body, name=True, pts=None, right=None, cls=""):
    score = (f'<div class="score">/ {pts}点</div>' if pts else
             '<div class="score" style="width:46mm;flex-direction:column;align-items:flex-start;justify-content:space-between"><span style="font-size:8.5pt">できた度（☆をぬろう）</span><span style="font-size:12pt;letter-spacing:1.5mm">☆☆☆☆☆</span></div>')
    rgt = right if right is not None else (NAME.format(score=score) if name else "")
    return f"""<section class="page {cls}">
  <div class="head">
    <div class="ttl"><small>中学3年 数学 ／ 関数 y＝ax²　　シート {no}</small><b>{title} <span class="tag">{tag}</span></b></div>
    {rgt}
  </div>
  {body}
</section>
"""


def vtable(xs, ys=None, ylab="y", ans=False, xlab="x"):
    """値の表。ys の要素が None なら空欄"""
    tr1 = f"<tr><th>{xlab}</th>" + "".join(f"<td>{num(x)}</td>" for x in xs) + "</tr>"
    cells = []
    for i, x in enumerate(xs):
        v = None if ys is None else ys[i]
        if v is None:
            cells.append('<td class="blank"></td>')
        else:
            cells.append(f'<td class="{"ans" if ans else ""}">{v if isinstance(v, str) else num(v)}</td>')
    tr2 = f"<tr><th>{ylab}</th>" + "".join(cells) + "</tr>"
    return f'<table class="vt">{tr1}{tr2}</table>'


def qc(no, text, ans="", unit="", sp="計算", minh=None):
    st = f' style="min-height:{minh}mm"' if minh else ""
    box = f'<div class="ansbox">{ans or '<span class="tiny">答え</span>'}<span style="flex:1"></span>{unit}</div>'
    return f'<div class="qc"{st}><div class="t"><b>({no})</b> {text}</div><div class="sp">{sp}</div>{box}</div>'


def qh(no, title, pts=None, kind="練習"):
    p = f'　<span style="font-weight:400;font-size:10.5pt">【{pts}】</span>' if pts else ""
    return f'<div class="qh"><span class="no">{kind} {no}</span>{title}{p}</div>'
