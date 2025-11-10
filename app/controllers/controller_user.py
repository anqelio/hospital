from typing import Optional
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.core.hashing_password import get_password_hash
from app.models.user import User


def get_user_by_id(id, session, current_user) -> User:
    '''
    Поиск пользователя по ID
    :param id:
    :param session:
    :return: Trip
    '''
    try:
        result = session.get(User, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        return result
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def add_user(data, session, current_user) -> Optional[User]:
    '''
    Добавление пользователя
    :param data:
    :param session:
    :return: data
    '''
    try:
        obj = User(
            username=data.username,
            password=data.password,
            full_name=data.full_name,
            role=data.role,
            email=data.email,
            phone=data.phone,
            is_active=data.is_active,
            hashed_password=get_password_hash(data.password)
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


def delete_user(id, session, current_user) -> str:
    '''
    Удаление пользователя
    :param id:
    :param session:
    :return: str
    '''
    try:
        result = session.get(User, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID не найден")
        session.delete(result)
        session.commit()
        return "Удаление выполнено"
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")


def update_user(id, data, session, current_user) -> User:
    '''
    Изменение пользователя
    :param data:
    :param session:
    :return: User
    '''
    try:
        result = session.get(User, id)
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


def show_users(session: Session, page: int = 1, size: int = 10, current_user: User = None) -> Page[User]:
    '''
    Вывод информации о пользователях
    :param session:
    :param page
    :param size
    :return: Page[User]
    '''
    try:
        sql = select(User)
        return paginate(session, sql)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Внутренняя ошибка сервера: {str(e)}")
