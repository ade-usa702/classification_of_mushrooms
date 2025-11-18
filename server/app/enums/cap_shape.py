from enum import Enum


# форма шляпки
class CapShape(Enum):
    x = "Выпуклая"
    b = "Раструб"
    f = "Плоская"
    s = "Утопленная"
    o = "Нисходящая"
    c = "Коническая"
    oth = "Другая"
