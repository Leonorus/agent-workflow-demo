# agent-workflow-demo

Практический Python CLI demo repo для выступления о переносимых AI-agent workflows.

Главная мысль демо: agent runtime заменяем, а переносимый актив команды — это процесс вокруг него: `AGENTS.md`, skills/task instructions, task taxonomy, hooks/checks, долговременная knowledge base, MCP tool boundary, subagent policy и context-reduction tooling.

## Что показывает repo

1. Debug workflow: агент получает падающий тест CLI, воспроизводит проблему, исправляет минимально и запускает проверку.
2. Vault / LLM Wiki workflow: агент улучшает ingest/lint локального Markdown vault и фиксирует знания как структуру, а не как ephemeral chat.
3. Scheduled-agent mindset: фоновые задачи описываются как markdown-инструкции, без machine-specific scheduler configs в git.
4. Lecture 2 flow: `docs/lecture-2-flow.ru.md` связывает принципы, skills, taxonomy, hooks, memory, reasoning guard, subagents, MCP и RTK в один рассказ.

## Быстрый старт

```bash
cd agent-workflow-demo
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
scripts/verify.sh
```

Без установки пакета тоже работает:

```bash
PYTHONPATH=src python -m agent_workflow_demo calc add 2 3
PYTHONPATH=src python -m agent_workflow_demo vault ingest tests/fixtures/vault-clean --out .talk-private/vault-index.json
```

## CLI examples

```bash
agent-demo calc add 2 3
agent-demo calc div 10 2
agent-demo vault ingest tests/fixtures/vault-clean --out .talk-private/vault-index.json
agent-demo vault lint tests/fixtures/vault-clean
```

## Демо 1: debug CLI

Репозиторий хранится в passing state. Чтобы начать live demo с понятной поломкой:

```bash
scripts/reset-demo.sh
scripts/verify.sh
```

После этого тест `test_calc_add` должен упасть: `calc add 2 3` вернёт `-1` вместо `5`. Дальше можно попросить Codex исправить bug минимально и снова запустить `scripts/verify.sh`.

Чтобы восстановить passing state вручную:

```bash
scripts/restore-demo.sh
scripts/verify.sh
```

## Демо 2: LLM Wiki / vault

```bash
PYTHONPATH=src python -m agent_workflow_demo vault ingest tests/fixtures/vault --out .talk-private/vault-index.json
PYTHONPATH=src python -m agent_workflow_demo vault lint tests/fixtures/vault
```

Fixture `tests/fixtures/vault` намеренно содержит lint issues: missing H1, duplicate title, unresolved wiki links и synthetic absolute path leak. Это удобно для демонстрации agent workflow: сначала увидеть проблему, затем добавить/исправить правило, тест и verification.

## Локальные заметки

Локальные заметки для выступления лежат в `.talk-private/*.md`. Они находятся внутри repo для удобства live demo, но исключены из git через `.gitignore`.

Правило: не хранить там секреты. Команды, тезисы и заметки — можно; токены, пароли и приватные connection strings — нельзя.

## Карта лекции

См. `docs/lecture-2-flow.ru.md`: там перечислено, какие шаги лекции демонстрируются файлами repo, а какие намеренно остаются outside-git local configuration.

## Проверка

```bash
scripts/verify.sh
```

Проверка запускает:

- syntax check shell scripts;
- Python compile check;
- unit tests через стандартный `unittest`.

## Лицензия

MIT.
