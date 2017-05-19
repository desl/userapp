"""empty message

Revision ID: 141edd73caf2
Revises: b4d03aadca2a
Create Date: 2017-05-18 16:06:09.151128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '141edd73caf2'
down_revision = 'b4d03aadca2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('excuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('is_believeable', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('excuses')
    # ### end Alembic commands ###