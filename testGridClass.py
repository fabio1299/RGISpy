#!/usr/bin/python

# Loads a gdbc file into the object of class rgis.grid
# Call testGridClass.py with the following options:
#   -i ./USA_WaterTemp_MonthlyAverages2012.gdbc.gz -V -T


import time
import rgis as rg
import argparse
import random


# For debug purposes, set to True
print_if_flag=True

# We first read the command line arguments and check that we have all the info needed
# to run the routine

parser = argparse.ArgumentParser(description='Tests reading of GDBC files into python',
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-i', '--input',
                    dest='Grid',
                    help="gdbc file",
                    default='./USA_WaterTemp_MonthlyAverages2012.gdbc.gz')

parser.add_argument('-o', '--output',
                    dest='OutFile',
                    help="Out gdbc file",
                    default="./TestOutput.gdbc.gz")

parser.add_argument('-V', '--verbose',
                    dest='print_if_flag',
                    action='store_true',
                    help=    "Prints some debugging info",
                    default=False)

parser.add_argument('-T', '--timeseries',
                    action='store_true',
                    help=    "Define if Grid is timeseries",
                    default=False)

args = parser.parse_args()

# For debug purposes, set the Verbose flag (e.g True)
print_if_flag=args.print_if_flag


print(args)

# Save the start time to monitor how much time it takes...
start_time = time.time()

IsTimeSeries=args.timeseries

# This is where we catually test the grid class
# Initialize the class with:
#       the name of the GDBC file
#       the optional timeseries flag (if odmitted assumed False, dataset is not a time series)
rgGrid = rg.grid(args.Grid,args.timeseries)
# Now we can load the data from gdbc file
rgGrid.Load()

print("--- %s minutes for READ---" % ((time.time() - start_time) / 60))

print('Number of rows {}, cols {}, layers {} and bytes {}'.format(rgGrid.nRows,rgGrid.nCols,rgGrid.nLayers,rgGrid.nByte))

print('LLx {}, LLy {}, URx {} URy {}'.format(rgGrid.LLx,rgGrid.LLy,rgGrid.URx,rgGrid.URy))

print('Grid data shape {}'.format(rgGrid.Data.shape))

print('Grid view as an Xarray')
# Access the data as an Xarray
# ref https://pypi.org/project/xarray/
print(rgGrid.Xarray())

# Change the option below to add a layer to the dataset (can save to the GDBC file)
AddLayer=2

if AddLayer > 0:
    # We Add layers to the dataset before saving it
    CurLayers=rgGrid.nLayers
    print('Adding {} layers'.format(AddLayer))
    NewNames=[]
    for i in range(0,AddLayer):
        NewNames.append(str(i+1))
    if rgGrid.TimeSeries:
        Step='MS'
    else:
        Step=None
    rgGrid.AddLayer(NewNames,AddLayer) #,Step)
    for i in range(CurLayers, rgGrid.nLayers):
        rgGrid.Data[i, :, :] = random.randint(0, 10)

# And finally we save the data to the output GDBC file
print('Saving file {}'.format(args.OutFile))
rgGrid.SaveAs(args.OutFile, rgGrid.Name, 'Out title', True, 'Month', rgGrid.Year, 1)

print("-- %s minutes --" % ((time.time() - start_time) / 60))
