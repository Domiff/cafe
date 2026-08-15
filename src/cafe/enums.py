from enum import StrEnum


class EmploymentType(StrEnum):
    FULL = "Полная ставка"
    PARTIAL = "Неполная ставка"
    SHIFT = "Сменный график"
    PROBATION = "Стажировка"
    CONTRACT = "Договор ГПХ"
