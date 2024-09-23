from alembic import op
import sqlalchemy as sa
from alembic import revision

revision = 'manual_add_log_file'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('audit_log', sa.Column('log_file', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('audit_log', 'log_file')
