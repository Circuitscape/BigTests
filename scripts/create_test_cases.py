# Author: Brad McRae

"""Creates test resistance grids with resistances that vary from 1 to 10^mag,
where mag is defined by user. Upper left quadrant varies from 10^(mag-1) to 10^mag.
Lower right quadrant varies from 1 to 10. Rest of grid varies from 1 to 10^mag.
Horizontal and vertical bands with resistances of 1 and 10^mag are inserted.
A point file is also produced. Points 1 and 2 are along a band with r=1, spaced 
two cells apart.

"""
from numpy import *
import os, gzip

############## User settings #################################
nrows = 11 # at least 11
ncols = 11 # at least 11
mag = 15 # order of magnitude variation. Resistances will vary from 1 to 10^mag
outputFolder = "c:\\temp\\cs\\"
add_structure = True # Adds vertical and horizontal bands with max and min resistance values to give structure to grid
compress = True # Compress to gzip format
#############################################################

# Files to be written with this path and prefix:
fileBase = outputFolder + str(nrows) + 'x' + str(ncols)+'mag'+str(mag)

def writer(file, data, state, compress):    
    outputBase, outputExtension = os.path.splitext(file) 
           
    f = False
    if compress == True:
        file = file + '.gz'
        f = gzip.open(file, 'w')
    else:
        f = open(file, 'w')

    f.write('ncols         ' + str(state['ncols']) + '\n')
    f.write('nrows         ' + str(state['nrows']) + '\n')
    f.write('xllcorner     ' + str(state['xllcorner']) + '\n')
    f.write('yllcorner     ' + str(state['yllcorner']) + '\n')
    f.write('cellsize      ' + str(state['cellsize']) + '\n')
    f.write('NODATA_value  ' + str(state['nodata']) + '\n')
    
    delimiter = ''
    # fmt = ['%.6f ']*state['ncols'] 
    fmt = ['%d ']*state['ncols'] 
    format = delimiter.join(fmt)
    for row in data:
        f.write(format % tuple(row) + '\n')

    f.close()

print 'Magnitude:',mag
print'nrows = ',ncols
print'ncols = ',ncols,'\n'

a = 1
b = 10
N = 100 # Number of integers
test = a + (b - a) * (random.random_integers(N, size = (nrows,ncols)) - 1) / (N - 1.)
test = random.random_integers(1,10, size = (nrows,ncols)) 
test = test.astype('float64')
resistances = power(test,mag).astype('int64')
middlecol = int(ncols/2)
middlerow = int(nrows/2)


print 'Min, max values:'
print amin(resistances),',',amax(resistances)

middlecol = int(ncols/2)
middlerow = int(nrows/2)

if add_structure:
    maxVal = math.pow(10,mag)
    #Set lower right quadrant to low random numbers (1-10)
    resistances[middlerow :,middlecol :] = test[middlerow :,middlecol :]
    #set upper left quadrant to high random numbers (10^mag-1 - 10^mag)
    resistances[0:middlerow,0:middlecol] = math.pow(10,mag-1)*(test[0:middlerow,0:middlecol])
    # Vertical strips with min and max vals
    resistances[:,middlecol] = 1
    resistances[:,middlecol-1] = maxVal
    # Horizontal strips with min and max vals
    resistances[middlerow,:] = maxVal
    resistances[middlerow-3,:] = 1
    # resistances[0:5,0:5] = 1
    # resistances[nrows-5:nrows,ncols-5:ncols] = maxVal
state = {}
options = {}
state['ncols'] = ncols
state['nrows'] = nrows
state['xllcorner'] = 0
state['yllcorner'] = 0
state['cellsize'] = 1
state['nodata'] = -9999            

# Create points file
# x1, x4 are along band of 1's, separated by 6 cells
# Points 1 and 2 are on line of 1's separted by 2 spaces
c1=middlecol-5
r1=middlerow-3
c2 = middlecol-3
r2=middlerow-3
c3=middlecol+3
r3=middlerow-3
c4=middlecol+3
r4=middlerow+3
c5=middlecol-3
r5=middlerow+3
c6 = 1
r6 = 1
c7=ncols-2
r7=1
c8=ncols-2
r8 = nrows-2
c9=1
r9=nrows-2

points =  -9999 + zeros((nrows,ncols),dtype='int32')
points[r1,c1]=1
points[r2,c2]=2
points[r3,c3]=3
points[r4,c4]=4
points[r5,c5]=5
points[r6,c6]=6
points[r7,c7]=7
points[r8,c8]=8
points[r9,c9]=9

if compress:
    suffix = '.gz' 
else:
    suffix = ''

resistFile = fileBase + 'resist.asc'
print 'writing ',resistFile + suffix
writer(resistFile, resistances, state, compress)

pointFile = fileBase + 'points.asc'
print 'writing ',pointFile + suffix
writer(pointFile, points, state, compress)


