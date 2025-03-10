# filepath: /Users/nathan/Documents/GitHub/FlaskCMDB/migrations/versions/bcbb2d92ad04_.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import DateTime, func

# revision identifiers, used by Alembic.
revision = 'bcbb2d92ad04'
down_revision = '9637a003743c'
branch_labels = None
depends_on = None

def upgrade():
    # Create a temporary table to hold the existing data
    op.create_table(
        '_alembic_tmp_controls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created', sa.DateTime, nullable=False, server_default=func.now()),
        sa.Column('updated', sa.DateTime, nullable=False, server_default=func.now()),
        sa.Column('archived', sa.DateTime, nullable=True)
    )

    # Copy data from the old table to the temporary table
    op.execute(
        """
        INSERT INTO _alembic_tmp_controls (id, name, created, updated)
        SELECT id, name, COALESCE(created, CURRENT_TIMESTAMP), COALESCE(updated, CURRENT_TIMESTAMP)
        FROM controls
        """
    )

    # Drop the old table and rename the temporary table to the original name
    op.drop_table('controls')
    op.rename_table('_alembic_tmp_controls', 'controls')

def downgrade():
    # Reverse the upgrade process
    op.create_table(
        '_alembic_tmp_controls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False),
        sa.Column('archived', sa.DateTime, nullable=True)
    )

    op.execute(
        """
        INSERT INTO _alembic_tmp_controls (id, name, created, updated, archived)
        SELECT id, name, created, updated, archived
        FROM controls
        """
    )

    op.drop_table('controls')
    op.rename_table('_alembic_tmp_controls', 'controls')