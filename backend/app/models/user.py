from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    """Modelo de Usuário"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    # nullable=True: contas anônimas (enfermeiras identificadas por nome+hospital, sem
    # login) recebem um e-mail sintético só para satisfazer o unique index — mas o campo
    # em si deixou de ser obrigatório com a remoção do login do lado do hospital.
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    nome = db.Column(db.String(120), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True)
    # CPF (só dígitos, 11 caracteres) das enfermeiras identificadas via formulário
    # anônimo — usado para confirmar a identidade de quem recebe o certificado e
    # para reconhecer a mesma pessoa se ela se identificar de novo (evita duplicar
    # progresso/certificados quando duas pessoas têm nomes iguais/parecidos).
    cpf = db.Column(db.String(11), unique=True, nullable=True, index=True)
    funcao = db.Column(db.String(50), nullable=False, default='usuario')  # admin, instrutor, usuario
    # 'manual' | 'anonimo' | 'convite' | 'microsoft' — origem do cadastro, usado pelo
    # admin/super-admin para saber que o e-mail é sintético e esconder esse campo na UI.
    origem = db.Column(db.String(20), nullable=False, default='manual')
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    hospital = db.relationship('Hospital', backref='usuarios')
    progresso = db.relationship('Progress', backref='usuario', cascade='all, delete-orphan')
    conversas_ia = db.relationship('IAConversation', backref='usuario', cascade='all, delete-orphan')
    certificados = db.relationship('Certificate', backref='usuario', cascade='all, delete-orphan')
    
    def __init__(self, email, nome, senha, hospital_id=None, funcao='usuario', ativo=True, origem='manual', cpf=None):
        self.email = email
        self.nome = nome
        self.hospital_id = hospital_id
        self.funcao = funcao
        self.ativo = ativo
        self.origem = origem
        self.cpf = cpf
        self.set_password(senha)
    
    def set_password(self, senha):
        """Hashear e armazenar senha"""
        self.senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, senha):
        """Verificar senha"""
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))
    
    def cpf_mascarado(self):
        """
        CPF mascarado para exibição (LGPD): mantém o 1º grupo e os dígitos
        verificadores, esconde o miolo — o mesmo padrão usado em extratos e
        documentos brasileiros. O valor completo nunca sai do backend.
        """
        if not self.cpf or len(self.cpf) != 11:
            return None
        return f'{self.cpf[0:3]}.***.***-{self.cpf[9:11]}'

    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            # e-mail sintético (origem='anonimo') não é mostrado para não confundir a UI
            'email': self.email if self.origem != 'anonimo' else None,
            'nome': self.nome,
            'cpf': self.cpf_mascarado(),
            'hospital_id': self.hospital_id,
            'funcao': self.funcao,
            'origem': self.origem,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
