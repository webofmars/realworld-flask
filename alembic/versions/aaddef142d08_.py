"""Initial realworld schema and tables.

Revision ID: aaddef142d08
Revises: 
Create Date: 2024-03-17 16:05:40.243114

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aaddef142d08"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    ####################
    # -- extensions -- #
    ####################
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    #####################
    # -- data tables -- #
    #####################
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("username", sa.Text()),
        sa.Column("email", sa.Text()),
        sa.Column("password_hash", sa.Text()),
        sa.Column("image", sa.LargeBinary()),
        sa.Column("bio", sa.Text()),
        sa.Column(
            "created_date", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_date", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )

    op.create_table(
        "user_follows",
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("following_user_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["following_user_id"], ["users.id"]),
        sa.CheckConstraint("user_id != following_user_id"),
        sa.PrimaryKeyConstraint("user_id", "following_user_id"),
    )

    op.create_table(
        "articles",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("author_user_id", postgresql.UUID(), nullable=False),
        sa.Column("slug", sa.Text(), unique=True),
        sa.Column("title", sa.Text()),
        sa.Column("description", sa.Text()),
        sa.Column("body", sa.Text()),
        sa.Column("tags", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column(
            "created_date", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_date", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.ForeignKeyConstraint(["author_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "article_favorites",
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("article_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.PrimaryKeyConstraint("article_id", "user_id"),
    )

    op.create_table(
        "article_comments",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("article_id", postgresql.UUID(), nullable=False),
        sa.Column("commenter_user_id", postgresql.UUID(), nullable=False),
        sa.Column("body", sa.Text()),
        sa.Column(
            "created_date", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_date", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.ForeignKeyConstraint(["commenter_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("user_follows")
    op.drop_table("articles")
    op.drop_table("article_favorites")
    op.drop_table("article_comments")
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
