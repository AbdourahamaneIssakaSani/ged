"""test child folders

Revision ID: b17e4ba8914e
Revises: d4d822084d2f
Create Date: 2021-06-15 09:48:08.753943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b17e4ba8914e'
down_revision = 'd4d822084d2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fk_archive_space', table_name='archive')
    op.create_foreign_key('fk_archive_space', 'archive', 'space', ['space_archived'], ['id_space'])
    op.drop_index('fk_file_folder', table_name='file')
    op.create_foreign_key('fk_file_folder', 'file', 'user', ['owner'], ['id_user'])
    op.create_foreign_key(None, 'file', 'folder', ['folder'], ['id_folder'])
    op.drop_index('fk_folder_parent', table_name='folder')
    op.create_foreign_key('fk_folder_parent', 'folder', 'folder', ['parent_folder'], ['id_folder'])
    op.drop_index('fk_msg_space', table_name='message')
    op.drop_index('fk_msg_user', table_name='message')
    op.create_foreign_key('fk_msg_user', 'message', 'user', ['sender'], ['id_user'])
    op.create_foreign_key('fk_msg_space', 'message', 'space', ['space'], ['id_space'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_msg_space', 'message', type_='foreignkey')
    op.drop_constraint('fk_msg_user', 'message', type_='foreignkey')
    op.create_index('fk_msg_user', 'message', ['sender'], unique=False)
    op.create_index('fk_msg_space', 'message', ['space'], unique=False)
    op.drop_constraint('fk_folder_parent', 'folder', type_='foreignkey')
    op.create_index('fk_folder_parent', 'folder', ['parent_folder'], unique=False)
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.drop_constraint('fk_file_folder', 'file', type_='foreignkey')
    op.create_index('fk_file_folder', 'file', ['owner'], unique=False)
    op.drop_constraint('fk_archive_space', 'archive', type_='foreignkey')
    op.create_index('fk_archive_space', 'archive', ['space_archived'], unique=False)
    # ### end Alembic commands ###
