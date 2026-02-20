"""
Script para setup completo do banco de dados
Limpa, reconstri e popula com dados CORRETOS

Executar: python setup_database_correctly.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.hospital import Hospital
from app.models.user import User
from app.models.course import Course
from app.models.lesson import Lesson

# Cores
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_section(title):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

class DatabaseSetup:
    def __init__(self):
        self.app = create_app()
        self.hospitais_criados = []
        self.usuarios_criados = []
        self.cursos_criados = []

    def reset_database(self):
        """Limpar tudo e comear do zero"""
        print_section("[DELETE] LIMPANDO BANCO DE DADOS")
        
        with self.app.app_context():
            print(f"{YELLOW}Dropping all tables...{RESET}")
            db.drop_all()
            
            print(f"{YELLOW}Creating schema...{RESET}")
            db.create_all()
            
            print(f"{GREEN} Banco de dados resetado com sucesso!{RESET}")

    def populate_hospitals(self):
        """Preencher com hospitais REAIS"""
        print_section("[HOSPITAL] ADICIONANDO HOSPITAIS")
        
        hospitais = [
            {
                'nome': 'Hospital Universitrio Evanglico',
                'estado': 'PR',
                'cidade': 'Curitiba',
                'endereco': 'Rua XV de Novembro, 1111, Curitiba - PR',
                'email': 'contato@hue.org.br',
                'telefone': '(41) 3310-1000',
                'cnpj': '00.123.456/0000-01'
            },
            {
                'nome': 'Hospital Moinhos de Vento',
                'estado': 'RS',
                'cidade': 'Porto Alegre',
                'endereco': 'Av. Jos de Alencar, 286, Porto Alegre - RS',
                'email': 'contato@hmv.org.br',
                'telefone': '(51) 3414-8000',
                'cnpj': '00.234.567/0000-02'
            },
            {
                'nome': 'Santa Casa de Misericrdia de So Paulo',
                'estado': 'SP',
                'cidade': 'So Paulo',
                'endereco': 'Rua Santa Ifigenia, 362, So Paulo - SP',
                'email': 'contato@santacasasp.org.br',
                'telefone': '(11) 3391-0000',
                'cnpj': '00.345.678/0000-03'
            },
            {
                'nome': 'Hospital Vera Cruz',
                'estado': 'MG',
                'cidade': 'Belo Horizonte',
                'endereco': 'Avenida Getlio Vargas, 1000, Belo Horizonte - MG',
                'email': 'contato@hveracruz.com.br',
                'telefone': '(31) 3237-7000',
                'cnpj': '00.456.789/0000-04'
            },
            {
                'nome': 'Hospital Portugus de Beneficncia',
                'estado': 'BA',
                'cidade': 'Salvador',
                'endereco': 'Rua da Graa, Salvador - BA',
                'email': 'contato@hportugues.org.br',
                'telefone': '(71) 3203-8000',
                'cnpj': '00.567.890/0000-05'
            },
        ]
        
        with self.app.app_context():
            for h_data in hospitais:
                # Verificar se j existe
                if Hospital.query.filter_by(email=h_data['email']).first():
                    print(f"{YELLOW} j existe: {h_data['nome']}{RESET}")
                    continue
                
                h = Hospital(
                    nome=h_data['nome'],
                    estado=h_data['estado'],
                    cidade=h_data['cidade'],
                    endereco=h_data['endereco'],
                    email=h_data['email'],
                    telefone=h_data['telefone'],
                    cnpj=h_data['cnpj'],
                    ativo=True
                )
                db.session.add(h)
                self.hospitais_criados.append(h)
                print(f"{GREEN} Adicionado: {h.nome}{RESET}")
            
            db.session.commit()
            print(f"\n{GREEN} {len(self.hospitais_criados)} hospitais adicionados{RESET}")

    def populate_users(self):
        """Preencher com usurios VLIDOS"""
        print_section("[USERS] ADICIONANDO USUARIOS")
        
        with self.app.app_context():
            # Pegar o primeiro hospital
            hospital = Hospital.query.first()
            
            if not hospital:
                print(f"{RED} Nenhum hospital encontrado!{RESET}")
                print(f"   Execute populate_hospitals() primeiro")
                return
            
            usuarios = [
                {
                    'email': 'admin@infantid.com.br',
                    'nome': 'Admin INFANT.ID',
                    'senha': 'admin_seguro_123456',
                    'funcao': 'admin'
                },
                {
                    'email': 'professor@infantid.com.br',
                    'nome': 'Professor Treinamento',
                    'senha': 'prof_seguro_123456',
                    'funcao': 'instrutor'
                },
                {
                    'email': 'usuario.teste@infantid.com.br',
                    'nome': 'Usurio Teste',
                    'senha': 'user_seguro_123456',
                    'funcao': 'usuario'
                },
                {
                    'email': 'usuario2@infantid.com.br',
                    'nome': 'Segundo Usurio',
                    'senha': 'user_seguro_123456',
                    'funcao': 'usuario'
                },
            ]
            
            for u_data in usuarios:
                # Verificar se j existe
                if User.query.filter_by(email=u_data['email']).first():
                    print(f"{YELLOW} J existe: {u_data['email']}{RESET}")
                    continue
                
                u = User(
                    email=u_data['email'],
                    nome=u_data['nome'],
                    senha=u_data['senha'],
                    hospital_id=hospital.id,  #  IMPORTANTE: Hospital vlido!
                    funcao=u_data['funcao'],
                    ativo=True
                )
                db.session.add(u)
                self.usuarios_criados.append(u)
                print(f"{GREEN} Adicionado: {u.nome} (Hospital: {hospital.nome}){RESET}")
            
            db.session.commit()
            print(f"\n{GREEN} {len(self.usuarios_criados)} usurios adicionados{RESET}")

    def populate_courses(self):
        """Preencher com cursos DE VERDADE"""
        print_section("[COURSES] ADICIONANDO CURSOS")
        
        with self.app.app_context():
            cursos = [
                {
                    'titulo': 'Onboarding INFANT.ID - Mdulo 1',
                    'descricao': 'Introduo ao sistema INFANT.ID para profissionais de sade',
                    'nivel': 'basico',
                    'tempo': 120
                },
                {
                    'titulo': 'Integrao Hospitalar',
                    'descricao': 'Como integrar INFANT.ID com sistemas hospitalares existentes',
                    'nivel': 'intermediario',
                    'tempo': 180
                },
                {
                    'titulo': 'Gerenciamento de Usurios',
                    'descricao': 'Administrao de contas, permisses e lojistas',
                    'nivel': 'avancado',
                    'tempo': 150
                },
            ]
            
            for c_data in cursos:
                # Verificar se j existe
                if Course.query.filter_by(titulo=c_data['titulo']).first():
                    print(f"{YELLOW} J existe: {c_data['titulo']}{RESET}")
                    continue
                
                c = Course(
                    titulo=c_data['titulo'],
                    descricao=c_data['descricao'],
                    nivel=c_data['nivel'],
                    tempo_estimado=c_data['tempo'],
                    autor='INFANT.ID',
                    ativo=True
                )
                db.session.add(c)
                self.cursos_criados.append(c)
                print(f"{GREEN} Adicionado: {c.titulo}{RESET}")
            
            db.session.commit()
            
            # Adicionar aulas para o primeiro curso
            if self.cursos_criados:
                curso = self.cursos_criados[0]
                aulas = [
                    {
                        'titulo': 'Bem-vindo ao INFANT.ID',
                        'descricao': 'Apresentao do sistema e seus objetivos',
                        'conteudo': '<h1>Bem-vindo!</h1><p>Este mdulo introduce o INFANT.ID...</p>',
                        'ordem': 1,
                        'duracao': 30
                    },
                    {
                        'titulo': 'Funcionalidades Principais',
                        'descricao': 'Explore os principais recursos do sistema',
                        'conteudo': '<h1>Funcionalidades</h1><p>Conhea os recursos...</p>',
                        'ordem': 2,
                        'duracao': 45
                    },
                    {
                        'titulo': 'Melhores Prticas',
                        'descricao': 'Como usar o INFANT.ID de forma eficiente',
                        'conteudo': '<h1>Melhores Prticas</h1><p>Dicas importante...</p>',
                        'ordem': 3,
                        'duracao': 45
                    },
                ]
                
                for a_data in aulas:
                    a = Lesson(
                        curso_id=curso.id,
                        titulo=a_data['titulo'],
                        descricao=a_data['descricao'],
                        conteudo=a_data['conteudo'],
                        ordem=a_data['ordem'],
                        duracao=a_data['duracao'],
                        ativo=True
                    )
                    db.session.add(a)
                    print(f"   Adicionada aula: {a.titulo}")
                
                db.session.commit()
            
            print(f"\n{GREEN} {len(self.cursos_criados)} cursos adicionados{RESET}")

    def validate(self):
        """Validar integridade depois de popular"""
        print_section("[VALIDATE] VALIDANDO DADOS")
        
        with self.app.app_context():
            # Contar total
            hospitals = Hospital.query.count()
            users = User.query.count()
            courses = Course.query.count()
            lessons = Lesson.query.count()
            
            print(f"Hospitais: {hospitals}")
            print(f"Usurios: {users}")
            print(f"Cursos: {courses}")
            print(f"Aulas: {lessons}")
            
            # Verificar Foreign Keys
            broken = []
            for user in User.query.all():
                if user.hospital_id and not Hospital.query.get(user.hospital_id):
                    broken.append(f"User {user.id}: Hospital {user.hospital_id} no existe")
            
            if broken:
                print(f"\n{RED} Problemas encontrados:{RESET}")
                for issue in broken:
                    print(f"   - {issue}")
                return False
            else:
                print(f"{GREEN}[OK] Todos os dados estao validos!{RESET}")
                return True

    def run(self):
        """Executar setup completo"""
        print_section("[SETUP] SETUP COMPLETO DO BANCO DE DADOS")
        
        try:
            # 1. Resetar
            self.reset_database()
            
            # 2. Popular
            self.populate_hospitals()
            self.populate_users()
            self.populate_courses()
            
            # 3. Validar
            is_valid = self.validate()
            
            # 4. Resumo final
            print_section(" RESUMO FINAL")
            
            if is_valid:
                print(f"{GREEN} SETUP CONCLUDO COM SUCESSO!{RESET}\n")
                print(f"   Seu banco de dados est pronto para usar")
                print(f"   {YELLOW}Prximo passo:{RESET}")
                print(f"   1. python test_api_integration.py")
                print(f"   2. Comear a trabalhar com a API\n")
            else:
                print(f"{RED} SETUP COM PROBLEMAS{RESET}")
                print(f"   Veja os erros acima\n")
        
        except Exception as e:
            print(f"\n{RED} ERRO:{RESET}")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    setup = DatabaseSetup()
    setup.run()
