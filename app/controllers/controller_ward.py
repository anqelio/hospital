from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.models.ward import Ward
from app.models.user import User


def get_ward_by_id(id, session, current_user) -> Ward:
    '''
    Поиск палаты по ID
    :param id:
    :param session:
    :return: Ward
    '''
    try:
        result = session.get(Ward, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_ward(data, session, current_user) -> Optional[Ward]:
    '''
    Добавление палаты
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = Ward(
            number=data.number,
            department_id=data.department_id,
            gender_type=data.gender_type
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


def delete_ward(id, session, current_user) -> str:
    '''
    Удаление палаты
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(Ward, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_ward(id, data, session, current_user) -> Ward:
    '''
    Изменение палаты
    :param data:
    :param session:
    :return: Ward
    '''
    try:
        result = session.get(Ward, id)
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


def show_wards(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[Ward]:
    '''
    Вывод информации о палатах
    :param session:
    :param page
    :param size
    :return: Page[Ward]
    '''
    try:
        sql = select(Ward)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
