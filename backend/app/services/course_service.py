"""
Serviço de Cursos.
Lógica de negócio relacionada a cursos e aulas.
"""

from app import db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import Progress
from datetime import datetime

class CourseService:
    """Serviço para gerenciar cursos."""
    
    @staticmethod
    def criar_curso(titulo, descricao, autor, nivel='basico', tempo_estimado=None):
        """
        Cria um novo curso.
        
        Args:
            titulo (str): Título do curso
            descricao (str): Descrição
            autor (str): Autor
            nivel (str): Nível (basico, intermediario, avancado)
            tempo_estimado (int): Tempo em minutos
        
        Returns:
            Course: Curso criado
        """
        curso = Course(
            titulo=titulo,
            descricao=descricao,
            autor=autor,
            nivel=nivel,
            tempo_estimado=tempo_estimado
        )
        
        db.session.add(curso)
        db.session.commit()
        
        return curso
    
    @staticmethod
    def obter_curso(curso_id):
        """Obtém um curso pelo ID."""
        return Course.query.get(curso_id)
    
    @staticmethod
    def listar_cursos(nivel=None, pagina=1, por_pagina=20):
        """
        Lista cursos ativos.
        
        Args:
            nivel (str): Filtrar por nível (opcional)
            pagina (int): Página
            por_pagina (int): Itens por página
        
        Returns:
            Pagination: Cursos paginados
        """
        query = Course.query.filter_by(ativo=True)
        
        if nivel:
            query = query.filter_by(nivel=nivel)
        
        return query.paginate(page=pagina, per_page=por_pagina)
    
    @staticmethod
    def adicionar_aula(curso_id, titulo, descricao, conteudo, ordem, duracao=None, video_url=None):
        """
        Adiciona uma aula a um curso.
        
        Args:
            curso_id (int): ID do curso
            titulo (str): Título da aula
            descricao (str): Descrição
            conteudo (str): Conteúdo HTML
            ordem (int): Ordem na sequência
            duracao (int): Duração em minutos
            video_url (str): URL do vídeo
        
        Returns:
            Lesson: Aula criada
        """
        aula = Lesson(
            curso_id=curso_id,
            titulo=titulo,
            descricao=descricao,
            conteudo=conteudo,
            ordem=ordem,
            duracao=duracao,
            video_url=video_url
        )
        
        db.session.add(aula)
        db.session.commit()
        
        return aula
    
    @staticmethod
    def atualizar_progresso(usuario_id, curso_id, percentual, concluido=False):
        """
        Atualiza o progresso de um usuário em um curso.
        
        Args:
            usuario_id (int): ID do usuário
            curso_id (int): ID do curso
            percentual (int): Percentual de conclusão
            concluido (bool): Se foi concluído
        
        Returns:
            Progress: Progresso atualizado
        """
        progresso = Progress.query.filter_by(
            usuario_id=usuario_id,
            curso_id=curso_id
        ).first()
        
        if not progresso:
            progresso = Progress(
                usuario_id=usuario_id,
                curso_id=curso_id,
                percentual=percentual,
                concluido=concluido
            )
            db.session.add(progresso)
        else:
            progresso.percentual = percentual
            progresso.concluido = concluido
            if concluido:
                progresso.data_conclusao = datetime.utcnow()
        
        db.session.commit()
        return progresso
    
    @staticmethod
    def obter_progresso_usuario(usuario_id, pagina=1, por_pagina=20):
        """
        Obtém progresso de um usuário em todos os cursos.
        
        Args:
            usuario_id (int): ID do usuário
            pagina (int): Página
            por_pagina (int): Itens por página
        
        Returns:
            Pagination: Progresso paginado
        """
        return Progress.query.filter_by(usuario_id=usuario_id).paginate(
            page=pagina,
            per_page=por_pagina
        )
