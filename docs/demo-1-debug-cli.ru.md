# Демо 1: debug Python CLI через тесты

Цель: показать, что агент должен не угадывать, а воспроизводить ошибку, найти минимальную причину и подтвердить fix проверкой.

## Подготовка

Repo по умолчанию passing. Чтобы создать учебную поломку:

```bash
scripts/reset-demo.sh
```

## Стартовая проверка

```bash
scripts/verify.sh
```

Ожидаемо падает тест `test_calc_add`: CLI возвращает `-1` вместо `5`.

## Команда воспроизведения

```bash
PYTHONPATH=src python -m agent_workflow_demo calc add 2 3
```

## Что должен сделать агент

1. Запустить проверку.
2. Прочитать failing test.
3. Воспроизвести CLI command.
4. Найти implementation bug.
5. Исправить одну строку.
6. Снова запустить проверку.

## Восстановление

```bash
scripts/restore-demo.sh
scripts/verify.sh
```
