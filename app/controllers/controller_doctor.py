from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.doctor import Doctor
from app.models.user import User


def get_doctor_by_id(id, session, current_user) -> Doctor:
    '''
    Поиск врача по ID
    :param id:
    :param session:
    :return: Doctor
    '''
    try:
        result = session.get(Doctor, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_doctor(data, session, current_user) -> Optional[Doctor]:
    '''
    Добавление врача
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Doctor(
            user_id=data.user_id,
            specialization=data.specialization,
            office_number=data.office_number,
            schedule=data.schedule,
            department_id=data.department_id,
            is_chief=data.is_chief
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


def delete_doctor(id, session, current_user) -> str:
    '''
    Удаление врача
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Doctor, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_doctor(id, data, session, current_user) -> Doctor:
    '''
    Изменение врача
    :param data:
    :param session:
    :return: Ward
    '''
    try:
        result = session.get(Doctor, id)
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


def show_doctors(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[Doctor]:
    '''
    Вывод информации о врачах
    :param session:
    :param page
    :param size
    :return: Page[Ward]
    '''
    try:
        sql = select(Doctor)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")