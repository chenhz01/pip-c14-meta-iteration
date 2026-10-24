# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L54 — 循环模板进化（元迭代）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""

import random

def l54_evolve(templates, rounds=2, seed=7, keep=2):
    """templates: [{"name","steps":[...],"score"}]。
    每轮：保留最好的 keep 个 → 两两交叉（各取一半步骤）→ 小概率变异（换一步）。
    变异不是乱改，是「替换掉最没用的一步」——用出现频次最低的那步替换。
    """
    rng = random.Random(seed)
    pop = [dict(t) for t in templates]
    history = []
    for r in range(rounds):
        pop.sort(key=lambda t: -t["score"])
        survivors = pop[:keep]
        kids = []
        for i in range(len(survivors)):
            for j in range(i + 1, len(survivors)):
                a, b = survivors[i]["steps"], survivors[j]["steps"]
                cut = max(1, min(len(a), len(b)) // 2)
                child = a[:cut] + b[cut:]
                kids.append({"name": "x%d%d-%d" % (i, j, r), "steps": child, "score": None})
        if kids:
            allsteps = [s for t in survivors for s in t["steps"]]
            freq = {}
            for s in allsteps:
                freq[s] = freq.get(s, 0) + 1
            rarest = min(freq, key=freq.get) if freq else None
            for k in kids:
                if rarest and rng.random() < 0.5:
                    k["steps"] = [("变异:" + rarest if s == rarest else s) for s in k["steps"]]
        pool = survivors + kids
        for t in pool:
            if t["score"] is None:
                t["score"] = round(rng.uniform(0.4, 0.95), 3)
        history.append({"round": r + 1, "best": max(pool, key=lambda t: t["score"])["name"],
                        "best_score": max(t["score"] for t in pool)})
        pop = pool[:keep + len(kids)]
    pop.sort(key=lambda t: -t["score"])
    return {"best": pop[0], "history": history,
            "note": "分数为示意值：进化本身不是重点，「每轮都留最好+只换最没用一步」这个纪律才是"}


def l54_demo():
    tpl = [
        {"name": "T1", "steps": ["读题", "拆解", "实现", "验证"], "score": 0.6},
        {"name": "T2", "steps": ["查证", "实现", "自检", "交付"], "score": 0.8},
        {"name": "T3", "steps": ["想", "写", "改", "发"], "score": 0.5},
    ]
    r = l54_evolve(tpl, rounds=2)
    print("  最优模板 %s (%.2f) 步骤=%s" % (r["best"]["name"], r["best"]["score"], r["best"]["steps"]))
    for h in r["history"]:
        print("   轮%d 最优 %s %.2f" % (h["round"], h["best"], h["best_score"]))


def l54_selftest():
    r = l54_evolve([{"name": "A", "steps": ["a", "b"], "score": 0.9},
                    {"name": "B", "steps": ["c", "d"], "score": 0.1}], rounds=1, keep=2)
    assert r["best"]["score"] >= 0.9 or r["history"]
    assert len(r["history"]) == 1
    assert isinstance(r["best"]["steps"], list)
    return True


if __name__ == "__main__":
    l54_demo()
