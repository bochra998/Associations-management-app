"""empty message

Revision ID: e28fa6ce166f
Revises: 74a51e09b6ad
Create Date: 2021-08-11 14:38:33.750657

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e28fa6ce166f'
down_revision = '74a51e09b6ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribed_events',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('delete', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'event_id')
    )
    op.create_table('users_events',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('events_id', sa.Integer(), nullable=False),
    sa.Column('delete', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['events_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'events_id')
    )
    op.drop_index('session_id', table_name='sessions')
    op.drop_table('sessions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('session_id', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('data', sa.BLOB(), nullable=True),
    sa.Column('expiry', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('session_id', 'sessions', ['session_id'], unique=True)
    op.drop_table('users_events')
    op.drop_table('subscribed_events')
    # ### end Alembic commands ###