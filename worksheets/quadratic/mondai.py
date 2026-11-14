"""問題編（A3両面 × 5枚）"""
from qlib import fr, num, bl, R, graph, sq
from common import HEAD, page, vtable, qc, qh

H = fr(1, 2)


def g_blank(xr=(-4, 4), yr=(-1, 9), u=7.2, **kw):
    return graph(*xr, *yr, u=u, **kw)


# ============================================================ シート1 表
def p1():
    left = f"""
    <div class="col">
      <div class="col-title">STEP 1　y＝ax² ってなに？<small>まずは読んで，しくみをつかもう</small></div>
      <div class="expl">
        <h3>■ ボールを落としてみよう</h3>
        ボールを落とすと，落ち始めてから <b>x 秒間</b>に落ちる距離 <b>y m</b> は，およそ <b>y＝5x²</b> で表せます。
        <div class="row" style="align-items:center; gap:3mm">
          {vtable([0, 1, 2, 3, 4], [0, 5, 20, 45, 80], ylab="y (m)", xlab="x (秒)")}
          <div class="note">x＝2 のとき y＝5×2²＝5×4＝20<br>x＝3 のとき y＝5×3²＝5×9＝45</div>
        </div>
        <div class="note">x が 1→2 と <b>2倍</b>になると，y は 5→20 と <b>4倍（＝2²倍）</b>。x が 1→3 と <b>3倍</b>になると，y は 5→45 と <b>9倍（＝3²倍）</b>。</div>
        <div class="key">y が x の関数で，<b class="big">y＝ax²</b>（a は 0 でない定数）と表されるとき，<br>
          「<b>y は x の2乗に比例する</b>」といい，a を <b>比例定数</b> という。（上の例では a＝5）</div>
        <table class="cmp">
          <tr><th></th><th>中1でならった比例</th><th>今回の関数</th></tr>
          <tr><td>式</td><td>y＝ax</td><td><b>y＝ax²</b></td></tr>
          <tr><td>x が 2倍，3倍…</td><td>y も 2倍，3倍…</td><td>y は <b>4倍，9倍…</b>（2²倍，3²倍…）</td></tr>
          <tr><td>グラフ</td><td>原点を通る直線</td><td>原点を通る<b>放物線</b>（シート2で学習）</td></tr>
        </table>
      </div>

      <div class="q grow">
        {qh(1, "2乗の計算（ここが土台！）", "1問ずつていねいに")}
        <div class="lead">「2乗」は<b>同じ数を2回かける</b>こと。3²＝3×3＝9，(−3)²＝(−3)×(−3)＝9</div>
        <div class="qg qg4 grow">
          {qc(1, "3²", "", "")}{qc(2, "(−3)²", "", "")}{qc(3, "−3²", "", "")}{qc(4, "(−5)²", "", "")}
          {qc(5, f"({fr(1, 2)})²", "", "")}{qc(6, f"(−{fr(2, 3)})²", "", "")}{qc(7, "2×(−4)²", "", "")}{qc(8, "−(−2)²", "", "")}
        </div>
        <div class="warn">(−3)² は「−3 を2回かける」＝ <b>＋9</b>。−3² は「3² に − をつける」＝ <b>−9</b>。かっこがあるかどうかで答えが変わる！</div>
      </div>
      <div class="q">
        {qh(5, "y＝ax² で x が □倍 になると，y は何倍？")}
        <div class="proof-fill" style="line-height:2.4">
          x が 2倍 → y は {bl("ア", "s")} 倍　　x が 3倍 → y は {bl("イ", "s")} 倍　　x が 4倍 → y は {bl("ウ", "s")} 倍<br>
          x が 5倍 → y は {bl("エ", "s")} 倍　　x が {H}倍 → y は {bl("オ", "s")} 倍　　x が n倍 → y は {bl("カ", "s")} 倍
        </div>
      </div>
    </div>"""
    right = f"""
    <div class="col">
      <div class="col-title">STEP 2　x の値から y の値を求めよう</div>
      <div class="q">
        {qh(2, "x の値を代入して y を求めよう")}
        <div class="lead"><span class="stp">例</span>y＝3x² で x＝−2 のとき　y＝3×(−2)²＝3×4＝<b>12</b>　…<b>先に2乗</b>，あとでかけ算！<br>
        <span class="tiny">（負の数は必ず（ ）をつけて代入しよう）</span></div>
        <div class="qg qg3">
          {qc(1, "y＝2x² で x＝3", "y ＝", "", minh=24)}{qc(2, "y＝2x² で x＝−3", "y ＝", "", minh=24)}{qc(3, "y＝−x² で x＝4", "y ＝", "", minh=24)}
          {qc(4, "y＝−3x² で x＝−2", "y ＝", "", minh=24)}{qc(5, f"y＝{H}x² で x＝6", "y ＝", "", minh=24)}{qc(6, f"y＝−{fr(1, 4)}x² で x＝−4", "y ＝", "", minh=24)}
        </div>
      </div>
      <div class="q">
        {qh(3, "表を完成させよう（空らんに y の値を書く）")}
        <div><b>(1)</b> y＝2x²</div>{vtable([-3, -2, -1, 0, 1, 2, 3])}
        <div><b>(2)</b> y＝−x²</div>{vtable([-3, -2, -1, 0, 1, 2, 3])}
        <div><b>(3)</b> y＝{H}x²　<span class="tiny">（分数のままでOK）</span></div>{vtable([-4, -3, -2, -1, 0, 1, 2, 3, 4])}
        <div class="tiny">気づいたこと：x＝2 と x＝−2 のように，<b>符号だけちがう x</b> では y の値は（　　　　　　　）になっている。</div>
      </div>
      <div class="q">
        {qh(4, "y が x の2乗に比例するものを<b>すべて</b>選ぼう")}
        <div class="qg qg2" style="font-size:10.6pt; gap:1mm 4mm">
          <div>ア　y＝3x²</div><div>イ　y＝3x</div>
          <div>ウ　y＝−x²</div><div>エ　y＝x＋2</div>
          <div>オ　1辺が x cm の正方形の面積 y cm²</div><div>カ　1辺が x cm の正方形のまわりの長さ y cm</div>
          <div>キ　半径 x cm の円の面積 y cm²</div><div>ク　たて 3cm，横 x cm の長方形の面積 y cm²</div>
        </div>
        <div class="ansline"><div class="calc">メモ（式で表してみよう）</div><div class="ansbox w">答え</div></div>
      </div>
    </div>"""
    return page(1, "関数 y＝ax² 対策プリント", "導入①　y＝ax² とは", f'<div class="cols">{left}{right}</div>')


