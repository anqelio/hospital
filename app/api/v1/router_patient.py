from fastapi import Depends, APIRouter
from app.controllers.controller_patient import *
from app.db.session import get_session
from app.schemas.schemas_patient import PatientCreate
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/patient/{patient_id}', description='Поиск пациента по ID')
def router_get_patient_by_id(
    patient_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor", "employee_doctor"]))
):
    return get_patient_by_id(patient_id, session, current_user)

@router.post('/patient', status_code=status.HTTP_201_CREATED, description='Добавление пациента')
def router_add_patient(
    data: PatientCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_doctor"]))
):
    return add_patient(data, session, current_user)

@router.delete('/patient/{patient_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление пациента')
def router_delete_patient(
    patient_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_doctor"]))
):
    return delete_patient(patient_id, session, current_user)

@router.put('/patient/{patient_id}', status_code=status.HTTP_200_OK, description='Изменение пациента')
def router_update_patient(
    patient_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_doctor"]))
):
    return update_patient(patient_id, data, session, current_user)

@router.get('/patient', description='Вывод информации о пациентах', response_model=Page[Patient])
def router_show_patient(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return show_patients(session, page, size, current_user)