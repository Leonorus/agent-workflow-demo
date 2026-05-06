# Prompt: scheduled MR report task

Сформулируй portable scheduled-agent task для daily MR report.

Требования:

- task хранится как markdown-инструкция;
- scheduler implementation не попадает в git;
- GitLab MCP используется read-only для списка MR, diff summary и pipeline status;
- comments, merge, retry/cancel pipelines запрещены без approval;
- output format фиксирован: summary, risks, blocked, next actions;
- execution bounded: без рекурсивных subagents, с лимитом MR и timeout expectation.
