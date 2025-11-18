import zipfile
import io

from fastapi import UploadFile


def extract_csv_from_zip(upload_file: UploadFile) -> io.BytesIO | None:
    """Извлечение CSV из ZIP и возврат его содержимого

    Args:
        upload_file (UploadFile): ZIP-файл

    Returns:
        io.BytesIO | None: Байтовый файл или None
    """    
    zip_bytes = upload_file.file.read()
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        for name in z.namelist():
            if name.lower().endswith(".csv"):
                return io.BytesIO(z.read(name))
    return None