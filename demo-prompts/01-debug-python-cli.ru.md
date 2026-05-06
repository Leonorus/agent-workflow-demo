# Prompt: debug Python CLI

Ты работаешь в публичном Python CLI demo repo. Используй Codex-first workflow и инструкции из `AGENTS.md`.

Задача:

1. Запусти `scripts/verify.sh`.
2. Найди падающий тест CLI.
3. Воспроизведи поведение командой `PYTHONPATH=src python -m agent_workflow_demo calc add 2 3`.
4. Исправь причину минимально.
5. Снова запусти `scripts/verify.sh`.
6. В финале напиши, какой файл изменился и какая проверка прошла.

Ограничения:

- не добавляй vendor-specific runtime configs;
- не меняй публичные docs без необходимости;
- локальные заметки можно писать только в `.talk-private/*.md`;
- секреты не хранить и не выводить.
