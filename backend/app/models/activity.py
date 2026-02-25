"""
Modelo de Atividades Práticas
Rastreia o progresso dos usuários nas atividades interativas
"""

from app import db
from datetime import datetime
import json

class UserActivity(db.Model):
    """Rastreia atividades do usuário"""
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    
    activity_type = db.Column(db.String(50), nullable=False)  # 'protocol', 'cases', 'troubleshooting', 'live'
    status = db.Column(db.String(20), default='ongoing')  # 'ongoing', 'completed', 'failed'
    
    score = db.Column(db.Integer, default=0)  # 0-100
    attempts = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # em segundos
    
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamentos
    user = db.relationship('User', backref='activities')
    course = db.relationship('Course', backref='user_activities')
    lesson = db.relationship('Lesson', backref='user_activities')
    attempts_list = db.relationship('ActivityAttempt', backref='activity', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'lesson_id': self.lesson_id,
            'activity_type': self.activity_type,
            'status': self.status,
            'score': self.score,
            'attempts': self.attempts,
            'time_spent': self.time_spent,
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    def __repr__(self):
        return f'<UserActivity {self.user_id} - {self.activity_type}>'


class ActivityAttempt(db.Model):
    """Rastreia cada tentativa de atividade"""
    __tablename__ = 'activity_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('user_activities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    attempt_number = db.Column(db.Integer, default=1)
    
    # Dados da tentativa (JSON)
    responses = db.Column(db.Text, default='{}')  # Respostas do usuário
    result = db.Column(db.Text, default='{}')  # Resultado/feedback
    score = db.Column(db.Integer, default=0)
    time_taken = db.Column(db.Integer, default=0)  # segundos
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='activity_attempts')
    
    def get_responses(self):
        try:
            return json.loads(self.responses)
        except:
            return {}
    
    def set_responses(self, data):
        self.responses = json.dumps(data, ensure_ascii=False)
    
    def get_result(self):
        try:
            return json.loads(self.result)
        except:
            return {}
    
    def set_result(self, data):
        self.result = json.dumps(data, ensure_ascii=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'activity_id': self.activity_id,
            'attempt_number': self.attempt_number,
            'score': self.score,
            'time_taken': self.time_taken,
            'responses': self.get_responses(),
            'result': self.get_result(),
            'timestamp': self.timestamp.isoformat(),
        }
    
    def __repr__(self):
        return f'<ActivityAttempt {self.user_id} - Attempt {self.attempt_number}>'


class ActivityBadge(db.Model):
    """Badges/conquistas por atividades completadas"""
    __tablename__ = 'activity_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    badge_type = db.Column(db.String(50), nullable=False)  # 'protocol_master', 'perfect_score', etc
    badge_name = db.Column(db.String(100), nullable=False)
    badge_description = db.Column(db.String(255), nullable=True)
    badge_icon = db.Column(db.String(100), nullable=True)  # emoji ou URL
    
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    user = db.relationship('User', backref='badges')
    
    def to_dict(self):
        return {
            'id': self.id,
            'badge_type': self.badge_type,
            'badge_name': self.badge_name,
            'badge_description': self.badge_description,
            'badge_icon': self.badge_icon,
            'earned_at': self.earned_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<ActivityBadge {self.user_id} - {self.badge_type}>'
