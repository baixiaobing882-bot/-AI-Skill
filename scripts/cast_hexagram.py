#!/usr/bin/env python3
"""Reproducible I Ching hexagram calculator using bottom-to-top line order."""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timezone


TRIGRAMS = {
    "111": ("乾", "天"), "000": ("坤", "地"), "100": ("震", "雷"),
    "011": ("巽", "风"), "010": ("坎", "水"), "101": ("离", "火"),
    "001": ("艮", "山"), "110": ("兑", "泽"),
}

HEXAGRAM_NAMES = {
    1: "乾", 2: "坤", 3: "屯", 4: "蒙", 5: "需", 6: "讼", 7: "师", 8: "比",
    9: "小畜", 10: "履", 11: "泰", 12: "否", 13: "同人", 14: "大有", 15: "谦", 16: "豫",
    17: "随", 18: "蛊", 19: "临", 20: "观", 21: "噬嗑", 22: "贲", 23: "剥", 24: "复",
    25: "无妄", 26: "大畜", 27: "颐", 28: "大过", 29: "坎", 30: "离", 31: "咸", 32: "恒",
    33: "遁", 34: "大壮", 35: "晋", 36: "明夷", 37: "家人", 38: "睽", 39: "蹇", 40: "解",
    41: "损", 42: "益", 43: "夬", 44: "姤", 45: "萃", 46: "升", 47: "困", 48: "井",
    49: "革", 50: "鼎", 51: "震", 52: "艮", 53: "渐", 54: "归妹", 55: "丰", 56: "旅",
    57: "巽", 58: "兑", 59: "涣", 60: "节", 61: "中孚", 62: "小过", 63: "既济", 64: "未济",
}

# Rows are upper trigrams; columns are lower trigrams.
KING_WEN = {
    "乾": {"乾": 1, "兑": 10, "离": 13, "震": 25, "巽": 44, "坎": 6, "艮": 33, "坤": 12},
    "兑": {"乾": 43, "兑": 58, "离": 49, "震": 17, "巽": 28, "坎": 47, "艮": 31, "坤": 45},
    "离": {"乾": 14, "兑": 38, "离": 30, "震": 21, "巽": 50, "坎": 64, "艮": 56, "坤": 35},
    "震": {"乾": 34, "兑": 54, "离": 55, "震": 51, "巽": 32, "坎": 40, "艮": 62, "坤": 16},
    "巽": {"乾": 9, "兑": 61, "离": 37, "震": 42, "巽": 57, "坎": 59, "艮": 53, "坤": 20},
    "坎": {"乾": 5, "兑": 60, "离": 63, "震": 3, "巽": 48, "坎": 29, "艮": 39, "坤": 8},
    "艮": {"乾": 26, "兑": 41, "离": 22, "震": 27, "巽": 18, "坎": 4, "艮": 52, "坤": 23},
    "坤": {"乾": 11, "兑": 19, "离": 36, "震": 24, "巽": 46, "坎": 7, "艮": 15, "坤": 2},
}


def bits_from_values(values: list[int]) -> list[int]:
    return [1 if value in (7, 9) else 0 for value in values]


def hexagram(bits: list[int]) -> dict:
    if len(bits) != 6 or any(bit not in (0, 1) for bit in bits):
        raise ValueError("hexagram requires exactly six binary lines")
    lower_bits = "".join(map(str, bits[:3]))
    upper_bits = "".join(map(str, bits[3:]))
    lower, lower_image = TRIGRAMS[lower_bits]
    upper, upper_image = TRIGRAMS[upper_bits]
    number = KING_WEN[upper][lower]
    return {
        "number": number, "name": HEXAGRAM_NAMES[number],
        "lower_trigram": lower, "lower_image": lower_image,
        "upper_trigram": upper, "upper_image": upper_image,
        "bits_bottom_to_top": "".join(map(str, bits)),
    }


