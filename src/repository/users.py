from datetime import datetime, timedelta
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_


from schemas.user import UserSchema
from entity.models import User


async def get_users(limit: int, offset: int, db: AsyncSession) -> list[User]:
    """
    Retrieves a list of users from the database.

    Args:
        limit (int): The maximum number of users to retrieve.
        offset (int): The offset for pagination.
        db (AsyncSession): The asynchronous database session.

    Returns:
        list[User]: A list of users retrieved from the database.
    """
    search = select(User).offset(offset).limit(limit)
    users = await db.execute(search)
    return users.scalars().all()


async def get_users_by(
    first_name: str = None,
    second_name: str = None,
    email_add: str = None,
    db: AsyncSession = None,
) -> list[User]:
    """
    Retrieves users from the database based on specified criteria.

    Args:
        first_name (str, optional): The first name of the user.
        second_name (str, optional): The second name of the user.
        email_add (str, optional): The email address of the user.
        db (AsyncSession, optional): The asynchronous database session.

    Returns:
        list[User]: A list of users retrieved from the database.
    """
    search = select(User)
    if first_name and second_name and email_add:
        search = search.where(
            or_(
                User.first_name == first_name,
                User.second_name == second_name,
                User.email_add == email_add,
            )
        )

    elif first_name and second_name:
        search = search.where(
            or_(
                User.first_name == first_name,
                User.second_name == second_name,
                User.email_add == email_add,
            )
        )

    elif first_name and email_add:
        search = search.where(
            or_(User.first_name == first_name, User.email_add == email_add)
        )

    elif second_name and email_add:
        search = search.where(
            or_(User.second_name == second_name, User.email_add == email_add)
        )

    elif first_name:
        search = search.where(User.first_name == first_name)

    elif second_name:
        search = search.where(User.second_name == second_name)

    elif email_add:
        search = search.where(User.email_add == email_add)

    else:
        return []

    users = await db.execute(search)
    print(type(users.scalars().all()))
    return users.scalars().all()


async def get_user(user_id: int, db: AsyncSession) -> User:
    """
    Retrieves a user from the database by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (AsyncSession): The asynchronous database session.

    Returns:
        User: The user retrieved from the database.
    """
    search = select(User).filter_by(id=user_id)
    user = await db.execute(search)
    return user.scalar_one_or_none()


async def get_users_birth(limit: int, db: AsyncSession) -> list[User]:
    """
    Retrieves users from the database whose birthdays fall within a specified limit.

    Args:
        limit (int): The limit for the range of birthdays.
        db (AsyncSession): The asynchronous database session.

    Returns:
        list[User]: A list of users retrieved from the database.
    """
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=limit)

    search = select(User).filter(
        User.birth_date >= current_date, User.birth_date <= end_date
    )
    result = await db.execute(search)

    return result.scalars().all()


async def create_user(body: UserSchema, db: AsyncSession) -> User:
    """
    Creates a new user in the database.

    Args:
        body (UserSchema): The data of the user to be created.
        db (AsyncSession): The asynchronous database session.

    Returns:
        User: The user that was created in the database.
    """
    user = User(**body.model_dump(exclude_unset=True))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(user_id: int, body: UserSchema, db: AsyncSession) -> User:
    """
    Updates an existing user in the database.

    Args:
        user_id (int): The ID of the user to be updated.
        body (UserSchema): The updated data for the user.
        db (AsyncSession): The asynchronous database session.

    Returns:
        User: The user that was updated in the database.
    """
    search = select(User).filter_by(id=user_id)
    result = await db.execute(search)
    user = result.scalar_one_or_none()
    if user:
        user.first_name = body.first_name
        user.second_name = body.second_name
        user.email_add = body.email_add
        user.phone_num = body.phone_num
        user.birth_date = body.birth_date
        await db.commit()
        await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession) -> User:
    """
    Deletes a user from the database.

    Args:
        user_id (int): The ID of the user to be deleted.
        db (AsyncSession): The asynchronous database session.

    Returns:
        User: The user that was deleted from the database.
    """
    search = select(User).filter_by(id=user_id)
    user = await db.execute(search)
    user = user.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user