# ============================================================ シート1 裏
def p2():
    left = f"""
    <div class="col">
      <div class="col-title">STEP 3　式を求めよう<small>「y＝ax² とおく」から始めるのがコツ</small></div>
      <div class="expl">
        <h3>■ 式の求め方は 3ステップ</h3>
        <div><b>問題</b>　y は x の2乗に比例し，x＝2 のとき y＝12 である。y を x の式で表しなさい。</div>
        <div class="key" style="line-height:1.9">
          <span class="stp">1</span>まず <b>y＝ax²</b> とおく（a がわからない数）<br>
          <span class="stp">2</span>x＝2，y＝12 を<b>代入</b>する　→　12＝a×2²　→　12＝4a<br>
          <span class="stp">3</span><b>a を求める</b>　→　a＝12÷4＝3　→　答え <b>y＝3x²</b>
        </div>
        <div class="note">確かめ：y＝3x² に x＝2 を入れると 3×4＝12。ちゃんと y＝12 になる！</div>
      </div>

      <div class="q">
        {qh(6, "空らんをうめて，式を完成させよう")}
        <div class="lead">y は x の2乗に比例し，x＝3 のとき y＝18 である。</div>
        <div class="proof-fill" style="line-height:2.45">
          {bl("ア", "l")} とおく。　x＝3，y＝18 を代入すると<br>
          18 ＝ a × {bl("イ", "s")}²　→　18 ＝ {bl("ウ", "s")} a　→　a ＝ {bl("エ", "s")}　　答え　y ＝ {bl("オ")}
        </div>
      </div>

      <div class="q grow">
        {qh(7, "y は x の2乗に比例する。次の条件から式を求めよう")}
        <div class="qg qg2 grow">
          {qc(1, "x＝2 のとき y＝8", "y ＝", "")}{qc(2, "x＝3 のとき y＝27", "y ＝", "")}
          {qc(3, "x＝−2 のとき y＝−8", "y ＝", "")}{qc(4, "x＝4 のとき y＝8　<span class='tiny'>（a は分数）</span>", "y ＝", "")}
          {qc(5, "x＝−3 のとき y＝3", "y ＝", "")}{qc(6, "x＝6 のとき y＝−9", "y ＝", "")}
        </div>
      </div>
    </div>"""
    right = f"""
    <div class="col">
      <div class="col-title">STEP 4　式を使って値を求めよう</div>
      <div class="q">
        {qh(8, "まず式を求めて，それから y の値を求めよう")}
        <div class="qg qg2">
          {qc(1, "y は x の2乗に比例し，x＝2 のとき y＝−12。<br>x＝−3 のときの y の値は？", "y ＝", "", minh=40)}
          {qc(2, "y は x の2乗に比例し，x＝−4 のとき y＝4。<br>x＝6 のときの y の値は？", "y ＝", "", minh=40)}
        </div>
      </div>
      <div class="expl">
        <h3>■ y の値から x を求めるときは「±」に注意！</h3>
        y＝2x² で y＝18 となる x は？　→　18＝2x²　→　x²＝9　→　<b>x＝3 と x＝−3</b>（まとめて <b>x＝±3</b>）<br>
        <span class="note">3²＝9 も (−3)²＝9 も成り立つので，<b>答えは2つ</b>。片方だけ書くと×！</span>
      </div>
      <div class="q grow">
        {qh(9, "y が次の値になるときの x の値を求めよう")}
        <div class="qg qg3 grow">
          {qc(1, "y＝x² で y＝16", "x ＝", "")}{qc(2, "y＝3x² で y＝12", "x ＝", "")}{qc(3, "y＝−2x² で y＝−50", "x ＝", "")}
          {qc(4, f"y＝{H}x² で y＝8", "x ＝", "")}{qc(5, f"y＝{fr(1, 4)}x² で y＝9", "x ＝", "")}{qc(6, "y＝5x² で y＝0", "x ＝", "")}
        </div>
      </div>
      <div class="q">
        {qh(10, "関数 y＝ax² のグラフが次の点を通るとき，a の値を求めよう")}
        <div class="lead">「点 (3, 18) を通る」＝「x＝3 のとき y＝18」と同じ意味！</div>
        <div class="qg qg3">
          {qc(1, "点 (3, 18)", "a ＝", "", minh=26)}{qc(2, "点 (−2, −2)", "a ＝", "", minh=26)}{qc(3, "点 (4, 4)", "a ＝", "", minh=26)}
        </div>
      </div>
    </div>"""
    return page(1, "関数 y＝ax² 対策プリント", "導入②　式を求める", f'<div class="cols">{left}{right}</div>', name=False,
                right='<div class="name" style="font-size:10pt;align-items:center">シート1（裏）</div>')


