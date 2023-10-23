"""empty message

Revision ID: 252af510279b
Revises: 89a5dab8f4b7
Create Date: 2023-10-09 21:13:14.537064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '252af510279b'
down_revision = '89a5dab8f4b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('products_image_key', type_='unique')
        batch_op.drop_constraint('products_type_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_unique_constraint('products_type_key', ['type'])
        batch_op.create_unique_constraint('products_image_key', ['image'])

    # ### end Alembic commands ###
