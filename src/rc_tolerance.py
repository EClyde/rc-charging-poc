import numpy as np
import matplotlib.pyplot as plt
import os

V0 = 5.0
VIH = 0.7 * V0

# Chosen for the appliance-controller application in Part A:
# 100 kOhm, 1% metal-film resistor; 1 uF, +/-10% X7R ceramic capacitor
# (typical datasheet tolerances, not the tutorial's 83 kOhm/100 nF/10% demo values).
R_nominal = 100e3   # ohm
C_nominal = 1e-6     # F
tol_R = 0.01         # +/-1%
tol_C = 0.10         # +/-10%

k = -np.log(1 - VIH / V0)   # independent of R, C

# Corner cases: smallest R,C -> fastest release; largest R,C -> slowest release
R_fast, C_fast = R_nominal * (1 - tol_R), C_nominal * (1 - tol_C)
R_slow, C_slow = R_nominal * (1 + tol_R), C_nominal * (1 + tol_C)

t_nominal = k * R_nominal * C_nominal
t_fast = k * R_fast * C_fast
t_slow = k * R_slow * C_slow

print(f"t_release nominal = {t_nominal*1e3:.2f} ms")
print(f"t_release fastest = {t_fast*1e3:.2f} ms")
print(f"t_release slowest = {t_slow*1e3:.2f} ms")

def vc(t, R, C):
    return V0 * (1 - np.exp(-t / (R * C)))

t = np.linspace(0, 1.4 * t_slow, 500)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(t * 1e3, vc(t, R_nominal, C_nominal), 'k-',  label='Nominal')
ax.plot(t * 1e3, vc(t, R_fast, C_fast),       'k--', label='Fastest case')
ax.plot(t * 1e3, vc(t, R_slow, C_slow),       'k-.', label='Slowest case')
ax.axhline(VIH, color='k', linestyle=':', linewidth=1, label=r'$V_{IH}$')

ax.set_xlabel('Time (ms)')
ax.set_ylabel('Capacitor voltage (V)')
ax.set_title('RC Charging with Component Tolerance')
ax.legend()
fig.tight_layout()

os.makedirs('figures/generated', exist_ok=True)
fig.savefig('figures/generated/rc_tolerance.pdf')