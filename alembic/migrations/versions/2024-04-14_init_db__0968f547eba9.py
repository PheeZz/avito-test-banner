"""init db

Revision ID: 0968f547eba9
Revises: 
Create Date: 2024-04-14 16:20:14.398809

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0968f547eba9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "feature",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_table(
        "banner",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("text", sa.String(length=2000), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("feature_id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["feature_id"], ["public.feature.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_table(
        "banner_tag",
        sa.Column("banner_id", sa.BIGINT(), nullable=False),
        sa.Column("tag_id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["banner_id"], ["public.banner.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["public.tag.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("banner_id", "tag_id"),
        schema="public",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("banner_tag", schema="public")
    op.drop_table("banner", schema="public")
    op.drop_table("tag", schema="public")
    op.drop_table("feature", schema="public")
    # ### end Alembic commands ###
