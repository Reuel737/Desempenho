import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

df = pd.read_csv('ensaio.csv') 

peso_modelo = 50.0  # Ajuste com o peso
frequencia = 100  # frequencia do ESP32

# Savitzky-Golay
# ordem 3
window_size = 51 
df['forca_suave'] = savgol_filter(df['Peso'], window_size, 3)
df['mu'] = df['forca_suave'] / peso_modelo

idx_pico = df['mu'].idxmax()
mu_estatico = df['mu'].iloc[idx_pico]
tempo_pico = df['Tempo_ms'].iloc[idx_pico]

# PLATEAU
df_pos_pico = df.iloc[idx_pico:].copy()

# Desvio Padrão Móvel
df_pos_pico['estabilidade'] = df_pos_pico['mu'].rolling(window=100).std()

threshold = df_pos_pico['estabilidade'].min() * 2.0 
regiao_estavel = df_pos_pico[df_pos_pico['estabilidade'] < threshold]

if not regiao_estavel.empty:
    mu_dinamico = regiao_estavel['mu'].mean()
    inicio_din = regiao_estavel['tempo'].iloc[0]
    fim_din = regiao_estavel['tempo'].iloc[-1]
else:
    # Fallback se o ensaio foi muito curto
    mu_dinamico = df_pos_pico['mu'].tail(200).mean()
    inicio_din, fim_din = df_pos_pico['tempo'].iloc[0], df_pos_pico['tempo'].iloc[-1]

plt.figure(figsize=(12, 6))

plt.plot(df['tempo'], df['forca']/peso_modelo, color='lightgray', alpha=0.5, label='Dados Brutos')
plt.plot(df['tempo'], df['mu'], color='#1f77b4', linewidth=2, label='Filtro Savitzky-Golay')

plt.scatter(tempo_pico, mu_estatico, color='red', s=100, zorder=5)
plt.annotate(f'$\mu_e$: {mu_estatico:.3f}', (tempo_pico, mu_estatico), 
             textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')

plt.axvspan(inicio_din, fim_din, color='green', alpha=0.15, label='Região de Estabilidade')
plt.axhline(y=mu_dinamico, color='green', linestyle='--', label=f'$\mu_d$ Médio: {mu_dinamico:.3f}')

plt.title('Análise de Coeficiente de Atrito - Modelo Aerodesign', fontsize=14)
plt.xlabel('Tempo (s)')
plt.ylabel('Coeficiente de Atrito ($\mu$)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"RESULTADOS")
print(f"C. Estático (Máximo): {mu_estatico:.4f}")
print(f"C. Dinâmico (Médio): {mu_dinamico:.4f}")