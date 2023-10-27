from fastapi import APIRouter

from app.api.endpoints import (charity_router, donation_router, google_router,
                               user_router)

main_router = APIRouter()
main_router.include_router(charity_router, prefix='/charity_project', tags=['Charity'])
main_router.include_router(donation_router, prefix='/donation', tags=['Donation'])
main_router.include_router(google_router, prefix='/google', tags=['Google'])
main_router.include_router(user_router)
