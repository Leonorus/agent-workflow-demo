# Лекция 2: как демо-репозиторий ложится на рассказ

Этот файл синхронизирует публичный демо-репозиторий с заметками лекции о переходе от «агент как чат» к «агент как инженерная система».

## Главный тезис

Runtime агента заменяем: Claude Code, Codex, Hermes или OpenCode могут отличаться интерфейсом, но переносимыми активами остаются:

- инструкции уровня репозитория (`AGENTS.md`);
- навыки / skills с повторяемыми процессами;
- таксономия задач и правила эскалации;
- hooks и автоматические проверки;
- долговременная память и LLM Wiki / vault;
- управляемая поверхность MCP tools;
- subagents для больших задач;
- инструменты сокращения контекста вроде RTK.

## Карта лекции

| Шаг | Тема | Что показывать в репозитории |
|---|---|---|
| 1 | Четыре принципа Карпатого | `AGENTS.md`, секции про минимальные и хирургические изменения |
| 2 | Skills | `demo-prompts/`, повторяемые task instructions |
| 3 | Таксономия задач | bucket rule в `AGENTS.md` и `docs/demo-script.md` |
| 4 | Hooks | `scripts/verify.sh` как дешёвая safety net; в реальной конфигурации hooks вызывают такие проверки автоматически |
| 5 | Постоянная память | не хранится в репозитории; показать, как runtime memory сохраняет компактные facts |
| 6 | LLM Wiki / vault | `docs/demo-2-vault-llm-wiki.ru.md`, `tests/fixtures/vault*` |
| 7 | Reasoning guard | debug demo требует доказательств: failing test, CLI repro, diff, verification |
| 8 | Subagents | объяснить как правило: использовать только для независимых крупных workstreams |
| 9 | MCP servers | `docs/mcp-and-scheduled-tasks.md`, `demo-prompts/03-scheduled-mr-report.ru.md` |
| Bonus | RTK / сокращение контекста | объяснить как слой инструментов вокруг terminal/file reads, не как часть бизнес-логики |

## Контрольные точки demo

### До demo 1

Показать проблему: без правил агент может начать менять слишком рано, выйти за scope и забыть проверки. Затем открыть `AGENTS.md`: он задаёт принципы и verification contract.

### Demo 1: debug CLI

`docs/demo-1-debug-cli.ru.md` показывает исправление, основанное на доказательствах:

1. создать поломку;
2. увидеть failing test;
3. воспроизвести CLI;
4. исправить минимальную причину;
5. повторить verification.

### Demo 2: LLM Wiki / vault

`docs/demo-2-vault-llm-wiki.ru.md` показывает, что знания становятся тестируемым артефактом:

- детерминированный ingest;
- стабильные коды lint issues;
- fixtures как contract;
- notes как слой между chat history и repo docs.

### Demo 3: MCP и scheduled tasks

`docs/mcp-and-scheduled-tasks.md` показывает границу ответственности:

- repo описывает ожидаемые возможности и task prompt;
- реальные credentials, local scheduler configs и absolute paths остаются вне git;
- write/destructive MCP actions требуют approval.

## Что намеренно не хранится в демо-репозитории

- реальные agent configs;
- приватная база памяти;
- Obsidian vault;
- machine-specific scheduler files;
- RTK local rules;
- tokens, secrets, private hostnames.

Демо-репозиторий должен оставаться public-safe и воспроизводимым.
