# MCP and scheduled tasks in the talk

## MCP story

В реальном agent workflow tools должны быть явными и управляемыми. MCP здесь не «ещё один plugin», а контракт между агентом и внешними системами: какие операции доступны, какие read-only, какие требуют approval.

Эволюция из лекции:

1. Сначала каждый agent session может запускать свои MCP subprocesses.
2. Это приводит к дублированию процессов, разному tool surface и лишней стоимости startup.
3. Docker MCP Gateway решает common tools как один long-lived endpoint.
4. MCP servers, которых нет или недостаточно в gateway catalog, можно вынести в отдельный HTTP service.
5. Write/destructive tools стоит отключать или держать за approval boundary.
6. Чем больше MCP/tools включено, тем тяжелее prompt/tool schema; неиспользуемые tools надо отключать.

Conceptual topology:

```text
Codex / Hermes / compatible agent
  -> MCP client config
    -> Docker MCP Gateway for common tools
    -> GitLab MCP HTTP service for MR/pipeline workflows
    -> vault/LLM Wiki access
    -> workflow/taxonomy MCP, если команда автоматизирует классификацию
```

## Scheduled tasks

В публичном demo не показываем machine-specific scheduler configs. Показываем переносимый слой:

- markdown task instruction;
- allowed tools;
- forbidden actions;
- declared inputs/outputs;
- bounded execution;
- verification/failure behavior.

Scheduler implementation — local detail: cron, launchd, CI schedule, Hermes cron или другой runner. В git должен попадать reusable prompt/contract, а не персональные абсолютные пути и credentials.

## MR report example

Daily MR report как scheduled agent task:

- read open MRs;
- read diff summaries;
- read pipeline status;
- group by risk and next action;
- write report to declared output;
- do not comment/merge/retry/cancel without explicit approval.

## Safety talking points

- Repo описывает expected capabilities, но не хранит реальные tokens.
- Read-only MCP calls подходят для автономных reports.
- External writes, comments, merges, deploy/apply и pipeline mutations требуют explicit approval.
- Если tool surface меняется, demo/task docs должны обновиться вместе с verification steps.
