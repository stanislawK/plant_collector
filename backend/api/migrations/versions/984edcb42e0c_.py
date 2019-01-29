"""empty message

Revision ID: 984edcb42e0c
Revises: 4587b1b9fe07
Create Date: 2019-01-29 17:44:54.518355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '984edcb42e0c'
down_revision = '4587b1b9fe07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_model', 'password',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=256),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_model', 'password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###