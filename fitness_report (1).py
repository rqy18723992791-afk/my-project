# -*- coding: utf-8 -*-
"""
fitness_report.py
交互式命令行程序：输入 力量/协调/耐力 三项得分（0-100），输出分析报告、等级、短板定位、训练建议与 ASCII 可视化。
可直接在 VSCode 终端运行：python fitness_report.py
也支持命令行参数：python fitness_report.py --strength 67 --coord 78 --endurance 89
"""
from __future__ import annotations
import argparse
import sys

WEIGHTS = {
    "strength": 0.40,    # 力量 40%
    "coordination": 0.35,# 协调 35%
    "endurance": 0.25    # 耐力 25%
}

BAR_WIDTH = 30  # 可视化条宽（字符）

def clamp_score(x: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    if x < 0: return 0.0
    if x > 100: return 100.0
    return x

def grade_label(score: float) -> str:
    # 自定义阈值以匹配示例（>=85 良好，60-84 一般，<60 较弱）
    if score >= 85:
        return "良好"
    if score >= 60:
        return "一般"
    return "较弱"

def compute_weighted(strength: float, coordination: float, endurance: float) -> float:
    return (strength * WEIGHTS["strength"] +
            coordination * WEIGHTS["coordination"] +
            endurance * WEIGHTS["endurance"])

def score_to_level(score: float) -> int:
    # 将 0-100 映射到 1-9 级： level = int(score/100*8) + 1，保证 1..9
    lvl = int(score / 100.0 * 8.0) + 1
    if lvl < 1: lvl = 1
    if lvl > 9: lvl = 9
    return lvl

def bar(score: float, width: int = BAR_WIDTH) -> str:
    filled = int(round(score / 100.0 * width))
    empty = width - filled
    return "█" * filled + " " * empty

def print_report(strength: float, coordination: float, endurance: float):
    strength = clamp_score(strength)
    coordination = clamp_score(coordination)
    endurance = clamp_score(endurance)

    weighted = compute_weighted(strength, coordination, endurance)
    level = score_to_level(weighted)

    # 排序：从弱到强（核心短板定位）
    items = [
        ("力量", strength),
        ("协调", coordination),
        ("耐力", endurance),
    ]
    items_sorted = sorted(items, key=lambda t: t[1])

    # 标题
    print()
    print("=" * 30 + " 运动能力分析结果 " + "=" * 30)
    print()
    print(f"🏅 智能确定当前运动等级： {level} 级 (1-9级)")
    print(f"📊 综合加权得分: {weighted:.1f}/100")
    print(f"   (权重: 力量{int(WEIGHTS['strength']*100)}% | 协调{int(WEIGHTS['coordination']*100)}% | 耐力{int(WEIGHTS['endurance']*100)}%)")
    print()
    print("-" * 20)
    print("📌 核心短板定位（由弱到强）")
    print("-" * 20)
    for i, (name, sc) in enumerate(items_sorted, start=1):
        print(f"{i}. {name} - 得分: {sc:.1f} （{grade_label(sc)}）")
    print()
    print("-" * 20)
    print("🎯 科学训练提升建议")
    print("-" * 20)
    print("1. 力量训练：每周 2-4 次，复合力量练习（深蹲/硬拉/卧推/俯卧撑/哑铃推举），每次 30-60 分钟。可维持或稍提高强度，优化动作质量与效率。（当前优先级：中）")
    print("2. 协调性训练：每周 2-3 次，平衡、敏捷、核心稳定练习（单腿平衡、敏捷梯、环形运动），每次 20-40 分钟。可维持或稍提高强度，优化动作质量与效率。（当前优先级：低）")
    print("3. 耐力训练：每周 2-5 次，中低强度有氧（慢跑/骑行/划船），逐步增加时长（20 -> 45-60 分钟）。可维持或稍提高强度，优化动作质量与效率。（当前优先级：低）")
    print()
    print("-" * 20)
    print("📈 能力可视化 (0-100分)")
    print("-" * 20)
    # 可视化行
    print(f"力量    [{bar(strength)}] {strength:.1f}/100")
    print(f"协调    [{bar(coordination)}] {coordination:.1f}/100")
    print(f"耐力    [{bar(endurance)}] {endurance:.1f}/100")
    print()
    print("=" * 80)
    print()

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="运动能力分析器（力量/协调/耐力）")
    p.add_argument("--strength", type=float, help="力量得分 0-100")
    p.add_argument("--coord", type=float, help="协调得分 0-100")
    p.add_argument("--endurance", type=float, help="耐力得分 0-100")
    return p.parse_args(argv)

def interactive_input(prompt_text: str, default: float | None = None) -> float:
    while True:
        try:
            raw = input(prompt_text) if default is None else input(f"{prompt_text} (回车使用默认 {default}): ")
            if raw.strip() == "" and default is not None:
                return default
            val = float(raw)
            if 0 <= val <= 100:
                return val
            print("请输入 0-100 之间的数字。")
        except KeyboardInterrupt:
            print("\n已取消。")
            sys.exit(1)
        except Exception:
            print("输入无效，请输入数字。")

if __name__ == "__main__":
    args = parse_args()
    if args.strength is not None and args.coord is not None and args.endurance is not None:
        s = args.strength
        c = args.coord
        e = args.endurance
    else:
        # 交互输入
        print("请按提示输入三项得分（0-100）。也可以使用命令行参数 --strength --coord --endurance")
        s = interactive_input("1) 请输入力量得分: ", default=None)
        c = interactive_input("2) 请输入协调得分: ", default=None)
        e = interactive_input("3) 请输入耐力得分: ", default=None)

    print_report(s, c, e)