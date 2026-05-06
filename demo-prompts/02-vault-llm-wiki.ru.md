# Prompt: vault / LLM Wiki ingest-lint

Ты работаешь в Python CLI demo repo. Нужно улучшить workflow ingest/lint для локального Markdown vault.

Задача:

1. Прочитай `docs/demo-2-vault-llm-wiki.ru.md` и `AGENTS.md`.
2. Запусти `scripts/verify.sh`.
3. Осмотри `src/agent_workflow_demo/vault.py` и tests.
4. Добавь или улучши одно правило lint: unresolved wiki links, duplicate titles, missing H1 или absolute local path leaks.
5. Добавь/обнови тест на fixture vault.
6. Убедись, что ingest output детерминирован.
7. Запусти `scripts/verify.sh`.

Ожидаемый результат: маленький diff, стабильные issue codes и passing verification.
