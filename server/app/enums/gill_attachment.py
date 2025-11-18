from enum import Enum


# насадка для жабр
class GillAttachment(Enum):
    a = "Прижатая"
    e = "Вырезанная"
    p = "Свободная"
    x = "Выпуклая"
    d = "Нисходящая"
    s = "Изогнутая"
    oth = "Другая"
