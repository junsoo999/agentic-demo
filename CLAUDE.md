# agentic-demo

Live-demo template: a coding agent (opencode) completes `memfit`, a CLI that tells whether an LLM fits in
accelerator memory and how many concurrent requests it can serve.

- `src/memfit/capacity.py` and `tests/test_capacity.py` are **intentionally unfinished**. Do not implement
  them unless the user asks to run or rehearse the demo.
- `AGENTS.md` is the script the demo agent follows. Keep it, and the two unfinished files, as short as possible.
- Rules for maintaining the template are in `.claude/rules/template.md`.
- Run everything through `uv run --no-sync ...`. There is no linter; pytest is the only check.
