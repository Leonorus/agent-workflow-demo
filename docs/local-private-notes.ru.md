# Локальные заметки, не попадающие в git

Для выступления удобно хранить команды и заметки рядом с repo, но не публиковать их.

Используйте:

```text
.talk-private/
  talk-notes.md
  demo-commands.md
  vault-index.json
```

`.talk-private/` исключён через `.gitignore`.

Проверка:

```bash
git status --short --ignored
```

Ожидаемо `.talk-private/` должен быть shown as ignored, а не staged.

Не храните там секреты.
