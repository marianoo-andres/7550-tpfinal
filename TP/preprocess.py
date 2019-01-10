import pandas as pd
import csv
from sklearn.utils import shuffle


def createVolume(dataFrame):
    exportDataframe(dataFrame, "temp.csv")
    file = open("temp.csv")
    reader = csv.reader(file, delimiter=',')
    columns = next(reader)
    xIndex = 0
    yIndex = 0
    zIndex = 0
    for x in range(len(columns)):
        if columns[x] == 'x':
            xIndex = x
        if columns[x] == 'y':
            yIndex = x
        if columns[x] == 'z':
            zIndex = x
    output = open("temp2.csv", "w")
    columns.append("volume")
    output.write(",".join(columns)+"\n")
    for row in reader:
        volume = str(round(float(row[xIndex]) * float(row[yIndex]) * float(row[zIndex]), 2))
        row.append(volume)
        output.write(",".join(row)+"\n")
    output.close()
    file.close()
    dataFrame = pd.read_csv('temp2.csv')
    printColumns(dataFrame)
    return dataFrame.drop('x', axis=1).drop('y', axis=1).drop('z', axis=1)

def printUnique(dataFrame):
    for col in dataFrame:
        print(dataFrame[col].unique())


def printColumns(dataFrame):
    print(dataFrame.columns)


def groupColumnsDataframe(dataFrame):
    colorReplace = {"D": "Colorless", "E": "Colorless", "F": "Colorless", "G": "Not Colorless", "H": "Not Colorless", "I": "Not Colorless", "J": "Not Colorless"}
    dataFrame["color"] = dataFrame["color"].replace(colorReplace)

    clarityReplace = {"IF": "IF", "VVS1": "VVS", "VVS2": "VVS", "VS1": "VS", "VS2": "VS", "SI1": "SI", "SI2": "SI",
                      "I1": "I1"}
    dataFrame["clarity"] = dataFrame["clarity"].replace(clarityReplace)

    #cutReplace = {"Ideal": "Premium", "Premium": "Premium", "Good": "NotPremium", "Very Good": "NotPremium", "Fair": "NotPremium"}
    #dataFrame["cut"] = dataFrame["cut"].replace(cutReplace)

    return dataFrame


def dropUnnecessaryColumns(dataFrame):
    return dataFrame.drop('table', axis=1).drop('depth', axis=1).drop('Unnamed: 0', axis=1)


def exportDataframe(dataFrame, name):
    dataFrame.to_csv(name, sep=",", encoding="utf-8", index=False)


def countXYZWithZeroValue(dataFrame):
    return len(dataFrame[(dataFrame['x'] == 0) | (dataFrame['y'] == 0) | (dataFrame['z'] == 0)])


def eliminateXYZWithZeroValue(dataFrame):
    return dataFrame[(dataFrame[['x', 'y', 'z']] != 0).all(axis=1)]


def eliminateOutliers(dataFrame, includeDepthAndTable=False):
    # Excluimos a price y carat por no tener una distribucion normal
    columns = ["x", "y", "z"]
    if includeDepthAndTable:
        columns.append("depth")
        columns.append("table")
    rowIndeces = []
    for column in columns:
        mean = dataFrame[column].mean()
        std = dataFrame[column].std()
        lower = mean - 3 * std
        upper = mean + 3 * std
        indeces = dataFrame[(dataFrame[column] < lower) | (dataFrame[column] > upper)].index
        for index in indeces:
            if index in rowIndeces:
                continue
            rowIndeces.append(index)
        # print("OUTLIERS IN {}: {}".format(column, str(len(indeces))))
        # print(lower, upper)

    # print("TOTAL UNIQUE OUTLIERS: {}".format(str(len(rowIndeces))))
    dataFrame = dataFrame.drop(rowIndeces)
    return dataFrame


def eliminateDuplicates(dataFrame):
    return dataFrame.drop_duplicates()

def main():
    dataFrame = pd.read_csv("diamonds.csv")

    print("Drop unnecessary columns...")
    dataFrame = dropUnnecessaryColumns(dataFrame)
    print("DATAFRAME COUNT: {}".format(dataFrame["carat"].count()))

    print("Delete duplicates...")
    dataFrame = eliminateDuplicates(dataFrame)
    print("DATAFRAME COUNT: {}".format(dataFrame["carat"].count()))

    print("Eliminate X, Y, Z = 0...")
    dataFrame = eliminateXYZWithZeroValue(dataFrame)
    print("DATAFRAME COUNT: {}".format(dataFrame["carat"].count()))

    print("Eliminate outliers...")
    dataFrame = eliminateOutliers(dataFrame)
    dataFrame = eliminateOutliers(dataFrame)
    print("DATAFRAME COUNT: {}".format(dataFrame["carat"].count()))

    print("Create volume..")
    dataFrame = createVolume(dataFrame)
    print("DATAFRAME COUNT: {}".format(dataFrame["carat"].count()))

    print("Group columns..")
    dataFrame = groupColumnsDataframe(dataFrame)
    print("DATAFRAME COUNT: {}".format(dataFrame["carat"].count()))


    # Discretize numerical variables
    dataFrame["carat"], bins = pd.qcut(dataFrame["carat"], 4, labels=["Low", "Medium", "High", "Very High"], retbins=True)
    print(bins)
    dataFrame["volume"], bins = pd.qcut(dataFrame["volume"], 4, labels=["Low", "Medium", "High", "Very High"], retbins=True)
    print(bins)
    dataFrame["price"], bins = pd.qcut(dataFrame["price"], 4, labels=["Low", "Medium", "High", "Very High"], retbins=True)
    #priceMin = dataFrame["price"].min()
    #priceMax = dataFrame["price"].max()
    #dataFrame["price"], bins = pd.cut(dataFrame["price"], bins=[priceMin, 2500, 7000, 10000, priceMax], labels=["Low", "Medium", "High", "Very High"], retbins=True)
    print(bins)

    # Shuffle dataframe
    dataFrame = shuffle(dataFrame)

    # Change order columns
    dataFrame = dataFrame.reindex(columns=['carat', 'cut', 'color', 'clarity', 'volume', 'price'])

    fileName = "diamonds_processed.csv"


    
    exportDataframe(dataFrame, fileName)


main()
