import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from typing import Optional, Dict, Union

class FundamentusScraper:
    # Mapeamento de siglas para os campos completos
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

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _make_request(self, ticker: str) -> Optional[BeautifulSoup]:
        """Faz a requisição HTTP e retorna o BeautifulSoup object"""
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None

    def _clean_value(self, value: str) -> Union[float, str]:
        """Limpa e formata valores numéricos e porcentagens"""
        if not value:
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

    def _extract_table_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extrai dados de todas as tabelas da página"""
        data = {}
        tables = soup.find_all('table', {'class': 'w728'})
        
        if not tables:
            return data
        
        # Processa cada tabela conforme sua posição
        for i, table in enumerate(tables):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                
                if i in (0, 1, 3):  # Tabelas com 4 colunas (0-indexed)
                    if len(cells) == 4:
                        self._process_4_column_row(cells, data)
                
                elif i == 2:  # Tabela de oscilações/indicadores
                    if len(cells) == 6:
                        self._process_6_column_row(cells, data)
                
                elif i == 4:  # Tabela de demonstrativos
                    if len(cells) == 4:
                        self._process_demonstrativos_row(cells, data)
        
        return data

    def _process_4_column_row(self, cells, data: dict):
        """Processa linhas com 4 colunas"""
        key1 = cells[0].find('span', {'class': 'txt'}).text.strip() if cells[0].find('span', {'class': 'txt'}) else ''
        val1 = cells[1].find('span', {'class': 'txt'}).text.strip() if cells[1].find('span', {'class': 'txt'}) else ''
        key2 = cells[2].find('span', {'class': 'txt'}).text.strip() if cells[2].find('span', {'class': 'txt'}) else ''
        val2 = cells[3].find('span', {'class': 'txt'}).text.strip() if cells[3].find('span', {'class': 'txt'}) else ''
        
        if key1 and val1:
            data[key1] = val1
        if key2 and val2:
            data[key2] = val2

    def _process_6_column_row(self, cells, data: dict):
        """Processa linhas com 6 colunas (tabela de oscilações/indicadores)"""
        key1 = cells[0].find('span', {'class': 'txt'}).text.strip() if cells[0].find('span', {'class': 'txt'}) else ''
        val1_elem = cells[1].find('span', {'class': 'oscil'}) or cells[1].find('span', {'class': 'txt'})
        val1 = val1_elem.text.strip() if val1_elem else ''
        
        key2 = cells[2].find('span', {'class': 'txt'}).text.strip() if cells[2].find('span', {'class': 'txt'}) else ''
        val2 = cells[3].find('span', {'class': 'txt'}).text.strip() if cells[3].find('span', {'class': 'txt'}) else ''
        
        key3 = cells[4].find('span', {'class': 'txt'}).text.strip() if cells[4].find('span', {'class': 'txt'}) else ''
        val3 = cells[5].find('span', {'class': 'txt'}).text.strip() if cells[5].find('span', {'class': 'txt'}) else ''
        
        if key1 and val1:
            data[key1] = val1
        if key2 and val2:
            data[key2] = val2
        if key3 and val3:
            data[key3] = val3

    def _process_demonstrativos_row(self, cells, data: dict):
        """Processa linhas da tabela de demonstrativos"""
        key1 = cells[0].find('span', {'class': 'txt'}).text.strip() if cells[0].find('span', {'class': 'txt'}) else ''
        val1 = cells[1].find('span', {'class': 'txt'}).text.strip() if cells[1].find('span', {'class': 'txt'}) else ''
        key2 = cells[2].find('span', {'class': 'txt'}).text.strip() if cells[2].find('span', {'class': 'txt'}) else ''
        val2 = cells[3].find('span', {'class': 'txt'}).text.strip() if cells[3].find('span', {'class': 'txt'}) else ''
        
        if key1 and val1:
            data[f"{key1} (12m)"] = val1
        if key2 and val2:
            data[f"{key2} (3m)"] = val2

    def get_company_data(self, ticker: str) -> Optional[Dict[str, Union[float, str]]]:
        """Obtém todos os dados financeiros de uma empresa
        
        Args:
            ticker: Código da ação (ex: 'PETR4')
            
        Returns:
            Dicionário com todos os dados disponíveis ou None em caso de erro
        """
        soup = self._make_request(ticker)
        if not soup:
            return None
        
        raw_data = self._extract_table_data(soup)
        
        # Processa e limpa os valores
        processed_data = {}
        for key, value in raw_data.items():
            processed_data[key] = self._clean_value(value)
        
        return processed_data

    def get_single_data(self, ticker: str, field_code: str) -> Optional[Union[float, str]]:
        """Obtém um único dado específico de uma empresa
        
        Args:
            ticker: Código da ação (ex: 'PETR4')
            field_code: Código do campo desejado (ex: 'p_l' para P/L)
            
        Returns:
            Valor do campo solicitado ou None se não encontrado
        """
        if field_code not in self.FIELD_MAPPING:
            print(f"Código de campo inválido. Opções válidas: {list(self.FIELD_MAPPING.keys())}")
            return None
        
        full_data = self.get_company_data(ticker)
        if not full_data:
            return None
        
        field_name = self.FIELD_MAPPING[field_code]
        return full_data.get(field_name)

    def export_to_excel(self, ticker: str, filename: str = None) -> bool:
        """Exporta os dados para um arquivo Excel
        
        Args:
            ticker: Código da ação
            filename: Nome do arquivo (opcional)
            
        Returns:
            True se exportado com sucesso, False caso contrário
        """
        data = self.get_company_data(ticker)
        if not data:
            return False
        
        if not filename:
            filename = f"dados_{ticker}.xlsx"
        
        try:
            # Converte para DataFrame
            df = pd.DataFrame(list(data.items()), columns=['Indicador', 'Valor'])
            
            # Exporta para Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            return True
        except Exception as e:
            print(f"Erro ao exportar para Excel: {e}")
            return False