# ============================================================ シート2 表
def p3():
    ex = graph(-4, 4, -1, 9, u=6.2, curves=[dict(f=sq(1), w=0.6)],
               pts=[(x, x * x, f"({x},{x * x})".replace("-", "−"), 0 if x == 0 else (5.5 if x > 0 else -5.5), 0.5 if x else 3.6) for x in (-3, -2, -1, 0, 1, 2, 3)])
    bad1 = graph(-3, 3, -1, 9, u=3.1, nums=False, curves=[dict(f=lambda x: 3 * abs(x), w=0.5)])
    bad2 = graph(-3, 3, -1, 9, u=3.1, nums=False, segs=[(-3, 9, -2, 4, False), (-2, 4, -1, 1, False), (-1, 1, 0, 0, False), (0, 0, 1, 1, False), (1, 1, 2, 4, False), (2, 4, 3, 9, False)])
    good = graph(-3, 3, -1, 9, u=3.1, nums=False, curves=[dict(f=sq(1), w=0.5)])
    left = f"""
    <div class="col">
      <div class="col-title">STEP 5　グラフをかこう<small>表 → 点 → なめらかな曲線</small></div>
      <div class="expl">
        <h3>■ 例：y＝x² のグラフのかき方</h3>
        <div class="row" style="gap:3mm">
          <div style="flex:1">
            <span class="stp">1</span><b>表</b>をつくる<br>{vtable([-3, -2, -1, 0, 1, 2, 3], [9, 4, 1, 0, 1, 4, 9])}
            <span class="stp">2</span>(x, y) の<b>点</b>をとる<br>
            <span class="stp">3</span>点を<b>なめらかな曲線</b>で結ぶ<br>
            <div class="key" style="font-size:10.4pt">この曲線を <b>放物線</b> という。<br>原点を通り，<b>y軸について左右対称</b>。</div>
          </div>
          <div class="fig">{ex}</div>
        </div>
        <div class="row" style="gap:2mm; margin-top:1mm; align-items:flex-end">
          <div style="text-align:center"><div class="fig">{good}</div><b>○ なめらかなUの形</b></div>
          <div style="text-align:center"><div class="fig">{bad1}</div>× 原点でとがらせない</div>
          <div style="text-align:center"><div class="fig">{bad2}</div>× 点を直線で結ばない</div>
        </div>
      </div>
      <div class="q grow">
        {qh(11, "y＝2x² のグラフをかこう")}
        <div class="row grow" style="gap:4mm">
          <div style="flex:1"><b>(1)</b> 表を完成させよう<br>{vtable([-2, -1, 0, 1, 2])}
            <div style="margin-top:2mm"><b>(2)</b> 点をとって，なめらかな曲線で結ぼう。</div>
            <div class="tiny" style="margin-top:2mm">ヒント：x＝±{fr(3, 2)} のとき y＝2×{fr(9, 4)}＝{fr(9, 2)}（4.5）。この点もとると，よりきれいにかける。</div></div>
          <div class="fig">{g_blank()}</div>
        </div>
      </div>
    </div>"""
    right = f"""
    <div class="col">
      <div class="col-title">STEP 5（つづき）　グラフをかこう</div>
      <div class="q grow">
        {qh(12, f"y＝{H}x² のグラフをかこう")}
        <div class="row grow" style="gap:4mm">
          <div style="flex:1"><b>(1)</b> 表を完成させよう<br>{vtable([-4, -3, -2, -1, 0, 1, 2, 3, 4])}
            <div style="margin-top:2mm"><b>(2)</b> 点をとって，なめらかな曲線で結ぼう。</div>
            <div class="tiny" style="margin-top:2mm">{fr(9, 2)}＝4.5，{H}＝0.5 のように小数にすると点がとりやすい。</div>
            <div style="margin-top:2mm"><b>(3)</b> y＝x²（左の例）とくらべて，開き方は大きい？小さい？<br>
            <span class="ansbox" style="display:inline-flex; margin-top:1mm; min-width:60mm">開き方は</span></div></div>
          <div class="fig">{g_blank()}</div>
        </div>
      </div>
      <div class="q grow">
        {qh(13, "y＝−x² のグラフをかこう（a がマイナスだと…？）")}
        <div class="row grow" style="gap:4mm">
          <div style="flex:1"><b>(1)</b> 表を完成させよう<br>{vtable([-3, -2, -1, 0, 1, 2, 3])}
            <div style="margin-top:2mm"><b>(2)</b> 点をとって，なめらかな曲線で結ぼう。</div>
            <div style="margin-top:2mm"><b>(3)</b> y＝x² のグラフと y＝−x² のグラフは，<br>どの軸について対称？</div>
            <span class="ansbox" style="display:inline-flex; margin-top:1mm; min-width:50mm"><span style="flex:1"></span>について対称</span></div>
          <div class="fig">{g_blank(yr=(-9, 1))}</div>
        </div>
      </div>
    </div>"""
    return page(2, "関数 y＝ax² 対策プリント", "グラフ①　かいてみよう", f'<div class="cols">{left}{right}</div>')


