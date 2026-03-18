import pandas as pd

def ler_dados_acelerometro(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, sep='|', skiprows=[1], skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df

def extrair_aceleracao_direcional(caminho_arquivo, t_inicio_ms, t_fim_ms):
    df = ler_dados_acelerometro(caminho_arquivo)
    
    df_parado = df[df['Time(ms)'] < t_inicio_ms]
    
    if df_parado.empty:
        tara_y = 0.34
    else:
        tara_y = df_parado['Accy'].tail(20).mean() # Média dos últimos instantes parado
        
    print(f"Tara calculada para o eixo Y: {tara_y:.4f} m/s²")
    
    df_descida = df[(df['Time(ms)'] >= t_inicio_ms) & (df['Time(ms)'] <= t_fim_ms)].copy()
    
    # Isolar a aceleração removendo a tara
    df_descida['Mov_Y'] = df_descida['Accy'] - tara_y
    
    # A aceleração experimental é a média simples do eixo Y (as vibrações se cancelam)
    a_exp = df_descida['Mov_Y'].mean()
    
    print("-" * 40)
    print(f"RESULTADO DO TRECHO ({t_inicio_ms} a {t_fim_ms}):")
    print(f"Aceleração Experimental (a_exp): {a_exp:.4f} m/s²")
    print("-" * 40)
    
    return a_exp

a_exp_final = extrair_aceleracao_direcional('CSV acelerometro/atrito_70_50.csv', 335250, 338200)