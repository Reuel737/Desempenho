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

os.makedirs("PNG Plots/PxV", exist_ok=True)

gmps = [
    {
        "arquivo": "Dados GMP/16x8E_4043.txt",
        "label": "Monoplano / 16x8x3 / 4043 rpm",
        "fig": "plot_PxV_16x8x3.png"
    },
    {
        "arquivo": "Dados GMP/19x12E_3007.txt",
        "label": "Monoplano / 19x12E / 3007 rpm",
        "fig": "plot_PxV_19x12E.png"
    },
    {
        "arquivo": "Dados GMP/20x10E_4025.txt",
        "label": "Monoplano / 20x10E / 4025 rpm",
        "fig": "plot_PxV_20x10E.png"
    }
]

for gmp in gmps:

    df = pd.read_csv(gmp["arquivo"], delim_whitespace=True)

    V = df["V"]
    T = df["T"]

    df["P_disp"] = T * V

    df["P_nec"] = (
        0.5 * rho * V**3 * S * CD0
        + (2 * W**2) / (rho * V * S * np.pi * e * AR)
    )

    df.to_csv(
        gmp["arquivo"],
        sep=" ",
        index=False,
        float_format="%.6f"
    )

    plt.figure()

    plt.plot(V, df["P_disp"], label="Potência disponível")
    plt.plot(V, df["P_nec"], "--", label="Potência necessária")

    plt.xlabel("Velocidade do ar (m/s)")
    plt.ylabel("Potência (W)")
    plt.title(gmp["label"])
    plt.grid()
    plt.legend()

    plt.savefig(f"PNG Plots/PxV/{gmp['fig']}", dpi=300, bbox_inches="tight")
    plt.close()