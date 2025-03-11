"""empty message

Revision ID: 0b4b5825406e
Revises: 
Create Date: 2025-03-10 15:06:50.714765

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '0b4b5825406e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Get the current connection
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if the 'number' column already exists in the 'controls' table
    columns = [col['name'] for col in inspector.get_columns('controls')]
    if 'number' not in columns:
        with op.batch_alter_table('controls') as batch_op:
            batch_op.add_column(sa.Column('number', sa.String(length=20), nullable=True))


def downgrade():
    with op.batch_alter_table('controls') as batch_op:
        batch_op.drop_column('number')
