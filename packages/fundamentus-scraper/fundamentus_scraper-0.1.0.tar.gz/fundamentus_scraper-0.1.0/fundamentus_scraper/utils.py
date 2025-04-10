from typing import Union

def clean_value(value: str) -> Union[float, str]:
    """Limpa e formata valores numéricos e porcentagens"""
    if not value or not isinstance(value, str):
        return value
    
    value = value.replace('.', '').replace(',', '.').strip()
    
    if '%' in value:
        value = value.replace('%', '')
        try:
            return float(value) / 100
        except ValueError:
            return value
    
    try:
        return float(value)
    except ValueError:
        return value

def format_currency(value: Union[str, float, int]) -> str:
    """Formata valor para exibição como moeda"""
    try:
        num = float(value)
        if num >= 1_000_000_000:
            return f"R$ {num/1_000_000_000:.2f} bilhões"
        elif num >= 1_000_000:
            return f"R$ {num/1_000_000:.2f} milhões"
        elif num >= 1_000:
            return f"R$ {num/1_000:.2f} mil"
        else:
            return f"R$ {num:.2f}"
    except (ValueError, TypeError):
        return str(value)

def format_percentage(value: Union[str, float]) -> str:
    """Formata valor para exibição como porcentagem"""
    try:
        return f"{float(value)*100:.2f}%"
    except (ValueError, TypeError):
        if isinstance(value, str) and '%' in value:
            return value
        return str(value)