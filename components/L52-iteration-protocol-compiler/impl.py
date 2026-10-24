# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L52 — 迭代协议编译（元迭代）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l52_compile(steps, stop_when, checkpoints_at=None):
    """把流程描述编译成可执行协议：每步带 entry / exit / on_fail，整体带停止条件。

    「可执行」的判据：任何一步失败时，协议本身能说出下一步做什么。
    """
    if not steps:
        return {"ok": False, "reason": "无步骤"}
    checkpoints_at = checkpoints_at or []
    compiled = []
    unknown = []
    for i, s in enumerate(steps):
        if isinstance(s, str):
            name, on_fail = s, None
        else:
            name, on_fail = s.get("name"), s.get("on_fail")
        if not on_fail:
            unknown.append(name)
        compiled.append({
            "n": i + 1,
            "step": name,
            "entry": "上一步 exit=ok" if i else "输入齐备",
            "exit": "产物 + 一句可核验的结论",
            "on_fail": on_fail or "未定义：这一步失败时谁都不知道该做什么",
            "checkpoint": (i + 1) in checkpoints_at,
        })
    return {
        "ok": not unknown,
        "steps": compiled,
        "stop_when": stop_when,
        "undefined_failure_handling": unknown,
        "verdict": "executable" if not unknown else "incomplete",
        "advice": "给这些步补 on_fail：" + ",".join(map(str, unknown)) if unknown else "协议可执行",
    }


def l52_demo():
    steps = [
        {"name": "跑基准", "on_fail": "换语料重跑一次，仍失败则降级为定性结论"},
        "写素材",
        {"name": "过五门", "on_fail": "只修被抓的那一项，不重写全篇"},
    ]
    r = l52_compile(steps, stop_when="连续两轮无改进", checkpoints_at=[1, 3])
    print("  编译结果 %s，问题步：%s" % (r["verdict"], r["undefined_failure_handling"]))
    for s in r["steps"]:
        print("   %d. %-6s 检查点=%-5s | 失败时：%s" % (s["n"], s["step"], s["checkpoint"], s["on_fail"][:26]))


def l52_selftest():
    r = l52_compile([{"name": "a", "on_fail": "x"}], "done")
    assert r["ok"] is True and r["verdict"] == "executable"
    r2 = l52_compile(["a"], "done")
    assert r2["ok"] is False and r2["undefined_failure_handling"] == ["a"]
    assert l52_compile([], "d")["ok"] is False
    return True


if __name__ == "__main__":
    l52_demo()
