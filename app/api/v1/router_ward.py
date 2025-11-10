from fastapi import Depends, APIRouter
from app.controllers.controller_ward import *
from app.db.session import get_session
from app.models.ward import Ward
from app.schemas.schemas_ward import WardCreate
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/ward/{ward_id}', description='Поиск палаты по ID')
def router_get_ward_by_id(
    ward_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return get_ward_by_id(ward_id, session, current_user)

@router.post('/ward', status_code=status.HTTP_201_CREATED, description='Добавление палаты')
def router_add_ward(
    data: WardCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return add_ward(data, session, current_user)

@router.delete('/ward/{ward_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление палаты')
def router_delete_ward(
    ward_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return delete_ward(ward_id, session, current_user)

@router.put('/ward/{ward_id}', status_code=status.HTTP_200_OK, description='Изменение палаты')
def router_update_ward(
    ward_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return update_ward(ward_id, data, session, current_user)

@router.get('/ward', description='Вывод информации о палатах', response_model=Page[Ward])
def router_show_ward(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor"]))
):
    return show_wards(session, page, size, current_user)