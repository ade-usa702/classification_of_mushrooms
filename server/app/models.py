from pydantic import BaseModel, Field
from typing import List
from app.enums.cap_shape import CapShape
from app.enums.cap_surface import CapSurface
from app.enums.color import Color
from app.enums.bool import Bool
from app.enums.gill_attachment import GillAttachment
from app.enums.habitat import Habitat
from app.enums.ring_type import RingType
from app.enums.season import Season


class MushroomModel(BaseModel):
    """Модель гриба

    Атрибуты:
        cap_shape (CapShape): Форма шляпки гриба.
        cap_surface (CapSurface): Структура/поверхность шляпки.
        cap_color (Color): Основной цвет шляпки.
        does_bruise_or_bleed (Bool): Есть ли у гриба синие пятна или выделения при повреждении.
        gill_attachment (GillAttachment): Способ крепления жабр к ножке.
        gill_color (Color): Цвет жабр.
        stem_color (Color): Цвет ножки.
        has_ring (Bool): Наличие кольца на ножке.
        ring_type (RingType): Тип кольца, если оно присутствует.
        habitat (Habitat): Тип среды обитания гриба.
        season (Season): Сезон, в который гриб встречается.
        cap_diameter (float): Диаметр шляпки гриба в сантиметрах.
        stem_height (float): Высота ножки гриба в сантиметрах.
        stem_width (float): Толщина ножки гриба в сантиметрах.
    """    
    cap_shape: CapShape = Field(description="Форма шляпки")
    cap_surface: CapSurface = Field(description="Поверхность шляпки")
    cap_color: Color = Field(description="Цвет шляпки")
    does_bruise_or_bleed: Bool = Field(description="")
    gill_attachment: GillAttachment = Field(description="")
    gill_color: Color = Field(description="Цвет жабр")
    stem_color: Color = Field(description="Цвет ножки")
    has_ring: Bool = Field(description="Наличие колец")
    ring_type: RingType = Field(description="Тип колец")
    habitat: Habitat = Field(description="Среда обитания")
    season: Season = Field(description="Сезон")
    cap_diameter: float = Field(description="Диаметр шляпки", ge=0, le=58.4)
    stem_height: float = Field(description="Длина ножки", ge=0, le=27.3)
    stem_width: float = Field(description="Ширина ножки", ge=0, le=66.3)


class MushroomsBatch(BaseModel):
    """Pydantic-модель списка грибов

    Атрибуты:
        mushrooms (List[MushroomModel]): список MushroomModel
    """    
    mushrooms: List[MushroomModel]
