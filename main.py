from numpy import sin, cos
import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
def oblicz_rozniczke(mux, t):

    dydx = np.zeros_like(mux)
    dydx[0] = mux[1]

    del_ = mux[2] - mux[0]
    den1 = (M1 + M2)*L1 + M2*L1*L2*sin(del_)*cos(del_)
    dydx[1] = (M2*L1*mux[1]*mux[1]*sin(del_)*cos(del_) +
               M2*G*sin(mux[2])*cos(del_) +
               M2*L2*mux[3]*mux[3]*sin(del_) -
               (M1 + M2)*G*sin(mux[0]))/den1

    dydx[2] = mux[3]

    den2 = (L2/L1)*den1
    dydx[3] = (M2*L2*L1*mux[3]*mux[3]*sin(del_)*cos(del_) +
               (M1 + M2)*G*sin(mux[0])*cos(del_) -
               (M1 + M2)*L1*mux[1]*mux[1]*sin(del_) -
               (M1 + M2)*G*sin(mux[2]))/den2

    return dydx

G = 9.8  
L1 = 1.0  
L2 = 1.0  
M1 = 1.0 
M2 = 2.0  
dt = 0.1 #czas
th1 = 90.0
w1 = 10.0
th2 = 90.0
w2 = 0.0
t = np.arange(0.0, 20, dt)
# stan poczatkowy
mux = np.radians([th1, w1, th2, w2])

y = integrate.odeint(oblicz_rozniczke, mux, t)

x1 = L1*sin(y[:, 0])
y1 = -L1*cos(y[:, 0])

x2 = L2*sin(y[:, 2]) + x1
y2 = -L2*cos(y[:, 2]) + y1

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-3, 3), ylim=(-3, 3), facecolor='darkslategray')
ax.grid()

line, = ax.plot([], [], 'o-', lw=4, color="white")
anim_napis = 'czas = %.1fs'
anim_text = ax.text(0.04, 0.04, '',color="white", transform=ax.transAxes)


def init():
    line.set_data([], [])
    anim_text.set_text('')
    return line, anim_text


def animate(i):
    animx = [0, x1[i], x2[i]]
    animy = [0, y1[i], y2[i]]

    line.set_data(animx, animy)
    anim_text.set_text(anim_napis % (i*dt))
    return line, anim_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=15, blit=True, init_func=init)

ani.save('podwojne_wahadlo.htm', fps=144)
