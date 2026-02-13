"""
Utilitários gerais da aplicação.
"""

import re
import secrets
from datetime import datetime

class ValidadorEmail:
    """Valida emails."""
    
    REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validar(email):
        """Valida se o formato do email é correto."""
        return re.match(ValidadorEmail.REGEX, email) is not None


class FormatadorDados:
    """Formatadores de dados para respostas."""
    
    @staticmethod
    def formatar_data(data):
        """Formata data para ISO format."""
        if isinstance(data, datetime):
            return data.isoformat()
        return str(data)
    
    @staticmethod
    def formatar_percentual(valor):
        """Formata percentual com 2 casas decimais."""
        return f"{float(valor):.2f}%"
    
    @staticmethod
    def paginar_resultado(items, pagina, por_pagina, total):
        """Formata resultado paginado."""
        return {
            'total': total,
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': (total + por_pagina - 1) // por_pagina,
            'items': items
        }


class GeradorToken:
    """Gera tokens seguros."""
    
    import secrets
    
    @staticmethod
    def gerar_token(length=32):
        """Gera um token seguro aleatório."""
        return secrets.token_urlsafe(length)
