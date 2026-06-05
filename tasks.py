from crewai import Task

from pydantic_schemas import ParsedIncidents
from agents import log_analyst, report_writer

# Задача 1: парсинг инцидентов с валидацией
parse_task = Task(
    description=(
        "Проанализируй содержимое лога и извлеки ВСЕ инциденты (строки с уровнями ERROR и WARN).\n"
        "\nПРИМЕР ВХОДНОЙ СТРОКИ:\n"
        "ERROR [payment-service]: TimeoutError: DB connection pool exhausted\n"
        "\nПРИМЕР ВЫХОДА ИНСТРУМЕНТА:\n"
        '{"incidents": [{"service": "payment-service", "error_type": "TimeoutError", "message": "DB connection pool exhausted", "severity": "HIGH"}]}\n'
        "\nТВОЯ ЗАДАЧА:\n"
        "- ВЫЗВАТЬ инструмент parse_incidents ОДИН раз со всем содержимым лога:\n{log_content}\n"
        "- ВЕРНУТЬ ТОЛЬКО результат инструмента без изменений"
    ),
    expected_output=(
        "Валидный JSON объектов с полями: service, error_type, message, severity. "
        "Без дополнительного текста."
        "ТОЛЬКО JSON."
    ),
    agent=log_analyst,
    output_pydantic=ParsedIncidents,  # строгая валидация результата
)

# Задача 2: генерация отчёта
report_task = Task(
    description=(
        "На основе результатов парсинга сформируй текстовый анализ инцидентов:\n"
        "1. Общее количество инцидентов\n"
        "2. Распределение по критичности (HIGH/MEDIUM/LOW)\n"
        "3. Краткий анализ каждой ошибки (1 предложение на инцидент)\n"
        "\nЗатем ВЫЗОВИ инструмент generate_markdown_report "
        "с распределением по критичности и кратким анализом каждой ошибки."
    ),
    expected_output=(
        "Готовый отчёт в формате Markdown с разделами: "
        "Дата анализа, Источник, Сводка инцидентов, Рекомендации. "
        "На русском языке, без вымышленных данных."
        "Не изменяй Markdown шаблон, только добавь свой анализ."
    ),
    agent=report_writer,
    context=[parse_task],  # результат парсинга - на вход для генерации
    output_file="result/incident_report.md",
)
