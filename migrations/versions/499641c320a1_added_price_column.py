"""added price column

Revision ID: 499641c320a1
Revises: b972e36846c3
Create Date: 2024-01-22 15:16:14.654085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '499641c320a1'
down_revision: Union[str, None] = 'b972e36846c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'price',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Numeric(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'price',
               existing_type=sa.Numeric(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=False)
    # ### end Alembic commands ###
