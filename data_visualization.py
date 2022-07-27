import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.stats import multivariate_normal
from matplotlib import cm


BANDWIDTH_X = 1 #Select the width of pdf functions. The original fuzzy set sigma is multiplied with this.
BANDWIDTH_Y = 1 #Select the width of pdf functions. The original fuzzy set sigma is multiplied with this
EXTRA_RANGE = 20 #How many percents of the total range is sunbstracted from minimum or added to maximum value of modeled variable to define axes
ACCURACY = 0.1 #Distance between points in axes

parser = argparse.ArgumentParser(description='Visualize data.')
parser.add_argument('-m', type=str, nargs='+', required=False, help='Define which variables are visualized')
args = parser.parse_args()
vars = args.m
if vars != None and len(vars) != 2:
    print("Wrong number of variables in argument -m!")
    exit()
T = pd.read_csv('data_for_visualization.csv',sep=';')

if vars == None:
    sigmas = []
    x = np.arange(-30, 80, 0.1) # Temperature Axis
    y = np.arange(-5, 5, 0.1) # Voltage axis
elif vars[0]+'Mean' not in T or vars[1]+'Mean' not in T:
    print("Variable not found in the dataset")
    exit()
else:
    sigmas = [vars[0]+'Sigma', vars[1]+'Sigma']
    means = [vars[0]+'Mean', vars[1]+'Mean']
    # Use the user determined variables and add 10% additional range to each end
    x_extra_range = (np.amax(T[means[0]]) - np.amin(T[means[0]])) * EXTRA_RANGE/100
    x = np.arange(np.amin(T[means[0]])-x_extra_range, np.amax(T[means[0]])+x_extra_range, ACCURACY)
    y_extra_range = (np.amax(T[means[1]]) - np.amin(T[means[1]])) * EXTRA_RANGE/100
    y = np.arange(np.amin(T[means[1]])-x_extra_range, np.amax(T[means[1]])+y_extra_range, ACCURACY)

X,Y = np.meshgrid(x,y, indexing='xy')
Z = 0

#Test sigmas. If sigma = -1, variable is binary and cannot be visualized.
if args.m == None:
    if T.TemperatureSigma[0] == -1:
        print("Temperature is binary variable, cannot visualize data. Try another variable. Quit...")
        quit()
    if T.VoltageSigma[0] == -1:
        print("Voltage is binary variable, cannot visualize data. Try another variable. Quit...")
        quit()            
else:
    if T[sigmas[0]][0] == -1:
        print("{} is binary variable, cannot visualize data. Try another variable. Quit...".format(vars[0]))
        quit()
    if T[sigmas[1]][0] == -1:
        print("{} is binary variable, cannot visualize data. Try another variable. Quit...".format(vars[1]))
        quit()

for i in range(T.shape[0]):
    if args.m == None:
        mu = [T.TemperatureMean[i], T.VoltageMean[i]]
        sigma = [[(T.TemperatureSigma[i] * BANDWIDTH_X), 0],[ 0, (T.VoltageSigma[i] * BANDWIDTH_Y)]]
    else:
        mu = [T[means[0]][i], T[means[1]][i]]
        sigma = [[(T[sigmas[0]][i] * BANDWIDTH_X), 0], [0, (T[sigmas[1]][i] * BANDWIDTH_Y)]]
    pdf = multivariate_normal.pdf(np.transpose([X.flatten(),Y.flatten()]),mean=mu, cov=sigma)
    Z = Z + pdf*T.Weight[i]

Z = Z.reshape(X.shape)
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax1.plot_surface(X, Y, Z, cmap=plt.get_cmap('viridis'))
if args.m == None:
    ax1.set_xlabel("Temperature ($^\circ$C)")
    ax1.set_ylabel('Voltage (V)')
else:
    ax1.set_xlabel(vars[0])
    ax1.set_ylabel(vars[1])
fig2, ax2 = plt.subplots()
contour = ax2.contour(X,Y, Z)
if args.m == None:
    ax2.set_xlabel("Temperature ($^\circ$C)")
    ax2.set_ylabel('Voltage (V)')
else:
    ax2.set_xlabel(vars[0])
    ax2.set_ylabel(vars[1])
plt.show()

