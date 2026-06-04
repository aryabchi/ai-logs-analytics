from pydantic import BaseModel, Field


class Incident(BaseModel):
    """Структура одного инцидента."""

    service: str = Field(description="Имя сервиса (например, payment-service)")
    error_type: str = Field(description="Тип ошибки (например, TimeoutError)")
    message: str = Field(description="Текст сообщения об ошибке")
    severity: str = Field(description="Критичность: HIGH, MEDIUM или LOW")


class ParsedIncidents(BaseModel):
    """Результат парсинга — список инцидентов."""

    incidents: list[Incident] = Field(description="Список всех найденных инцидентов")
