from pathlib import Path


def validate_input_file(filepath: str) -> str:
    """
    Проверяет существование и содержимое файла логов.
    Возвращает содержимое файла или выбрасывает исключение.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"Файл {filepath} не найден. Создайте файл с логами в каталоге logs/"
        )

    if path.stat().st_size == 0:
        raise ValueError(f"Файл {filepath} пустой")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Файл {filepath} содержит только пробелы")

    # Минимум 3 строки с уровнями логирования
    lines = [
        line
        for line in content.strip().split("\n")
        if any(level in line for level in ["ERROR", "WARN", "INFO"])
    ]

    if len(lines) < 3:
        raise ValueError(
            f"Недостаточно валидных строк лога (найдено {len(lines)}). "
            "Требуется минимум 3 строки с уровнями ERROR/WARN/INFO."
        )

    return content
