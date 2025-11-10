from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.patient import Patient
from app.models.user import User


def get_patient_by_id(id, session, current_user) -> Patient:
    '''
    Поиск пациента по ID
    :param id:
    :param session:
    :return: Patient
    '''
    try:
        result = session.get(Patient, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_patient(data, session, current_user) -> Optional[Patient]:
    '''
    Добавление пациента
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Patient(
            full_name=data.full_name,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            address=data.address,
            phone=data.phone,
            ward_id=data.ward_id,
            attending_doctor_id=data.attending_doctor_id,
            date_start=data.date_start,
            date_end=data.date_end,
            status=data.status
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


def delete_patient(id, session, current_user) -> str:
    '''
    Удаление пациента
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Patient, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_patient(id, data, session, current_user) -> Patient:
    '''
    Изменение пациента
    :param data:
    :param session:
    :return: Patient
    '''
    try:
        result = session.get(Patient, id)
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


def show_patients(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[Patient]:
    '''
    Вывод информации о пациентах
    :param session:
    :param page
    :param size
    :return: Page[Patient]
    '''
    try:
        sql = select(Patient)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")