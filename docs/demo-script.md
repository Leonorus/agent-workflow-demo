# Demo script

## Setup

```bash
cd agent-workflow-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
scripts/verify.sh
```

## Демо 1: debug CLI

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

## Демо 2: LLM Wiki / vault

```bash
PYTHONPATH=src python -m agent_workflow_demo vault ingest tests/fixtures/vault --out .talk-private/vault-index.json
PYTHONPATH=src python -m agent_workflow_demo vault lint tests/fixtures/vault || true
```

Показать:

- deterministic index;
- stable lint issue codes;
- как agent task превращается в тестируемую функцию, а не в разовый prompt.

## Демо 3: scheduled task thinking

Открыть `demo-prompts/03-scheduled-mr-report.ru.md` и `docs/mcp-and-scheduled-tasks.md`.

Показать, что переносимый артефакт — markdown-инструкция с allowed tools, outputs и approval gates, а не локальный scheduler config.
