from fastapi import Depends, APIRouter
from app.controllers.controller_department import *
from app.db.session import get_session
from app.models.department import Department
from app.schemas.schemas_department import DepartmentCreate
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/department/{department_id}', description='Поиск отделения по ID')
def router_get_department_by_id(
    department_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return get_department_by_id(department_id, session, current_user)

@router.post('/department', status_code=status.HTTP_201_CREATED, description='Добавление отделения')
def router_add_ward(
    data: DepartmentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return add_department(data, session, current_user)

@router.delete('/department/{department_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление отделения')
def router_delete_ward(
    department_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return delete_department(department_id, session, current_user)

@router.put('/department/{department_id}', status_code=status.HTTP_200_OK, description='Изменение отделения')
def router_update_ward(
    department_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return update_department(department_id, data, session, current_user)

@router.get('/department', description='Вывод информации о отделениях', response_model=Page[Department])
def router_show_ward(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return show_departments(session, page, size, current_user)