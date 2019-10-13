# pyHole.py

# Imports
import argparse as arg
import src.read as read
#import src.cl_polygon as plg

# Functions
def main(xyzFileName,polygonFileName):
    '''
    pyHole is developed to allow the user to create holes in predefined atomic structures using any closed polygon.
    '''

    # Variables
    rmMasterList = []

    # Read input structure
    molecule = read.read_xyz(xyzFileName)

    # Read polygon vertices
    polygonList = read.read_polygons(polygonFileName)

    # Calculate bounding squares
    for poly in polygonList:
        poly.calc_boundSquare()

    # Determine candidate atoms
    for index,atom in enumerate(molecule.vertList):
        for poly in polygonList:
            poly.calc_candidateAtom(atom,index)

    #print len(polygonList[0].candidateVerts)

    # Determine which atoms must be removed
    for poly in polygonList:
        poly.calc_holes()

        # Create master list of atoms to be removed
        for rmAtom in poly.rmList:
            if (rmAtom not in rmMasterList):
                rmMasterList.append(rmAtom)

    # Sort rmMasterList
    rmMasterList.sort()
    #print len(rmMasterList)

    # Create holes in structure
    delCounter = 0

    for rmAtom in rmMasterList:
        molecule.rm_vertex(rmAtom-delCounter)
        molecule.rm_string(rmAtom-delCounter)
        delCounter += 1

    # Output final structure
    read.write_xyz("hole_"+xyzFileName,molecule)

# Main
if (__name__ == '__main__'):
    # Read command line arguments
    parser = arg.ArgumentParser(description='Create holes in a molecular structure.')

    parser.add_argument('-xyz',
                        '--xyz',
                        type=str,
                        help='Name of xyz file.')

    parser.add_argument('-poly',
                        '--polygon',
                        type=str,
                        help='Name of polygon file.')

    args = parser.parse_args()

    main(args.xyz,args.polygon)
