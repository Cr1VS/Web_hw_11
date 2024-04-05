import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession


from schemas.user import UserSchema, UserResponse
from repository import users as repository_users
from database.db import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    """
    Get a list of users.

    Args:
        limit (int): The maximum number of users to retrieve.
        offset (int): The number of users to skip.
        db (AsyncSession): The database session.

    Returns:
        list[UserResponse]: A list of user objects.
    """
    users = await repository_users.get_users(limit, offset, db)
    return users


@router.get("/birth_date", response_model=list[UserResponse])
async def get_users_birth(
    limit: int = Query(7, ge=7, le=100), db: AsyncSession = Depends(get_db)
) -> list[UserResponse]:
    """
    Get a list of users whose birthdays fall within a specified limit.

    Args:
        limit (int): The number of days to search for birthdays.
        db (AsyncSession): The database session.

    Returns:
        list[UserResponse]: A list of user objects.
    """
    users = await repository_users.get_users_birth(limit, db)
    return users


@router.get("/search_by", response_model=list[UserResponse])
async def get_users_by(
    first_name: str = Query(None, min_length=3, description="First name search query"),
    second_name: str = Query(
        None, min_length=3, description="Second name search query"
    ),
    email_add: str = Query(None, min_length=3, description="Email search query"),
    db: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    """
    Search for users by their first name, second name, or email.

    Args:
        first_name (str): The first name to search for.
        second_name (str): The second name to search for.
        email_add (str): The email address to search for.
        db (AsyncSession): The database session.

    Returns:
        list[UserResponse]: A list of user objects.
    """
    users = await repository_users.get_users_by(first_name, second_name, email_add, db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Get a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (AsyncSession): The database session.

    Returns:
        UserResponse: The user object.
    """
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserSchema,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Create a new user.

    Args:
        body (UserSchema): The user data to create.
        db (AsyncSession): The database session.

    Returns:
        UserResponse: The created user object.
    """
    user = await repository_users.create_user(body, db)
    return user


@router.put("/{user_id}")
async def update_user(
    body: UserSchema,
    user_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Update an existing user.

    Args:
        body (UserSchema): The updated user data.
        user_id (int): The ID of the user to update.
        db (AsyncSession): The database session.

    Returns:
        UserResponse: The updated user object.
    """
    user = await repository_users.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (AsyncSession): The database session.

    Returns:
        UserResponse: The deleted user object.
    """
    user = await repository_users.delete_user(user_id, db)
    return user
