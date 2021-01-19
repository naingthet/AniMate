"""empty message

Revision ID: 4ee16c5c0928
Revises: a39059dc3570
Create Date: 2021-01-15 19:56:34.412470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ee16c5c0928'
down_revision = 'a39059dc3570'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'animes', ['anime_name'], ['name'])
        batch_op.create_foreign_key(None, 'animes', ['anime_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
