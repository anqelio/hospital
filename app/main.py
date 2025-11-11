from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_pagination import add_pagination
from app.db.database import *
from app.models import *
from app.api.v1.router_user import router as router_user_v1
from app.api.v1.router_auth import router as router_auth_v1
from app.api.v1.router_ward import router as router_ward_v1
from app.api.v1.router_department import router as router_department_v1
from app.api.v1.router_doctor import router as router_doctor_v1
from app.api.v1.router_patient import router as router_patient_v1
from app.api.v1.router_icd import router as router_icd_v1
from app.api.v1.router_referral import router as router_referral_v1
from app.api.v1.router_medical_card import router as router_medical_record_v1
from app.api.v1.router_daily_record import router as router_daily_record_v1

main_app = FastAPI()


@asynccontextmanager
async def on_startup(app: FastAPI):
    init_db()
    yield
    close_db()


app_v1 = FastAPI(title="Hospital API v1", version="1.0.0",
                 openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs",
                 redoc_url="/api/v1/redoc",
                 description='Приложение, предназначенное для обработки данных о пациентах стационара больницы.'
                 , lifespan=on_startup)

main_app.mount("/api/v1", app_v1)

app_v1.include_router(router_auth_v1, tags=['Authorization'])
app_v1.include_router(router_user_v1, tags=['User'])
app_v1.include_router(router_ward_v1, tags=['Ward'])
app_v1.include_router(router_department_v1, tags=['Department'])
app_v1.include_router(router_doctor_v1, tags=['Doctor'])
app_v1.include_router(router_patient_v1, tags=['Patient'])
app_v1.include_router(router_icd_v1, tags=['ICD'])
app_v1.include_router(router_referral_v1, tags=['Referral'])
app_v1.include_router(router_medical_record_v1, tags=['MedicalRecord'])
app_v1.include_router(router_daily_record_v1, tags=['DailyRecord'])
add_pagination(app_v1)