"""empty message

Revision ID: 79d845a36d97
Revises: 817459924717
Create Date: 2024-07-22 18:08:25.973872

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '79d845a36d97'
down_revision = '817459924717'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('local_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('prep_time', sa.String(length=64), nullable=True),
    sa.Column('serving_size', sa.String(length=64), nullable=True),
    sa.Column('instructions', postgresql.ARRAY(sa.String(length=256)), nullable=True),
    sa.Column('notes', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recipes_local_id'), ['local_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_recipes_name'), ['name'], unique=True)

    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('local_id', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ingredients_local_id'), ['local_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_ingredients_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ingredients', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ingredients_name'))
        batch_op.drop_index(batch_op.f('ix_ingredients_local_id'))

    op.drop_table('ingredients')
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recipes_name'))
        batch_op.drop_index(batch_op.f('ix_recipes_local_id'))

    op.drop_table('recipes')
    # ### end Alembic commands ###
