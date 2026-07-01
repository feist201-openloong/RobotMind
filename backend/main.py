from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.database import init_db
from app.routes.code import router as code_router
from app.routes.knowledge import router as knowledge_router
from app.routes.learning import router as learning_router
from app.routes.article import router as article_router
from app.routes.todo import router as todo_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(code_router, prefix=settings.API_V1_PREFIX)
app.include_router(knowledge_router, prefix=settings.API_V1_PREFIX)
app.include_router(learning_router, prefix=settings.API_V1_PREFIX)
app.include_router(article_router, prefix=settings.API_V1_PREFIX)
app.include_router(todo_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok", "version": settings.VERSION}


@app.get("/")
def root():
    return {"message": f"欢迎使用 {settings.PROJECT_NAME} API"}
