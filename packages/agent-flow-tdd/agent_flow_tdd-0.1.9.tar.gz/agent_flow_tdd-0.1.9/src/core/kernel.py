"""
src/core/kernel.py
Utilitários para o sistema.
Módulo com funções comuns usadas em diferentes partes do sistema.
"""
import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, List, Dict, Union

from src.core.logger import get_logger, log_execution

logger = get_logger(__name__)

@log_execution
def setup_paths():
    """Configura e valida os caminhos base do projeto"""
    logger.info("INÍCIO - setup_paths | Configurando caminhos base")
    
    try:
        # Constrói caminhos dentro do projeto
        base_dir = Path(__file__).resolve().parent.parent.parent
        logger.debug(f"Diretório base: {base_dir}")

        # Configurações de caminhos
        log_dir = os.path.join(base_dir, 'logs')
        configs_dir = os.path.join(base_dir, 'src', 'configs')

        # Criar diretórios se não existirem
        os.makedirs(log_dir, exist_ok=True)
        
        logger.info("SUCESSO - Caminhos configurados e validados")
        return base_dir, log_dir, configs_dir
        
    except Exception as e:
        logger.error(f"FALHA - setup_paths | Erro: {str(e)}", exc_info=True)
        raise

# Executa a configuração de caminhos
BASE_DIR, LOG_DIR, CONFIGS_DIR = setup_paths()

