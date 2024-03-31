import pandas as pd
from pandas import ExcelFile
import sqlite3
import unicodedata

excel_file = ExcelFile('acoes_pura.xlsx')
sheet_names = excel_file.sheet_names
dfs = {}

for sheet_name in sheet_names:
  dfs[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)

dfs['Principal'] = dfs['Principal'].iloc[:, [0, 1, 2, 3, 4]]
dfs['Principal'] = dfs['Principal'].rename(columns={'Ativo':'Ticker','Último (R$)':'Valor Final','Var. Dia (%)':'Var Dia','Var. Sem. (%)':'Var Semana'}).copy()
dfs['Principal']['Var_pct'] = dfs['Principal']['Var Dia'] / 100
dfs['Principal']['Valor Inic'] = dfs['Principal']['Valor Final'] / (dfs['Principal']['Var_pct'] + 1)
dfs['Total_de_acoes'] = dfs['Total_de_acoes'].rename(columns={'Código':'Ticker'}).copy()
dfs['Principal'] = dfs['Principal'].merge(dfs['Total_de_acoes'], left_on='Ticker', right_on='Ticker', how='left').copy()
dfs['Principal'] = dfs['Principal'].rename(columns={'Qtde. Teórica':'Qtd Acoes'})
dfs['Principal']['Variacao'] = (dfs['Principal']['Valor Final'] - dfs['Principal']['Valor Inic']) * dfs['Principal']['Qtd Acoes']
pd.options.display.float_format = '{:.2f}'.format
dfs['Principal']['Resultado'] = ['Subiu' if x > 0 else 'Caiu' if x < 0 else 'Sem Variacao' for x in dfs['Principal']['Variacao']]
dfs['Principal'] = dfs['Principal'].merge(dfs['Ticker'], left_on='Ticker', right_on='Ticker', how='left').copy()

# Function to normalize special characters
def normalize_special_characters(text):
    if isinstance(text, str):
        return ''.join(char if unicodedata.category(char)[0] != 'P' else unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode() for char in text)
    else:
        return text

# Apply the function to each column in 'Principal' DataFrame
for column in dfs['Principal'].select_dtypes(include='object').columns:
    dfs['Principal'][column] = dfs['Principal'][column].apply(normalize_special_characters)


conn = sqlite3.connect('acoes.db')
dfs['Principal'].to_sql('principal_data', conn, index=False, if_exists='replace')

for sheet_name, df in dfs.items():
  print(f"Sheet Name: {sheet_name}")
  print(df.head())
