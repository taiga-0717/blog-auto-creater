"""円（円周角と中心角）対策プリントの HTML を生成する。
python3 gen.py → en_mondai.html（A3両面：問題）, en_kaitou.html（A3片面：解答・解説）"""
import figs as F

HEAD = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="style.css">
<style>
  .grid {{ display:grid; gap:2.5mm; flex:1; min-height:0; }}
  .g3 {{ grid-template-columns: repeat(3, 1fr); }}
  .cell {{ border:.3mm solid #666; border-radius:1.5mm; padding:1.2mm 2mm; display:flex; flex-direction:column; min-height:0; }}
  .cell .ct {{ font-size:9.6pt; line-height:1.35; min-height:9mm; }}
  .cell .ct b {{ margin-right:1mm; }}
  .cell .fig {{ flex:1; min-height:0; }}
  .cell .ansbox {{ align-self:flex-end; height:8.5mm; min-width:30mm; }}
  .q.adv {{ flex:1; }}
  .q.adv .row {{ flex:1; }}
  .subs.c3 {{ grid-template-columns: repeat(3, 1fr); }}
  .sub {{ min-height:24mm; }}
  .sub .calc {{ flex:1; font-size:8pt; color:#777; }}
  .thm {{ font-size:10.2pt; line-height:1.45; }}
  .thm td {{ border:.3mm solid #444; padding:.7mm 2mm; }}
  .thm td.n {{ width:8mm; text-align:center; font-weight:700; background:#222; color:#fff; }}
  .alist {{ display:grid; grid-template-columns: 1fr 1fr; gap:.6mm 4mm; font-size:9.8pt; line-height:1.45; }}
  .alist p {{ margin:.3mm 0; }}
</style></head><body>
"""


def header(sub, title, tag, right):
    return f"""<div class="head">
    <div class="ttl"><small>{sub}</small><b>{title} <span class="tag">{tag}</span></b></div>
    {right}
  </div>"""


NAME = """<div class="name"><div>組<span class="w1"></span></div><div>番<span class="w1"></span></div>
      <div>名前<span class="w2"></span></div><div class="score">/ 100点</div></div>"""


def cell(no, text, fig, unit="°", w=44, label="∠x ＝"):
    return f"""<div class="cell"><div class="ct"><b>({no})</b>{text}</div>
      <div class="fig">{fig.svg(w)}</div>
      <div class="ansbox">{label}<span style="flex:1"></span>{unit}</div></div>"""


def adv(no, title, pts, given, proof_q, fig, w, subs):
    sub_html = "".join(
        f'<div class="sub"><div class="st">{t}</div><div class="calc">計算</div><div class="ansbox">{a}</div></div>'
        for t, a in subs)
    return f"""<div class="q adv">
      <div class="qh"><span class="no">応用 {no}</span>{title}　<span style="font-weight:400;font-size:10.5pt">【{pts}点】</span></div>
      <div class="qtext given" style="font-size:10.5pt">{given}</div>
      <div class="row">
        <div style="flex:1; display:flex; flex-direction:column; min-width:0">
          <div style="font-size:10.5pt; margin-bottom:1mm"><b>(1)</b> {proof_q}【8点】</div>
          <div class="ruled"><span class="lab">証明</span></div>
        </div>
        <div class="fig" style="width:{w + 2}mm">{fig.svg(w)}</div>
      </div>
      <div class="subs c3" style="grid-template-columns: repeat({len(subs)}, 1fr)">{sub_html}</div>
    </div>"""


def bl(ch, cls=""):
    return f'<span class="bl {cls}"><i>{ch}</i></span>'


# ======================================================================== 問題
def mondai():
    intro_cells = [
        cell(1, "", F.f_d1(), w=36),
        cell(2, "", F.f_d2(), w=36),
        cell(3, "", F.f_d3(), w=36),
        cell(4, "AB は直径", F.f_d4(), w=38),
        cell(5, "点 P は弧 AB（短いほう）上", F.f_d5(), w=36),
        cell(6, "", F.f_d6(), w=36),
    ]
    ex_cells = [
        cell(1, "弦 AC と BD の交点が E", F.f_e1()),
        cell(2, "AB は直径", F.f_e2()),
        cell(3, "O は円の中心", F.f_e3()),
        cell(4, "直線 BA と CD の交点が P", F.f_e4(), w=48),
        cell(5, "円周を10等分する点 A〜J。AD と CH の交点が P", F.f_e5()),
        cell(6, "弧 AB ＝ 弧 BC", F.f_e6()),
        cell(7, "O は円の中心", F.f_e7()),
        cell(8, "弧AB:弧BC:弧CA＝3:4:5<br>（弧は残りの点を含まないほう）", F.f_e8()),
        cell(9, "円はかかれていません。<br>A，D は直線 BC について同じ側", F.f_e9()),
    ]
    a2, a4 = F.f_a2(), F.f_a4()[0]
    h = HEAD.format(title="円周角と中心角 問題")
    h += f"""
<!-- ======================= 表面 ======================= -->
<section class="page">
  {header("中学3年 数学 ／ 円", "円周角と中心角 対策プリント", "導入・演習・応用", NAME)}
  <div class="cols">
    <div class="col">
      <div class="col-title">STEP 1　導入<small>円周角の定理を覚えて，まずは使ってみよう</small></div>
      <div class="box memo" style="padding:2.5mm 4mm">
        <div class="qh" style="margin-bottom:1mm">★ 円周角の定理（ここが全部の土台！）</div>
        <table class="cond thm">
          <tr><td class="n">①</td><td>1つの弧に対する円周角は，その弧に対する<b>中心角の半分</b>　（∠APB ＝ <span class="frac"><span>1</span><span>2</span></span>∠AOB）</td></tr>
          <tr><td class="n">②</td><td><b>同じ弧</b>に対する円周角は<b>等しい</b>　（∠APB ＝ ∠AQB）</td></tr>
          <tr><td class="n">③</td><td><b>半円の弧</b>（直径）に対する円周角は <b>90°</b></td></tr>
          <tr><td class="n">④</td><td><b>等しい弧</b>に対する円周角は等しい（弧の長さと円周角は比例する）</td></tr>
          <tr><td class="n">⑤</td><td><b>円周角の定理の逆</b>：2点 P，Q が直線 AB について同じ側にあり ∠APB ＝ ∠AQB ならば，4点 A，B，P，Q は1つの円周上にある</td></tr>
        </table>
      </div>

      <div class="q" style="flex:0 0 auto">
        <div class="qh"><span class="no">導入 1</span>ことばの確認　<span style="font-weight:400;font-size:10.5pt">【各2点】</span></div>
        <div class="row">
          <div style="flex:1" class="proof-fill">
            右の図で，∠APB を 弧AB に対する {bl("①", "l")} といい，<br>
            ∠AOB を 弧AB に対する {bl("②", "l")} という。<br>
            ∠AOB ＝ 100° のとき，∠ア ＝ {bl("③")} °
          </div>
          <div class="fig" style="width:40mm">{F.f_intro1().svg(38)}</div>
        </div>
      </div>

      <div class="q grow">
        <div class="qh"><span class="no">導入 2</span>∠x の大きさを求めなさい（O は円の中心）　<span style="font-weight:400;font-size:10.5pt">【各3点】</span></div>
        <div class="grid g3">{"".join(intro_cells)}</div>
      </div>
    </div>

    <div class="col">
      <div class="col-title">STEP 2　演習<small>どの弧に対する円周角かを図に書きこもう</small></div>
      <div class="q grow">
        <div class="qh"><span class="no">演習</span>∠x の大きさを求めなさい　<span style="font-weight:400;font-size:10.5pt">【各3点】</span>
          <span class="hint" style="margin:0 0 0 2mm">ヒント：同じ弧に対する円周角に<b>同じ印</b>をつけると見えてくる！</span></div>
        <div class="grid g3">{"".join(ex_cells)}</div>
      </div>
    </div>
  </div>
</section>

<!-- ======================= 裏面 ======================= -->
<section class="page">
  {header("中学3年 数学 ／ 円", "円周角と中心角 対策プリント", "応用：円と相似の証明", '<div class="name" style="font-size:10pt;align-items:center">（表面とあわせて 100点）</div>')}
  <div class="box memo" style="padding:2mm 4mm; font-size:10.3pt; margin-bottom:3.5mm">
    <b>円と相似の証明の作戦</b>
    <span class="tg">1</span>円周角の定理で<b>等しい角</b>を見つける（「弧○○に対する円周角は等しいから」と書く）
    <span class="tg">2</span>もう1組を<b>対頂角・共通な角・90°・仮定</b>から見つける
    <span class="tg">3</span>「2組の角がそれぞれ等しいから」で結論
  </div>
  <div class="cols">
    <div class="col">
      {adv(1, "円の中で交わる2本の弦", 12,
           "円周上に4点 A，B，C，D があり，弦 AC と弦 BD の交点を P とします。",
           "△PAB∽△PDC を証明しなさい。", F.f_a1(), 58,
           [("<b>(2)</b> PA＝4cm，PB＝6cm，PC＝9cm のとき，PD の長さ【2点】", "PD ＝<span style='flex:1'></span>cm"),
            ("<b>(3)</b> (2)のとき，AB＝5cm なら DC の長さは？【2点】", "DC ＝<span style='flex:1'></span>cm")])}
      {adv(2, "円の外の点からひいた2本の直線", 12,
           "円の外の点 P を通る2本の直線が，円とそれぞれ点 A，B（PA&lt;PB）と点 C，D（PC&lt;PD）で交わっています。",
           "△PAD∽△PCB を証明しなさい。", a2, 62,
           [("<b>(2)</b> PA＝4cm，AB＝5cm，PC＝3cm のとき，CD の長さ【2点】", "CD ＝<span style='flex:1'></span>cm"),
            ("<b>(3)</b> (2)のとき，△PAD の面積は △PCB の面積の何倍？【2点】", "<span style='flex:1'></span>倍")])}
    </div>
    <div class="col">
      {adv(3, "直径と垂線（直角を2つ見つけよう）", 13,
           "△ABC の3つの頂点は円 O の周上にあり，線分 AD は円 O の直径です。頂点 A から辺 BC に垂線 AH をひきます。",
           "△ABH∽△ADC を証明しなさい。", F.f_a3(), 56,
           [("<b>(2)</b> AB＝10cm，AC＝9cm，AD＝12cm のとき，AH の長さ【3点】", "AH ＝<span style='flex:1'></span>cm"),
            ("<b>(3)</b> ∠ABC＝50° のとき，∠CAD の大きさ【2点】", "∠CAD ＝<span style='flex:1'></span>°")])}
      {adv(4, "角の二等分線と円（発展）", 12,
           "△ABC の3つの頂点は円周上にあります。∠BAC の二等分線が辺 BC と交わる点を D，円と交わる点を E とします。",
           "△ABE∽△ADC を証明しなさい。", a4, 54,
           [("<b>(2)</b> AB＝6cm，AC＝8cm，AD＝4cm のとき，DE の長さ【2点】", "DE ＝<span style='flex:1'></span>cm"),
            ("<b>(3)</b> (2)のとき，△EBD∽△EAB となることを利用して BE の長さを求めなさい。【2点】", "BE ＝<span style='flex:1'></span>cm")])}
    </div>
  </div>
</section>
</body></html>"""
    return h


# ======================================================================== 解答
def kaitou():
    def pf(*lines):
        return '<div class="pf">' + "".join(f"<p>{l}</p>" for l in lines) + "</div>"
    fr = lambda a, b: f'<span class="frac"><span>{a}</span><span>{b}</span></span>'
    R = lambda t: f'<span class="red">{t}</span>'
    h = HEAD.format(title="円周角と中心角 解答")
    h += f"""
<section class="page ans" style="font-size:9.8pt">
  {header("中学3年 数学 ／ 円", "円周角と中心角 対策プリント", "解答・解説",
          '<div class="name" style="font-size:10pt;align-items:center">配点：導入1 各2点×3／導入2 各3点×6／演習 各3点×9／応用 49点　計100点</div>')}
  <div class="cols">
    <div class="col" style="gap:3mm">
      <div class="col-title">STEP 1・2　導入・演習の答え</div>
      <div class="q">
        <div class="qh"><span class="no">導入 1</span>① {R("円周角")}　② {R("中心角")}　③ {R("50")}°　<span style="font-weight:400;font-size:9.6pt">（中心角の半分：100° ÷ 2）</span></div>
      </div>
      <div class="q">
        <div class="qh"><span class="no">導入 2</span>答え</div>
        <div class="alist">
          <p>(1) {R("55°")}　中心角 110° の半分</p>
          <p>(2) {R("70°")}　中心角は円周角の2倍 → 35° × 2</p>
          <p>(3) {R("40°")}　弧AB に対する円周角どうし</p>
          <p>(4) {R("62°")}　直径なので ∠ACB＝90°，180°−90°−28°</p>
          <p style="grid-column:1/3">(5) {R("115°")}　P と反対側の弧（長いほう）に対する中心角は 360°−130°＝230°。その半分で 115°<br>
          　<span class="tg">注意</span>「130° ÷ 2 ＝ 65°」は×。<b>P が見ている弧</b>（P をふくまない弧）の中心角を使う。</p>
          <p style="grid-column:1/3">(6) {R("40°")}　∠AOB＝50°×2＝100°。OA＝OB（半径）なので △OAB は二等辺三角形 → (180°−100°) ÷ 2</p>
        </div>
      </div>
      <div class="q">
        <div class="qh"><span class="no">演習</span>答え</div>
        <div class="alist" style="grid-template-columns:1fr; gap:.8mm">
          <p>(1) {R("100°")}　弧AD に対する円周角より ∠ABD＝∠ACD＝45°。△ABE で ∠AEB＝180°−35°−45°</p>
          <p>(2) {R("36°")}　弧AC に対する円周角より ∠ABC＝∠ADC＝54°。直径なので ∠ACB＝90°。180°−90°−54°</p>
          <p>(3) {R("70°")}　OB＝OC より ∠OCB＝20°，∠BOC＝180°−40°＝140°。∠BAC はその半分</p>
          <p>(4) {R("35°")}　△PBD で，外角 ∠BDC ＝ ∠P ＋ ∠PBD（三角形の外角はとなり合わない2つの内角の和）→ ∠x＝60°−25°</p>
          <p>(5) {R("72°")}　1つの弧は 360°÷10＝36°，その円周角は 18°。△APC の外角より<br>
          　∠x ＝ ∠PAC ＋ ∠PCA ＝ ∠DAC（弧CD：1つ分）＋ ∠HCA（弧HA：3つ分）＝ 18° ＋ 54°</p>
          <p>(6) {R("56°")}　等しい弧に対する円周角は等しいので ∠BDC＝∠ADB＝28°。∠x＝28°×2</p>
          <p>(7) {R("110°")}　OA＝OB，OB＝OC より ∠OBA＝25°，∠OBC＝30° → ∠ABC＝55°。∠AOC はその2倍（弧AC に対する中心角）</p>
          <p>(8) {R("75°")}　弧CA ＝ 360° × {fr(5, 12)} ＝ 150°。∠ABC はその弧に対する円周角なので 150° ÷ 2</p>
          <p>(9) {R("35°")}　A，D は BC について同じ側で ∠BAC＝∠BDC＝50° → <b>円周角の定理の逆</b>より4点 A，B，C，D は1つの円周上。<br>
          　だから弧AD に対する円周角として ∠ACD＝∠ABD＝35°</p>
        </div>
        <div class="pt"><span class="tg">コツ</span>角度の問題で迷ったら，①中心 O があれば<b>半径で二等辺三角形</b>，②<b>同じ弧</b>の円周角に同じ印，③直径を見たら<b>90°</b>，④三角形の<b>外角</b>，の順にチェック。</div>
      </div>
      <div class="col-title">STEP 3　応用（円と相似の証明）の答え</div>
      <div class="q" style="flex:1">
        <div class="qh"><span class="no">応用 1</span>(2) {R("PD＝6cm")}　(3) {R("DC＝7.5cm")}</div>
        {pf("(1)【証明】 △PAB と △PDC において",
            "弧BC に対する円周角は等しいから　∠BAP ＝ ∠CDP　…①",
            "対頂角は等しいから　∠APB ＝ ∠DPC　…②",
            "①，②より，2組の角がそれぞれ等しいから　△PAB ∽ △PDC")}
        <p>(2) 対応は P→P，A→D，B→C なので PA : PD ＝ PB : PC → 4 : PD ＝ 6 : 9 → 6PD ＝ 36 → PD ＝ 6</p>
        <p>(3) 相似比 PA : PD ＝ 4 : 6 ＝ 2 : 3。AB : DC ＝ 2 : 3 → 5 : DC ＝ 2 : 3 → DC ＝ 7.5</p>
        <div class="pt"><span class="tg">発展</span>(2) から PA × PC ＝ PB × PD（4×9＝6×6）が成り立つ。これを「方べきの定理」という（高校で学習）。</div>
      </div>
    </div>

    <div class="col" style="gap:3mm">
      <div class="col-title">STEP 3　応用の答え（つづき）</div>
      <div class="q">
        <div class="qh"><span class="no">応用 2</span>(2) {R("CD＝9cm")}　(3) {R(fr(16, 9) + "倍")}</div>
        {pf("(1)【証明】 △PAD と △PCB において",
            "共通な角だから　∠APD ＝ ∠CPB　…①",
            "弧AC に対する円周角は等しいから　∠ADP ＝ ∠CBP　…②",
            "①，②より，2組の角がそれぞれ等しいから　△PAD ∽ △PCB")}
        <p>(2) PB ＝ 4＋5 ＝ 9。PA : PC ＝ PD : PB → 4 : 3 ＝ PD : 9 → 3PD ＝ 36 → PD ＝ 12。CD ＝ 12 − 3 ＝ 9</p>
        <p>(3) 相似比 PA : PC ＝ 4 : 3 → 面積比 4² : 3² ＝ 16 : 9 → {fr(16, 9)} 倍</p>
        <div class="pt"><span class="tg">注意</span>∠ADP（＝∠ADC）と ∠CBP（＝∠CBA）は，どちらも<b>弧AC</b> に対する円周角。「△PAD∽△PCB」の頂点の順番（A↔C，D↔B）に気をつけよう。</div>
      </div>
      <div class="q">
        <div class="qh"><span class="no">応用 3</span>(2) {R("AH＝7.5cm")}　(3) {R("∠CAD＝40°")}</div>
        {pf("(1)【証明】 △ABH と △ADC において",
            "仮定より ∠AHB ＝ 90°，AD は直径だから ∠ACD ＝ 90°。よって　∠AHB ＝ ∠ACD　…①",
            "弧AC に対する円周角は等しいから　∠ABH ＝ ∠ADC　…②",
            "①，②より，2組の角がそれぞれ等しいから　△ABH ∽ △ADC")}
        <p>(2) AB : AD ＝ AH : AC → 10 : 12 ＝ AH : 9 → 12AH ＝ 90 → AH ＝ 7.5</p>
        <p>(3) ∠ADC ＝ ∠ABC ＝ 50°，∠ACD ＝ 90° なので △ACD で ∠CAD ＝ 180° − 90° − 50° ＝ 40°（∠BAH ＝ ∠CAD にもなっている）</p>
      </div>
      <div class="q" style="flex:1">
        <div class="qh"><span class="no">応用 4</span>(2) {R("DE＝8cm")}　(3) {R("BE＝4√<span style='border-top:.25mm solid currentColor'>6</span> cm")}</div>
        {pf("(1)【証明】 △ABE と △ADC において",
            "仮定より　∠BAE ＝ ∠DAC　…①",
            "弧AB に対する円周角は等しいから　∠AEB ＝ ∠ACD　…②",
            "①，②より，2組の角がそれぞれ等しいから　△ABE ∽ △ADC")}
        <p>(2) AB : AD ＝ AE : AC → 6 : 4 ＝ AE : 8 → 4AE ＝ 48 → AE ＝ 12。DE ＝ 12 − 4 ＝ 8</p>
        <p>(3) △EBD と △EAB で，∠BED ＝ ∠AEB（共通），∠EBD ＝ ∠EBC ＝ ∠EAC（弧EC）＝ ∠BAE（仮定）→ △EBD∽△EAB<br>
        　EB : EA ＝ ED : EB → BE² ＝ ED × EA ＝ 8 × 12 ＝ 96 → BE ＝ √<span style='border-top:.25mm solid currentColor'>96</span> ＝ 4√<span style='border-top:.25mm solid currentColor'>6</span></p>
        <div class="pt"><span class="tg">ポイント</span>角の二等分線＋円では「<b>等しい角が次々に移る</b>」。∠BAE ＝ ∠EAC ＝ ∠EBC と，弧EC に対する円周角を経由して角を移動させるのがカギ。</div>
      </div>
    </div>
  </div>
</section>
</body></html>"""
    return h


if __name__ == "__main__":
    open("en_mondai.html", "w", encoding="utf-8").write(mondai())
    open("en_kaitou.html", "w", encoding="utf-8").write(kaitou())
    print("written")
