# PIP-1.0 · Meta Iteration

**4 primitives on one question: Are the checkers above accurate? Something needs to watch them too.**

[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE) [![Spec: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](LICENSE-SPEC)

---

## The problem

An AI agent that iterates — draft, check, revise, check again — leaks value in four ways:

1. **It does not know when to stop.** Either it loops forever, or it declares success on garbage.
2. **It does not know which step earned the win.** So the win cannot be reused.
3. **It drifts off spec**, while every intermediate step claims to be on-spec.
4. **It gets more expensive per unit of gain**, and nobody keeps the ledger.

`PIP-1.0` is a set of **4 primitives** that close these holes one at a time. Each one is **30–80 lines, standard library only, embeddable in any loop**.

It is not a framework. It is a toolbox — take the wrench you need.

```python
ok, why, at = l01_converged([0.40, 0.71, 0.88, 0.89, 0.89])
# ok=True  why='flat-tail'  at=2  ->  two flat rounds, safe to stop
```

---

## What is in here

| Cluster | What it protects you from | Primitives |
|---|---|---|
| **Meta Iteration** | Are the checkers above accurate? Something needs to watch them too. | 4 |
| | **total** | **4** |

<sub>Learning cards in `cards/CARDS.md` are written in Chinese (four layers: plain-language, mechanism, usage, and the case where the primitive fails). Code, identifiers and this README are English.</sub>

---

## Quick start

```bash
# see what one primitive does (runs on built-in demo data)
python components/L52-iteration-protocol-compiler/impl.py

# verify it does what it claims (hard assertions)
python components/L52-iteration-protocol-compiler/selftest.py

# run every component, each in its own process
python run_all.py
```

Use one inside your own loop:

```python
import sys; sys.path.insert(0, 'components/L52-iteration-protocol-compiler')
from impl import l01_converged
```

---

## What has been verified, and what has not

| Check | Result | Note |
|---|---|---|
| Runs in its own process | **4/4** | `selftest.py` and `impl.py` each spawn a fresh interpreter |
| Third-party dependencies | **0** | stdlib only, by construction |
| Explicit bad-input contract | **not all** | roughly 32/55 repo-wide; the rest rely on native `TypeError`. We did not pad them with no-op guards just to make a checker happy |
| Real-world adoption | **none yet** | these are new; no production usage is claimed |

**Honest limits.** Every primitive only applies when the iteration produces a *rankable number*. For purely qualitative work — does this song sound good, does this paragraph have a voice — they cannot help, and should not be forced.

---

## License and attribution

Dual-licensed:

- **Code** — Apache License 2.0. See [LICENSE](LICENSE).
- **Specification & docs** — Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE-SPEC](LICENSE-SPEC).

If you publicly claim that your implementation **conforms to / passes / implements PIP-1.0**, you must attribute: `PIP-1.0 · pip-c14-meta-iteration © 2026 chenhz01, CC BY 4.0` plus the spec link https://github.com/chenhz01/pip-process-iteration-primitives.

If you make no such claim, use it freely — commercial, closed-source, renamed, no attribution needed.