def load_config(config_file: str) -> dict:
    """
    Carrega configurações de um arquivo YAML.
    
    Args:
        config_file: Caminho do arquivo de configuração
        
    Returns:
        dict: Configurações carregadas
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"FALHA - Erro ao carregar configuração: {str(e)}", exc_info=True)
        raise

# Carrega configurações usando caminho absoluto
CONFIG_FILE = os.path.join(CONFIGS_DIR, 'kernel.yaml')
CONFIG = load_config(CONFIG_FILE)

def get_env_var(name: str, default: Optional[str] = None, args_value: Optional[str] = None) -> Optional[str]:
    """
    Obtém uma variável de ambiente, priorizando args sobre os.environ.

    Args:
        name: Nome da variável.
        default: Valor padrão se a variável não existir.
        args_value: Valor passado via argumentos de linha de comando.

    Returns:
        Valor da variável ou None se não encontrada.
    """
    # Prioriza valor passado via args
    if args_value is not None:
        return args_value
    
    # Se não houver valor em args, tenta os.environ
    return os.environ.get(name, default)


def get_env_status(context: str = "cli") -> Dict[str, Dict[str, bool]]:
    """
    Obtém o status das variáveis de ambiente.
    
    Args:
        context: Contexto para verificação (cli, github, etc)
        
    Returns:
        Dict com o status das variáveis
    """
    # Usa a configuração já carregada
    config = CONFIG
    required_vars = config['required_vars']
    optional_vars = config.get('optional_vars', {})
    
    # Seleciona variáveis do contexto
    if context == "all":
        selected_required = []
        for vars_list in required_vars.values():
            selected_required.extend(vars_list)
        selected_optional = {}
        for opt_dict in optional_vars.values():
            selected_optional.update(opt_dict)
    else:
        selected_required = required_vars.get(context, [])
        selected_optional = optional_vars.get(context, {})

    # Verifica variáveis obrigatórias
    required_status = {var: bool(get_env_var(var)) for var in selected_required}

    # Verifica variáveis opcionais
    optional_status = {var: bool(get_env_var(var)) for var in selected_optional}

    return {
        "required": required_status,
        "optional": optional_status,
        "all_required_set": all(required_status.values()) if required_status else True,
    }


def validate_env(component: str) -> None:
    """
    Valida variáveis de ambiente necessárias.
    
    Args:
        component: Componente que está solicitando a validação
    """
    get_logger(__name__)
    
    # Usa a configuração já carregada
    config = CONFIG
    
    # Obtém variáveis requeridas para o componente
    required_vars = config['required_vars'].get(component, [])
    
    # Se estiver publicando, adiciona PYPI_TOKEN como requerido
    if os.environ.get('PUBLISHING') == 'true':
        required_vars.append('PYPI_TOKEN')
    
    # Verifica variáveis
    missing_vars = []
    for var in required_vars:
        if not get_env_var(var):
            missing_vars.append(var)
            
    if missing_vars:
        raise ValueError(
            f"Variáveis de ambiente obrigatórias não definidas: {', '.join(missing_vars)}\n"
            "IMPORTANTE: Não use arquivos .env. Configure as variáveis diretamente no ambiente ou via argumentos."
        )

def mask_sensitive_data(data: Union[str, Dict[str, Any], List[Any]]) -> Union[str, Dict[str, Any], List[Any]]:
    """
    Mascara dados sensíveis em strings, dicionários ou listas.

    Args:
        data: Dados a serem mascarados. Pode ser uma string, dicionário ou lista.

    Returns:
        Dados com informações sensíveis mascaradas.
    """
    if isinstance(data, str):
        # Mascara tokens e chaves de API usando padrões do config
        patterns = CONFIG["sensitive_data_patterns"]
        masked = data
        for pattern_config in patterns:
            masked = re.sub(pattern_config["pattern"], pattern_config["replacement"], masked)
        return masked
    elif isinstance(data, dict):
        return {k: mask_sensitive_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [mask_sensitive_data(item) for item in data]
    return data

def mask_partially(text, mask_str='***'):
    """
    Mascara parcialmente conteúdo sensível, mantendo caracteres iniciais.
    
    Args:
        text: Texto a ser mascarado
        mask_str: String de substituição
        
    Returns:
        Texto mascarado
    """
    if not text or len(text) < 8:
        return mask_str
        
    # Mostra os primeiros 4 caracteres e mascara o resto
    visible = min(4, len(text) // 3)
    return text[:visible] + mask_str

def format_timestamp(timestamp: str) -> str:
    """
    Formata timestamp para exibição.
    
    Args:
        timestamp: String com o timestamp
        
    Returns:
        String formatada no padrão YYYY-MM-DD HH:MM:SS
    """
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp

def format_json(data: str) -> str:
    """
    Formata JSON para exibição.
    
    Args:
        data: String com o JSON
        
    Returns:
        String formatada com indentação
    """
    try:
        parsed = json.loads(data)
        return json.dumps(parsed, indent=2)
    except:
        return data

"""
Utilitário para validação de tokens e chaves de API.
"""

class TokenValidator:
    """
    Validador de tokens de API e chaves de ambiente.
    Garante que os tokens necessários estejam presentes e válidos.
    """
    
    @staticmethod
    def validate_token(token: Optional[str], token_name: str, required: bool = True) -> bool:
        """
        Valida se um token está presente e tem uma estrutura mínima válida.
        
        Args:
            token: O token a ser validado
            token_name: Nome do token para mensagens de erro
            required: Se o token é obrigatório
            
        Returns:
            bool: True se o token for válido, False caso contrário
            
        Raises:
            ValueError: Se o token for obrigatório e estiver ausente ou inválido
        """
        if not token or token.strip() == "":
            if required:
                raise ValueError(f"Token {token_name} é obrigatório mas não foi encontrado nas variáveis de ambiente")
            return False
            
        # Verificação básica de estrutura mínima usando configuração
        min_length = CONFIG["token_validation"]["min_length"]
        if len(token) < min_length or " " in token:
            if required:
                raise ValueError(f"Token {token_name} parece inválido (formato incorreto)")
            return False
            
        return True
    
    @staticmethod
    def validate_openai_token(token: Optional[str] = None, required: bool = True) -> bool:
        """
        Valida token da OpenAI, com verificações específicas para o formato do token.
        
        Args:
            token: Token da OpenAI. Se None, será buscado na variável de ambiente
            required: Se o token é obrigatório
            
        Returns:
            bool: True se o token for válido, False caso contrário
            
        Raises:
            ValueError: Se o token for obrigatório e estiver ausente ou inválido
        """
        # Se não fornecido, tenta buscar da variável de ambiente
        if token is None:
            token = os.environ.get("OPENAI_API_KEY", "")
            
        # Verificação específica para tokens da OpenAI usando configuração
        openai_prefix = CONFIG["token_validation"]["openai_prefix"]
        if token and not token.startswith(openai_prefix):
            if required:
                raise ValueError(f"Token da OpenAI inválido (deve começar com '{openai_prefix}')")
            return False
            
        return TokenValidator.validate_token(token, "OpenAI", required)
        
    @staticmethod
    def validate_github_token(token: Optional[str] = None, required: bool = True) -> bool:
        """
        Valida token do GitHub, com verificações específicas para o formato do token.
        
        Args:
            token: Token do GitHub. Se None, será buscado na variável de ambiente
            required: Se o token é obrigatório
            
        Returns:
            bool: True se o token for válido, False caso contrário
            
        Raises:
            ValueError: Se o token for obrigatório e estiver ausente ou inválido
        """
        # Se não fornecido, tenta buscar da variável de ambiente
        if token is None:
            token = os.environ.get("GITHUB_TOKEN", "")
            
        # GitHub tokens geralmente têm um formato específico, como começar com "ghp_"
        # Mas isso pode variar, então faremos uma verificação básica
        
        return TokenValidator.validate_token(token, "GitHub", required)
    
    @staticmethod
    def validate_all_required_tokens() -> bool:
        """
        Valida todos os tokens obrigatórios.
        
        Returns:
            bool: True se todos os tokens são válidos, False caso contrário
        """
        return (
            TokenValidator.validate_openai_token(required=True)
            and TokenValidator.validate_github_token(required=False)
        )

# A classe VersionAnalyzer foi movida para src/core/version.py