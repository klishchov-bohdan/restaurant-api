"""created tables

Revision ID: 09096943c77d
Revises:
Create Date: 2024-01-22 10:33:22.041503

"""
from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '09096943c77d'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('time_created', sa.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('time_updated', sa.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_menu'))
                    )
    op.create_index(op.f('ix_menu_id '), 'menu', ['id'], unique=True)
    op.create_table('submenu',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('menu_id', sa.Integer(), nullable=False),
                    sa.Column('time_created', sa.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('time_updated', sa.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), nullable=False),
                    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], name=op.f(
                        'fk_submenu_menu_id_menu'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_submenu'))
                    )
    op.create_index(op.f('ix_submenu_id '), 'submenu', ['id'], unique=True)
    op.create_table('dish',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('submenu_id', sa.Integer(), nullable=False),
                    sa.Column('time_created', sa.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('time_updated', sa.TIMESTAMP(), server_default=sa.text(
                        'CURRENT_TIMESTAMP'), nullable=False),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], name=op.f(
                        'fk_dish_submenu_id_submenu'), ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_dish'))
                    )
    op.create_index(op.f('ix_dish_id '), 'dish', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dish_id '), table_name='dish')
    op.drop_table('dish')
    op.drop_index(op.f('ix_submenu_id '), table_name='submenu')
    op.drop_table('submenu')
    op.drop_index(op.f('ix_menu_id '), table_name='menu')
    op.drop_table('menu')
    # ### end Alembic commands ###
