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