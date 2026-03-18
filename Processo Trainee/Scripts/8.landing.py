import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# Constantes
# ======================
rho = 1.225
S = 1.08263
W = 23.6        # N
m = W / 9.81
CL_land = 1.2   # CL típico em aterrissagem (menor que takeoff)
CD = 0.058
mu_r = 0.04
b = 3.65
h = 0.0

# ======================
# GMPs (mesmos do takeoff)
# ======================
gmps = [
    {
        "arquivo": "Dados GMP/16x8E_4043.txt",
        "label": "Monoplano / 16x8x3 / 4043 rpm",
        "fig": "plot_landing_16x8x3.png"
    },
    {
        "arquivo": "Dados GMP/19x12E_3007.txt",
        "label": "Monoplano / 19x12E / 3007 rpm",
        "fig": "plot_landing_19x12E.png"
    },
    {
        "arquivo": "Dados GMP/20x10E_4025.txt",
        "label": "Monoplano / 20x10E / 4025 rpm",
        "fig": "plot_landing_20x10E.png"
    }
]

# ======================
# Efeito solo
# ======================
def phi_ground(h, b):
    return 1 / (1 + (16*h/b)**2)

phi = phi_ground(h, b)

# ======================
# Loop dos GMPs
# ======================
for gmp in gmps:

    # Velocidade de toque (aprox. 1.15 Vs)
    V_stall = np.sqrt(2 * W / (rho * S * CL_land))
    V = 1.15 * V_stall

    dx = 0.5
    s = 0.0

    s_hist = []
    D_hist = []
    L_hist = []
    F_atrito_hist = []
    R_hist = []

    # ======================
    # Integração da corrida
    # ======================
    while V > 0.5:

        D = 0.5 * rho * V**2 * S * CD * phi
        L = 0.5 * rho * V**2 * S * CL_land * phi

        F_atrito = mu_r * (W - L)
        R = D + F_atrito     # resistência total

        # desaceleração
        V = np.sqrt(max(V**2 - 2 * R / m * dx, 0.0))
        s += dx

        s_hist.append(s)
        D_hist.append(D)
        L_hist.append(L)
        F_atrito_hist.append(F_atrito)
        R_hist.append(R)

    # ======================
    # Plot – Figura tipo 6.51
    # ======================
    plt.figure(figsize=(8,5))

    plt.plot(s_hist, L_hist, label="Sustentação L")
    plt.plot(s_hist, D_hist, label="Arrasto D")
    plt.plot(s_hist, F_atrito_hist, label=r"Atrito $\mu_r (W - L)$")
    plt.plot(s_hist, R_hist, "--", label=r"$D + \mu_r (W - L)$")

    plt.xlabel("Distância ao longo do solo [m]")
    plt.ylabel("Força [N]")
    plt.title(f"Desempenho de Aterrissagem – {gmp['label']}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"PNG Plots/Landing/{gmp['fig']}", dpi=300, bbox_inches="tight")
    plt.close()
