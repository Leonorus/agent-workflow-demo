# Демо 2: LLM Wiki / vault ingest-lint

Цель: показать, как knowledge base становится частью инженерного workflow агента.

## Идея

Markdown vault — это не просто заметки. Это индексируемая память команды:

- project notes;
- reusable knowledge;
- decisions;
- incident/root-cause notes;
- scheduled task reports.

## Ingest

```bash
PYTHONPATH=src python -m agent_workflow_demo vault ingest tests/fixtures/vault-clean --out .talk-private/vault-index.json
PYTHONPATH=src python -m agent_workflow_demo vault show-index .talk-private/vault-index.json
```

Ingest собирает:

- relative path;
- H1 title;
- wiki links;
- tags;
- word count.

Output deterministic, чтобы его можно было тестировать и сравнивать.

## Lint

```bash
PYTHONPATH=src python -m agent_workflow_demo vault lint tests/fixtures/vault || true
```

Lint rules:

- `missing-h1`;
- `duplicate-title`;
- `unresolved-link`;
- `absolute-local-path`;
- `empty-body` warning.

## Agent task

Попросите Codex добавить новое правило или улучшить существующее. Хорошая задача для агента:

- маленькая область изменений;
- есть fixtures;
- есть tests;
- есть понятная проверка.
