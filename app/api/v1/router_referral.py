from fastapi import Depends, APIRouter
from app.controllers.controller_referral import *
from app.db.session import get_session
from app.schemas.schemas_referral import ReferralCreate
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/referral/{referral_id}', description='Поиск направления по ID')
def router_get_referral_by_id(
    referral_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return get_referral_by_id(referral_id, session, current_user)

@router.post('/referral', status_code=status.HTTP_201_CREATED, description='Добавление направления')
def router_add_referral(
    data: ReferralCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return add_referral(data, session, current_user)

@router.delete('/referral/{referral_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление направления')
def router_delete_referral(
    referral_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return delete_referral(referral_id, session, current_user)

@router.put('/referral/{referral_id}', status_code=status.HTTP_200_OK, description='Изменение направления')
def router_update_referral(
    referral_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return update_referral(referral_id, data, session, current_user)

@router.get('/referral', description='Вывод информации о направлениях', response_model=Page[Referral])
def router_show_referral(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return show_referrals(session, page, size, current_user)