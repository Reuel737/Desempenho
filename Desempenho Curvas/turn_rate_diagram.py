"""
    NISUS Aerodesign — UFSC Joinville
    Turn Rate Diagram — Modelo 2432
    Setor de Desempenho 2026

    Parâmetros extraídos de: Melhores_individuos_TOP_10.csv
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Parametros — 2432
MTOW_kg = 9.449249
g = 9.81
W = MTOW_kg * g

S = 0.743228 * 2   # m²  área total
b = 1.800 * 2   # m  envergadura total
CLmax = 2.10395
CD0 = 0.030490
k = 0.07115

T_static = 35.18   # PREENCHER CORRETAMENTE
P_disp = 572.80   # PREENCHER CORrETAMENTE
ALT_m = 120.0   # m  altitude-densidade do ensaio
rho = 1.225*(1-2.26e-5*ALT_m)**5.256

n_max = 3.0   # fator de carga máximo estrutural

def T(V):
    """Tração disp: potência constante, limitada pela tração estática."""
    return float(min(T_static, P_disp / V))

def n_stall(V):
    """nmax antes do estol em V."""
    return (rho * V**2 * S * CLmax) / (2 * W)

def drag(V, n):
    """Arrasto total em curva [N]."""
    CL = (2*n*W) / (rho*V**2*S)
    return 0.5*rho*V**2*S*(CD0 + k*CL**2)

def omega(V, n):
    """Taxa de curva [°/s]."""
    return np.degrees(g*np.sqrt(max(n**2-1, 0))/V)

def n_sus(V):
    """Maior n sustentável em V (Ps=0): T_disp = D_curva."""
    nl = min(n_stall(V), n_max)
    if nl <= 1.0: return 1.0
    nb = 1.0
    for ni in np.linspace(1.0, nl, 3000):
        if drag(V, ni) <= T(V): nb = ni
        else: break
    return nb

# varredura
V0 = np.sqrt(2*W/(rho*S*CLmax))
V_corner = np.sqrt(2*n_max*W/(rho*S*CLmax))

Varr = np.linspace(V0*0.99, 28.0, 1200)
omega_inst = np.array([omega(V, min(n_stall(V), n_max)) for V in Varr])
n_sus_arr = np.array([n_sus(V) for V in Varr])
omega_sus = np.array([omega(V, n) if n > 1.001 else 0.0 for V, n in zip(Varr, n_sus_arr)])

i_best  = np.argmax(omega_sus)
V_best  = Varr[i_best]; om_best = omega_sus[i_best]
n_best  = n_sus_arr[i_best]
R_best  = V_best**2 / (g*np.sqrt(max(n_best**2-1, 1e-9)))

VP   = 25.0;  VMIN = 5.0
mk   = Varr <= VP
Vp   = Varr[mk]; oi = omega_inst[mk]; os_ = omega_sus[mk]
oi_clip = np.maximum(oi, os_)

# plotagem
fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Limite de estol
ax.fill_between([VMIN, V0], [0,0], [160,160], color='#BBDEFB', alpha=0.55)

# Região B — excesso de energia
ax.fill_between(Vp, 0, os_, color='#C8E6C9', alpha=0.55)

# Região A — déficit de energia
ax.fill_between(Vp, os_, oi_clip, color='#FFD54F', alpha=0.55)

# limite estrutural
mk_s = Vp >= V_corner
ax.fill_between(Vp[mk_s], oi_clip[mk_s], 160, color='#FFCDD2', alpha=0.55)

# labels de limite
ax.axvline(V0, color='#1565C0', lw=1.4, ls='--', alpha=0.7)
ax.text(V0 - 0.25, 150, 'Limite\nde estol',
        ha='right', fontsize=9, color='#1565C0', fontweight='bold')
ax.text(VP - 0.3, 150, 'Limite\nestrutural',
        ha='right', fontsize=9, color='#C62828', fontweight='bold')

# curvas principais
ax.plot(Vp, oi,  color='#1B5E20', lw=2.4, label='Curva instantânea')
ax.plot(Vp, os_, color='#E65100', lw=2.4, label='Curva sustentada')

# iso-n
for n_ref in [1.5, 2.0, 2.5, n_max]:
    V_n0 = np.sqrt(2*n_ref*W/(rho*S*CLmax))
    if V_n0 > VP: continue
    Vn  = np.linspace(V_n0, VP, 300)
    omn = [omega(v, n_ref) for v in Vn]
    ax.plot(Vn, omn, color='#B0BEC5', lw=0.8, ls=':', alpha=0.8)
    ax.text(Vn[len(Vn)//3], omn[len(Vn)//3] + 1.5,
            f'n={n_ref:.1f}g', fontsize=7.5, color='#78909C')

# Ponto ótimo
ax.scatter([V_best], [om_best], color='#C62828', s=70, zorder=6)
ax.annotate(f'V={V_best:.1f} m/s   ω={om_best:.0f}°/s\nn={n_best:.2f}g   R={R_best:.1f} m',
            xy=(V_best, om_best), xytext=(V_best + 2.0, om_best - 35),
            fontsize=8.5, color='#C62828',
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.1))

# caixa de parâmetros
dados = (f"Modelo 2432\n"
         f"MTOW={MTOW_kg:.2f} kg   S={S:.3f} m²   AR={b**2/S:.2f}\n"
         f"CLmax={CLmax:.3f}   CD0={CD0:.4f}   k={k:.4f}\n"
         f"V_estol={V0:.1f} m/s   n_max={n_max}g")
ax.text(0.015, 0.985, dados, transform=ax.transAxes,
        fontsize=7.5, va='top', family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.88, ec='#90A4AE'))

# legenda
pA = mpatches.Patch(color='#FFD54F', alpha=0.7, label='A — déficit de energia')
pB = mpatches.Patch(color='#C8E6C9', alpha=0.7, label='B — excesso de energia')
pE = mpatches.Patch(color='#FFCDD2', alpha=0.7, label='Limite estrutural')
h, _ = ax.get_legend_handles_labels()
ax.legend(handles=h + [pA, pB, pE], loc='upper right',
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
plt.savefig('turn_rate_diagram_2432.png', dpi=200, bbox_inches='tight')
plt.show()

# resumo
print("=" * 50)
print("  Modelo 2432 — Resumo")
print("=" * 50)
print(f"  V_estol (1g):       {V0:.2f} m/s")
print(f"  Corner velocity:    {V_corner:.2f} m/s")
print(f"  Melhor sustentada:")
print(f"    V:                {V_best:.2f} m/s")
print(f"    ω:                {om_best:.1f} °/s")
print(f"    n:                {n_best:.3f} g")
print(f"    R:                {R_best:.2f} m")
print("=" * 50)