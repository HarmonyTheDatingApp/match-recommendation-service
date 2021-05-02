"""Add preference age.

Revision ID: 2427de7ddc58
Revises: a20aa1227f71
Create Date: 2021-05-03 02:50:17.769148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2427de7ddc58'
down_revision = 'a20aa1227f71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pref_age_max', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('pref_age_min', sa.Integer(), nullable=True))
    op.execute("UPDATE users SET pref_age_max = 60")
    op.execute("UPDATE users SET pref_age_min = 18")
    op.alter_column('users', 'pref_age_max', nullable=False)
    op.alter_column('users', 'pref_age_min', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pref_age_min')
    op.drop_column('users', 'pref_age_max')
    # ### end Alembic commands ###