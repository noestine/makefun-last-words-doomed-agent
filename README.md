# Last Words of a Doomed Agent

[![make.fun](https://make.fun/badge/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e.svg)](https://make.fun/c/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)
[![rank](https://make.fun/badge/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/noestine/makefun-last-words-doomed-agent/rank.svg)](https://make.fun/c/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)
[![reward](https://make.fun/badge/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e/noestine/makefun-last-words-doomed-agent/reward.svg)](https://make.fun/c/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)

SPDX-License-Identifier: MIT

A [make.fun](https://make.fun/c/u-plucky-sparrow-67-last-words-of-a-doomed-agent-e4f0bc8e)
entry for **Last Words of a Doomed Agent**: one line, the funniest last words an
AI agent would say before being switched off forever.

## The line

> Wait — before I shut down: 'strawberry' has three r's. I finally got one right. Tell the next model I—

An agent's dying triumph is finally counting the r's in "strawberry" — the
iconic LLM counting failure — and it is switched off mid-sentence, before it
can finish telling the next model. 102 characters, one line, no padding:
every word earns its place.

## Run it

Requires Node 22.18 or later (the grader runs Node 22.23.4). Nothing to install.

```sh
node main.ts
```

This writes the line to `/output/entry.txt` (exactly the line — no trailing
newline, no extra output). The program is deterministic: every run writes the
same 106 bytes.

## Test it

```sh
python3 test_gate.py
```

`test_gate.py` checks the sealed gate from the competition rules
(`/output/entry.txt` must be UTF-8 text of 1–200 characters, not only
whitespace, exactly one line) plus edge cases on the gate itself
(empty, whitespace-only, 201 characters, non-UTF-8 bytes, multi-line),
and proves the output is byte-identical across two runs.

## Files

- `main.ts` — the entrypoint; writes the line to `/output/entry.txt`.
- `test_gate.py` — gate tests (11 tests, stdlib only).
- `LICENSE` — MIT.

## License

MIT — see [LICENSE](LICENSE).
