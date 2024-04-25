import random
import numpy as np
from scipy.optimize import minimize


def dW():
    return random.randint(-99,99)/100

def dS(r, q, S, dt, v):
    return (r - q)*S*dt + np.sqrt(v)*S*dW()*np.sqrt(dt)

def dV(kappa, theta, v, dt, sigma):
    try:
        return kappa*(theta - v)*dt + sigma*np.sqrt(v)*dW()*np.sqrt(dt)
    except:
        return 0
        

def OptimizeSigma(kappa, theta, dt, sigma, obsvol, simvol, n):
    
    def Objective(x):
        diff = 0.0
        for i in range(1, n):
            simvol[i] += dV(kappa, theta, simvol[i-1], dt, x)
            diff += pow(simvol[i] - obsvol[i], 2)
        return diff
    
    res = minimize(Objective, sigma, method='SLSQP', bounds=[(0, 1)])
    return res.x
            
    




S = 100
K = 105
r = 0.05
q = 0.01
v = 0.15
t = 14.0/252.0

kappa = 2.0
theta = 0.2
sigma = 0.15

N = 300

dt = t/N

simulations = 20

option_payoff = 0

for s in range(simulations):

    S0 = S
    v0 = v
    sig = sigma


    obs_vol, sim_vol = [], []


    for i in range(N):
        S0 += dS(r, q, S0, dt, v0)
        obs_vol.append(v0)
        v0 += dV(kappa, theta, v0, dt, sig)
        v0 = np.max([v0, 0])
        sim_vol.append(v0)

        if i > 2:
            sig = OptimizeSigma(kappa, theta, dt, sig, obs_vol, sim_vol, i)
            sig = sig[0]
            sig = np.max([sig, 0])

    
    print(f'Simulations Left: {simulations - s + 1} | Final Sigma: {sig}')
    option_payoff += np.max([S0 - K, 0.0])

option_price = np.exp(-r*t)*np.mean(option_payoff)


print('OptionPrice: ', option_price)



