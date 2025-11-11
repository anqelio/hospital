from fastapi import Depends, APIRouter
from app.controllers.controller_medical_card import *
from app.db.session import get_session
from app.schemas.schemas_medical_card import MedicalRecordCreate
from app.core.authorization import require_roles

router = APIRouter()

@router.get('/medical_card/{medical_card_id}', description='Поиск мед. книжки по ID')
def router_get_patient_by_id(
    medical_card_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return get_medical_card_by_id(medical_card_id, session, current_user)

@router.post('/medical_card', status_code=status.HTTP_201_CREATED, description='Добавление мед. книжки')
def router_add_patient(
    data: MedicalRecordCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return add_medical_card(data, session, current_user)

@router.delete('/medical_card/{medical_card_id}', status_code=status.HTTP_204_NO_CONTENT, description='Удаление мед. книжки')
def router_delete_patient(
    medical_card_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return delete_medical_card(medical_card_id, session, current_user)

@router.put('/medical_card/{medical_card_id}', status_code=status.HTTP_200_OK, description='Изменение мед. книжки')
def router_update_patient(
    medical_card_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_roles(["employee_hospital"]))
):
    return update_medical_card(medical_card_id, data, session, current_user)

@router.get('/medical_card', description='Вывод информации о мед. книжках', response_model=Page[MedicalRecord])
def router_show_patient(
    session: Session = Depends(get_session),
    page: int = 1,
    size: int = 10,
    current_user: User = Depends(require_roles(["main_doctor", "employee_hospital"]))
):
    return show_medical_cards(session, page, size, current_user)