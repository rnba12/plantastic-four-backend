"""Added foreign keys

Revision ID: ef908493ad79
Revises: 92f370083ddc
Create Date: 2023-02-03 14:42:11.454113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef908493ad79'
down_revision = '92f370083ddc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'plant__data', ['plant_data_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
