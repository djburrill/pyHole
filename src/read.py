# read.py
#
# I/O.

# Imports
import src.cl_polygon as cl_polygon

# Functions
def read_xyz(inFileName):
    '''
    Read XYZ file.
    '''

    # Initialize storage container
    cl_storage = cl_polygon.polygon()

    # Read through file and store atom positions
    with open(inFileName,'r') as inFile:
        for index,line in enumerate(inFile):
            # Format line
            line = line.strip().split()

            # Skip first two lines
            if (index < 2): continue

            # Skip empty lines
            if (len(line) == 0): continue

            # Read atomic position
            cl_storage.add_string(line[0])
            cl_storage.add_vertex([float(line[1]),float(line[2]),float(line[3])])

    return cl_storage

def write_xyz(outFileName,cl_poly):
    '''
    Write xyz file given polygon class (needs string!).
    '''

    # Write XYZ file
    with open(outFileName,'w') as outFile:
        # Write header
        outFile.write(str(len(cl_poly.vertList))+'\n')
        outFile.write("Structure with holes\n")

        for index,atom in enumerate(cl_poly.vertList):
            outString = cl_poly.strList[index]+' '+str(atom[0])+' '+str(atom[1])+' '+str(atom[2])+'\n'
            outFile.write(outString)


def read_polygons(inFileName):
    '''
    Read polygons from file.
    '''

    # Initialize storage container
    polyList = []

    # Read through file and store atom positions
    with open(inFileName,'r') as inFile:
        for index,line in enumerate(inFile):
            # Format line
            line = line.strip().split()

            # Initialize
            if (index == 0):
                cl_storage = cl_polygon.polygon()

            # Empty lines separate polygons
            if (len(line) == 0):
                polyList.append(cl_storage)
                cl_storage = cl_polygon.polygon()
                continue

            # Read atomic position
            cl_storage.add_vertex([float(line[0]),float(line[1]),float(line[2])])

        # Store last polygon
        polyList.append(cl_storage)

    return polyList

# Main
if (__name__ == '__main__'):
    pass
