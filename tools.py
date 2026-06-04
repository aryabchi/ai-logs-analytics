from crewai.tools import tool


@tool
def parse_incidents(log_content: str) -> str:
    """
    Извлекает ВСЕ инциденты (строки с ERROR/WARN) из содержимого лога за ОДИН вызов.

    Формат входа:
        Многострочный текст с логами

    Формат выхода:
        Валидный JSON-массив объектов вида:
        {"incidents": [{"service": "...", "error_type": "...", "message": "...", "severity": "..."}, ...]}
        ИЛИ строка "Ошибка: ..."

    Пример выхода:
        {"incidents": [{"service": "payment-service", "error_type": "TimeoutError", "message": "DB connection pool exhausted", "severity": "HIGH"}]}
    """
    try:
        if not log_content or not log_content.strip():
            return "Ошибка: пустое содержимое лога"

        lines = log_content.strip().split("\n")
        incidents = []

        for line in lines:
            line = line.strip()
            if not line or ("ERROR [" not in line and "WARN [" not in line):
                continue

            try:
                # Извлечение сервиса
                service = line.split("[")[1].split("]")[0].strip()

                # Извлечение типа ошибки и сообщения
                after_bracket = line.split("]: ", 1)[1]
                parts = after_bracket.split(": ", 1)
                error_type = parts[0].strip()
                message = (
                    parts[1].strip()
                    if len(parts) > 1
                    else "без дополнительного сообщения"
                )

                # Определение критичности
                severity = "HIGH" if "ERROR" in line else "MEDIUM"

                incidents.append(
                    {
                        "service": service,
                        "error_type": error_type,
                        "message": message,
                        "severity": severity,
                    }
                )
            except Exception as e:
                # Пропускаем некорректную строку, продолжаем обработку
                continue

        if not incidents:
            return "Ошибка: не найдено инцидентов для анализа"

        # Ручная сериализация в валидный JSON (без внешних зависимостей)
        json_items = []
        for inc in incidents:
            item = (
                f'{{"service": "{inc["service"]}", '
                f'"error_type": "{inc["error_type"]}", '
                f'"message": "{inc["message"]}", '
                f'"severity": "{inc["severity"]}"}}'
            )
            json_items.append(item)

        return f"[{', '.join(json_items)}]"

    except Exception as e:
        return f"Ошибка парсинга инцидентов: {str(e)}"


@tool
def generate_markdown_report(analysis_summary: str) -> str:
    """
    Формирует итоговый отчёт в формате Markdown.

    Аргументы:
        analysis_summary: текстовое резюме анализа инцидентов

    Возвращает:
        Валидный Markdown или строку "Ошибка: ..."
    """
    try:
        if not analysis_summary or not analysis_summary.strip():
            return "Ошибка: пустые данные для генерации отчёта"

        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        report = f"""# Отчёт об инцидентах

**Дата анализа:** {timestamp}
**Источник:** файл логов `logs/log.txt`

## Сводка инцидентов

{analysis_summary}

## Рекомендации

- **Критичность HIGH:** требуется немедленное вмешательство инженера
- **Критичность MEDIUM:** запланировать исправление в ближайшем релизе
- **Критичность LOW:** мониторинг в рамках регулярных проверок
        """
        return report

    except Exception as e:
        return f"Ошибка генерации отчёта: {str(e)}"