def parse_coins(tokens: list[str]) -> tuple[list[int], list[str]]:
    if len(tokens) != 6:
        raise ValueError("--coins requires six tosses, ordered bottom to top")
    normalized = [token.upper() for token in tokens]
    for token in normalized:
        if len(token) != 3 or any(ch not in "HT" for ch in token):
            raise ValueError(f"invalid toss {token!r}; use exactly three H/T characters")
    return [sum(3 if ch == "H" else 2 for ch in token) for token in normalized], normalized


def random_cast() -> tuple[list[int], list[str]]:
    tosses = ["".join("H" if secrets.randbits(1) else "T" for _ in range(3)) for _ in range(6)]
    values, _ = parse_coins(tosses)
    return values, tosses


def build_result(question: str, values: list[int], source: str, tosses: list[str] | None) -> dict:
    if len(values) != 6 or any(value not in (6, 7, 8, 9) for value in values):
        raise ValueError("line values must be six integers chosen from 6, 7, 8, 9")
    primary_bits = bits_from_values(values)
    changed_bits = [1 - bit if value in (6, 9) else bit for bit, value in zip(primary_bits, values)]
    nuclear_bits = primary_bits[1:4] + primary_bits[2:5]
    opposite_bits = [1 - bit for bit in primary_bits]
    reversed_bits = list(reversed(primary_bits))
    moving = [index + 1 for index, value in enumerate(values) if value in (6, 9)]
    line_labels = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}
    return {
        "question": question,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input_source": source,
        "randomness_note": "Python secrets simulated coins" if source == "machine_random" else None,
        "coin_tosses_bottom_to_top": tosses,
        "line_values_bottom_to_top": values,
        "line_labels_bottom_to_top": [line_labels[value] for value in values],
        "moving_lines": moving,
        "primary": hexagram(primary_bits),
        "changed": hexagram(changed_bits),
        "nuclear": hexagram(nuclear_bits),
        "opposite": hexagram(opposite_bits),
        "reversed": hexagram(reversed_bits),
    }


def format_markdown(result: dict) -> str:
    def title(item: dict) -> str:
        return f"第{item['number']}卦 {item['name']}（{item['upper_trigram']}上{item['lower_trigram']}下）"

    moving = "、".join(str(line) for line in result["moving_lines"]) or "无"
    tosses = " ".join(result["coin_tosses_bottom_to_top"] or []) or "未提供（直接输入爻值）"
    return "\n".join([
        "# 起卦计算结果", "", f"- 问题：{result['question']}",
        f"- 生成时间（UTC）：{result['generated_at_utc']}", f"- 输入来源：{result['input_source']}",
        f"- 三币记录（初→上）：{tosses}",
        f"- 爻值（初→上）：{' '.join(map(str, result['line_values_bottom_to_top']))}",
        f"- 动爻：{moving}", "", "## 卦象", "",
        f"- 本卦：{title(result['primary'])}", f"- 之卦：{title(result['changed'])}",
        f"- 互卦：{title(result['nuclear'])}", f"- 错卦：{title(result['opposite'])}",
        f"- 综卦：{title(result['reversed'])}", "",
        "> 六爻均按自下而上记录。此输出只完成可复算排卦，不自动宣称吉凶。",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", required=True, help="single concrete question")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--coins", nargs=6, metavar="HHT", help="six 3-coin tosses, bottom to top")
    group.add_argument("--lines", nargs=6, type=int, metavar="N", help="six values 6/7/8/9, bottom to top")
    group.add_argument("--random", action="store_true", help="simulate six tosses with secrets")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    try:
        if args.coins:
            values, tosses = parse_coins(args.coins)
            source = "user_coin_tosses"
        elif args.lines:
            values, tosses, source = args.lines, None, "user_line_values"
        else:
            values, tosses = random_cast()
            source = "machine_random"
        result = build_result(args.question, values, source, tosses)
    except ValueError as exc:
        parser.error(str(exc))
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
