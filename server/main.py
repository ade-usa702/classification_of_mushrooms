from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.routes.predictions import router as router_pred
from app.routes.training import router as router_train


TITLE_APP = "🍄 The toxicity of mushrooms Prediction API"
VERSION_APP = "0.0.1"

app = FastAPI(title=TITLE_APP, version=VERSION_APP)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["Переадресация"]
)
def redirect_func():
    """Get-запрос на переадресацию
    """    
    return RedirectResponse(url='/docs')


app.include_router(router_pred)
app.include_router(router_train)

