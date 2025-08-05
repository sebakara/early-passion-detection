from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, children, games, sessions, passions, analytics, questions

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(children.router, prefix="/children", tags=["children"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(passions.router, prefix="/passions", tags=["passions"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"]) 