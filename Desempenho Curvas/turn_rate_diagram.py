"""
=============================================================
NISUS Aerodesign — UFSC Joinville
Turn Rate Diagram — Modelo 2432
Setor de Desempenho · 2026
=============================================================
Parâmetros aerodinâmicos: Melhores_individuos_TOP_10.csv
Motor: Run_22x8_MN7005 (QPROP) — MAD MN7005 + hélice 22x8
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import interp1d

#  PARÂMETROS AERODINÂMICOS — modelo 2432
MTOW_kg  = 9.792
g        = 9.81
W        = MTOW_kg * g
S        = 0.7972875 * 2  # m²  área total
b        = 1.900 * 2  # m   envergadura total
CLmax    = 2.09929
CD0      = 0.02856104001
k        = 0.07051
ALT_m    = 120.0
rho      = 1.225 * (1 - 2.26e-5 * ALT_m)**5.256
n_max    = 2.5


#  PARÂMETROS AERODINÂMICOS — modelo 2432
# MTOW_kg  = 9.449249
# g        = 9.81
# W        = MTOW_kg * g
# S        = 0.743228 * 2  # m²  área total
# b        = 1.800 * 2  # m   envergadura total
# CLmax    = 2.10395
# CD0      = 0.030490
# k        = 0.07115
# ALT_m    = 120.0
# rho      = 1.225 * (1 - 2.26e-5 * ALT_m)**5.256
# n_max    = 2.5

#  CURVA T(V) REAL — QPROP Run_22x8_MN7005
#  MAD MN7005 + hélice 22x8  @ rho=1.225 kg/m³
_V_data = np.array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                    10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                    20, 21, 22, 23, 24], dtype=float)
_T_data = np.array([44.32, 43.38, 42.34, 41.17, 39.91, 38.54,
                    37.11, 35.62, 34.06, 32.44, 30.76, 29.03,
                    27.23, 25.37, 23.46, 21.49, 19.47, 17.40,
                    15.28, 13.11, 10.90,  8.639, 6.337, 3.994, 1.602])

# Interpola T(V) extrapolação constante
_T_interp = interp1d(_V_data, _T_data, kind='cubic',
                     bounds_error=False,
                     fill_value=(_T_data[0], 0.0))

def T(V):
    """Tração disponível [N] — curva real QPROP MN7005 22x8."""
    return float(max(_T_interp(V), 0.0))

#  FUNÇÕES
def n_stall(V):
    return (rho * V**2 * S * CLmax) / (2 * W)

def drag(V, n):
    CL = (2*n*W) / (rho*V**2*S)
    return 0.5*rho*V**2*S*(CD0 + k*CL**2)

def omega(V, n):
    return np.degrees(g*np.sqrt(max(n**2-1, 0))/V)

def n_sus(V):
    nl = min(n_stall(V), n_max)
    if nl <= 1.0: return 1.0
    nb = 1.0
    for ni in np.linspace(1.0, nl, 3000):
        if drag(V, ni) <= T(V): nb = ni
        else: break
    return nb

#  VARREDURA
V0       = np.sqrt(2*W/(rho*S*CLmax))
V_corner = np.sqrt(2*n_max*W/(rho*S*CLmax))

Varr       = np.linspace(V0*0.99, 26.0, 1200)
omega_inst = np.array([omega(V, min(n_stall(V), n_max)) for V in Varr])
n_sus_arr  = np.array([n_sus(V) for V in Varr])
omega_sus  = np.array([omega(V, n) if n > 1.001 else 0.0
                       for V, n in zip(Varr, n_sus_arr)])

i_best  = np.argmax(omega_sus)
V_best  = Varr[i_best]; om_best = omega_sus[i_best]
n_best  = n_sus_arr[i_best]
R_best  = V_best**2 / (g*np.sqrt(max(n_best**2-1, 1e-9)))

VP   = 25.0;  VMIN = 5.0
mk   = Varr <= VP
Vp   = Varr[mk]; oi = omega_inst[mk]; os_ = omega_sus[mk]
oi_clip = np.maximum(oi, os_)

#  PLOTAGEM
fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Estol: da esquerda até onde a curva instantânea começa a ter valor
# Estol se estende até onde a curva instantânea realmente decola
# fill_between cobre o mesmo intervalo para não deixar branco
ax.fill_between(Vp, 0, oi_clip, where=(oi_clip == 0), 
                color="#BBDEFB", alpha=0.55)
ax.axvspan(VMIN, Vp[oi_clip > 0][0] if np.any(oi_clip > 0) else V0,
           color="#BBDEFB", alpha=0.55)
# Região B — verde onde há curva possível
ax.fill_between(Vp, 0, oi_clip, color="#C8E6C9", alpha=0.55)
# Região A — amarelo por cima onde há déficit
ax.fill_between(Vp, os_, oi_clip, color="#FFD54F", alpha=0.55)
# Acima da curva instantânea: duas regiões distintas
# Estol acelerado: à esquerda da corner velocity (limitado pela aerodinâmica)
mk_estol_ac = Vp < V_corner
ax.fill_between(Vp[mk_estol_ac], oi_clip[mk_estol_ac], 160,
                color='#90CAF9', alpha=0.55)   # azul — estol acelerado
# Limite estrutural: à direita da corner velocity (limitado pela estrutura)
mk_struct = Vp >= V_corner
ax.fill_between(Vp[mk_struct], oi_clip[mk_struct], 160,
                color='#FFCDD2', alpha=0.55)   # vermelho — limite estrutural

# Linha e label do estol normal
ax.axvline(V0, color='#1565C0', lw=1.4, ls='--', alpha=0.7)
ax.text(V0 - 0.2, 8, f'Estol\n{V0:.1f} m/s',
        ha='right', fontsize=8.5, color='#1565C0', fontweight='bold')

# Corner speed — linha vertical e label
ax.axvline(V_corner, color='#2E7D32', lw=1.4, ls='--', alpha=0.7)
ax.text(V_corner + 0.2, 8, f'Corner\n{V_corner:.1f} m/s',
        ha='left', fontsize=8.5, color='#2E7D32', fontweight='bold')

# Labels das regiões proibidas — discretos, dentro de cada faixa
ax.text(V0 + (V_corner - V0)/2, 148, 'Estol acelerado',
        ha='center', fontsize=8, color='#1565C0', alpha=0.8,
        fontweight='bold')
ax.text(VP - 1.0, 148, 'Limite estrutural',
        ha='right', fontsize=8, color='#C62828', alpha=0.8,
        fontweight='bold')

ax.plot(Vp, oi,  color='#1B5E20', lw=2.4, label='Curva instantânea')
ax.plot(Vp, os_, color='#E65100', lw=2.4, label='Curva sustentada')

for n_ref in [1.5, 2.0, 2.5, n_max]:
    V_n0 = np.sqrt(2*n_ref*W/(rho*S*CLmax))
    if V_n0 > VP: continue
    Vn  = np.linspace(V_n0, VP, 300)
    omn = [omega(v, n_ref) for v in Vn]
    ax.plot(Vn, omn, color='#B0BEC5', lw=0.8, ls=':', alpha=0.8)
    ax.text(Vn[len(Vn)//3], omn[len(Vn)//3] + 1.5,
            f'n={n_ref:.1f}g', fontsize=7.5, color='#78909C')

ax.scatter([V_best], [om_best], color='#C62828', s=70, zorder=6)
ax.annotate(f'V={V_best:.1f} m/s   ω={om_best:.0f}°/s\nn={n_best:.2f}g   R={R_best:.1f} m',
            xy=(V_best, om_best), xytext=(V_best + 2.0, om_best - 35),
            fontsize=8.5, color='#C62828',
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.1))

dados = (f"Modelo 2432\n"
         f"MTOW={MTOW_kg:.2f} kg   S={S:.3f} m²   AR={b**2/S:.2f}\n"
         f"CLmax={CLmax:.3f}   CD0={CD0:.4f}   k={k:.4f}\n"
         f"Motor: MAD MN7005 + 22x8 (QPROP)\n"
         f"T(0)={_T_data[0]:.1f} N   V_estol={V0:.1f} m/s   n_max={n_max}g")
ax.text(0.015, 0.985, dados, transform=ax.transAxes,
        fontsize=7.5, va='top', family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.88, ec='#90A4AE'))

pA  = mpatches.Patch(color='#FFD54F', alpha=0.7, label='A — déficit de energia')
pB  = mpatches.Patch(color='#C8E6C9', alpha=0.7, label='B — excesso de energia')
pES = mpatches.Patch(color='#90CAF9', alpha=0.7, label='Estol acelerado')
pE  = mpatches.Patch(color='#FFCDD2', alpha=0.7, label='Limite estrutural')
h, _ = ax.get_legend_handles_labels()
ax.legend(handles=h + [pA, pB, pES, pE], loc='upper right',
          fontsize=9, framealpha=0.95, edgecolor='#BDBDBD')

ax.set_xlim(VMIN, VP)
ax.set_ylim(0, 160)
ax.set_xlabel('Velocidade [m/s]', fontsize=11)
ax.set_ylabel('Taxa de curva [°/s]', fontsize=11)
ax.set_title('Diagrama de Manobrabilidade — Modelo 2432',
             fontsize=13, fontweight='bold', pad=12)
ax.grid(True, ls='--', alpha=0.25, color='#CFD8DC')
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('Desempenho Curvas/turn_rate_diagram_466.png', dpi=200, bbox_inches='tight')
print("Salvo.")

print(f"\n{'='*50}")
print(f"  Modelo 2432 — Resumo")
print(f"{'='*50}")
print(f"  Motor:              MAD MN7005 + hélice 22x8")
print(f"  T(V=0):             {_T_data[0]:.2f} N")
print(f"  V_estol (1g):       {V0:.2f} m/s")
print(f"  Corner velocity:    {V_corner:.2f} m/s")
print(f"  Melhor sustentada:")
print(f"    V:                {V_best:.2f} m/s")
print(f"    ω:                {om_best:.1f} °/s")
print(f"    n:                {n_best:.3f} g")
print(f"    R:                {R_best:.2f} m")
print(f"{'='*50}")