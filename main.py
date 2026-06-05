from crewai import Crew
from pathlib import Path

from utils import validate_input_file
from tasks import parse_task, report_task
from agents import log_analyst, report_writer

# Валидация входных данных
log_content = validate_input_file("logs/log.txt")

# Создание команды
crew = Crew(
    agents=[log_analyst, report_writer],
    tasks=[parse_task, report_task],
    process="sequential",
    verbose=True,
    memory=False,
)

# Запуск анализа
print("===> Запуск анализа инцидентов...\n")

result = crew.kickoff(inputs={"log_content": log_content})

print("\n===> Анализ завершён. Отчёт сохранён в result/incident_report.md")
