# Fundamentus Scraper

Pacote Python para coleta de dados do site Fundamentus.com.br

## Instalação

```bash
pip install fundamentus-scraper
```

## Uso Básico

```python
from fundamentus_scraper import FundamentusScraper

scraper = FundamentusScraper()

# Obter todos os dados
dados = scraper.get_company_data("PETR4")

# Obter um dado específico
p_l = scraper.get_single_data("PETR4", "p_l")

# Exportar para Excel
scraper.export_to_excel("PETR4", "petr4.xlsx")
```

## Campos Disponíveis

Consulte o mapeamento completo de campos em `FIELD_MAPPING`

## Licença

MIT