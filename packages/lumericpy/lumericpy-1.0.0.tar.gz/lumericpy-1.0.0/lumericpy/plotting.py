import numpy as np
import matplotlib.pyplot as plt

def plot2D(x,y,z):

    X,Y=np.meshgrid(x,y)

    fig, axs = plt.subplots(1, 1, figsize=(10, 8))

    im1 = axs[0, 0].pcolormesh(X, Y, np.abs(np.real(z)), cmap='jet')
    
    fig.colorbar(im1, ax=axs[0, 0])

    return fig, axs