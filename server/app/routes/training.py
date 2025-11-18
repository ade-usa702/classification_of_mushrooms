from fastapi import APIRouter, HTTPException, UploadFile, File
from ml.mushrooms_model import MushroomsModel
from utils.extract_csv_from_zip import extract_csv_from_zip

router = APIRouter(prefix="/fit", tags=["Training"])


@router.post("/")
def fit_model(filename: UploadFile = File(...)) -> dict:
    """Обучение модели на загруженном файле с данными.

    Args:
        filename (UploadFile, optional): Загруженный файл

    Returns:
        dict:
            Словарь вида:
            {
                "success": bool,
            }

            - success — True, если модель успешно обучена  
    """    
    try:
        file_ext = filename.filename.split(".")[-1].lower()
        if file_ext == "zip":
            file = extract_csv_from_zip(filename)
        elif file_ext == "csv":
            file = filename.file
        else:
            raise HTTPException(status_code=400, 
                                detail="Некорректное расширение файла. Допустимо только .csv")
        mushroom = MushroomsModel(file)
        mushroom.preprocess_data()
        mushroom.fit_model()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

