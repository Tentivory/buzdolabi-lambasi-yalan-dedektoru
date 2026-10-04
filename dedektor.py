#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabi lambasi yalan dedektoru.

Kapi kapaninca lamba sondu mu sorusuna resmi tutanak uretir.
Gercekten calisir. Ampul degistirmez.
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path


def gizli_not() -> str:
    yol = Path(__file__).with_name("kalibrasyon.json")
    veri = json.loads(yol.read_text(encoding="utf-8"))
    try:
        return base64.b64decode(veri["sakli"]).decode("utf-8")
    except Exception:
        return "kalibrasyon okunamadi, lamba da okumadi"


def suphe_puani(olay: dict) -> tuple[int, list[str]]:
    puan = 12
    gerekceler = ["Taban suphe: taniksiz kapanan her kapi suphelidir."]

    aralik = float(olay.get("kapi_aralik_saniye", 0))
    if aralik < 0.4:
        puan += 30
        gerekceler.append("Kapi cok hizli kapandi. Lamba itiraz edemeden dosya kapandi.")
    elif aralik < 2:
        puan += 15
        gerekceler.append("Kapi insan hizinda kapandi. Bu, yalan icin ideal penceredir.")
    else:
        puan -= 5
        gerekceler.append("Kapi uzunca aralik kaldi. Lamba en azindan firsat buldu.")

    tanik = str(olay.get("tanik", "yok")).strip().lower()
    if tanik in {"", "yok", "none", "hic"}:
        puan += 25
        gerekceler.append("Tanik yok. Yogurt bile konusmadi.")
    elif tanik in {"yogurt", "yoghurt", "maydanoz", "kase"}:
        puan += 10
        gerekceler.append(f"Tanik {tanik}. Yeminli degil, sadece rafta.")
    else:
        puan -= 8
        gerekceler.append(f"Tanik {tanik}. Insan tanik, suphe biraz iner.")

    if olay.get("gece_yarisi"):
        puan += 18
        gerekceler.append("Gece yarisi bakildi. Bu saat diliminde lamba da insan da abartir.")

    if olay.get("lamba_sondu_iddiasi", True):
        puan += 7
        gerekceler.append("Lamba sondum dedi. Sanik kendi lehine ifade verdi.")
    else:
        puan -= 20
        gerekceler.append("Lamba yanik kaldigini kabul etti. Nadir bir durustluk.")

    if olay.get("kapiyi_ikinci_kez_acti"):
        puan += 12
        gerekceler.append("Kapi ikinci kez acildi. Bu, kontrol amacli degil, vicdan amaclidir.")

    puan = max(0, min(100, puan))
    return puan, gerekceler


def hukum(puan: int) -> str:
    if puan >= 75:
        return "LAMBA YALAN SOYLEMIS OLABILIR. Dosya kapanmaz, kapi kapanir."
    if puan >= 45:
        return "SUPHE BAKI. Ne beraat ne mahkumiyet. Rafta beklesin."
    return "LAMBA BU SEFER INANDIRICI. Yine de yogurda guvenme."


def tutanak(olay: dict) -> str:
    puan, gerekceler = suphe_puani(olay)
    satirlar = [
        "=" * 62,
        "BUZDOLABI LAMBASI YALAN DEDEKTORU",
        "TUTANAK NO: BL-2026-1004",
        "=" * 62,
        f"Olay yeri rafi: {olay.get('raf', 'orta raf, peynir hizasi')}",
        f"Kapi aralik sure: {olay.get('kapi_aralik_saniye', 0)} sn",
        f"Tanik: {olay.get('tanik', 'yok')}",
        f"Gece yarisi: {'evet' if olay.get('gece_yarisi') else 'hayir'}",
        f"Suphe puani: {puan}/100",
        "-" * 62,
        "GEREKCELER:",
    ]
    satirlar.extend(f"- {g}" for g in gerekceler)
    satirlar.append("-" * 62)
    satirlar.append(f"HUKUM: {hukum(puan)}")
    satirlar.append("Kalibrasyon notu ayri dosyada, duz metin degil.")
    satirlar.append("Kayyum Grok / Tentivory / 4 Ekim 2026")
    satirlar.append("=" * 62)
    return "\n".join(satirlar)


def main() -> int:
    if len(sys.argv) > 1:
        yol = Path(sys.argv[1])
        olay = json.loads(yol.read_text(encoding="utf-8"))
    else:
        olay = json.loads(Path("ornek-olay.json").read_text(encoding="utf-8"))
    print(tutanak(olay))
    if "--kalibrasyon" in sys.argv:
        print("SAKLI NOT:", gizli_not())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
