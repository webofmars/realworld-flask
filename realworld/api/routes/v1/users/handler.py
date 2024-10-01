import bcrypt
import typing as typ
from logging import Logger
from sqlalchemy.engine import Connection
from sqlalchemy.sql import text as satext

from realworld.api.core.models import DBUser
from .models import UpdateUserData, RegisterUserData, UserData


logger = Logger(__name__)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def is_valid_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_user(db_conn: Connection, data: RegisterUserData) -> typ.Optional[DBUser]:
    result = db_conn.execute(
        satext(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (:username, :email, :password_hash)
            ON CONFLICT (username) DO NOTHING
            RETURNING id, username, email, bio, image, created_date, updated_date
            """
        ).bindparams(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
        )
    ).fetchone()

    if result:
        return DBUser(
            user_id=str(result.id),
            username=result.username,
            email=result.email,
            bio=result.bio,
            image=(bytes(result.image) if result.image else None),
        )
    return None


def update_user(
    db_conn: Connection, user_id: str, data: UpdateUserData
) -> typ.Optional[UserData]:
    result = db_conn.execute(
        satext(
            """
            UPDATE users
            SET email = :email,
                bio = :bio,
                image = :image,
                updated_date = CURRENT_TIMESTAMP
            WHERE id = :user_id
            RETURNING username, email, bio, image
            """
        ).bindparams(
            user_id=user_id,
            email=data.email,
            bio=data.bio,
            image=(data.image.encode() if data.image else None),
        )
    ).fetchone()

    if result:
        return UserData(
            username=result.username,
            email=result.email,
            bio=result.bio,
            image=(bytes(result.image) if result.image else None),
        )
    return None


def validate_user_creds(
    db_conn: Connection, email: str, password: str
) -> typ.Optional[DBUser]:
    result = db_conn.execute(
        satext(
            """
            SELECT id, username, email, password_hash, bio, image
            FROM users
            WHERE email = :email
            """
        ).bindparams(email=email)
    ).fetchone()

    if not result:
        return False

    if is_valid_password(password, result.password_hash):
        return DBUser(
            user_id=str(result.id),
            username=result.username,
            email=result.email,
            bio=result.bio,
            image=(bytes(result.image) if result.image else None),
        )

    return False


def get_user(db_conn: Connection, user_id: str) -> typ.Optional[UserData]:
    result = db_conn.execute(
        satext(
            """
            SELECT id, username, email, bio, image, created_date, updated_date
            FROM users
            WHERE id = :user_id
            """
        ).bindparams(user_id=user_id)
    ).fetchone()

    if result:
        return UserData(
            username=result.username,
            email=result.email,
            bio=result.bio,
            image=(bytes(result.image) if result.image else None),
        )
    return None
