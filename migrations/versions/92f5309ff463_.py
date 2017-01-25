"""empty message

Revision ID: 92f5309ff463
Revises: c967a0c1050b
Create Date: 2016-05-19 21:06:07.008847

"""

# revision identifiers, used by Alembic.
revision = '92f5309ff463'
down_revision = 'c967a0c1050b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rankings', sa.Column('email', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rankings', 'email')
    ### end Alembic commands ###
