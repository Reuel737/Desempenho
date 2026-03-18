import pandas as pd
import numpy as np

rho0 = 1.225
S = 1.08263
W = 23.6
CLmax = 2.02287

gmps = [
    {
        "arquivo": "Dados GMP/16x8E_4043.txt",
        "nome": "Monoplano / 16x8x3 / 4043 rpm",
        "fig": "plot_RCxV_16x8x3.png"
    },
    {
        "arquivo": "Dados GMP/19x12E_3007.txt",
        "nome": "Monoplano / 19x12E / 3007 rpm",
        "fig": "plot_RCxV_19x12E.png"
    },
    {
        "arquivo": "Dados GMP/20x10E_4025.txt",
        "nome": "Monoplano / 20x10E / 4025 rpm",
        "fig": "plot_RCxV_20x10E.png"
    }
]

# Velocidade de estol
Vs = np.sqrt((2 * W) / (rho0 * S * CLmax))
print(f"\nVelocidade de estol: Vs = {Vs:.2f} m/s\n")

for gmp in gmps:
    df = pd.read_csv(gmp["arquivo"], delim_whitespace=True)

    V = df["V"].values
    RC = df["RC"].values

    idx_sort = np.argsort(V)
    V = V[idx_sort]
    RC = RC[idx_sort]

    # Ignora região de estol
    mask = V >= Vs
    V = V[mask]
    RC = RC[mask]

    idx_rcmax = np.argmax(RC)
    RCmax = RC[idx_rcmax]
    V_rcmax = V[idx_rcmax]

    h_total = 100.0  # m
    tempo_subida = h_total / RCmax if RCmax > 0 else np.inf

    # Teto absoluto (RC = 0 por interpolação)
    # encontra troca de sinal
    sinal = np.sign(RC)
    troca = np.where(np.diff(sinal) < 0)[0]

    if len(troca) > 0:
        i = troca[0]
        V_teto = np.interp(
            0.0,
            [RC[i], RC[i + 1]],
            [V[i], V[i + 1]]
        )
    else:
        V_teto = np.nan

    # Resultados
    print(f"GMP: {gmp['nome']}")
    print(f"  RC máximo     = {RCmax:.2f} m/s")
    print(f"  Vel. RC máx   = {V_rcmax:.2f} m/s")
    print(f"  Tempo subida  = {tempo_subida:.1f} s (até {h_total:.0f} m)")
    print(f"  Teto absoluto = RC = 0 em V ≈ {V_teto:.2f} m/s\n")
