"""New Life 13

Revision ID: 8bf07b35c94c
Revises: 14c2c0cfcea2
Create Date: 2020-10-05 21:55:55.468517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bf07b35c94c'
down_revision = '14c2c0cfcea2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Email_confirm',
    sa.Column('confirm_number', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=64), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('confirm_number')
    )
    op.create_index(op.f('ix_Email_confirm_user_email'), 'Email_confirm', ['user_email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Email_confirm_user_email'), table_name='Email_confirm')
    op.drop_table('Email_confirm')
    # ### end Alembic commands ###
