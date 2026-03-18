import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from drag_function import drag_function

# Dados do monoplano
rho = 1.225   # kg/m³ (0 m)
S = 1.08263
CD0 = 0.03644413
W = 23.6
AR = 12.3
e = 0.8

gmps = [
    {
        "nome": "20x10E / 4025 rpm / Altitude = 0m",
        "arquivo": "Dados GMP/20x10E_4025.txt",
        "plot": "PNG Plots/Vmax/Vmax_20x10E.png"
    },
    {
        "nome": "19x12E / 3007 rpm / Altitude = 0m",
        "arquivo": "Dados GMP/19x12E_3007.txt",
        "plot": "PNG Plots/Vmax/Vmax_19x12E.png"
    },
    {
        "nome": "16x8x3 / 4043 rpm / Altitude = 0m",
        "arquivo": "Dados GMP/16x8E_4043.txt",
        "plot": "PNG Plots/Vmax/Vmax_16x8x3.png"
    }
]

for gmp in gmps:
    df = pd.read_csv(gmp["arquivo"], delim_whitespace=True)

    V = df["V"].values
    Ta = df["T"].values

    # Arrasto
    D = drag_function(V, rho, S, CD0, W, e, AR)

    diff = Ta - D

    i = np.where(np.diff(np.sign(diff)))[0][0]

    # interpolação linear
    Vmax = V[i] - diff[i] * (V[i+1] - V[i]) / (diff[i+1] - diff[i])
    Ta_Vmax = np.interp(Vmax, V, Ta)

    plt.figure()

    plt.plot(V, Ta, label="Tração disponível")
    plt.plot(V, D, "--", label="Arrasto")

    plt.scatter(Vmax, Ta_Vmax, color="k", zorder=3)
    plt.text(
        Vmax, Ta_Vmax,
        f"  Vmax = {Vmax:.2f} m/s",
        verticalalignment="bottom"
    )

    plt.xlabel("Velocidade do ar (m/s)")
    plt.ylabel("Força (N)")
    plt.title(gmp["nome"])
    plt.grid()
    plt.legend()

    plt.savefig(gmp["plot"], dpi=300, bbox_inches="tight")
    plt.close()