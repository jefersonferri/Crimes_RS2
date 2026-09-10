import pandas as pd
from pathlib import Path
import re

# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta onde estão os arquivos Excel
pasta = Path(r"C:\Users\Jéferson\Documents\Crimes_RS")

# Arquivo de saída
arquivo_saida = pasta / "crimes_RS_compilado.xlsx"


# ============================================================
# DICIONÁRIO DE MESES
# ============================================================

meses = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,

    # Caso as abas utilizem abreviações
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12
}


# ============================================================
# LISTA PARA ARMAZENAR OS DATASETS
# ============================================================

datasets = []


# ============================================================
# PERCORRER OS ARQUIVOS
# ============================================================

for arquivo in sorted(pasta.glob("*.xlsx")):

    # Ignora o próprio arquivo de saída
    if arquivo.name == arquivo_saida.name:
        continue

    # --------------------------------------------------------
    # Identifica o ano pelo nome do arquivo
    # Exemplo: 2025.xlsx -> 2025
    # --------------------------------------------------------

    resultado_ano = re.search(r"(20\d{2})", arquivo.stem)

    if not resultado_ano:
        print(f"Aviso: não foi possível identificar o ano: {arquivo.name}")
        continue

    ano = int(resultado_ano.group(1))

    print(f"\nProcessando: {arquivo.name} | Ano: {ano}")

    # --------------------------------------------------------
    # Abre o Excel
    # --------------------------------------------------------

    excel = pd.ExcelFile(arquivo)

    # --------------------------------------------------------
    # Percorre todas as planilhas (meses)
    # --------------------------------------------------------

    for nome_aba in excel.sheet_names:

        print(f"   -> Aba: {nome_aba}")

        # Normaliza o nome da aba
        nome_mes = nome_aba.strip().lower()

        # Procura o mês
        if nome_mes not in meses:
            print(f"      Aviso: mês não reconhecido: {nome_aba}")
            continue

        mes = meses[nome_mes]

        # ----------------------------------------------------
        # Lê a planilha
        # ----------------------------------------------------

        df = pd.read_excel(
            arquivo,
            sheet_name=nome_aba
        )

        # Remove linhas completamente vazias
        df = df.dropna(how="all")

        # Se a planilha estiver vazia, pula
        if df.empty:
            print("      Planilha vazia - ignorada.")
            continue

        # ----------------------------------------------------
        # Cria a coluna de data
        # ----------------------------------------------------

        data = pd.Timestamp(year=ano, month=mes, day=1)

        df["data"] = data

        # ----------------------------------------------------
        # Adiciona informações de origem
        # ----------------------------------------------------

        df["ano"] = ano
        df["mes"] = mes

        # Opcional: nome da aba
        df["sheet_origem"] = nome_aba

        # Guarda o dataset
        datasets.append(df)


# ============================================================
# COMPILAR TODOS OS DATASETS
# ============================================================

if datasets:

    df_final = pd.concat(
        datasets,
        ignore_index=True
    )

    # --------------------------------------------------------
    # Ordena por data
    # --------------------------------------------------------

    df_final = df_final.sort_values(
        by=["data"]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Salva o resultado
    # --------------------------------------------------------

    df_final.to_excel(
        arquivo_saida,
        index=False
    )

    print("\n============================================")
    print("COMPILAÇÃO CONCLUÍDA")
    print("============================================")
    print(f"Arquivo criado: {arquivo_saida}")
    print(f"Quantidade de linhas: {len(df_final):,}")
    print(f"Quantidade de colunas: {len(df_final.columns)}")
    print(f"Período: {df_final['data'].min()} até {df_final['data'].max()}")

else:

    print("\nNenhum dado foi encontrado.")


# ============================================================
# VISUALIZAÇÃO
# ============================================================

print("\nPrimeiras linhas:")
print(df_final.head())

print("\nColunas:")
print(df_final.columns.tolist())