# ============================================================ シート2 裏
def p4():
    fam = graph(-4, 4, -8, 8, u=5.4, nums=False, curves=[
        dict(f=sq(2), lab="2x²", lx=1.05, ly=7.0, fs=3.2), dict(f=sq(1), lab="x²", lx=2.33, ly=7.4, fs=3.2),
        dict(f=sq(.5), lab="½x²", lx=3.45, ly=4.3, fs=3.2),
        dict(f=sq(-.5), lab="−½x²", lx=-3.4, ly=-4.3, fs=3.2), dict(f=sq(-1), lab="−x²", lx=-2.33, ly=-7.4, fs=3.2),
        dict(f=sq(-2), lab="−2x²", lx=-1.05, ly=-7.0, fs=3.2)])
    match = graph(-4, 4, -6, 6, u=4.6, nums=False, curves=[
        dict(f=sq(2), lab="①", lx=-1.35, ly=5.2), dict(f=sq(.5), lab="②", lx=3.5, ly=4.2),
        dict(f=sq(-1), lab="③", lx=-2.1, ly=-5.2), dict(f=sq(-.25), lab="④", lx=3.6, ly=-2.4)])
    read = graph(-4, 4, -5, 6, u=5.2, curves=[
        dict(f=sq(3), lab="①", lx=-1.6, ly=5.5), dict(f=sq(.5), lab="②", lx=-3.6, ly=5.2),
        dict(f=sq(-1 / 3), lab="③", lx=-3.6, ly=-3.3)],
        pts=[(1, 3, "", 0, 0), (2, 2, "", 0, 0), (3, -3, "", 0, 0)])
    left = f"""
    <div class="col">
      <div class="col-title">STEP 6　グラフの特徴をまとめよう</div>
      <div class="expl">
        <h3>■ y＝ax² のグラフ（放物線）の性質</h3>
        <div class="row" style="gap:3mm">
          <div style="flex:1; font-size:10.6pt; line-height:1.65">
            ① <b>原点 O</b> を通る<br>
            ② <b>y軸</b>について対称（y軸を<b>放物線の軸</b>，原点を<b>頂点</b>という）<br>
            ③ <b>a＞0</b> のとき <b>上に開く</b>（∪の形）<br>
            ④ <b>a＜0</b> のとき <b>下に開く</b>（∩の形）<br>
            ⑤ a の<b>絶対値が大きいほど</b>，開き方は<b>小さい</b>（細くなる）<br>
            ⑥ y＝ax² と y＝−ax² は <b>x軸</b>について対称<br>
            <span class="tiny">（右の図は「y＝」を省略して式を書いています）</span>
            <div class="warn">「a が大きいほど細い」ではなく「a の<b>絶対値</b>が大きいほど細い」。y＝−2x² は y＝−½x² より細い！</div>
          </div>
          <div class="fig">{fam}</div>
        </div>
      </div>
      <div class="q">
        {qh(14, "（　）にあてはまることばを書こう")}
        <div class="proof-fill" style="line-height:2.35">
          (1) y＝ax² のグラフは {bl("ア", "l")} を通る。<br>
          (2) グラフは {bl("イ", "l")} について対称である。<br>
          (3) a＞0 のとき，グラフは {bl("ウ", "s")} に開く。a＜0 のとき {bl("エ", "s")} に開く。<br>
          (4) a の {bl("オ", "l")} が大きいほど，グラフの開き方は {bl("カ")}。<br>
          (5) y＝ax² のグラフのような曲線を {bl("キ", "l")} という。
        </div>
      </div>
      <div class="q grow">
        {qh(17, "ア〜オの関数について答えよう（あてはまるものをすべて）")}
        <div style="font-size:10.8pt">ア　y＝−3x²　　イ　y＝{fr(1, 3)}x²　　ウ　y＝2x²　　エ　y＝−2x²　　オ　y＝−{fr(1, 5)}x²</div>
        <div class="qg qg2 grow" style="margin-top:1.5mm">
          {qc(1, "グラフが下に開くもの", "", "")}{qc(2, "グラフの開き方がいちばん小さいもの", "", "")}
          {qc(3, "y＝2x² のグラフと x軸について対称なもの", "", "")}{qc(4, "x＞0 のとき，x が増加すると y も増加するもの", "", "")}
        </div>
      </div>
    </div>"""
    right = f"""
    <div class="col">
      <div class="col-title">STEP 7　グラフを読みとろう</div>
      <div class="q">
        {qh(15, "右の①〜④は，下のア〜エのどれのグラフ？")}
        <div class="row" style="gap:4mm">
          <div style="flex:1">
            <div style="line-height:1.9">ア　y＝2x²　　イ　y＝{H}x²<br>ウ　y＝−x²　　エ　y＝−{fr(1, 4)}x²</div>
            <div class="tiny">ヒント：まず「上に開く？下に開く？」で2つに分けて，次に「細いほうは a の絶対値が大きい」で決める。</div>
            <div class="qg qg2" style="margin-top:2mm">
              <div class="ansbox">① →</div><div class="ansbox">② →</div><div class="ansbox">③ →</div><div class="ansbox">④ →</div>
            </div>
          </div>
          <div class="fig">{match}</div>
        </div>
      </div>
      <div class="q grow">
        {qh(16, "グラフ①〜③の式を求めよう（・は目盛りの交点を通る点）")}
        <div class="row" style="gap:4mm">
          <div style="flex:1">
            <div class="tiny">ヒント：グラフが通る<b>目盛りぴったりの点</b>を読み，y＝ax² に代入して a を求める（練習10と同じ）。</div>
            <div class="qg" style="grid-template-columns:1fr; margin-top:1.5mm">
              {qc(1, "①", "y ＝", "", minh=17)}{qc(2, "②", "y ＝", "", minh=17)}{qc(3, "③", "y ＝", "", minh=17)}
            </div>
          </div>
          <div class="fig">{read}</div>
        </div>
      </div>
    </div>"""
    return page(2, "関数 y＝ax² 対策プリント", "グラフ②　特徴と読みとり", f'<div class="cols">{left}{right}</div>', name=False,
                right='<div class="name" style="font-size:10pt;align-items:center">シート2（裏）</div>')


