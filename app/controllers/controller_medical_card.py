from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.medical_card import MedicalRecord
from app.models.user import User


def get_medical_card_by_id(id, session, current_user) -> MedicalRecord:
    '''
    Поиск мед. книжки по ID
    :param id:
    :param session:
    :return: MedicalRecord
    '''
    try:
        result = session.get(MedicalRecord, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_medical_card(data, session, current_user) -> Optional[MedicalRecord]:
    '''
    Добавление мед. книжки
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = MedicalRecord(
            patient_id=data.patient_id,
            diagnosis=data.diagnosis,
            icd_id=data.icd_id,
            complaints=data.complaints,
            treatment=data.treatment,
            outcomes=data.outcomes,
            created_by=data.created_by
        )
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Ошибка: нарушение целостности данных")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


def delete_medical_card(id, session, current_user) -> str:
    '''
    Удаление мед. книжки
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(MedicalRecord, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_medical_card(id, data, session, current_user) -> MedicalRecord:
    '''
    Изменение мед. книжки
    :param data:
    :param session:
    :return: MedicalRecord
    '''
    try:
        result = session.get(MedicalRecord, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(result, key, value)
        session.commit()
        session.refresh(result)
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def show_medical_cards(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[
    MedicalRecord]:
    '''
    Вывод информации о мед. книжках
    :param session:
    :param page
    :param size
    :return: Page[MedicalRecord]
    '''
    try:
        sql = select(MedicalRecord)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
