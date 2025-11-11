from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.daily_record import DailyRecord
from app.models.user import User


def get_daily_record_by_id(id, session, current_user) -> DailyRecord:
    '''
    Поиск ежедневной записи по ID
    :param id:
    :param session:
    :return: DailyRecord
    '''
    try:
        result = session.get(DailyRecord, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_daily_record(data, session, current_user) -> Optional[DailyRecord]:
    '''
    Добавление ежедневной записи
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = DailyRecord(
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            record_date=data.record_date,
            subjective_data=data.subjective_data,
            plan=data.plan
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


def delete_daily_record(id, session, current_user) -> str:
    '''
    Удаление ежедневной записи
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(DailyRecord, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_daily_record(id, data, session, current_user) -> DailyRecord:
    '''
    Изменение ежедневной записи
    :param data:
    :param session:
    :return: DailyRecord
    '''
    try:
        result = session.get(DailyRecord, id)
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


def show_daily_record(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[DailyRecord]:
    '''
    Вывод информации о ежедневной записях
    :param session:
    :param page
    :param size
    :return: Page[DailyRecord]
    '''
    try:
        sql = select(DailyRecord)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")