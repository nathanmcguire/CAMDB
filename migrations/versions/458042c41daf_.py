"""Add foreign keys and number to safeguards

Revision ID: 458042c41daf
Revises: 60b6cfeb33b7
Create Date: 2025-03-11 11:39:18.856820

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '458042c41daf'
down_revision = '60b6cfeb33b7'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    columns = [col['name'] for col in inspector.get_columns('safeguards')]

    with op.batch_alter_table('safeguards', schema=None) as batch_op:
        if 'number' not in columns:
            batch_op.add_column(sa.Column('number', sa.String(length=20), nullable=True))
        if 'asset_type_id' not in columns:
            batch_op.add_column(sa.Column('asset_type_id', sa.Integer(), nullable=True))
        if 'implementation_group_id' not in columns:
            batch_op.add_column(sa.Column('implementation_group_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('safeguards', schema=None) as batch_op:
        if 'fk_safeguards_asset_type_id' not in inspector.get_foreign_keys('safeguards'):
            batch_op.create_foreign_key('fk_safeguards_asset_type_id', 'asset_types', ['asset_type_id'], ['id'])
        if 'fk_safeguards_implementation_group_id' not in inspector.get_foreign_keys('safeguards'):
            batch_op.create_foreign_key('fk_safeguards_implementation_group_id', 'implementation_groups', ['implementation_group_id'], ['id'])


def downgrade():
    with op.batch_alter_table('safeguards', schema=None) as batch_op:
        batch_op.drop_constraint('fk_safeguards_asset_type_id', type_='foreignkey')
        batch_op.drop_constraint('fk_safeguards_implementation_group_id', type_='foreignkey')
        batch_op.drop_column('number')
        batch_op.drop_column('asset_type_id')
        batch_op.drop_column('implementation_group_id')