# ============================================================ シート3 表
def p5():
    f1 = sq(1)
    ex = graph(-3, 3, -1, 9, u=6, curves=[dict(f=f1, w=0.45, dash=True)], hl=[dict(f=f1, x0=-1, x1=2)],
               pts=[(-1, 1, "(−1, 1)", -7, -2.2), (2, 4, "(2, 4)", 5.5, 0.5), (0, 0, "最小 (0, 0)", 10, -1.2)],
               segs=[(-1, 0, -1, 1, True), (2, 0, 2, 4, True), (-3, 4, 2, 4, True), (-3, 1, -1, 1, True)])

    def mini():
        return graph(-4, 4, -1, 10, u=3.6, curves=[dict(f=f1, w=0.45)], xstep=1, ystep=2)
    left = f"""
    <div class="col">
      <div class="col-title">STEP 8　変域を求めよう<small>グラフをかけば一発でわかる！</small></div>
      <div class="expl">
        <h3>■ 例：y＝x² で x の変域が −1≦x≦2 のとき，y の変域は？</h3>
        <div class="row" style="gap:3mm">
          <div style="flex:1; font-size:10.6pt; line-height:1.6">
            <span class="stp">1</span>グラフをざっくりかく<br>
            <span class="stp">2</span>x が −1〜2 の部分を<b>太くなぞる</b><br>
            <span class="stp">3</span>なぞった部分の<b>いちばん下</b>と<b>いちばん上</b>の y を読む<br>
            　・いちばん下：<b>原点 (0, 0)</b> → y＝0<br>
            　・いちばん上：x＝2 のとき → y＝4<br>
            <div class="key">答え　<b class="big">0≦y≦4</b></div>
            <div class="warn">両はしの値だけで「1≦y≦4」とするのは<b>まちがい</b>！ x の変域に <b>0 がふくまれる</b>（−と＋をまたぐ）ときは，y の最小（a＜0なら最大）は <b>0</b> になる。</div>
          </div>
          <div class="fig">{ex}</div>
        </div>
      </div>
      <div class="q grow">
        {qh(18, "y＝x² のグラフに x の範囲をなぞって，y の変域を求めよう")}
        <div class="qg qg2 grow">
          <div class="qc"><div class="t"><b>(1)</b> 1≦x≦3</div><div class="row" style="gap:1mm"><div class="fig">{mini()}</div><div class="ansbox" style="align-self:flex-end;min-width:30mm"></div></div></div>
          <div class="qc"><div class="t"><b>(2)</b> −2≦x≦1</div><div class="row" style="gap:1mm"><div class="fig">{mini()}</div><div class="ansbox" style="align-self:flex-end;min-width:30mm"></div></div></div>
          <div class="qc"><div class="t"><b>(3)</b> −3≦x≦−1</div><div class="row" style="gap:1mm"><div class="fig">{mini()}</div><div class="ansbox" style="align-self:flex-end;min-width:30mm"></div></div></div>
          <div class="qc"><div class="t"><b>(4)</b> −3≦x≦2</div><div class="row" style="gap:1mm"><div class="fig">{mini()}</div><div class="ansbox" style="align-self:flex-end;min-width:30mm"></div></div></div>
        </div>
      </div>
    </div>"""
    sk = "ざっくりグラフをかいて考えよう"
    right = f"""
    <div class="col">
      <div class="col-title">STEP 9　変域の練習<small>必ず小さなグラフをかいてから！</small></div>
      <div class="q grow">
        {qh(19, "x の変域が次のとき，y の変域を求めよう")}
        <div class="qg qg2 grow">
          {qc(1, "y＝2x²　（1≦x≦3）", "", "", sk)}{qc(2, "y＝2x²　（−3≦x≦−1）", "", "", sk)}
          {qc(3, "y＝2x²　（−2≦x≦1）", "", "", sk)}{qc(4, "y＝2x²　（−1≦x≦3）", "", "", sk)}
          {qc(5, "y＝−x²　（1≦x≦2）", "", "", "a＜0 → 下に開くグラフ！")}{qc(6, "y＝−x²　（−3≦x≦2）", "", "", sk)}
          {qc(7, f"y＝{H}x²　（−4≦x≦2）", "", "", sk)}{qc(8, f"y＝{H}x²　（−2≦x≦4）", "", "", sk)}
        </div>
      </div>
      <div class="q">
        {qh(20, "チャレンジ：変域から a や文字の値を求めよう", kind="挑戦")}
        <div class="qg qg3">
          {qc(1, "y＝ax² で，x の変域が −2≦x≦4 のとき，y の変域は 0≦y≦8。a の値は？", "a ＝", "", minh=40)}
          {qc(2, "y＝ax² で，x の変域が −3≦x≦1 のとき，y の変域は −18≦y≦0。a の値は？", "a ＝", "", minh=40)}
          {qc(3, "y＝x² で，x の変域が −2≦x≦t のとき，y の変域は 0≦y≦9。t の値は？", "t ＝", "", minh=40)}
        </div>
      </div>
    </div>"""
    return page(3, "関数 y＝ax² 対策プリント", "変域", f'<div class="cols">{left}{right}</div>')


