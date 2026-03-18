import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def ler_dados_acelerometro(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, sep='|', skiprows=[1], skipinitialspace=True)
    df.columns = df.columns.str.strip()
    return df

def filtro_asfalto(dados, cutoff=2.0, fs=50.0, order=4):
    """Filtro Passa-Baixa para limpar o sinal"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, dados)

def plotar_eixos_separados(caminho_arquivo):
    df = ler_dados_acelerometro(caminho_arquivo)
    
    # Tempo em segundos a partir do zero
    df['Tempo_s'] = (df['Time(ms)'] - df['Time(ms)'].iloc[0]) / 1000.0
    
    # Aplicando o filtro em cada eixo individualmente
    df['X_Filt'] = filtro_asfalto(df['Accx'])
    df['Y_Filt'] = filtro_asfalto(df['Accy'])
    df['Z_Filt'] = filtro_asfalto(df['Accz'])
    
    # Criando 3 gráficos empilhados
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # --- Eixo X (Lateral) ---
    ax1.plot(df['Tempo_s'], df['Accx'], color='lightgray', label='Bruto')
    ax1.plot(df['Tempo_s'], df['X_Filt'], color='red', linewidth=2, label='Filtrado')
    ax1.set_title('Eixo X (Lateral / Asas)', fontsize=12)
    ax1.set_ylabel('m/s²')
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.legend(loc='upper right')
    
    # --- Eixo Y (Longitudinal / Frente-Trás) ---
    # É AQUI QUE A MÁGICA ACONTECE!
    ax2.plot(df['Tempo_s'], df['Accy'], color='lightgray', label='Bruto')
    ax2.plot(df['Tempo_s'], df['Y_Filt'], color='blue', linewidth=2, label='Filtrado')
    ax2.set_title('Eixo Y (Longitudinal / Frente do Avião) -> OLHE AQUI PARA ACHAR A DESCIDA', fontsize=12, color='blue')
    ax2.set_ylabel('m/s²')
    ax2.grid(True, linestyle=':', alpha=0.7)
    
    # --- Eixo Z (Vertical / Gravidade) ---
    ax3.plot(df['Tempo_s'], df['Accz'], color='lightgray', label='Bruto')
    ax3.plot(df['Tempo_s'], df['Z_Filt'], color='green', linewidth=2, label='Filtrado')
    ax3.set_title('Eixo Z (Vertical / Gravidade e Impacto)', fontsize=12)
    ax3.set_ylabel('m/s²')
    ax3.set_xlabel('Tempo (Segundos)', fontsize=12)
    ax3.grid(True, linestyle=':', alpha=0.7)
    
    plt.suptitle('Identificação de Movimento por Eixos Isolados', fontsize=16)
    plt.tight_layout()
    plt.savefig('plot_acc_70_50.png')
    plt.show()

# === COMO EXECUTAR ===
plotar_eixos_separados('CSV acelerometro/atrito_70_50.csv')