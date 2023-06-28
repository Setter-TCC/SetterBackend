"""Add transaction model to database

Revision ID: fb804d8c6b6e
Revises: 62db66c00551
Create Date: 2023-06-27 19:49:21.216633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb804d8c6b6e'
down_revision = '62db66c00551'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transacao_transaciona',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('data_acontecimento', sa.DateTime(), nullable=False),
    sa.Column('tipo', sa.Enum('mensalidade', 'tecnico', 'despesa', 'ganho', name='tipotransacao'), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.Column('time_id', sa.UUID(), nullable=True),
    sa.Column('pessoa_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['pessoa_id'], ['pessoa.id'], ),
    sa.ForeignKeyConstraint(['time_id'], ['time.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transacao_transaciona')
    # ### end Alembic commands ###