# ============================================================ シート3 裏
def p6():
    left = f"""
    <div class="col">
      <div class="col-title">STEP 10　変化の割合<small>「y の増え方 ÷ x の増え方」</small></div>
      <div class="expl">
        <h3>■ 変化の割合とは</h3>
        <div class="key"><b class="big">変化の割合 ＝ <span class="frac"><span>y の増加量</span><span>x の増加量</span></span></b></div>
        <div><span class="stp">例</span>y＝x² で，x が <b>1 から 3</b> まで増加するとき</div>
        <div class="row" style="align-items:center; gap:3mm">
          {vtable([1, 3], [1, 9])}
          <div class="eq">x の増加量：3−1＝<b>2</b>　　y の増加量：9−1＝<b>8</b><br>変化の割合：8÷2＝<b>4</b></div>
        </div>
        <div class="note" style="margin-top:1mm">x が 3 から 5 のときは，(25−9)÷(5−3)＝16÷2＝<b>8</b>。<br>
        → 1次関数 y＝ax＋b の変化の割合は<b>いつも a（一定）</b>だったが，<b>y＝ax² の変化の割合は区間によってちがう</b>。</div>
        <div class="warn">「後 − 前」の順でひく。x も y も<b>同じ順番</b>でひき算すること。y の値は<b>必ず式に代入して</b>求める。</div>
      </div>
      <div class="q">
        {qh(21, "空らんをうめて，変化の割合を求めよう")}
        <div class="lead">y＝2x² で，x が 1 から 4 まで増加するとき</div>
        <div class="proof-fill" style="line-height:2.4">
          x＝1 のとき y＝{bl("ア", "s")}，x＝4 のとき y＝{bl("イ", "s")}<br>
          x の増加量 ＝ 4 − 1 ＝ {bl("ウ", "s")}　　y の増加量 ＝ {bl("エ", "s")}<br>
          変化の割合 ＝ {bl("オ", "s")} ÷ {bl("カ", "s")} ＝ {bl("キ", "s")}
        </div>
      </div>
      <div class="q grow">
        {qh(22, "x が □ から △ まで増加するときの変化の割合を求めよう")}
        <div class="qg qg3 grow">
          {qc(1, "y＝x²<br>1 から 4", "", "")}{qc(2, "y＝x²<br>−3 から −1", "", "")}{qc(3, "y＝2x²<br>1 から 3", "", "")}
          {qc(4, "y＝2x²<br>−2 から 1", "", "")}{qc(5, "y＝−x²<br>2 から 5", "", "")}{qc(6, "y＝−x²<br>−4 から −2", "", "")}
          {qc(7, f"y＝{H}x²<br>2 から 6", "", "")}{qc(8, f"y＝{H}x²<br>−6 から 2", "", "")}{qc(9, "y＝−3x²<br>−1 から 3", "", "")}
        </div>
      </div>
    </div>"""
    right = f"""
    <div class="col">
      <div class="col-title">STEP 11　変化の割合の利用</div>
      <div class="expl">
        <h3>■ 答え合わせに使える「たし算の公式」</h3>
        y＝ax² で x が <b>p から q</b> まで増加するときの変化の割合は　<b class="big" style="font-size:14pt">a × (p＋q)</b><br>
        <span class="note">例：y＝x²，1 から 3 → 1×(1＋3)＝4（左の例と同じ！）　y＝2x²，1 から 4 → 2×(1＋4)＝10</span>
        <div class="tiny">（なぜ？）{fr("a q² − a p²", "q − p")} ＝ {fr("a(q＋p)(q−p)", "q − p")} ＝ a(p＋q)。テストでは<b>まず表で求めて，公式で確かめる</b>のが安全。</div>
      </div>
      <div class="q">
        {qh(23, "平均の速さ")}
        <div class="lead">ある斜面でボールを転がすと，転がり始めてから x 秒間に転がる距離を y m とすると，<b>y＝2x²</b> の関係があった。<br>
        <b>平均の速さ ＝ 進んだ距離 ÷ かかった時間</b> ＝ 変化の割合 と同じ！</div>
        <div class="qg qg3">
          {qc(1, "0秒後から2秒後までの平均の速さ", "", "m/秒", minh=34)}
          {qc(2, "1秒後から3秒後までの平均の速さ", "", "m/秒", minh=34)}
          {qc(3, "2秒後から5秒後までの平均の速さ", "", "m/秒", minh=34)}
        </div>
      </div>
      <div class="q grow">
        {qh(24, "変化の割合から a を求めよう", kind="挑戦")}
        <div class="qg qg3 grow">
          {qc(1, "y＝ax² で，x が 1 から 3 まで増加するときの変化の割合が −8。a の値は？", "a ＝", "")}
          {qc(2, "y＝ax² で，x が −4 から −2 まで増加するときの変化の割合が 3。a の値は？", "a ＝", "")}
          {qc(3, "y＝ax² と y＝3x＋2 で，x が 2 から 4 まで増加するときの変化の割合が等しい。a の値は？", "a ＝", "")}
        </div>
      </div>
    </div>"""
    return page(3, "関数 y＝ax² 対策プリント", "変化の割合", f'<div class="cols">{left}{right}</div>', name=False,
                right='<div class="name" style="font-size:10pt;align-items:center">シート3（裏）</div>')


