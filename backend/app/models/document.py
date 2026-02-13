"""
Modelo para Documentos da Plataforma INFANT.ID
"""
from app import db
from datetime import datetime

class Document(db.Model):
    """Modelo para armazenar documentos (Word, PDF, etc)"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # pdf, docx, txt, etc
    file_size = db.Column(db.Integer)  # tamanho em bytes
    
    # Relacionamentos
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    hospital = db.relationship('Hospital', backref='documents')
    course = db.relationship('Course', backref='documents')
    
    def __init__(self, title, file_path, file_type, description=None, file_size=None, hospital_id=None, course_id=None):
        self.title = title
        self.file_path = file_path
        self.file_type = file_type
        self.description = description
        self.file_size = file_size
        self.hospital_id = hospital_id
        self.course_id = course_id
    
    def __repr__(self):
        return f'<Document {self.id}: {self.title}>'
    
    def to_dict(self):
        """Converter modelo para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
