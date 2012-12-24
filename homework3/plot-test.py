import matplotlib.pyplot as plt
import numpy as np

def xticklabels_example():
    fig = plt.figure() 

    x = np.arange(20)
    y1 = np.cos(x)
    y2 = (x**2)
    y3 = (x**3)
    yn = (y1,y2,y3)
    COLORS = ('b','g','k')

    for i,y in enumerate(yn):
        ax = fig.add_subplot(len(yn),1,i+1)

        ax.plot(x, y, ls='solid', color=COLORS[i]) 

        if i != len(yn) - 1:
            # all but last 
            ax.set_xticklabels( () )
        else:
            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(14) 
                # specify integer or one of preset strings, e.g.
                #tick.label.set_fontsize('x-small') 
                tick.label.set_rotation('vertical')

    fig.suptitle('Matplotlib xticklabels Example')
    plt.show()

if __name__ == '__main__':
    xticklabels_example()