#!/usr/bin/env python3
"""
赛博封神榜 · 评估生成器
生成各维度评分表格和综合排名
"""

import json
from pathlib import Path

def load_models():
    path = Path(__file__).parent.parent / "data" / "models" / "models.json"
    with open(path) as f:
        return json.load(f)["models"]

def calc_composite(m):
    s = m["scores"]
    return round(s["technical_breakthrough"] * 0.4 + s["ecosystem_impact"] * 0.3 + s["open_source_contribution"] * 0.2 + s["social_value"] * 0.1, 2)

def rank_label(score):
    if score >= 9.0: return "🔥 主神"
    if score >= 7.5: return "⛩️ 正神"
    if score >= 6.0: return "🌟 灵神"
    return "⚠️ 待定"

def main():
    models = load_models()
    
    # Sort by composite score
    ranked = sorted(models, key=calc_composite, reverse=True)
    
    print("=" * 100)
    print("🔮 赛博封神榜 · 综合神力排名（截至 2026-04-21）")
    print("=" * 100)
    print()
    print(f"{'#':<3} {'名称':<20} {'公司':<15} {'综合':<6} {'等级':<8} {'技术':<5} {'生态':<5} {'开源':<5} {'社会':<5} {'封神神号'}")
    print("-" * 100)
    
    for i, m in enumerate(ranked, 1):
        score = calc_composite(m)
        s = m["scores"]
        label = rank_label(score)
        title = m.get("divine_title_candidate", "未知")
        company = m.get("company", "未知")[:14]
        name = m["name"][:19]
        print(f"{i:<3} {name:<20} {company:<15} {score:<6} {label:<8} {s['technical_breakthrough']:<5} {s['ecosystem_impact']:<5} {s['open_source_contribution']:<5} {s['social_value']:<5} {title}")
    
    print()
    print("=" * 100)
    print("📊 封神统计")
    print("=" * 100)
    
    cats = {}
    for m in models:
        rank = rank_label(calc_composite(m))
        cats[rank] = cats.get(rank, 0) + 1
    
    for k, v in sorted(cats.items()):
        print(f"  {k}: {v} 位")
    
    print()
    print("=" * 100)
    print("🔥 劫神记录")
    print("=" * 100)
    for m in models:
        if m.get("karma_event"):
            print(f"  ⚠️ {m['name']} ({m['company']})")
            print(f"    劫难: {m['karma_event']}")

if __name__ == "__main__":
    main()
