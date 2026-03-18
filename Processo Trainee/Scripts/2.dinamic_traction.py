import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

altitude = 0
rho = 1.225

plt.figure()

# 20x10E — 4025 RPM
D_in = 20
RPM = 4025
arquivo = "Dados GMP/20x10E_4025.txt"

D = D_in * 0.0254
n = RPM / 60

df = pd.read_csv(arquivo, delim_whitespace=True)
V = df["J"] * n * D
T = df["CT"] * rho * n**2 * D**4

plt.plot(V, T, label="20x10E — 4025 rpm")

# 19x12E — 3007 RPM
D_in = 19
RPM = 3007
arquivo = "Dados GMP/19x12E_3007.txt"

D = D_in * 0.0254
n = RPM / 60

df = pd.read_csv(arquivo, delim_whitespace=True)
V = df["J"] * n * D
T = df["CT"] * rho * n**2 * D**4

plt.plot(V, T, label="19x12E — 3007 rpm")

# 16x8x3 — 4043 RPM (corrigida 2 → 3 pás)
D_in = 16
RPM = 4043
arquivo = "Dados GMP/16x8E_4043.txt"

D = D_in * 0.0254
n = RPM / 60

df = pd.read_csv(arquivo, delim_whitespace=True)
V = df["J"] * n * D
T = df["CT"] * rho * n**2 * D**4
T *= 1.5  # correção 2 pás → 3 pás

plt.plot(V, T, label="16x8x3 — 4043 rpm")

plt.xlabel("Velocidade do ar (m/s)")
plt.ylabel("Tração (N)")
plt.title(f"Altitude = {altitude} m")
plt.grid()
plt.legend()

plt.savefig("PNG Plots\TxV\plot_TxV_all.png", dpi=300, bbox_inches="tight")