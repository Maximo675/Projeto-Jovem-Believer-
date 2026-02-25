"""
Alembic migration script to create activity tracking tables
Generated for the practical activities implementation
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    """Create new tables for activity tracking"""
    
    # Create user_activities table
    op.create_table(
        'user_activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('activity_type', sa.String(50), nullable=False),  # 'protocol', 'cases', 'troubleshooting', 'live'
        sa.Column('status', sa.String(20), nullable=False),  # 'ongoing', 'completed', 'failed'
        sa.Column('score', sa.Integer(), default=0),
        sa.Column('attempts', sa.Integer(), default=0),
        sa.Column('time_spent', sa.Integer(), default=0),  # em segundos
        sa.Column('started_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['course_id'], ['course.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_activities_user_id'), 'user_activities', ['user_id'])
    op.create_index(op.f('ix_user_activities_lesson_id'), 'user_activities', ['lesson_id'])
    op.create_index(op.f('ix_user_activities_status'), 'user_activities', ['status'])

    # Create activity_attempts table
    op.create_table(
        'activity_attempt',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('attempt_number', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), default=0),
        sa.Column('time_taken', sa.Integer(), default=0),  # em segundos
        sa.Column('responses', sa.Text(), nullable=True),  # JSON armazenado como TEXT
        sa.Column('result', sa.Text(), nullable=True),  # JSON com feedback
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['activity_id'], ['user_activities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activity_attempt_activity_id'), 'activity_attempt', ['activity_id'])
    op.create_index(op.f('ix_activity_attempt_user_id'), 'activity_attempt', ['user_id'])
    op.create_index(op.f('ix_activity_attempt_attempt_number'), 'activity_attempt', ['attempt_number'])

    # Create activity_badge table
    op.create_table(
        'activity_badge',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('badge_type', sa.String(50), nullable=False),
        sa.Column('badge_name', sa.String(100), nullable=False),
        sa.Column('badge_description', sa.String(255), nullable=True),
        sa.Column('badge_icon', sa.String(100), nullable=True),  # emoji ou URL
        sa.Column('earned_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'badge_type', name='uq_user_badge_type')
    )
    op.create_index(op.f('ix_activity_badge_user_id'), 'activity_badge', ['user_id'])
    op.create_index(op.f('ix_activity_badge_badge_type'), 'activity_badge', ['badge_type'])


def downgrade():
    """Drop activity tracking tables"""
    
    # Drop in reverse order of creation
    op.drop_table('activity_badge')
    op.drop_table('activity_attempt')
    op.drop_table('user_activities')
