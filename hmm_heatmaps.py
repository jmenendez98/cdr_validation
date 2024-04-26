import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import argparse

def main():
    # read in the command line inputs
    parser = argparse.ArgumentParser(
        prog='hmm_heatmaps.py',
        description="""Separate candidate CDR containing reads from a bamfile""")

    parser.add_argument("-e", "--emissionMatrix",
                        required=True,
                        metavar="bed file containing estimate CDR Regions",
                        help="bed file containing estimate CDR Regions with chromosome, starting position and ending positon")
    parser.add_argument("-t", "--transitionMatrix",
                        required=True,
                        metavar="bed file containing estimate CDR Transition Regions",
                        help="bed file containing estimate CDR Transitions with chromosome, starting position and ending positon")
    parser.add_argument("-o", "--outputPrefix",
                        required=True,
                        metavar="output prefix",
                        help="The output prefix")
    
    args = parser.parse_args()
    emissionMatrix_path = args.emissionMatrix
    transitionMatrix_path = args.transitionMatrix
    outputPrefix = args.outputPrefix

    # read in the filepaths passed in and open them as numpy matrices
    emissionMatrix = pd.read_csv(emissionMatrix_path, 
                     sep=',', 
                     header=0, 
                     index_col=0)
    transitionMatrix = pd.read_csv(transitionMatrix_path, 
                     sep=',', 
                     header=0, 
                     index_col=0)
    
    '''# setup colors
    mainColors = [ (255, 105, 105), (255, 255, 255) ]
    colorsList = []
    for i in range( len(mainColors)-1 ):
        print('i:', i)
        key = 0
        firstColor, secondColor = mainColors[i], mainColors[i+1]
        r = np.linspace(firstColor[0], secondColor[0], 50, endpoint=True)
        g = np.linspace(firstColor[1], secondColor[1], 50, endpoint=True)
        b = np.linspace(firstColor[2], secondColor[2], 50, endpoint=True)

        [ colorsList.append( (round(r[j], 1), round(g[j], 1), round(b[j], 1)) ) for j in range(50) ]

        #colorsList.append( (r, g, b) )

    print('colorsList: ', colorsList)

    cmap = colors.ListedColormap(colorsList)'''

    ########################################
    ### make the emission matrix heatmap ###
    ########################################
    print( emissionMatrix )
    #print( emissionMatrix.values )
    #print( emissionMatrix.shape )

    # Plot the heatmap with custom colors and annotations
    plt.imshow(emissionMatrix.values, cmap="Reds", vmin=0,
           vmax=1, extent=[0, emissionMatrix.shape[1], 0, emissionMatrix.shape[0]])
    
    reversed_eMatrix = np.flip(emissionMatrix.values, axis=0)
    for y in range( emissionMatrix.shape[0] ): 
        for x in range( emissionMatrix.shape[1] ): 
            plt.annotate(str(round(reversed_eMatrix[y, x], 8)), xy=(x+0.5, y+0.5), 
                        ha='center', va='center', color='black', fontsize=8)

    # Add colorbar 
    cbar = plt.colorbar(ticks=[0, 0.25, 0.5, 0.75, 1], shrink=0.5) 
    cbar.ax.set_yticklabels(['0', '0.25', '0.5', '0.75', '1'])

    # Set plot title and axis labels 
    emissionMatrixTitle = "Emission Matrix"
    plt.title(emissionMatrixTitle) 
    plt.xlabel("Hidden State") 
    plt.ylabel("Emission")
    plt.tick_params(top=False, labeltop=True, 
                    bottom=False, labelbottom=False,
                    left=False, labelleft=True)
    plt.xticks([0.5, 1.5, 2.5], ['A', 'B', 'C'])
    plt.yticks([0.5, 1.5, 2.5, 3.5], ['w', 'x', 'y', 'z'])

    # Display the plot
    emissionMatrixHeatmap = outputPrefix + '.emissionMatrixHeatmap.png'
    plt.savefig(emissionMatrixHeatmap)
    plt.clf()

    ##########################################
    ### make the transition matrix heatmap ###
    ##########################################
    print( transitionMatrix )
    #print( transitionMatrix.values )

    # Plot the heatmap with custom colors and annotations
    plt.imshow(transitionMatrix.values, cmap="Reds", vmin=0,
           vmax=1, extent=[0, transitionMatrix.shape[1], 0, transitionMatrix.shape[0]])
    
    reversed_tMatrix = np.flip(transitionMatrix.values, axis=0)
    for i in range( transitionMatrix.shape[0] ): 
        for j in range( transitionMatrix.shape[1] ): 
            plt.annotate(str(round(reversed_tMatrix[i, j], 8)), xy=(j+0.5, i+0.5), 
                        ha='center', va='center', color='black', fontsize=8)

    # Add colorbar 
    cbar = plt.colorbar(ticks=[0, 0.25, 0.5, 0.75, 1], shrink=0.5) 
    cbar.ax.set_yticklabels(['0', '0.25', '0.5', '0.75', '1'])

    # Set plot title and axis labels 
    transitionMatrixTitle = "Transition Matrix"
    plt.title(transitionMatrixTitle) 
    plt.xlabel("From Hidden State") 
    plt.ylabel("To Hidden State")
    plt.tick_params(top=False, labeltop=True, 
                    bottom=False, labelbottom=False,
                    left=False, labelleft=True)
    plt.xticks([0.5, 1.5, 2.5], ['A', 'B', 'C'])
    plt.yticks([0.5, 1.5, 2.5], ['C', 'B', 'A'])

    # Display the plot 
    transitionMatrixHeatmap = outputPrefix + '.transitionMatrixHeatmap.png'
    plt.savefig(transitionMatrixHeatmap)
    plt.clf()

if __name__ == '__main__':
    main()
