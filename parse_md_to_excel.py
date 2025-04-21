"""Скрипт для преобразования markdown файлов с задачами в формат Excel."""

import argparse
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


def parse_markdown_file(file_path: Path) -> List[Dict[str, str]]:
    """
    Парсит markdown файл с задачами.

    Функция получает путь к файлу через аргументы командной строки.

    Returns:
        list: Список словарей с данными задач
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Разделяем на части по секциям
    parts = re.split(r'\\section\*?\{[^}]+\}', content)
    if len(parts) == 1:
        part_names = ['1']
    else:
        part_names = [str(i + 1) for i in range(len(parts))]

    questions = []

    for part_content, part_name in zip(parts, part_names):
        # Ищем задачи в формате "A1", "B2", ..., до следующей задачи или секции
        problem_matches = re.findall(
            r'([A-ZА-Я])(\d+)\s+(.*?)(?=[A-ZА-Я]\d+|\\section|$)',
            part_content,
            re.DOTALL,
        )

        for letter, num, text in problem_matches:
            # Извлекаем URL изображения, если оно есть
            image_matches = re.findall(
                r'!\[.*?\]\((.*?)\)|'
                r'\\includegraphics\{(.*?)\}|'
                r'<img.*?src="(.*?)".*?>',
                text,
            )
            image_urls = [
                url for match in image_matches for url in match if url
            ]
            image_url = image_urls[0] if image_urls else ''

            # Удаляем изображения (Markdown, LaTeX, HTML) и подписи к ним
            # нормализуем пробелы
            question_text = text
            question_text = re.sub(r'!\[.*?\]\(.*?\)', '', question_text)
            question_text = re.sub(
                r'\\includegraphics\{.*?\}', '', question_text
            )
            question_text = re.sub(r'<img.*?>', '', question_text)
            question_text = re.sub(
                r'\n\s*(Рис\.|Рисунок|Figure)\s*\d*\s*\n', '\n', question_text
            )
            question_text = re.sub(r'\s+', ' ', question_text).strip()

            questions.append(
                {
                    'Часть': part_name,
                    'Номер': f'{letter}{num}',
                    'Вопрос': question_text,
                    'Рисунок': image_url,
                }
            )

    # Сортируем задачи по части и номеру
    questions.sort(
        key=lambda x: (
            int(x['Часть']),
            int(re.search(r'\d+', x['Номер']).group()),
        )
    )
    return questions


def main():
    """Парсит markdown и сохраняет в Excel."""
    parser = argparse.ArgumentParser(
        description='Парсинг markdown файлов с задачами.'
    )
    parser.add_argument(
        'filename', type=str, help='Путь к markdown файлу для обработки'
    )
    args = parser.parse_args()

    # Путь к файлу
    md_file = Path(args.filename)
    output_file = Path('output.xlsx')

    try:
        if not md_file.exists():
            raise FileNotFoundError(f'Файл {md_file} не существует!')

        # Парсим markdown
        questions = parse_markdown_file(md_file)

        # Сохраняем в excel
        df = pd.DataFrame(questions)
        df.to_excel(output_file, index=False)
        print(f'Успешно преобразовано {len(questions)} задач в формат Excel')

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    main()
