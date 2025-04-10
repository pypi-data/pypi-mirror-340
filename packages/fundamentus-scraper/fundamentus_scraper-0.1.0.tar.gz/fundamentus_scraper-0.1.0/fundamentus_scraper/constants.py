FIELD_MAPPING = {
    # Informações Básicas
    'ticker': 'Papel',
    'type': 'Tipo',
    'company': 'Empresa',
    'sector': 'Setor',
    'subsector': 'Subsetor',
    
    # Cotações
    'price': 'Cotação',
    'date': 'Data últ cot',
    'min_52w': 'Min 52 sem',
    'max_52w': 'Max 52 sem',
    'avg_vol_2m': 'Vol $ méd (2m)',
    
    # Valores de Mercado
    'market_cap': 'Valor de mercado',
    'enterprise_value': 'Valor da firma',
    'shares': 'Nro. Ações',
    'last_balance': 'Últ balanço processado',
    
    # Indicadores Fundamentais
    'p_l': 'P/L',
    'p_vp': 'P/VP',
    'p_ebit': 'P/EBIT',
    'psr': 'PSR',
    'div_yield': 'Div. Yield',
    'ev_ebitda': 'EV / EBITDA',
    'ev_ebit': 'EV / EBIT',
    'roe': 'ROE',
    'roic': 'ROIC',
    'net_margin': 'Marg. Líquida',
    
    # Balanço Patrimonial
    'assets': 'Ativo',
    'current_assets': 'Ativo Circulante',
    'cash': 'Disponibilidades',
    'gross_debt': 'Dív. Bruta',
    'net_debt': 'Dív. Líquida',
    'equity': 'Patrim. Líq',
    
    # Demonstrativos
    'revenue_12m': 'Receita Líquida (12m)',
    'ebit_12m': 'EBIT (12m)',
    'net_income_12m': 'Lucro Líquido (12m)',
    'revenue_3m': 'Receita Líquida (3m)',
    'ebit_3m': 'EBIT (3m)',
    'net_income_3m': 'Lucro Líquido (3m)'
}

VALID_TICKERS = [
    # Exemplos de tickers válidos para validação
    'PETR4', 'VALE3', 'ITSA4', 'BBDC4', 'BBAS3'
]

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}