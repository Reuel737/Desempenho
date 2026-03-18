import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Dados do monoplano
rho = 1.225   # kg/m³ (0 m)
S = 1.08263
CD0 = 0.03644413
W = 23.6
AR = 12.3
e = 0.8

os.makedirs("PNG Plots/RCxV", exist_ok=True)

gmps = [
    {
        "arquivo": "Dados GMP/16x8E_4043.txt",
        "label": "Monoplano / 16x8x3 / 4043 rpm",
        "fig": "plot_RCxV_16x8x3.png"
    },
    {
        "arquivo": "Dados GMP/19x12E_3007.txt",
        "label": "Monoplano / 19x12E / 3007 rpm",
        "fig": "plot_RCxV_19x12E.png"
    },
    {
        "arquivo": "Dados GMP/20x10E_4025.txt",
        "label": "Monoplano / 20x10E / 4025 rpm",
        "fig": "plot_RCxV_20x10E.png"
    }
]

for gmp in gmps:

    df = pd.read_csv(gmp["arquivo"], delim_whitespace=True)

    P_disp = df["P_disp"]
    P_req = df["P_nec"]
    V = df["V"]

    df["RC"] = (P_disp-P_req)/W

    df.to_csv(
        gmp["arquivo"],
        sep=" ",
        index=False,
        float_format="%.6f"
    )

    plt.figure()

    plt.plot(V, df["RC"], label="Razão de subida")

    plt.xlabel("Velocidade do monoplano (m/s)")
    plt.ylabel("Razão de subida (m/s)")
    plt.title(gmp["label"])
    plt.grid()
    plt.legend()

    plt.savefig(f"PNG Plots/RCxV/{gmp['fig']}", dpi=300, bbox_inches="tight")
    plt.close()
