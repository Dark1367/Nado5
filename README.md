# Пакетный  менеджер UV
Установка
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Добавление пакетов
```bash
uv add $package
```
Добавление пакетов для разработки
```bash
uv add --dev $package
```
Быстрая установка всего
```bash
uv sync
```

# Запуск сервера
```bash
uv run fastapi dev src/main.py
```

# Запуск тестов
```bash
uv run pytest -v
```