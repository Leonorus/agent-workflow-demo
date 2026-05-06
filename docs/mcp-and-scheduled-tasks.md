# MCP and scheduled tasks in the talk

## MCP story

В реальном agent workflow tools должны быть явными и управляемыми.

Эволюция:

1. Сначала каждый agent session может запускать свои MCP subprocesses.
2. Это приводит к дублированию процессов и нестабильному tool surface.
3. Docker MCP Gateway решает common tools как один long-lived endpoint.
4. GitLab MCP можно вынести в отдельный HTTP service, если нужны богатые MR/pipeline/diff tools.

Conceptual topology:

```text
Codex or compatible agent
  -> MCP client config
    -> Docker MCP Gateway for common tools
    -> GitLab MCP HTTP service for MR/pipeline workflows
    -> vault/LLM Wiki access
```

## Scheduled tasks

В публичном demo не показываем machine-specific scheduler configs. Показываем переносимый слой:

- markdown task instruction;
- allowed tools;
- forbidden actions;
- declared inputs/outputs;
- bounded execution;
- verification/failure behavior.

## MR report example

Daily MR report как scheduled agent task:

- read open MRs;
- read diff summaries;
- read pipeline status;
- group by risk and next action;
- write report to declared output;
- do not comment/merge/retry/cancel without explicit approval.
