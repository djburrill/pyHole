# cl_polygon.py

class polygon:
    '''
    Contains methods and containers to operate on and store vertices.
    '''

    # Constructor
    def __init__(self):
        # Initialize variables
        self.vertList = []
        self.strList = []
        self.candidateVerts = {}
        self.boundSquare = []
        self.rmList = []

    def add_vertex(self,vertex):
        '''
        Add vertex.
        '''

        self.vertList.append(vertex)

    def add_string(self,strVal):
        '''
        Add string.

        Strings are used as a means of describing the vertices. Useful for molecules.
        '''

        self.strList.append(strVal)

    def rm_vertex(self,vertIdx):
        '''
        Remove vertex based on index.
        '''

        del self.vertList[vertIdx]

    def rm_string(self,strIdx):
        '''
        Remove string based on index.
        '''

        del self.strList[strIdx]

    def calc_holes(self):
        '''
        Calculate which atoms must be removed by determining if they are inside of the polygon.
        '''

        # Variables
        edge = []
        numVerts = len(self.vertList)

        # Loop over candidate vertices
        for key in self.candidateVerts:
            # Initialize
            atom = self.candidateVerts[key]
            crosses = 0

            # Loop over edges
            for index,vert in enumerate(self.vertList):
                # Initialize switches
                low_Yes = False
                high_Yes = False

                # Determine edge vertices
                if (index == numVerts-1):
                    edge = [vert,self.vertList[0]]
                else:
                    edge = [vert,self.vertList[index+1]]

                # At least one vertex must be to the right of the candidate vertices
                if ((edge[0][0] <= atom[0]) and (edge[1][0] <= atom[0])):
                    continue

                # Check for high value
                if (edge[0][1] > atom[1]) or (edge[1][1] > atom[1]):
                    #print "ATOM: " + str(key) + " | HIGH YES\n"
                    high_Yes = True

                # Check for low value
                if (edge[0][1] <= atom[1]) or (edge[1][1] <= atom[1]):
                    #print "ATOM: " + str(key) + " | LOW YES\n"
                    low_Yes = True

                if (not high_Yes or not low_Yes):
                    continue

                # Compute intersection
                x1 = atom[0]
                x2 = atom[0]+1.0
                x3 = edge[0][0]
                x4 = edge[1][0]

                y1 = atom[1]
                y2 = atom[1]
                y3 = edge[0][1]
                y4 = edge[1][1]

                t1 = (x1*y2-y1*x2)*(x3-x4)
                t2 = (x1-x2)*(x3*y4-y3*x4)
                t3 = (x1-x2)*(y3-y4)
                t4 = (y1-y2)*(x3-x4)

                xCross = (t1-t2)/(t3-t4)

                if (xCross > x1):
                    crosses += 1

            # Check for interior
            #print "\nATOM: " + str(key) + " | CROSSES: " + str(crosses)
            #print atom
            if (crosses%2 == 1):
                self.rmList.append(key)

    def calc_candidateAtom(self,vert,index):
        '''
        Determine if given atom is a candidate atom. If it is, then add it to candidateVerts.
        '''

        # Variables
        x_Yes = False
        y_Yes = False

        # Check X
        if ((vert[0] > self.boundSquare[0]) and (vert[0] < self.boundSquare[2])):
            x_Yes = True

        # Check Y
        if ((vert[1] > self.boundSquare[1]) and (vert[1] < self.boundSquare[3])):
            y_Yes = True

        # Add if within bounds
        if (x_Yes and y_Yes):
            self.candidateVerts[index] = vert

    def calc_boundSquare(self,padding=2.0):
        '''
        Determines a bounding square for the polygon. This helps choose candidate vertices.

        NOTE:
            List returned with format:
                [X_Low,Y_Low,X_High,Y_High]
        '''

        # Variables
        max_X = self.vertList[0][0]
        max_Y = self.vertList[0][1]
        min_X = self.vertList[0][0]
        min_Y = self.vertList[0][1]

        # Find extremes
        for vert in self.vertList:
            # Check X
            if (vert[0] > max_X):
                max_X = vert[0]

            if (vert[0] < min_X):
                min_X = vert[0]

            # Check Y
            if (vert[1] > max_Y):
                max_Y = vert[1]

            if (vert[1] < min_Y):
                min_Y = vert[1]

        # Add padding
        self.boundSquare = [min_X-padding,min_Y-padding,max_X+padding,max_Y+padding]
