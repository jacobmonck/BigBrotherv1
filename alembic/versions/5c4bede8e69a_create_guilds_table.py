"""create guilds table

Revision ID: 4b751814dbd6
Revises: 
Create Date: 2022-04-04 23:10:35.332877

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4b751814dbd6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "guilds",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("data", sa.JSON, nullable=False),
    )


def downgrade():
    op.drop_table("guilds")
