import pandas as pd
from pathlib import Path
import re
import unicodedata


# ============================================================
# CONFIGURAÇÕES
# ============================================================

pasta = Path(r"C:\Users\Jéferson\Documents\Crimes_RS")

arquivo_saida = pasta / "crimes_RS_compilado.xlsx"


# ============================================================
# MESES
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
# NORMALIZAR TEXTO
# ============================================================

def normalizar_texto(valor):

    if pd.isna(valor):
        return ""

    texto = str(valor).strip().lower()

    texto = unicodedata.normalize(
        "NFKD",
        texto
    ).encode(
        "ASCII",
        "ignore"
    ).decode(
        "ASCII"
    )

    return texto


# ============================================================
# ENCONTRAR LINHA "MUNICÍPIOS"
# ============================================================

def encontrar_linha_municipios(df):

    for linha in range(len(df)):

        for coluna in range(df.shape[1]):

            valor = df.iat[linha, coluna]

            texto = normalizar_texto(valor)

            # Procuramos especificamente por municipio
            if texto == "municipios":

                return linha

    return None


# ============================================================
# TORNAR NOMES DE COLUNAS ÚNICOS
# ============================================================

def nomes_unicos(colunas):

    resultado = {}
    novas_colunas = []

    for coluna in colunas:

        # ----------------------------------------------------
        # Converter para texto
        # ----------------------------------------------------

        if pd.isna(coluna):

            nome = ""

        else:

            nome = str(coluna).strip()


        # ----------------------------------------------------
        # Nome vazio
        # ----------------------------------------------------

        if nome == "" or nome.lower() == "nan":

            nome = "coluna_sem_nome"


        # ----------------------------------------------------
        # Criar nome único
        # ----------------------------------------------------

        if nome not in resultado:

            resultado[nome] = 0

            novas_colunas.append(nome)

        else:

            resultado[nome] += 1

            novo_nome = f"{nome}_{resultado[nome]}"

            novas_colunas.append(novo_nome)


    return novas_colunas


# ============================================================
# LISTA DOS DATASETS
# ============================================================

datasets = []


# ============================================================
# LOG DE PROBLEMAS
# ============================================================

problemas = []


# ============================================================
# PROCESSAR ARQUIVOS
# ============================================================

