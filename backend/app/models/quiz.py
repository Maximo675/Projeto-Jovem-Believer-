"""
Modelo de Prova (Quiz) de cada curso.

Cada curso tem no máximo uma prova (Quiz), composta de várias QuizQuestion,
cada uma com várias QuizOption. A opção correta (`correto=True`) NUNCA deve
ser serializada para o cliente antes da correção — a correção é sempre feita
no servidor (ver backend/app/routes/quizzes.py), diferente do padrão usado
em frontend/activities/etan_special_cases.html, onde a correção acontece no
próprio navegador (aceitável ali por ser uma atividade de prática, não a
prova que libera o próximo curso).
"""

from app import db
from datetime import datetime


class Quiz(db.Model):
    """Prova de um curso."""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, unique=True)
    titulo = db.Column(db.String(255), nullable=False, default='Avaliação do curso')
    nota_minima = db.Column(db.Integer, nullable=False, default=70)  # % mínimo para aprovação
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    curso = db.relationship('Course', backref=db.backref('quiz', uselist=False, cascade='all, delete-orphan'))
    perguntas = db.relationship(
        'QuizQuestion', backref='quiz', cascade='all, delete-orphan',
        order_by='QuizQuestion.ordem'
    )

    def to_dict(self, incluir_gabarito=False):
        return {
            'id': self.id,
            'curso_id': self.curso_id,
            'titulo': self.titulo,
            'nota_minima': self.nota_minima,
            'perguntas': [p.to_dict(incluir_gabarito=incluir_gabarito) for p in self.perguntas],
        }

    def __repr__(self):
        return f'<Quiz curso={self.curso_id}>'


class QuizQuestion(db.Model):
    """Uma pergunta de múltipla escolha da prova."""
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)
    ordem = db.Column(db.Integer, default=0)

    opcoes = db.relationship(
        'QuizOption', backref='pergunta', cascade='all, delete-orphan',
        order_by='QuizOption.ordem'
    )

    def to_dict(self, incluir_gabarito=False):
        return {
            'id': self.id,
            'enunciado': self.enunciado,
            'ordem': self.ordem,
            'opcoes': [o.to_dict(incluir_gabarito=incluir_gabarito) for o in self.opcoes],
        }

    def __repr__(self):
        return f'<QuizQuestion {self.id}>'


class QuizOption(db.Model):
    """Uma alternativa de uma pergunta."""
    __tablename__ = 'quiz_options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    texto = db.Column(db.String(500), nullable=False)
    correto = db.Column(db.Boolean, default=False)
    ordem = db.Column(db.Integer, default=0)

    def to_dict(self, incluir_gabarito=False):
        d = {
            'id': self.id,
            'texto': self.texto,
            'ordem': self.ordem,
        }
        if incluir_gabarito:
            d['correto'] = self.correto
        return d

    def __repr__(self):
        return f'<QuizOption {self.id} correto={self.correto}>'
