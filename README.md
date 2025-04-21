# Тестовое задание для Яндекс Практикум.

## Описание

Скрипт парсит markdown файлы, извлекает задачи, изображения и сохраняет их в формате Excel.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/your_username/YandexPracticumTZ1.git
    cd YandexPracticumTZ1
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/MacOS
    venv\Scripts\activate  # Для Windows
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Использование

Скрипт принимает путь к markdown файлу через аргументы командной строки и сохраняет результат в формате Excel.

Пример:

```bash
python parse_md_to_excel.py your_file.md
```

**Результат будет сохранён в файл output.xlsx**
