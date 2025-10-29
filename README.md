# TG-aggregated-analyze

Кратко: проект для анализа торговых сообщений с использованием DeepSeek API.

## Что сделано
- Добавлен `deepseek_analyzer.py` — основной анализатор.
- Конфигурация через `.env` + `python-dotenv` (`deepseek_config.py`).
- Тесты/утилиты: `test_analyzer.py`, `test_connection.py`, `test_request.py`, `check_api.py`.
- Добавлен `.gitignore`.

## Быстрый старт (Windows PowerShell)

1) Клонируйте/перейдите в папку проекта:

```powershell
cd C:\Users\re911\Desktop\прогии\krystal_bot\deepseekassist
```

2) Создайте виртуальное окружение (рекомендуется) и активируйте его:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Установите зависимости:

```powershell
pip install -r requirements.txt
```

4) Создайте или отредактируйте файл `.env` в корне проекта и добавьте:

```
DEEPSEEK_API_KEY=ваш-api-ключ
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

> Файл `.env` уже добавлен в `.gitignore` — не коммитьте ключи в репозиторий.

5) Запуск unit-тестов:

```powershell
python -m unittest test_analyzer.py -v
```

6) Быстрая проверка API / диагностика:

```powershell
python check_api.py
python test_request.py
python test_connection.py
```

## Частые проблемы и рекомендации

- 402 Payment Required / "Insufficient Balance":
  - API ключ может быть действительным, но на аккаунте нет средств.
  - Решение: зайти в панель DeepSeek, пополнить баланс или переключиться на тестовый/мок режим.

- DNS / соединение: если домен не резолвится (`getaddrinfo failed`), проверьте подключение к сети, DNS и/или прокси/фаервол.

## Как запускать в офлайн/мок режиме (рекомендация для тестов)

Если вы не хотите использовать платный API при тестах, можно:

1. Подменить `DEEPSEEK_API_URL` в `.env` на локальный мок-сервер, например `http://localhost:5000/v1/chat/completions`, и поднять простой мок (Flask/Express) который возвращает заранее подготовленный JSON.

2. В тестах использовать моки (pytest + responses / unittest.mock) — это надёжнее и делает тесты детерминированными.

Пример идеи (unittest.mock):
```python
from unittest.mock import patch

@patch('deepseek_analyzer.requests.Session.post')
def test_analyze_with_mock(post_mock):
    post_mock.return_value.json.return_value = { 'choices': [{ 'message': {'content': '{"signal_type":"BUY", "confidence_level":9, "risk_level":"LOW", "assets_mentioned": ["BTC"], "price_targets": {"entry":"35000","target":"40000","stop_loss":"33000"}, "timeframe":"SHORT", "summary":"Покупать","recommendation":"Вход","key_risks":"Волатильность"}'}}]}
    post_mock.return_value.status_code = 200
    # далее создаём анализатор и вызываем analyze_message
```

## Следующие шаги / follow-up
- Пополнить баланс аккаунта DeepSeek или заказать тестовые кредиты (из-за ошибки 402).
- Добавить моки в unit-тесты, чтобы CI не зависел от платного API.
- При необходимости — добавить README секцию с примером запуска Docker-мока.

Если нужно — могу добавить пример мока и интеграционные тесты (быстрая заготовка Flask/JSON), или автоматически добавить `requirements.txt` и обновить инструкции (сделал `requirements.txt`).
