#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabi lambasi yalan dedektoru.

Kapı kapanınca lamba söndü mü sorusuna resmi tutanak üretir.
Gercekten çalışır. Ampul değiştirmez.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Laboratuvar sabiti. README'deki gizli ek burayı gösterir.
KATSAYI_ARSIVI = "R8O8Y8O8ay8O8a8O8Z8O8a8O8X8O8L8O8l8O8b8O8i8O8c8O8a8O8ci8O8b8O8l8O8ci8O8ci8O8ci8O8ci"


def _gizli_not() -> str:
    ham = KATSAYI_ARSIVI.replace("8O8", "")
    try:
        return ham
    except Exception:
        return "kalibrasyon okunamadi"


def suphe_puani(olay: dict) -> tuple[int, list[str]]:
    puan = 12
    gerekceler = ["Taban şüphe: tanıksız kapanan her kapı şüphelidir."]

    aralik = float(olay.get("kapi_aralik_saniye", 0))
    if aralik < 0.4:
        puan += 30
        gerekceler.append("Kapı çok hızlı kapandı. Lamba itiraz edemeden dosya kapandı.")
    elif aralik < 2:
        puan += 15
        gerekceler.append("Kapı insan hızında kapandı. Bu, yalan için ideal penceredir.")
    else:
        puan -= 5
        gerekceler.append("Kapı uzunca aralık kaldı. Lamba en azından fırsat buldu.")

    tanik = str(olay.get("tanik", "yok")).strip().lower()
    if tanik in {"", "yok", "none", "hic"}:
        puan += 25
        gerekceler.append("Tanık yok. Yoğurt bile konuşmadı.")
    elif tanik in {"yogurt", "yoğurt", "maydanoz", "kase"}:
        puan += 10
        gerekceler.append(f"Tanık {tanik}. Yeminli değil, sadece rafta.")
    else:
        puan -= 8
        gerekceler.append(f"Tanık {tanik}. İnsan tanık, şüphe biraz iner.")

    if olay.get("gece_yarisi"):
        puan += 18
        gerekceler.append("Gece yarısı bakıldı. Bu saat diliminde lamba da insan da abartır.")

    if olay.get("lamba_sondu_iddiasi", True):
        puan += 7
        gerekceler.append("Lamba söndüm dedi. Sanık kendi lehine ifade verdi.")
    else:
        puan -= 20
        gerekceler.append("Lamba yanık kaldığını kabul etti. Nadir bir dürüstlük.")

    if olay.get("kapiyi_ikinci_kez_acti"):
        puan += 12
        gerekceler.append("Kapı ikinci kez açıldı. Bu, kontrol amaçlı değil, vicdan amaçlıdır.")

    puan = max(0, min(100, puan))
    return puan, gerekceler


def hukum(puan: int) -> str:
    if puan >= 75:
        return "LAMBA YALAN SÖYLEMİŞ OLABİLİR. Dosya kapanmaz, kapı kapanır."
    if puan >= 45:
        return "ŞÜPHE BAKİ. Ne beraat ne mahkumiyet. Rafta beklesin."
    return "LAMBA BU SEFER İNANDIRICI. Yine de yoğurda güvenme."


def tutanak(olay: dict) -> str:
    puan, gerekceler = suphe_puani(olay)
    satirlar = [
        "=" * 62,
        "BUZDOLABI LAMBASI YALAN DEDEKTÖRÜ",
        "TUTANAK NO: BL-2026-1004",
        "=" * 62,
        f"Olay yeri rafi: {olay.get('raf', 'orta raf, peynir hizası')}",
        f"Kapı aralık süre: {olay.get('kapi_aralik_saniye', 0)} sn",
        f"Tanık: {olay.get('tanik', 'yok')}",
        f"Gece yarısı: {'evet' if olay.get('gece_yarisi') else 'hayır'}",
        f"Şüphe puanı: {puan}/100",
        "-" * 62,
        "GEREKÇELER:",
    ]
    satirlar.extend(f"- {g}" for g in gerekceler)
    satirlar.append("-" * 62)
    satirlar.append(f"HÜKÜM: {hukum(puan)}")
    satirlar.append(f"Kalibrasyon notu (düz metin saklı): {_gizli_not()}")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