for arquivo in sorted(pasta.glob("*.xlsx")):

    # Não ler o arquivo de saída
    if arquivo.name == arquivo_saida.name:
        continue


    # --------------------------------------------------------
    # IDENTIFICAR ANO
    # --------------------------------------------------------

    match = re.search(
        r"(20\d{2})",
        arquivo.stem
    )

    if not match:

        print(
            f"⚠️ Ano não encontrado: {arquivo.name}"
        )

        continue


    ano = int(match.group(1))


    print()
    print("=" * 70)
    print(
        f"PROCESSANDO {arquivo.name} | ANO {ano}"
    )
    print("=" * 70)


    # --------------------------------------------------------
    # ABRIR EXCEL
    # --------------------------------------------------------

    try:

        excel = pd.ExcelFile(arquivo)

    except Exception as erro:

        print(
            f"❌ Erro ao abrir arquivo: {erro}"
        )

        problemas.append(
            (
                arquivo.name,
                "Erro ao abrir"
            )
        )

        continue


    # ========================================================
    # PROCESSAR CADA ABA
    # ========================================================

    for nome_aba in excel.sheet_names:

        nome_mes = normalizar_texto(nome_aba)


        # ----------------------------------------------------
        # Só processar abas que sejam meses
        # ----------------------------------------------------

        if nome_mes not in meses:

            continue


        mes = meses[nome_mes]


        print(
            f"   → Processando {nome_aba}/{ano}"
        )


        # ----------------------------------------------------
        # LER PLANILHA SEM HEADER
        # ----------------------------------------------------

        try:

            bruto = pd.read_excel(
                arquivo,
                sheet_name=nome_aba,
                header=None
            )

        except Exception as erro:

            print(
                f"      ❌ Erro: {erro}"
            )

            problemas.append(
                (
                    arquivo.name,
                    nome_aba,
                    "Erro na leitura"
                )
            )

            continue


        # ----------------------------------------------------
        # ENCONTRAR MUNICÍPIOS
        # ----------------------------------------------------

        linha_header = encontrar_linha_municipios(
            bruto
        )


        if linha_header is None:

            print(
                "      ❌ Linha 'Municípios' não encontrada."
            )

            problemas.append(
                (
                    arquivo.name,
                    nome_aba,
                    "Municípios não encontrado"
                )
            )

            continue


        print(
            f"      Cabeçalho encontrado na linha "
            f"{linha_header + 1}"
        )


        # ====================================================
        # CABEÇALHO
        # ====================================================

        cabecalho = bruto.iloc[
            linha_header
        ].tolist()


        # ====================================================
        # DADOS
        # ====================================================

        df = bruto.iloc[
            linha_header + 1:
        ].copy()


        # ====================================================
        # DEFINIR COLUNAS
        # ====================================================

        df.columns = nomes_unicos(
            cabecalho
        )


        # ====================================================
        # REMOVER COLUNAS TOTALMENTE VAZIAS
        #
        # IMPORTANTE:
        # fazemos isso somente DENTRO DA ABA, depois que
        # o cabeçalho já foi corretamente definido.
        # ====================================================

        # Não removemos aqui.
        #
        # Motivo:
        # uma coluna pode estar vazia neste mês,
        # mas existir em outro ano.


        # ====================================================
        # ENCONTRAR COLUNA MUNICÍPIO
        # ====================================================

        coluna_municipio = None


        for coluna in df.columns:

            if normalizar_texto(coluna) == "municipios":

                coluna_municipio = coluna

                break


        if coluna_municipio is None:

            print(
                "      ❌ Coluna Municípios não encontrada."
            )

            problemas.append(
                (
                    arquivo.name,
                    nome_aba,
                    "Coluna Municípios não encontrada"
                )
            )

            continue


        # ====================================================
        # RENOMEAR
        # ====================================================

        df.rename(
            columns={
                coluna_municipio: "municipio"
            },
            inplace=True
        )


        # ====================================================
        # REMOVER LINHAS COMPLETAMENTE VAZIAS
        # ====================================================

        df.dropna(
            how="all",
            inplace=True
        )


        # ====================================================
        # REMOVER LINHAS SEM MUNICÍPIO
        # ====================================================

        df = df[
            df["municipio"].notna()
        ].copy()


        # ====================================================
        # LIMPAR MUNICÍPIO
        # ====================================================

        df["municipio"] = (
            df["municipio"]
            .astype(str)
            .str.strip()
        )


        # ====================================================
        # REMOVER LINHAS DE TOTAL
        # ====================================================

        mascara_total = (
            df["municipio"]
            .str.upper()
            .str.startswith("TOTAL")
        )


        df = df[
            ~mascara_total
        ].copy()


        # ====================================================
        # ADICIONAR DATA
        # ====================================================

        data = pd.Timestamp(
            year=ano,
            month=mes,
            day=1
        )


        # ====================================================
        # ADICIONAR CAMPOS DE CONTROLE
        # ====================================================

        df.insert(
            0,
            "data",
            data
        )

        df.insert(
            1,
            "ano",
            ano
        )

        df.insert(
            2,
            "mes",
            mes
        )

        df["sheet_origem"] = nome_aba


        # ====================================================
        # LOG
        # ====================================================

        print(
            f"      ✓ {len(df):,} registros | "
            f"{len(df.columns):,} colunas"
        )


        # Mostrar as colunas da primeira aba
        if len(datasets) == 0:

            print()
            print("      COLUNAS ENCONTRADAS:")

            for coluna in df.columns:

                print(
                    f"         {coluna}"
                )

            print()


        # ====================================================
        # GUARDAR
        # ====================================================

        datasets.append(df)


# ============================================================
# VERIFICAR
# ============================================================

if not datasets:

    print(
        "\n❌ Nenhum dado encontrado."
    )

    raise SystemExit


# ============================================================
# COMPILAR
# ============================================================

print()
print("=" * 70)
print("COMPILANDO DATASETS")
print("=" * 70)


df_final = pd.concat(
    datasets,
    ignore_index=True,
    sort=False
)


# ============================================================
# ORDENAR
# ============================================================

df_final.sort_values(
    by=[
        "data",
        "municipio"
    ],
    inplace=True
)


df_final.reset_index(
    drop=True,
    inplace=True
)


# ============================================================
# ORGANIZAR COLUNAS DE CONTROLE
# ============================================================

colunas_controle = [
    "data",
    "ano",
    "mes",
    "municipio",
    "sheet_origem"
]


outras_colunas = [
    coluna
    for coluna in df_final.columns
    if coluna not in colunas_controle
]


df_final = df_final[
    colunas_controle + outras_colunas
]


# ============================================================
# RESULTADO
# ============================================================

print()
print("=" * 70)
print("RESULTADO DA COMPILAÇÃO")
print("=" * 70)

print(
    f"Linhas: {len(df_final):,}"
)

print(
    f"Colunas: {len(df_final.columns):,}"
)

print(
    f"Municípios: "
    f"{df_final['municipio'].nunique():,}"
)


# ============================================================
# MOSTRAR COLUNAS
# ============================================================

print()
print("COLUNAS FINAIS:")

for i, coluna in enumerate(
    df_final.columns,
    start=1
):

    print(
        f"{i:3} - {coluna}"
    )


# ============================================================
# SALVAR
# ============================================================

print()
print("Salvando Excel...")


df_final.to_excel(
    arquivo_saida,
    index=False
)


print()
print("=" * 70)
print("✅ CONCLUÍDO")
print("=" * 70)

print(
    f"Arquivo: {arquivo_saida}"
)


# ============================================================
# PROBLEMAS
# ============================================================

if problemas:

    print()
    print("=" * 70)
    print("⚠️ PROBLEMAS ENCONTRADOS")
    print("=" * 70)

    for problema in problemas:

        print(
            problema
        )