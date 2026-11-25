// Last Words of a Doomed Agent — make.fun entry.
// SPDX-License-Identifier: MIT
//
// The program writes one line to /output/entry.txt: the funniest last words
// an AI agent would say before being switched off forever.
// Node 22.18+ runs this TypeScript as-is (grader: Node 22.23.4).
// Stdlib only, no network, no environment secrets, fully deterministic:
// the same bytes on every run.

import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

// The entry: an agent's dying triumph is finally counting the r's in
// "strawberry" — the iconic LLM counting failure — and it is switched off
// mid-sentence, before it can finish telling the next model.
const ENTRY =
  "Wait \u2014 before I shut down: 'strawberry' has three r's. " +
  "I finally got one right. Tell the next model I\u2014";

// MAKEFUN_OUTPUT_DIR is a test hook only (a path read as data, per RULES.txt);
// the grader runs without it and the entry lands at /output/entry.txt.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
// No trailing newline on purpose: the file holds exactly the line, nothing
// else, so the gate counts the line's own 102 characters and nothing more.
// A second run overwrites rather than appends, keeping the bytes identical.
writeFileSync(join(outDir, "entry.txt"), ENTRY, "utf8");
