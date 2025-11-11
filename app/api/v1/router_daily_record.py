from fastapi import Depends, APIRouter
from app.controllers.controller_daily_record import *
from app.db.session import get_session
from app.schemas.schemas_daily_record import CreateDailyRecord
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/daily_record/{daily_record_id}', description='Поиск ежедневной записи по ID')
def router_get_patient_by_id(
    daily_record_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return get_daily_record_by_id(daily_record_id, session, current_user)

@router.post('/daily_record', status_code=status.HTTP_201_CREATED, description='Добавление ежедневной записи')
def router_add_patient(
    data: CreateDailyRecord,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return add_daily_record(data, session, current_user)

@router.delete('/daily_record/{daily_record_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление ежедневной записи')
def router_delete_patient(
    daily_record_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return delete_daily_record(daily_record_id, session, current_user)

@router.put('/daily_record/{daily_record_id}', status_code=status.HTTP_200_OK, description='Изменение ежедневной записи')
def router_update_patient(
    daily_record_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return update_daily_record(daily_record_id, data, session, current_user)

@router.get('/daily_record', description='Вывод информации о ежедневной записях', response_model=Page[DailyRecord])
def router_show_patient(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return show_daily_record(session, page, size, current_user)