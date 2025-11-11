from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.referral import Referral
from app.models.user import User


def get_referral_by_id(id, session, current_user) -> Referral:
    '''
    Поиск направления по ID
    :param id:
    :param session:
    :return: Referral
    '''
    try:
        result = session.get(Referral, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_referral(data, session, current_user) -> Optional[Referral]:
    '''
    Добавление направления
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Referral(
            patient_id=data.patient_id,
            attending_doctor_id=data.attending_doctor_id,
            reason=data.reason,
            referral_date=data.referral_date,
            is_completed=data.is_completed
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


def delete_referral(id, session, current_user) -> str:
    '''
    Удаление направления
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Referral, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_referral(id, data, session, current_user) -> Referral:
    '''
    Изменение направления
    :param data:
    :param session:
    :return: Referral
    '''
    try:
        result = session.get(Referral, id)
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


def show_referrals(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[Referral]:
    '''
    Вывод информации о направлениях
    :param session:
    :param page
    :param size
    :return: Page[Referral]
    '''
    try:
        sql = select(Referral)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")