# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L53 — 复盘模式挖掘（元迭代）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l53_mine(records, top=3):
    """records: [{"fail":"原因","waste":分钟,"stage":"阶段"}]。

    排的是「累计浪费」——不是单次最大，也不是出现次数。
    频次×平均浪费在数学上就等于累计浪费，所以这里不再假装是两件事；
    同额时比频次（常犯的错通常更好修）。
    """
    if not records:
        return {"verdict": "no-data"}
    agg = {}
    for r in records:
        k = r["fail"]
        a = agg.setdefault(k, {"count": 0, "waste": 0.0, "stages": set()})
        a["count"] += 1
        a["waste"] += r.get("waste", 0)
        if r.get("stage"):
            a["stages"].add(r["stage"])
    rows = []
    for k, a in agg.items():
        rows.append({
            "cause": k,
            "count": a["count"],
            "waste_total": round(a["waste"], 1),
            "waste_avg": round(a["waste"] / a["count"], 1),
            "stages": sorted(a["stages"]),
            "score": round(a["waste"], 1),
        })
    rows.sort(key=lambda x: (-x["score"], -x["count"]))
    total_waste = sum(r["waste_total"] for r in rows)
    top1 = rows[0]
    share = round(top1["waste_total"] / total_waste, 3) if total_waste else 0.0
    return {
        "rows": rows[:top],
        "total_waste": round(total_waste, 1),
        "top1_share": share,
        "verdict": "fix-this-first",
        "advice": "先修「%s」：出现 %d 次，累计浪费 %.0f 分钟，占全部浪费 %.0f%%"
                  % (top1["cause"], top1["count"], top1["waste_total"], share * 100),
    }


def l53_demo():
    recs = [
        {"fail": "HTTPS 推不动", "waste": 20, "stage": "推送"},
        {"fail": "HTTPS 推不动", "waste": 15, "stage": "推送"},
        {"fail": "HTTPS 推不动", "waste": 18, "stage": "推送"},
        {"fail": "乱码重写", "waste": 40, "stage": "写作"},
        {"fail": "门 5d 补写", "waste": 12, "stage": "验收"},
    ]
    r = l53_mine(recs)
    print(" ", r["advice"])
    for x in r["rows"]:
        print("   %-14s x%d 浪费%.0f 分" % (x["cause"], x["count"], x["waste_total"]))


def l53_selftest():
    r = l53_mine([{"fail": "a", "waste": 10}, {"fail": "a", "waste": 10},
                  {"fail": "b", "waste": 30}])
    assert r["rows"][0]["cause"] == "b"      # 累计浪费优先：30 > 10+10
    assert r["top1_share"] == round(30 / 50, 3)
    assert l53_mine([])["verdict"] == "no-data"
    return True


if __name__ == "__main__":
    l53_demo()
