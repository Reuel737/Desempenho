import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rho = 1.225
S = 1.08263
W = 23.6 # N
m = W / 9.81
CL = 1.81 # CL takeoff
CD = 0.058
CLmax = 2.02287
mu_r = 0.04
b = 3.65 # envergadura [m]
h = 0.3 # altura no solo

gmps = [
    {
        "arquivo": "Dados GMP/16x8E_4043.txt",
        "label": "Monoplano / 16x8x3 / 4043 rpm",
        "fig": "plot_takeoff_16x8x3.png"
    },
    {
        "arquivo": "Dados GMP/19x12E_3007.txt",
        "label": "Monoplano / 19x12E / 3007 rpm",
        "fig": "plot_takeoff_19x12E.png"
    },
    {
        "arquivo": "Dados GMP/20x10E_4025.txt",
        "label": "Monoplano / 20x10E / 4025 rpm",
        "fig": "plot_takeoff_20x10E.png"
    }
]

# Função efeito solo 6.99
def phi_ground(h, b):
    return 1 / (1 + (16*h/b)**2)

phi = phi_ground(h, b)

for gmp in gmps:

    df = pd.read_csv(gmp["arquivo"], delim_whitespace=True)
    V_tab = df["V"].values
    T_tab = df["T"].values

    # interpolador de tração
    def T_of_V(V):
        return np.interp(V, V_tab, T_tab, left=T_tab[0], right=0.0)

    dx = 0.5
    V = 0.1
    s = 0.0

    s_hist, T_hist, D_hist, L_hist, R_hist, Fnet_hist, F_atrito_hist, R_total_hist = [], [], [], [], [], [], [], []

    while True:

        T = T_of_V(V)
        D = 0.5 * rho * V**2 * S * CD * phi
        L = 0.5 * rho * V**2 * S * CL * phi
        R = D + mu_r * (W - L)

        F_atrito = mu_r * (W - L)
        R_total = D + F_atrito
        F_net = T - R_total

        R_hist.append(R)
        F_atrito_hist.append(F_atrito)
        R_total_hist.append(R_total)

        if F_net <= 0:
            break

        V = np.sqrt(V**2 + 2 * F_net / m * dx)
        s += dx

        s_hist.append(s)
        T_hist.append(T)
        D_hist.append(D)
        L_hist.append(L)
        Fnet_hist.append(F_net)

        if L >= W:
            break

    # Figura tipo 6.50
    plt.figure(figsize=(8,5))
    plt.plot(s_hist, T_hist, label="Tração T")
    plt.plot(s_hist, D_hist, label="Arrasto D")
    plt.plot(s_hist, L_hist, label="Sustentação L")
    plt.plot(s_hist, F_atrito_hist, label=r"Atrito $\mu_r (W - L)$")
    plt.plot(s_hist, R_hist, "--", label="Resistência no solo $D + \mu_r (W - L)$")

    # seta da diferença
    i_arrow = len(s_hist) // 2
    s_arrow = s_hist[i_arrow]
    T_arrow = T_hist[i_arrow]
    R_arrow = R_hist[i_arrow]

    plt.annotate(
        "",
        xy=(s_arrow, T_arrow),
        xytext=(s_arrow, R_arrow),
        arrowprops=dict(arrowstyle="<->", linewidth=1.5)
    )

    plt.text(
        s_arrow + 0.02 * max(s_hist),
        0.5 * (T_arrow + R_arrow),
        r"$T - [D + \mu_r (W - L)]$",
        va="center"
    )

    plt.xlabel("Distância ao longo do solo [m]")
    plt.ylabel("Força [N]")
    plt.title(f"Desempenho de Decolagem – {gmp['label']}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"PNG Plots/Takeoff/{gmp['fig']}", dpi=300, bbox_inches="tight")
    plt.close()
