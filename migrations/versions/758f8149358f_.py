"""empty message

Revision ID: 758f8149358f
Revises: 0b4b5825406e
Create Date: 2025-03-10 15:16:03.287038

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '758f8149358f'
down_revision = '0b4b5825406e'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current connection
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if the 'description' column already exists in the 'controls' table
    columns = [col['name'] for col in inspector.get_columns('controls')]
    if 'description' not in columns:
        with op.batch_alter_table('controls') as batch_op:
            batch_op.add_column(sa.Column('description', sa.String(length=255), nullable=True))


def downgrade():
    with op.batch_alter_table('controls') as batch_op:
        batch_op.drop_column('description')
