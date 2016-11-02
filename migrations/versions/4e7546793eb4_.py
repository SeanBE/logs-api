"""empty message

Revision ID: 4e7546793eb4
Revises: 8b9de539bfbf
Create Date: 2016-11-02 11:44:25.679942

"""

# revision identifiers, used by Alembic.
revision = '4e7546793eb4'
down_revision = '8b9de539bfbf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('date_proposed', sa.Date(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'date_proposed')
    ### end Alembic commands ###