# ============================================================ シート4 表
def pab_fig(a, xa, xb, u, xr, yr, lab=True, tri=False, extra_pts=()):
    f = sq(a)
    A, B = (xa, a * xa * xa), (xb, a * xb * xb)
    m = (B[1] - A[1]) / (B[0] - A[0]); b = A[1] - m * A[0]
    polys = [([(0, 0), A, B], "#e6e6e6")] if tri else []
    pts = [(A[0], A[1], "A", -2.5, -1.2), (B[0], B[1], "B", 2.5, -1.2)] if lab else []
    return graph(*xr, *yr, u=u, curves=[dict(f=f, w=0.55), dict(f=lambda x: m * x + b, w=0.45)],
                 polys=polys, pts=pts + list(extra_pts), nums=False)


def p7():
    ex = pab_fig(1, -1, 2, 7.2, (-3, 3), (-1, 6), tri=True, extra_pts=[(0, 2, "C", 2.6, -0.4)])
    left = f"""
    <div class="col">
      <div class="col-title">STEP 12　放物線と直線<small>座標 → 直線の式 → 面積 の順に</small></div>
      <div class="expl">
        <h3>■ 例：y＝x² 上の2点 A（x＝−1），B（x＝2）</h3>
        <div class="row" style="gap:3mm">
          <div style="flex:1; font-size:10.5pt; line-height:1.62">
            <span class="stp">1</span><b>座標</b>：x を y＝x² に代入<br>　A(−1, 1)，B(2, 4)<br>
            <span class="stp">2</span><b>直線 AB の傾き</b>＝{fr("4 − 1", "2 − (−1)")}＝{fr(3, 3)}＝1<br>
            <span class="stp">3</span><b>切片</b>：y＝x＋b に B(2, 4) を代入<br>　4＝2＋b → b＝2　→　<b>y＝x＋2</b><br>
            <span class="stp">4</span><b>△OAB の面積</b>：y軸で2つに切る<br>
            　△OAB＝△OCA＋△OCB（C は切片 (0, 2)）<br>
            　＝{fr(1, 2)}×2×1＋{fr(1, 2)}×2×2＝1＋2＝<b>3</b>
          </div>
          <div class="fig">{ex}</div>
        </div>
        <div class="key" style="font-size:10.4pt">△OAB の面積 ＝ {fr(1, 2)} × <b>OC（切片）</b> × <b>（A と B の x 座標の差）</b>　→　{fr(1, 2)}×2×3＝3</div>
      </div>
      <div class="q grow">
        {qh(25, f"y＝{H}x² 上の点 A（x＝−2），B（x＝4）について，空らんをうめよう")}
        <div class="row grow" style="gap:3mm">
          <div class="proof-fill" style="flex:1; line-height:2.35; font-size:11pt">
            (1) A( −2, {bl("ア", "s")} )　B( 4, {bl("イ", "s")} )<br>
            (2) 傾き＝{fr("イ − ア", "4 − (−2)")}＝{bl("ウ", "s")}<br>
            　 y＝{bl("ウ", "s")}x＋b に B を代入して b＝{bl("エ", "s")}<br>
            　 直線 AB の式　y＝{bl("オ")}<br>
            (3) △OAB＝{fr(1, 2)}×{bl("エ", "s")}×{bl("カ", "s")}＝{bl("キ", "s")}
          </div>
          <div class="fig">{pab_fig(.5, -2, 4, 4.4, (-4, 5), (-1, 9), tri=True)}</div>
        </div>
      </div>
    </div>"""

    def three(no, eq, a, xa, xb, xr, yr, u):
        return f"""<div class="q grow">
        {qh(no, f"{eq} 上の点 A（x＝{num(xa)}），B（x＝{num(xb)}）")}
        <div class="row grow" style="gap:3mm">
          <div class="qg qg3 grow" style="flex:1">
            {qc(1, "A，B の座標", "", "", "")}{qc(2, "直線 AB の式", "y ＝", "")}{qc(3, "△OAB の面積", "", "")}
          </div>
          <div class="fig">{pab_fig(a, xa, xb, u, xr, yr, tri=True)}</div>
        </div></div>"""
    right = f"""
    <div class="col">
      <div class="col-title">STEP 13　放物線と直線の練習</div>
      {three(26, "y＝x²", 1, -3, 1, (-4, 3), (-1, 10), 4.0)}
      {three(27, "y＝2x²", 2, -1, 2, (-3, 3), (-1, 9), 4.4)}
      <div class="q grow">
        {qh(28, "放物線 y＝ax² と直線 y＝x＋6 が，x 座標が 3 の点 A と，点 B で交わっている。")}
        <div class="row grow" style="gap:3mm">
          <div class="qg qg3 grow" style="flex:1">
            {qc(1, "点 A の y 座標", "", "", "直線の式を使う")}{qc(2, "a の値", "a ＝", "")}{qc(3, "点 B の座標<br><span class='tiny'>（2次方程式を使う）</span>", "", "")}
          </div>
          <div class="fig">{graph(-4, 4, -1, 10, u=3.9, nums=False, curves=[dict(f=sq(1)), dict(f=lambda x: x + 6, w=0.45)], pts=[(3, 9, "A", 2.6, 0.6), (-2, 4, "B", -2.6, -0.8)])}</div>
        </div>
      </div>
    </div>"""
    return page(4, "関数 y＝ax² 対策プリント", "放物線と直線", f'<div class="cols">{left}{right}</div>')


