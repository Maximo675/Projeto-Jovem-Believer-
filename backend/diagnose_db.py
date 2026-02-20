"""
Script de diagnóstico do banco de dados
Mostra exatamente o que está quebrado

Executar: python diagnose_db.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User
from app.models.hospital import Hospital
from app.models.course import Course
from app.models.lesson import Lesson

# Cores para output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_section(title):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def diagnose():
    app = create_app()
    
    with app.app_context():
        print_section("🔍 DIAGNÓSTICO DO BANCO DE DADOS")
        
        # ============ CONTAR REGISTROS ============
        print(f"{YELLOW}📊 Contando registros...{RESET}")
        
        hospital_count = Hospital.query.count()
        user_count = User.query.count()
        course_count = Course.query.count()
        lesson_count = Lesson.query.count()
        
        print(f"  ✓ Hospitais: {hospital_count}")
        print(f"  ✓ Usuários: {user_count}")
        print(f"  ✓ Cursos: {course_count}")
        print(f"  ✓ Aulas: {lesson_count}")
        
        # ============ VERIFICAR HOSPITAIS ============
        print_section("🏥 HOSPITAIS")
        
        if hospital_count == 0:
            print(f"{RED}❌ NENHUM HOSPITAL CADASTRADO!{RESET}")
            print(f"   {YELLOW}→ Execute: python setup_database_correctly.py{RESET}\n")
        else:
            print(f"{GREEN}✓ Hospitais cadastrados:{RESET}")
            for h in Hospital.query.all():
                print(f"   ID {h.id}: {h.nome} ({h.estado})")
        
        # ============ VERIFICAR FOREIGN KEYS ============
        print_section("🔗 INTEGRIDADE DAS FOREIGN KEYS")
        
        broken_users = []
        for user in User.query.all():
            if user.hospital_id:
                hospital = Hospital.query.get(user.hospital_id)
                if not hospital:
                    broken_users.append({
                        'user_id': user.id,
                        'email': user.email,
                        'missing_hospital_id': user.hospital_id
                    })
        
        if broken_users:
            print(f"{RED}❌ USUÁRIOS COM HOSPITAL INVÁLIDO:{RESET}")
            for user in broken_users:
                print(f"   ID {user['user_id']} ({user['email']})")
                print(f"      → Hospital {user['missing_hospital_id']} NÃO EXISTE")
            print(f"\n   {YELLOW}→ Ação: Deletar usuários com hospital inválido{RESET}\n")
        else:
            print(f"{GREEN}✓ Todas as Foreign Keys estão válidas{RESET}\n")
        
        # ============ USUÁRIOS SEM HOSPITAL ============
        print_section("👥 USUÁRIOS")
        
        users_without_hospital = User.query.filter(User.hospital_id == None).all()
        
        if users_without_hospital:
            print(f"{YELLOW}⚠️ Usuários sem hospital vinculado:{RESET}")
            for u in users_without_hospital:
                print(f"   - {u.email} ({u.nome})")
            print(f"\n   {YELLOW}→ Recomendação: Todo usuário deve ter hospital!{RESET}\n")
        else:
            print(f"{GREEN}✓ Todos os usuários têm hospital{RESET}\n")
        
        all_users = User.query.all()
        print(f"{GREEN}✓ Total de usuários: {len(all_users)}{RESET}")
        for u in all_users:
            hospital_name = u.hospital.nome if u.hospital else "SEM HOSPITAL"
            print(f"   - {u.email} → {hospital_name}")
        
        # ============ CURSOS E AULAS ============
        print_section("📚 CURSOS E AULAS")
        
        if course_count == 0:
            print(f"{YELLOW}⚠️ Nenhum curso cadastrado{RESET}\n")
        else:
            print(f"{GREEN}✓ {course_count} curso(s) cadastrado(s):{RESET}")
            for c in Course.query.all():
                lesson_count = Lesson.query.filter_by(curso_id=c.id).count()
                print(f"   - {c.titulo} ({lesson_count} aulas)")
        
        # ============ RESUMO FINAL ============
        print_section("📋 RESUMO")
        
        has_hospitals = hospital_count > 0
        has_users = user_count > 0
        all_users_valid = len(broken_users) == 0 and len(users_without_hospital) == 0
        
        print(f"Status de Hospitais:    {GREEN + '✓ OK' if has_hospitals else RED + '✗ ERRO'}{RESET}")
        print(f"Status de Usuários:     {GREEN + '✓ OK' if (has_users and all_users_valid) else RED + '✗ ERRO'}{RESET}")
        print(f"Foreign Keys:           {GREEN + '✓ OK' if len(broken_users) == 0 else RED + '✗ ERRO'}{RESET}")
        
        print("\n" + "="*60)
        
        if has_hospitals and has_users and all_users_valid and len(broken_users) == 0:
            print(f"{GREEN}✅ BANCO DE DADOS ESTÁ CORRETO!{RESET}")
            print(f"   Você pode usar a API normalmente")
        else:
            print(f"{RED}❌ BANCO DE DADOS PRECISA DE REPAROS{RESET}")
            print(f"   {YELLOW}→ Execute: python setup_database_correctly.py{RESET}")
        
        print("="*60 + "\n")

if __name__ == '__main__':
    try:
        diagnose()
    except Exception as e:
        print(f"\n{RED}❌ ERRO ao diagnosticar:{RESET}")
        print(f"   {str(e)}")
        print(f"\n{YELLOW}Certificar-se que:{RESET}")
        print(f"   1. Você está em: backend/")
        print(f"   2. Venv está ativo: .\\venv\\Scripts\\Activate.ps1")
        print(f"   3. Bank de dados existe: infant_id_platform.db")
