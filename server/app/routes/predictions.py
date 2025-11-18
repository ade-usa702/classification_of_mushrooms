import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
import joblib
import pandas as pd
from typing import List
from app.models import MushroomModel, MushroomsBatch
from ml.prepared_data import prepared_data
from app.enums.cap_shape import CapShape
from app.enums.cap_surface import CapSurface
from app.enums.color import Color
from app.enums.bool import Bool
from app.enums.gill_attachment import GillAttachment
from app.enums.habitat import Habitat
from app.enums.ring_type import RingType
from app.enums.season import Season


router = APIRouter(prefix="/predict", tags=["Prediction"])

# путь к модели
BASE_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "mushrooms_model.pkl")
if os.path.exists(MODEL_PATH):
    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
else:
    artifact = None
    model = None
    print("Файл модели ещё не существует")


@router.get(
    '/'
)
def predict(mushroom: MushroomModel = Depends()) -> dict:
    """Определение(предсказывание) гриба: ядовитый или съедобный 

    Args:
        mushroom (MushroomModel): Pydantic-модель гриба

    Return: 
        dict: Булево значение(True/False), ядовитый или нет
    """ 
    data = pd.DataFrame([{
        "cap-shape": mushroom.cap_shape,
        "cap-surface": mushroom.cap_surface,
        "cap-color": mushroom.cap_color,
        "does-bruise-or-bleed": mushroom.does_bruise_or_bleed,
        "gill-attachment": mushroom.gill_attachment,
        "gill-color": mushroom.gill_color,
        "stem-color": mushroom.stem_color,
        "has-ring": mushroom.has_ring,
        "ring-type": mushroom.ring_type,
        "habitat": mushroom.habitat,
        "season": mushroom.season,
        "cap-diameter": mushroom.cap_diameter,
        "stem-height": mushroom.stem_height,
        "stem-width": mushroom.stem_width,
    }])
    data_prep = prepared_data(data)
    if model:
        prediction = model.predict(data_prep)[0] 
        return {
            "poisonous": bool(prediction),
        }
    return {"poisonous": None}


@router.get(
    "/predict_proba",
)
def predict_proba(
        cap_shape: CapShape,
        cap_surface: CapSurface,
        cap_color: Color,
        does_bruise_or_bleed: Bool,
        gill_attachment: GillAttachment,
        gill_color: Color,
        stem_color: Color,
        has_ring: Bool,
        ring_type: RingType,
        habitat: Habitat,
        season: Season,
        cap_diameter: float,
        stem_height: float,
        stem_width: float,
) -> dict:
    """Определение(предсказывание) вероятности ядовитости гриба.

    Return: 
        dict: Численное значение вероятности ядовитости гриба"""
    data = pd.DataFrame([{
        "cap-shape": cap_shape,
        "cap-surface": cap_surface,
        "cap-color": cap_color,
        "does-bruise-or-bleed": does_bruise_or_bleed,
        "gill-attachment": gill_attachment,
        "gill-color": gill_color,
        "stem-color": stem_color,
        "has-ring": has_ring,
        "ring-type": ring_type,
        "habitat": habitat,
        "season": season,
        "cap-diameter": cap_diameter,
        "stem-height": stem_height,
        "stem-width": stem_width,
    }])
    data_prepared = prepared_data(data)
    if model:
        poisonous_prob = model.predict_proba(data_prepared)[0][1]
        return {
            "probability_of_poisonous": float(poisonous_prob) if poisonous_prob is not None else None
        }
    return {"probability_of_poisonous": None}


@router.post(
    "/predict_batch",
)
def predict_batch(batch: MushroomsBatch = Depends()) -> List[dict]:
    """Определение(предсказывание) списка грибов: ядовитый или съедобный.
    
    Return: 
        List(dict): Булево значение(True/False), ядовитый или нет"""
    # Проверка что все списки одной длины
    n = len(batch.mushrooms)
    
    data = pd.DataFrame([{
        "cap-shape": batch.mushrooms[i].cap_shape,
        "cap-surface": batch.mushrooms[i].cap_surface,
        "cap-color": batch.mushrooms[i].cap_color,
        "does-bruise-or-bleed": batch.mushrooms[i].does_bruise_or_bleed,
        "gill-attachment": batch.mushrooms[i].gill_attachment,
        "gill-color": batch.mushrooms[i].gill_color,
        "stem-color": batch.mushrooms[i].stem_color,
        "has-ring": batch.mushrooms[i].has_ring,
        "ring-type": batch.mushrooms[i].ring_type,
        "habitat": batch.mushrooms[i].habitat,
        "season": batch.mushrooms[i].season,
        "cap-diameter": batch.mushrooms[i].cap_diameter,
        "stem-height": batch.mushrooms[i].stem_height,
        "stem-width": batch.mushrooms[i].stem_width,
    } for i in range(n)])
    data_prepared = prepared_data(data)
    if model:
        predictions = model.predict(data_prepared)
        results = []
        for pred in predictions:
            results.append({
                "poisonous": bool(pred),
            })
        return results
    return n * {"poisonous": None}


@router.get(
    "/predict_proba_batch",
)
def predict_proba_batch(
        cap_shape: List[str] = Query(...),
        cap_surface: List[str] = Query(...),
        cap_color: List[str] = Query(...),
        does_bruise_or_bleed: List[str] = Query(...),
        gill_attachment: List[str] = Query(...),
        gill_color: List[str] = Query(...),
        stem_color: List[str] = Query(...),
        has_ring: List[str] = Query(...),
        ring_type: List[str] = Query(...),
        habitat: List[str] = Query(...),
        season: List[str] = Query(...),
        cap_diameter: List[float] = Query(...),
        stem_height: List[float] = Query(...),
        stem_width: List[float] = Query(...),
) -> List[dict]:
    """Определение(предсказывание) вероятности ядовитости списка грибов.
    
    Return: 
        List(dict): Численные значения вероятности ядовитости грибов"""
    # Проверка что все списки одной длины
    n = len(cap_shape)
    if not all(len(lst) == n for lst in [cap_surface, 
                                         cap_color, does_bruise_or_bleed, 
                                         gill_attachment, gill_color,
                                         stem_color, has_ring, ring_type, 
                                         habitat, season, cap_diameter,
                                         stem_height, stem_width]):
        return {"error": "Все списки должны быть одной длины"}
    
    data = pd.DataFrame([{
        "cap-shape": cap_shape[i],
        "cap-surface": cap_surface[i],
        "cap-color": cap_color[i],
        "does-bruise-or-bleed": does_bruise_or_bleed[i],
        "gill-attachment": gill_attachment[i],
        "gill-color": gill_color[i],
        "stem-color": stem_color[i],
        "has-ring": has_ring[i],
        "ring-type": ring_type[i],
        "habitat": habitat[i],
        "season": season[i],
        "cap-diameter": cap_diameter[i],
        "stem-height": stem_height[i],
        "stem-width": stem_width[i],
    } for i in range(n)])
    data_prepared = prepared_data(data)
    if model:
        probabilities = model.predict_proba(data_prepared)[:, 1] 

        results = []
        for prob in probabilities:
            results.append({
                "probability_of_poisonous": float(prob) if prob is not None else None
            })
        return results
    return n * {"probability_of_poisonous": None}


@router.get(
    "/status",
)
def status() -> dict:
    """Возвращает дату, когда модель была обучена

    Returns:
        dict: Дата, когда модель была обучена
    """
    try:
        return {
            "model_trained_at": artifact["trained_at"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера при получении статуса модели: {e}"
        )