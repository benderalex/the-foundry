# The Foundry

Проект в рамках **Hacker Sprint #1: Фабрика фичей** (https://www.notion.so/Hacker-Sprint-1-33f2db4c860e8064a657e199b4578f66?source=copy_link).

## Docs
Документы, логи встреч и прочие текстовые артефакты храним в папке `/docs`.

## Что нужно сделать вручную до первого прогона
1. `brew install uv gh`
2. `gh auth login` — токен с правом `repo`.
3. Создать на GitHub sandbox-репо (например `the-foundry-sandbox`, либо использовать существующий репо https://github.com/Zhurbin/the-foundry-sandbox), лейбл `agent-task`, 1–2 issue.
4. `cp .env.example .env` и заполнить `SOURCE_REPO`, `TARGET_REPO`.
5. `uv sync && uv run foundry run` — ожидаемый результат: в sandbox появился PR с новой строкой в README.

## Coding agent

Стадии `plan` и `implement` делегированы агентному слою (`src/foundry/agents/`). Бэкенды: `stub` (оффлайн, по умолчанию) и `claude_cli` (shell-out в `claude` CLI). Переключается переменной `CODING_AGENT` в `.env`; per-stage оверрайды — `AGENT_PLAN_*`, `AGENT_IMPLEMENT_*`, `AGENT_VERIFY_*`. Промты живут в [src/foundry/agents/prompts/](src/foundry/agents/prompts/).

Быстрый smoke-прогон с реальным claude: `scripts/add-and-process.sh` создаст issue в sandbox и пройдёт весь pipeline до PR.