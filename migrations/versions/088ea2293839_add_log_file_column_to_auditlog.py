"""Add log_file column to AuditLog

Revision ID: 088ea2293839
Revises: 01e34c7c4f32
Create Date: 2024-09-22 19:05:45.345681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '088ea2293839'
down_revision = '01e34c7c4f32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('audit_log', schema=None) as batch_op:
        batch_op.add_column(sa.Column('log_file', sa.String(length=128), nullable=True))
        batch_op.alter_column('filename',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=128),
               existing_nullable=False)

    with op.batch_alter_table('processed_trade', schema=None) as batch_op:
        batch_op.alter_column('trade_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=64),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    with op.batch_alter_table('processed_trade', schema=None) as batch_op:
        batch_op.alter_column('trade_id',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('audit_log', schema=None) as batch_op:
        batch_op.alter_column('filename',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.drop_column('log_file')

    # ### end Alembic commands ###
