# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L55 — 工具自测（元迭代）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l55_audit(results):
    """results: [{"name","returned","expected_type","assertions","silent"}]。
    检查「工具自己有没有沉默失败」：
      ① 返回 None 但没报错 → 沉默失败
      ② 类型不符 → 契约破坏
      ③ 零断言 → 假绿灯（跑了但没验）
    """
    issues = []
    for r in results:
        if r.get("returned") is None and not r.get("silent", False):
            issues.append({"tool": r["name"], "kind": "silent-none", "why": "返回 None 却无异常"})
        if r.get("expected_type") and r.get("returned") is not None:
            if not isinstance(r["returned"], r["expected_type"]):
                issues.append({"tool": r["name"], "kind": "contract", "why": "类型不符"})
        if r.get("assertions", 0) == 0:
            issues.append({"tool": r["name"], "kind": "fake-green", "why": "零断言：跑了算过"})
    names = {r["name"] for r in results}
    bad = {i["tool"] for i in issues}
    return {
        "tools": len(names),
        "issues": issues,
        "healthy": sorted(names - bad),
        "verdict": "clean" if not issues else "self-flawed",
        "advice": "工具自己沉默失败时，它报的所有绿灯都不可信" if issues else "自测通过",
    }


def l55_demo():
    rs = [
        {"name": "gate_depth", "returned": True, "expected_type": bool, "assertions": 4},
        {"name": "license_gate", "returned": None, "expected_type": bool, "assertions": 0},
        {"name": "check_links", "returned": "0", "expected_type": int, "assertions": 1},
        {"name": "runner", "returned": True, "expected_type": bool, "assertions": 0},
    ]
    r = l55_audit(rs)
    print("  %d 个工具 -> %s，健康 %s" % (r["tools"], r["verdict"], r["healthy"]))
    for i in r["issues"]:
        print("   ! %-12s %-12s %s" % (i["tool"], i["kind"], i["why"]))
    print(" ", r["advice"])


def l55_selftest():
    assert l55_audit([{"name": "a", "returned": True, "assertions": 1}])["verdict"] == "clean"
    r = l55_audit([{"name": "b", "returned": None, "assertions": 1}])
    assert r["issues"][0]["kind"] == "silent-none"
    # 注意：isinstance(True, int) 为真（bool 是 int 的子类），
    # 所以类型契约检查对 bool/int 混用是盲的——这里用真正的类型错来测。
    r2 = l55_audit([{"name": "c", "returned": "0", "expected_type": int, "assertions": 1}])
    assert r2["issues"][0]["kind"] == "contract"
    r3 = l55_audit([{"name": "d", "returned": True, "assertions": 0}])
    assert r3["issues"][0]["kind"] == "fake-green"
    return True


if __name__ == "__main__":
    l55_demo()
