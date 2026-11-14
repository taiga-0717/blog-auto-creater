"""python3 gen.py → kansu_mondai.html / kansu_kaitou.html"""
import mondai
import kaitou

open("kansu_mondai.html", "w", encoding="utf-8").write(mondai.build())
open("kansu_kaitou.html", "w", encoding="utf-8").write(kaitou.build())
print("written")
