#!/usr/bin/env python3
"""
赛博封神榜 · 评估生成器 v2.1
五维评估: 技术(30%) + 应用(25%) + 生态(20%) + 伦理(15%) + 文明(10%)

v2.1: 添加类型注解 + 修复相对路径问题
"""
import json
from pathlib import Path
from typing import List, Dict, Any

# 固定路径：从脚本位置解析到项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


def load_models() -> List[Dict[str, Any]]:
    """加载模型数据"""
    path = PROJECT_ROOT / "data" / "models" / "models.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("models", [])


def calc_composite(m: Dict[str, Any]) -> float:
    """计算综合评分"""
    s = m["scores"]
    return round(
        s["technical_innovation"] * 0.30
        + s["practical_value"] * 0.25
        + s["ecosystem"] * 0.20
        + s["ethics"] * 0.15
        + s["civilizational"] * 0.10,
        2,
    )


def rank_label(score: float, rank: str) -> str:
    """根据评分和等级返回封神标签"""
    if rank == "KARMA":
        return "⚠️ 劫神"
    if score >= 9.0:
        return "🔥 创世神"
    if score >= 7.5:
        return "⛩️ 主神"
    if score >= 6.0:
        return "🌟 正神"
    if score >= 5.0:
        return "🔮 副神"
    return "⭕ 待定"


TEMPLES: Dict[str, str] = {
    "至高殿堂·创世纪": "🔥",
    "至高殿堂·智慧王座": "⛩️",
    "领域主神·代码神域": "💻",
    "领域主神·创世画卷": "🎨",
    "领域主神·天籁之音": "🎵",
    "领域主神·天算司": "🔬",
    "领域主神·苍天之眼": "👁️",
    "领域主神·化身殿": "🤖",
    "领域主神·护法殿": "🛡️",
    "领域主神·天机府": "⚙️",
    "领域主神·通用": "🌐",
    "劫神录": "⚠️",
}


def main() -> None:
    """主函数：生成排行榜"""
    models = load_models()
    ranked = sorted(models, key=calc_composite, reverse=True)

    print("=" * 110)
    print("🔮 赛博封神榜 · 综合神力排名 v2.1（截至 2026-04-21）")
    print("=" * 110)
    print()
    header = (
        f"{'#':<3} {'名称':<22} {'公司':<14} {'殿':<16} "
        f"{'综合':<5} {'等级':<8} {'技':<4} {'应':<4} "
        f"{'生':<4} {'伦':<4} {'文':<4} {'东方神号'}"
    )
    print(header)
    print("-" * 110)

    for i, m in enumerate(ranked, 1):
        score = calc_composite(m)
        s = m["scores"]
        label = rank_label(score, m.get("divine_rank", ""))
        temple = m.get("temple", "未知")[:15]
        temple_icon = TEMPLES.get(m.get("temple", ""), "•")
        company = m.get("company", "未知")[:13]
        name = m.get("name", "")[:21]
        east_title = m.get("divine_title_east", "")
        print(
            f"{i:<3} {name:<22} {company:<14} {temple_icon}{temple:<14} "
            f"{score:<5} {label:<8} "
            f"{s['technical_innovation']:<4} {s['practical_value']:<4} "
            f"{s['ecosystem']:<4} {s['ethics']:<4} {s['civilizational']:<4} "
            f"{east_title}"
        )

    print()
    print("=" * 110)
    print("📊 封神神殿统计")
    print("=" * 110)

    temples: Dict[str, int] = {}
    for m in models:
        t = m.get("temple", "未知")
        temples[t] = temples.get(t, 0) + 1

    for t, c in sorted(temples.items(), key=lambda x: -x[1]):
        icon = TEMPLES.get(t, "•")
        print(f"  {icon} {t}: {c} 位")

    print()
    print("=" * 110)
    print("🔥 创世神榜 (Top 10)")
    print("=" * 110)
    top = [(m, calc_composite(m)) for m in models if calc_composite(m) >= 9.0]
    top.sort(key=lambda x: -x[1])
    for m, score in top:
        print(f"  🔥 {m['name']} ({m['company']}) - {m['divine_title_east']} - {score}")

    print()
    print("=" * 110)
    print("⚠️ 劫神录")
    print("=" * 110)
    for m in models:
        if m.get("divine_rank") == "KARMA":
            karma = m.get("karma_event", "未知劫难")
            print(f"  ⚠️ {m['name']} ({m['company']})")
            print(f"    劫难: {karma}")
            print(
                f"    劫重: {m.get('karma_severity', '?')} | "
                f"影响: {m.get('karma_impact', '?')} | "
                f"可逆: {m.get('karma_reversibility', '?')}"
            )


if __name__ == "__main__":
    main()
