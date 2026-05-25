"""init

Revision ID: 0001
Revises: 
Create Date: 2026-05-25

"""
from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('nickname', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=True),
        sa.Column('warmth_score', sa.Integer(), nullable=True),
        sa.Column('point_balance', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table('user_interests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('tag_name', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('terminals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=True),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('donor_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('terminal_id', sa.Integer(), sa.ForeignKey('terminals.id'), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('desc', sa.Text(), nullable=True),
        sa.Column('explain', sa.Text(), nullable=True),
        sa.Column('report_desc', sa.Text(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('tags', sa.String(500), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qr_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.id'), nullable=True),
        sa.Column('terminal_id', sa.Integer(), sa.ForeignKey('terminals.id'), nullable=True),
        sa.Column('qr_type', sa.String(50), nullable=True),
        sa.Column('expired_at', sa.DateTime(), nullable=True),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_table('point_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('transaction_type', sa.String(50), nullable=True),
        sa.Column('reason', sa.String(255), nullable=True),
        sa.Column('related_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recycle_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('terminal_id', sa.Integer(), sa.ForeignKey('terminals.id'), nullable=True),
        sa.Column('recycle_type', sa.String(50), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('ai_result', sa.Text(), nullable=True),
        sa.Column('point_earned', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rewards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('required_points', sa.Integer(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reward_exchanges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('reward_id', sa.Integer(), sa.ForeignKey('rewards.id'), nullable=True),
        sa.Column('points_used', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.id'), nullable=True),
        sa.Column('donor_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('receiver_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('terminal_id', sa.Integer(), sa.ForeignKey('terminals.id'), nullable=True),
        sa.Column('action_type', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('warmth_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.id'), nullable=True),
        sa.Column('sender_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('receiver_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('warmth_messages')
    op.drop_table('item_transactions')
    op.drop_table('reward_exchanges')
    op.drop_table('rewards')
    op.drop_table('recycle_records')
    op.drop_table('point_transactions')
    op.drop_table('qr_tokens')
    op.drop_table('items')
    op.drop_table('terminals')
    op.drop_table('user_interests')
    op.drop_table('users')
