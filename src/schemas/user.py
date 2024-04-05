from datetime import date


from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    """
    Schema representing user data for input validation.
    """

    first_name: str = Field(min_length=3, max_length=50)
    second_name: str = Field(min_length=3, max_length=50)
    email_add: EmailStr
    phone_num: str = Field()
    birth_date: date


class UserResponse(BaseModel):
    """
    Schema representing user data for response.
    """

    id: int = 1
    first_name: str
    second_name: str
    email_add: EmailStr
    phone_num: str
    birth_date: date

    class Config:
        """
        Configuration class for UserResponse.
        """

        from_attributes = True
