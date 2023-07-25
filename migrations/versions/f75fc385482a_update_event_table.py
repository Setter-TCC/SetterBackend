"""Update event table

Revision ID: f75fc385482a
Revises: 24256295aed0
Create Date: 2023-07-25 17:03:38.428089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f75fc385482a'
down_revision = '24256295aed0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('evento', sa.Column('observacao', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('evento', 'observacao')
    # ### end Alembic commands ###