"""empty message

Revision ID: 853bfd4ad565
Revises: 2ba3290bf20c
Create Date: 2025-03-11 10:13:08.926310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '853bfd4ad565'
down_revision = '2ba3290bf20c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('safeguards', schema=None) as batch_op:
        batch_op.add_column(sa.Column('security_function_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_safeguards_security_function_id', 'security_functions', ['security_function_id'], ['id'])


def downgrade():
    with op.batch_alter_table('safeguards', schema=None) as batch_op:
        batch_op.drop_constraint('fk_safeguards_security_function_id', type_='foreignkey')
        batch_op.drop_column('security_function_id')
