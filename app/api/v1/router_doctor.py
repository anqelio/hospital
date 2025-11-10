from fastapi import Depends, APIRouter
from app.controllers.controller_doctor import *
from app.db.session import get_session
from app.schemas.schemas_doctor import DoctorCreate
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/doctor/{doctor_id}', description='Поиск врача по ID')
def router_get_doctor_by_id(
    doctor_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return get_doctor_by_id(doctor_id, session, current_user)

@router.post('/doctor', status_code=status.HTTP_201_CREATED, description='Добавление врача')
def router_add_doctor(
    data: DoctorCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return add_doctor(data, session, current_user)

@router.delete('/doctor/{doctor_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление врача')
def router_delete_doctor(
    doctor_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return delete_doctor(doctor_id, session, current_user)

@router.put('/doctor/{doctor_id}', status_code=status.HTTP_200_OK, description='Изменение врача')
def router_update_doctor(
    doctor_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return update_doctor(doctor_id, data, session, current_user)

@router.get('/doctor', description='Вывод информации о врачах', response_model=Page[Doctor])
def router_show_doctor(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return show_doctors(session, page, size, current_user)