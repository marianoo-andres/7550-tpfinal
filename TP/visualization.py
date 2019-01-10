import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plotHist(dataFrame):
	fig = dataFrame["price"].hist(bins=15,
	                 color='steelblue',
	                 edgecolor='black', linewidth=1.0,
	                 xlabelsize=10, ylabelsize=10,
	                 xrot=0, yrot=0,figsize=(10,10),
	                 grid=False)

	fig.set_title('Histograma Price', fontsize=16)
	fig.set_xlabel('price')
	fig.set_ylabel('Cantidad')
	plt.tight_layout()
	plt.savefig('Histogram_price.png')

def jointPlot(dataFrame):
	h = sns.jointplot(x='volume', y='price', data=dataFrame, size=10)
	h.set_axis_labels('Volume', 'Price', fontsize=16)
	plt.tight_layout()
	plt.savefig('Jointplot_volume-price.png')

def countPlot(dataFrame):
	h = sns.countplot(x='clarity', data=dataFrame, order=['IF','VVS','VS','SI','I1'])
	plt.title('Clarity Grouped counts')
	plt.xlabel('Clarity')
	plt.ylabel('Count')
	plt.tight_layout()
	plt.savefig('factorPlot_clarityGrouped.png')

dataFrame = pd.read_csv("diamonds_processed.csv")
jointPlot(dataFrame)


