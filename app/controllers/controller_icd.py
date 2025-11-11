from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.icd import ICD
from app.models.user import User


def get_icd_by_id(id, session, current_user) -> ICD:
    '''
    Поиск МКБ по ID
    :param id:
    :param session:
    :return: ICD
    '''
    try:
        result = session.get(ICD, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_icd(data, session, current_user) -> Optional[ICD]:
    '''
    Добавление МКБ
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = ICD(
            code=data.code,
            description=data.description
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


def delete_icd(id, session, current_user) -> str:
    '''
    Удаление МКБ
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(ICD, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_icd(id, data, session, current_user) -> ICD:
    '''
    Изменение МКБ
    :param data:
    :param session:
    :return: ICD
    '''
    try:
        result = session.get(ICD, id)
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


def show_icd(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[ICD]:
    '''
    Вывод информации о МКБ
    :param session:
    :param page
    :param size
    :return: Page[ICD]
    '''
    try:
        sql = select(ICD)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")