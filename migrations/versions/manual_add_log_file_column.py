from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('audit_log', sa.Column('log_file', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('audit_log', 'log_file')
