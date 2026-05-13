# Agent instructions

Этот demo repo рассчитан на Codex-first workflow, но сам рассказ подчёркивает переносимость процесса между compatible AI coding agents. Публичные docs пишутся на русском. Не добавляй vendor-specific конфиги других agent runtimes без прямой просьбы пользователя.

## First move

Для нетривиальных задач классифицируй bucket:

- Trivia
- Light Ops
- Heavy Ops
- App Code
- Script
- Debug
- Research
- Repo-maintenance
- Ambiguous

Скажи bucket в одном коротком предложении и применяй соответствующий вес процесса.

## Project rules

- Делай минимальные изменения, полезные для demo.
- Сохраняй repo в passing state, если пользователь не просит подготовить intentionally broken live demo.
- Для debug demo используй `scripts/reset-demo.sh`, а не ручное ломание нескольких файлов.
- Локальные заметки и команды пиши только в `.talk-private/*.md`.
- Не добавляй `.talk-private/` в git.
- Не храни секреты, токены, пароли, реальные connection strings или персональные абсолютные пути.
- Публичные docs и prompts держи на русском.
- Не меняй unrelated files.

## Verification

Перед финалом запускай:

```bash
scripts/verify.sh
```

Если менял только markdown, всё равно проверь shell syntax и unit tests — они быстрые.

## Demo behavior

Demo 1 starts from a passing repo. `scripts/reset-demo.sh` intentionally changes `calculator.add` from addition to subtraction; then tests fail. Codex should find and fix the smallest cause.

Demo 2 uses local Markdown vault fixtures. Ingest output must be deterministic; lint issue codes should stay stable because docs and tests reference them.