# ============================================================ シート4 裏
def p8():
    left = f"""
    <div class="col">
      <div class="col-title">STEP 14　身のまわりの y＝ax²（文章題）</div>
      <div class="q grow">
        {qh(29, "ボールの落下", kind="文章題")}
        <div class="lead">ボールを落とすとき，落ち始めてから x 秒間に落ちる距離を y m とすると，<b>y＝5x²</b> の関係がある。</div>
        <div class="qg qg3 grow">
          {qc(1, "3秒間で何 m 落ちる？", "", "m")}{qc(2, "80 m 落ちるのに何秒かかる？", "", "秒")}{qc(3, "1秒後から3秒後までの平均の速さ", "", "m/秒")}
        </div>
      </div>
      <div class="q grow">
        {qh(30, "車のブレーキ", kind="文章題")}
        <div class="lead">車がブレーキをかけてから止まるまでに進む距離（制動距離）y m は，速さ（時速 x km）の2乗に比例する。時速 40km のとき制動距離は 8m だった。</div>
        <div class="qg qg3 grow">
          {qc(1, "y を x の式で表そう", "y ＝", "")}{qc(2, "時速 60km のときの制動距離", "", "m")}{qc(3, "制動距離が 32m のときの速さ", "時速", "km")}
        </div>
      </div>
      <div class="q grow">
        {qh(31, "ふりこ", kind="文章題")}
        <div class="lead">ふりこが1往復する時間を x 秒，ふりこの長さを y m とすると，およそ <b>y＝{fr(1, 4)}x²</b> の関係がある。</div>
        <div class="qg qg3 grow">
          {qc(1, "1往復 2秒のふりこの長さ", "", "m")}{qc(2, "長さ 9m のふりこの1往復の時間", "", "秒")}{qc(3, "1往復の時間を2倍にするには，長さを何倍にすればよい？", "", "倍")}
        </div>
      </div>
    </div>"""
    right = f"""
    <div class="col">
      <div class="col-title">まとめテスト<small>ここまでの総復習（各10点）</small></div>
      <div class="q grow">
        <div class="qg qg2 grow">
          {qc(1, "y は x の2乗に比例し，x＝3 のとき y＝−18。y を x の式で表しなさい。", "y ＝", "")}
          {qc(2, "(1) の式で，x＝−2 のときの y の値は？", "y ＝", "")}
          {qc(3, "y＝3x² で，y＝27 となる x の値は？", "x ＝", "")}
          {qc(4, "y＝−x² で，x の変域が −2≦x≦3 のときの y の変域は？", "", "")}
          {qc(5, "y＝2x² で，x が 2 から 4 まで増加するときの変化の割合は？", "", "")}
          {qc(6, "y＝ax² のグラフが点 (−2, 6) を通る。a の値は？", "a ＝", "")}
          {qc(7, f"y＝{fr(1, 4)}x² で，x の変域が −4≦x≦2 のときの y の変域は？", "", "")}
          {qc(8, f"上に開き，開き方がいちばん大きいグラフは？<br>ア y＝3x²　イ y＝−x²　ウ y＝{fr(1, 5)}x²　エ y＝x²", "", "")}
          {qc(9, "y＝ax² で，x が 1 から 5 まで増加するときの変化の割合が 12。a の値は？", "a ＝", "")}
          {qc(10, "y＝x² 上の点 A(−2, 4)，B(3, 9) を通る直線の式は？", "y ＝", "")}
        </div>
      </div>
    </div>"""
    return page(4, "関数 y＝ax² 対策プリント", "文章題・まとめテスト", f'<div class="cols">{left}{right}</div>', pts=100)


PAGES = [p1, p2, p3, p4, p5, p6, p7, p8]


def build():
    return HEAD.replace("{title}", "関数y=ax2 問題") + "".join(p() for p in PAGES) + "</body></html>"
