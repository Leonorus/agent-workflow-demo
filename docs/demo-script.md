# Demo script

## Setup

```bash
cd agent-workflow-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
scripts/verify.sh
```

## Opening: почему просто chat недостаточно

Проблемы из лекции:

- агент может начать править раньше, чем понятен план;
- diff может выйти за scope;
- проверки запускаются непоследовательно;
- для похожих задач получаются разные процессы;
- контекст по связанным repo и архитектуре приходится повторять вручную.

Переход: agent runtime заменяем, engineering system переносим. Покажите `docs/lecture-2-flow.ru.md` как карту.

## Шаги 1-3: принципы, skills, taxonomy

Открыть:

- `AGENTS.md` — repo-level contract и четыре принципа;
- `demo-prompts/01-debug-python-cli.ru.md` — task instruction вместо разового prompt;
- bucket rule в `AGENTS.md` — lightweight taxonomy перед работой.

Ключевой тезис: правила должны быть короткими в `AGENTS.md`, а подробный повторяемый процесс лучше выносить в skills/docs/templates.

## Шаг 4 + демо 1: hooks и debug CLI

В публичном repo hooks не настраиваются, но `scripts/verify.sh` показывает, что именно должен запускать safety net.

```bash
scripts/reset-demo.sh
scripts/verify.sh
PYTHONPATH=src python -m agent_workflow_demo calc add 2 3
```

Попросить Codex выполнить `demo-prompts/01-debug-python-cli.ru.md`.

Expected story:

- тест падает;
- агент воспроизводит CLI output;
- находит минимальный bug в `calculator.add`;
- чинит одну строку;
- verification проходит.

## Шаги 5-6 + демо 2: memory и LLM Wiki / vault

Persistent memory нужна для компактных устойчивых facts. LLM Wiki / vault нужен для больших решений, архитектуры и проектных заметок.

```bash
PYTHONPATH=src python -m agent_workflow_demo vault ingest tests/fixtures/vault --out .talk-private/vault-index.json
PYTHONPATH=src python -m agent_workflow_demo vault lint tests/fixtures/vault || true
```

Показать:

- deterministic index;
- stable lint issue codes;
- как agent task превращается в тестируемую функцию, а не в разовый prompt;
- почему private vault и memory database не хранятся в public repo.

## Шаги 7-8: reasoning guard и subagents

На debug demo проговорить evidence loop:

1. failing test;
2. CLI reproduction;
3. implementation evidence;
4. minimal patch;
5. exact verification.

Subagents показывать как policy, не как обязательный hammer: они полезны для независимых workstreams, но на маленьком debug demo только замедлят работу.

## Шаг 9: MCP и scheduled task thinking

Открыть `demo-prompts/03-scheduled-mr-report.ru.md` и `docs/mcp-and-scheduled-tasks.md`.

Показать, что переносимый артефакт — markdown-инструкция с allowed tools, outputs и approval gates, а не локальный scheduler config.

## Bonus: RTK / context reduction

Объяснить RTK как слой вокруг terminal/file reads:

- уменьшает шум в tool output;
- помогает не тратить контекст на vendor/build artifacts;
- не заменяет tests, docs или reasoning guard;
- local rules остаются вне public repo, если они machine-specific.
