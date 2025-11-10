from fastapi import Depends, APIRouter
from app.controllers.controller_icd import *
from app.db.session import get_session
from app.schemas.schemas_icd import CreateICD
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/icd/{icd_id}', description='Поиск МКБ по ID')
def router_get_icd_by_id(
    icd_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor", "employee_doctor"]))
):
    return get_icd_by_id(icd_id, session, current_user)

@router.post('/icd', status_code=status.HTTP_201_CREATED, description='Добавление МКБ')
def router_add_icd(
    data: CreateICD,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return add_icd(data, session, current_user)

@router.delete('/icd/{icd_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление МКБ')
def router_delete_icd(
    icd_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return delete_icd(icd_id, session, current_user)

@router.put('/icd/{icd_id}', status_code=status.HTTP_200_OK, description='Изменение МКБ')
def router_update_icd(
    icd_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return update_icd(icd_id, data, session, current_user)

@router.get('/icd', description='Вывод информации о МКБ', response_model=Page[ICD])
def router_show_icd(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor", "employee_doctor"]))
):
    return show_icd(session, page, size, current_user)