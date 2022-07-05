import sys
import copy

import base
import numpy as np

from draw import Drawer

#Global Functions----------------------------------------------
def coordsToArray(coordslist, height, width):
    a= np.zeros((height, width), dtype='i')
    for cell in coordslist:
        a[ cell[0] ][ cell[1] ]=1
    return a

def toOriginUniversal(coordslist):
        rows=[]
        cols=[]
        for i in coordslist:
            rows.append(i[0])
        for j in coordslist:
            cols.append(j[1])
        rowdif=0-min(rows)
        coldif=0-min(cols)
        vyska=max(rows)-min(rows)+1
        sirka=max(cols)-min(cols)+1
        moved=[[], [ [ k[0]+rowdif, k[1]+coldif ] for k in coordslist], [sirka, vyska] ]
        return moved

def dict_print(slovnik):
    for key, value in slovnik.items() :
                    print('key:', key)
                    print('value:')
                    print(value)

#returns rotated coordslist, cnt= number of 90degree rotations
def rotateStone(coords, cnt):
    rotatedStone=[]
    if cnt==0:
        return coords
    elif cnt==1:
        for block in coords:
            rotatedStone.append([-1*block[1], block[0]])
    elif cnt==2:
        for block in coords:
            rotatedStone.append([-1*block[0], -1*block[1]])
    elif cnt==3:
        for block in coords:
            rotatedStone.append([block[1], -1*block[0]])

    rotatedStone= toOriginUniversal(rotatedStone)
    return rotatedStone

def FindIndexBasedOnColour(winner, ava, f_colours):
    for i in range( len(ava[winner][1]) ):
        if ava[winner][1][i][1] not in f_colours:
            return ava[winner][1][i][0]

def ArrayToCoordslist(a):
    coordslist=[]
    for i in range( len(a)):
        for j in range( len(a[0])):
            if a[i][j]==1:
                coordslist.append([i, j])
    return coordslist
#--------------------------------------------------------------

class Player(base.BasePlayer):
    def __init__(self, name, board, marks, stones, player):
        """ constructor of Player. Place you variables here with prefix 'self' -> e.g. 'self.myVariable' """
        self.diffrow=[0, 1, 0, -1]
        self.diffcol=[1, 0, -1 ,0]
        self.diagdiffrow=[-1, 1, 1, -1]
        self.diagdiffcol=[1, 1, -1, -1]

        base.BasePlayer.__init__(self, name, board, marks, stones, player)  #do not change this line!!
        self.algorithm = "Velky Bulo 3.0"  #name of your method. Will be used in tournament mode

    #check if there are any stones left
    def freeStonesCheck(self):
        for el in self.freeStones:
            if el==True:
                return True
        return False
    
    #moves ONE stone to coords in the origin
    def toOrigin(self, stone):
        rows=[]
        cols=[]
        for i in stone[1]:
            rows.append(i[0])
        for j in stone[1]:
            cols.append(j[1])
        rowdif=0-min(rows)
        coldif=0-min(cols)
        vyska=max(rows)-min(rows)+1
        sirka=max(cols)-min(cols)+1
        movedStone=[stone[0], [ [ k[0]+rowdif, k[1]+coldif ] for k in stone[1]], [sirka, vyska] ]
        return movedStone

    #returns *orderedStones* which is a list of stones(with coords in the origin) and orderes them, based on parameter
    #also returns *reordIndexes* which is a list of stones indexes where position of index corresponds to position of stone in *orderedStones*
    def orderedStones(self, stones, parameter):
        orderedStones=[]
        cnt=0
        for kamen in stones:
            coords=kamen[1]
            rows=[]
            cols=[]
            for i in coords:
                rows.append(i[0])
            for j in coords:
                cols.append(j[1])
            rowdif=0-min(rows)
            coldif=0-min(cols)
            vyska=max(rows)-min(rows)+1
            sirka=max(cols)-min(cols)+1
            movedStone=[kamen[0], [ [ k[0]+rowdif, k[1]+coldif ] for k in coords], [sirka, vyska], cnt ]
            orderedStones.append(movedStone)
            cnt+=1
        orderedStones.sort(key=lambda x: x[2][parameter], reverse=True)
        reordIndexes= [ i[3] for i in orderedStones ]
        orderedStones= [ i[:3] for i in orderedStones ]
        return orderedStones, reordIndexes

    #
    def longestSequence(self, direction, ind):
        if direction=='h':
            longest=0
            longest_sequence_start=[1,1]
            for s in range(len(self.marks[ind])):
                length_cnt=0
                current= self.marks[ind][s]
                acc=0
                while current== self.player:
                    length_cnt+=1
                    acc+=1
                    if s+acc> ( len(self.marks[ind]) -1):
                        break
                    current= self.marks[ind][s+acc]
                if length_cnt> longest:
                    longest= length_cnt
                    longest_sequence_start=[ind, s]
            return longest, 0, longest_sequence_start, ind                      # 0 je 'h'

        elif direction=='v':
            longest=0
            longest_sequence_start=[1,1]
            for r in range(len(self.marks)):
                length_cnt=0
                current= self.marks[r][ind]
                acc=0
                while current== self.player:
                    length_cnt+=1
                    acc+=1
                    if r+acc> ( len(self.marks) -1):
                        break
                    current= self.marks[r+acc][ind]
                if length_cnt> longest:
                    longest= length_cnt
                    longest_sequence_start=[r, ind]
            return longest, 1 , longest_sequence_start, ind                     # 1 je 'v'

    #move stone to ROW, COL so that FIRST coord of stone lies on ROW, COL 
    def moveTo(self, stone, row, col):
        movedStone=[]
        print('moveTo stone[1]', stone[1])
        coordlist=sorted(stone[1], key=lambda x:x[0])
        coordlist=sorted(stone[1], key=lambda x:x[1])
        print('moveto coordslist', coordlist)

        rowdiff= row- coordlist[0][0]
        coldiff= col- coordlist[0][1]
        for cell in coordlist:
            movedStone.append( [cell[0]+ rowdiff, cell[1]+ coldiff] )

        #very long and bad testing whether the moved Stone is or isnt in Board 
        rows, cols= [], []
        for i in movedStone:
            if i[0] <0:
                rows.append(i[0])
            if i[1]<0:
                cols.append(i[1])

        if rows:
            offset= min(rows)
            movedStone= [ [ i[0]-offset, i[1]  ] for i in movedStone ]
        if cols:
            offset=min(cols)
            movedStone= [ [i[0], i[1]-offset ] for i in movedStone]

        size= len(self.board)-1
        rows, cols= [], []
        for i in movedStone:
            if i[0] > size:
                rows.append(i[0])
            if i[1]> size:
                cols.append(i[1])

        if rows:
            offset= max(rows) - size
            movedStone= [ [ i[0]-offset, i[1]  ] for i in movedStone ]
        if cols:
            offset=max(cols) - size
            movedStone= [ [i[0], i[1]-offset ] for i in movedStone]

        movedStone=[stone[0], movedStone, stone[2]]       
        return movedStone

    #returns list of all adjacent tiles AND list of those adj tiles which have enemy mark on them (=enemyTiles) 
    def adjacent(self):
        #check how many nonzero tiles there are on the board
        '''
        nonzeroAmount=0
        for i in range( len(self.freeStones)):
            if self.freeStones[i]==False:
                nonzeroAmount+= len( self.stones[i][1] )
        '''
        #find out which tiles are nonzero
        nonzeroTiles=[]
        for r in range( len(self.board)):                                          
            for s in range( len(self.board)):
                if self.board[r][s]!=0:
                    nonzeroTiles.append([r,s])
        
        #create list of all empty adjacent tiles
        adjTiles=[]
        for tile in nonzeroTiles:
            for i in range(4):
                tilediff= [ tile[0]+self.diffrow[i], tile[1]+self.diffcol[i]]
                if (self.inBoard(tilediff[0], tilediff[1]) ) and ( self.board[ tilediff[0] ][ tilediff[1] ]==0 ) and ( tilediff not in adjTiles):           #3. podmienka dost zdlhava
                    adjTiles.append( tilediff )

        
        #create list of adjtiles which have enemy mark on them
        enemyTiles=[t for t in adjTiles if ( self.marks[t[0]][t[1]]==-self.player ) ]

        return adjTiles, enemyTiles

    #returns list of all tiles that are in close proximity to friendly tiles (=defTiles)
    def closeToFriendly(self, adjtiles):
        defTiles=[]
        for tile in adjtiles:
            if self.marks[ tile[0] ][ tile[1] ]== self.player:
                defTiles.append(tile) 
        
        return defTiles

    #return list of forbidden colours...
    def forb_colours(self, stone):
        forbidden_colours=[]
        for cell in stone:
            for i in range(4):
                searchTile= [ cell[0]+ self.diffrow[i], cell[1]+ self.diffcol[i] ]
                if self.inBoard( searchTile[0], searchTile[1] ) and (self.board[ searchTile[0] ][ searchTile[1] ]  != 0 ):
                    forbidden_colours.append(self.board[ searchTile[0] ][ searchTile[1] ])
        
        return forbidden_colours
 
    #returns TRUE if 
    # - there is no such a stone in availableShapes
    # - or the given stone can be placed without problems
    def colourRule(self, newcoordslist, newshape, availableShapes):
        if newshape not in availableShapes:
            return True
        else:
            adjTiles=[]
            for tile in newcoordslist:
                for i in range(4):
                    tilediff= [ tile[0]+self.diffrow[i], tile[1]+self.diffcol[i]]
                    if (self.inBoard(tilediff[0], tilediff[1]) ) and ( tilediff not in adjTiles):           #2. podmienka dost zdlhava
                        adjTiles.append( tilediff )

            forb_colours=[]
            for tile in adjTiles:
                farba= self.board[ tile[0] ][ tile[1] ]
                if (farba != 0) and (farba not in forb_colours):
                    forb_colours.append(farba)

            for i in range( len(availableShapes[newshape][1]) ):
                if availableShapes[newshape][1][i][1] not in forb_colours:
                    return True

        return False

    def colourRule2(self, stone, idx):
        adjTiles=[]
        for tile in stone:
            for i in range(4):
                tilediff= [ tile[0]+self.diffrow[i], tile[1]+self.diffcol[i]]
                if (self.inBoard(tilediff[0], tilediff[1]) ) and ( tilediff not in adjTiles):           #2. podmienka dost zdlhava
                    adjTiles.append( tilediff )

        forb_colours=[]
        for tile in adjTiles:
            farba= self.board[ tile[0] ][ tile[1] ]
            if (farba != 0) and (farba not in forb_colours):
                forb_colours.append(farba)

        stonecolour= self.stones[idx][0]
        if stonecolour not in forb_colours:
            return True
        else:
            return False

    #returns True if stone is touching at least one other stone
    def isTouching(self, stone):
        for tile in stone:
            for i in range(4):
                tilediff= [ tile[0]+self.diffrow[i], tile[1]+self.diffcol[i]]
                if (self.inBoard(tilediff[0], tilediff[1]) ) and (tilediff not in stone) and ( self.board[ tilediff[0] ][ tilediff[1] ] != 0 ):
                    return True
        return False

    #returns dictionary of all avalaible stone shapes (+ their rotated versions) in form of numpy arrays
    def stoneTypes_np(self):
        availableShapes={}
        orderedStones, reordIndexes= self.orderedStones(self.stones,0)
        cnt=0
        for stone in orderedStones:
            if self.freeStones[ reordIndexes[cnt] ]==True:
                a= coordsToArray(stone[1], stone[2][1], stone[2][0])
                a_string=str(a.tolist())
                if a_string in availableShapes.keys():
                    availableShapes[a_string][1].append( (reordIndexes[cnt], stone[0]) )
                else:
                    availableShapes[a_string]= [a, [ (reordIndexes[cnt], stone[0]) ], 0 ]
            cnt+=1

        rotated={}
        for key, value in availableShapes.items() :
            for i in range(3):
                a_rot= np.rot90(value[0], i+1, (0,1))
                a_rot_string= str(a_rot.tolist())
                
                if a_rot_string in rotated.keys():
                    continue
                else:
                    rotated[a_rot_string]= [a_rot, value[1], i]
        
        availableShapes.update(rotated)
        return availableShapes

    #INPUT: any coordslist
    #RETURNS numpy array of given shape
    def shapeArray(self, coordslist):
        movedCoordsList= toOriginUniversal( coordslist )
        return coordsToArray( movedCoordsList[1], movedCoordsList[2][1], movedCoordsList[2][0] )

    #return TRUE if there will not be a problem with the 2x2 rule, otherwise FALSE
    #INPUTS:
    # tile= tile to test 2x2 rule legality
    # coordsliost= list of coords that are not on board YET, but they are a part of the new shape 
    def twoxtwo(self, tile, coordslist):
        boollist=[]
        for i in range(4):
            adjtile= [ tile[0]+ self.diffrow[i], tile[1] + self.diffcol[i] ]
            if not boollist:
                if (self.inBoard( adjtile[0], adjtile[1]) ) and ( (self.board[ adjtile[0] ][ adjtile[1] ]  != 0 ) or (adjtile in coordslist) ):
                    boollist.append(True)
                else:
                    boollist.append(False)

            elif self.inBoard( adjtile[0], adjtile[1]):
                if ( (adjtile in coordslist) or ( self.board[ adjtile[0] ][ adjtile[1] ]  != 0  ) ) and ( boollist[-1]==True ) :
                    diagtile= [tile[0] + self.diagdiffrow[i], tile[1] + self.diagdiffcol[i]]
                    if ( self.board[ diagtile[0] ][ diagtile[1] ]  != 0) or ( diagtile in coordslist):
                        return False
                elif ( self.board[ adjtile[0] ][ adjtile[1] ]  != 0  ) or (adjtile in coordslist): 
                    boollist.append(True)
                else:
                    boollist.append(False)
            
            else:
                boollist.append(False)

        if boollist[0] and boollist[-1]:
            diagtile= [tile[0] -1, tile[1] + 1]
            if ( self.board[ diagtile[0] ][ diagtile[1] ]  != 0) or ( diagtile in coordslist):
                return False
        
        return True

    #returns:
    #newshapes= List, in it there are np_arrays IN FORM OF STRINGS, will be used as KEYS in *isInOpen*
    #newcoordslists= List, in it there are lists of coords, will be used as VALUES in *isInOpen*
    def expand(self, coordslist):
        newcoordslists=[]
        newshapes=[]
        scorelist=[]
        for coord in coordslist:
            for i in range(4):
                tile= [ coord[0] + self.diffrow[i], coord[1]+ self.diffcol[i] ]
                if ( self.inBoard( tile[0], tile[1] ) ):
                    if (tile in coordslist) or (self.board[ tile[0] ][ tile[1] ] != 0):
                        continue
                    elif self.twoxtwo(tile, coordslist[:]) :
                        child= coordslist[:]       #coordslist is its parent
                        child.append(tile)

                        newcoordslists.append(child)
                        scorelist.append(self.shapeScore(child))
                        newshapes.append( str( self.shapeArray(child).tolist() ) ) 
                    else:
                        continue
                else:
                    continue
        return newshapes, newcoordslists, scorelist

    #returns intersection, but that intersection can be empty
    def BFS_from_one_coord(self, intersection_, availableShapes, isInOpen, BFSstart):              
        if self.twoxtwo(BFSstart, []):
            openList=  [[BFSstart]] 
            stop_cnt=0
            while (len(intersection_)==0 and stop_cnt<40) or (stop_cnt<40):
                #print(stop_cnt)
                
                if not openList:        #if openList is empty
                    return set()
                
                actual= openList.pop(0)
                
                newshapes, newcoordslists, scorelist = self.expand(actual) 

                for i in range( len(newshapes) ):
                    openList.append(newcoordslists[i])
                    if (not newshapes[i] in isInOpen) and self.colourRule(newcoordslists[i], newshapes[i], availableShapes):
                        isInOpen[newshapes[i]]= [newcoordslists[i], scorelist[i] ]
                        
                        
                intersection_= set( availableShapes.keys() ) & set( isInOpen.keys() )
                stop_cnt+=1
            return intersection_
        else:
            return set()

    #returns the first valid of stone in its argument
    def ValidPosition(self, stone, idx):     #stone=coordslist
       rows=  [i[0] for i in stone]
       cols= [i[1] for i in stone]
       vyska=max(rows)-min(rows)+1
       sirka=max(cols)-min(cols)+1
       for i in range( len(self.board) - vyska +1 ):
           for j in range( len(self.board[0]) - sirka +1):
               movedStone=[]
               break_cond=False
               for tile in stone:
                    mtile=[tile[0] + i, tile[1]+j ]
                    if ( self.inBoard(mtile[0], mtile[1]) ) and (self.board[ mtile[0] ][ mtile[1] ] ==0) and ( self.twoxtwo(mtile, movedStone) ): 
                        movedStone.append( mtile )
                    else:
                        break_cond= True
                        break
               if break_cond==True:
                   continue
               #but we have to check a)whether stone is touching something, b)the colour rule
               else:
                   if self.isTouching(movedStone) and self.colourRule2(movedStone, idx):
                       skore= self.shapeScore(movedStone)
                       if skore<0:
                           badPositions.append([idx, movedStone])
                           continue
                       
                       return movedStone
                   else:
                       continue
       return None 

    def shapeScore(self, stone):      #stone=coordslist
        score=0
        for tile in stone:
            if self.marks[ tile[0] ][ tile[1] ] == -self.player:
                score+=1
            elif self.marks[ tile[0] ][ tile[1] ] == self.player:
                score-=2
        
        edgeAdjTiles=[]
        
        for tile in stone:
            for i in range(4):
                tilediff= [ tile[0]+self.diffrow[i], tile[1]+self.diffcol[i]]
                tilediff2= [ tilediff[0]+self.diffrow[i], tilediff[1]+self.diffcol[i]]
                if (self.inBoard(tilediff[0], tilediff[1]) ) and ( self.board[ tilediff[0] ][ tilediff[1] ]==0 ) and ( tilediff not in edgeAdjTiles) and (tilediff not in stone) and ( not self.inBoard(tilediff2[0], tilediff2[1]) ) :           #3. podmienka dost zdlhava
                    edgeAdjTiles.append( tilediff )

        #if edgeAdjTiles:
            #print('edgeAdjTiles',edgeAdjTiles)
        for tile in edgeAdjTiles:
            if self.marks[ tile[0] ][ tile[1] ] == self.player:
                score+=4

        return score

    def move(self):
        if self.isEmpty():
            print('self.player',self.player)
                        
            board_size= len(self.board)-1

            res= [ self.longestSequence('h',0), self.longestSequence('h',board_size), self.longestSequence('v',0), self.longestSequence('v',board_size)  ]
            result= max(res, key=lambda x: x[0])

            ordered_h, indexes_h = self.orderedStones(self.stones, 0)
            ordered_v, indexes_v = self.orderedStones(self.stones, 1)

            if ordered_h[0][2][0] > ordered_v[0][2][0]:
                biggger_orientation= 0
            elif ordered_h[0][2][0] < ordered_v[0][2][0]:
                biggger_orientation= 1
            elif ordered_h[0][2][0] == ordered_v[0][2][0]:
                biggger_orientation= result[1]

            #there is no need to rotate
            if biggger_orientation == result[1]:       
                if result[1]==0:
                    biggest= ordered_h[0]
                    biggestId= indexes_h[0]
                else:
                    biggest= ordered_v[0]
                    biggestId= indexes_v[0]
            
            #rotation is needed
            else:
                if biggger_orientation==0:
                    biggestId= indexes_h[0]
                    biggest= rotateStone(ordered_h[0][1], 1)
                else:
                    biggestId= indexes_v[0]
                    if result[3]==0:
                        biggest= rotateStone(ordered_v[0][1], 1)
                    else:
                        biggest= rotateStone(ordered_v[0][1], 3)


            if result[1]==0 and result[3]==0:
                moved= self.moveTo(biggest, result[2][0]+1, result[2][1])
            elif result[1]==0 and result[3]==board_size:
                moved= self.moveTo(biggest, result[2][0]-1, result[2][1])
            elif result[1]==1 and result[3]==0:
                moved= self.moveTo(biggest, result[2][0], result[2][1]+1)
            else:
                moved= self.moveTo(biggest, result[2][0], result[2][1]-1)

            print('-------------------------------------------------------------------------------------------')
            return [biggestId, moved[1]]
        
        elif self.freeStonesCheck():
            global badPositions
            badPositions=[]

            #1.) create availableShapes dict
            availableShapes= self.stoneTypes_np()
        
            #2.) create list of enemy tiles OR deftiles
            adjTiles, enemyTiles= self.adjacent()
            #defTiles=self.closeToFriendly(adjTiles)
            print('self.player',self.player)
            #print('AdjTiles',adjTiles)
            print('Enemytiles', enemyTiles)

            for tile in enemyTiles:
                adjTiles.remove(tile)

            #3.) isInOpen, jeho expandovanie
            isInOpen = {}
            intersection= set()
            determiner=''
                       
            #try enemyTiles
            if enemyTiles:
                cnt=0
                while enemyTiles and cnt<50:
                    BFSstart=enemyTiles.pop()
                    intersection= intersection | self.BFS_from_one_coord( {}, availableShapes, isInOpen, BFSstart )
                    cnt+=1
            else:
                determiner+='neboli ziadne enemyTiles, '

            '''
            #try defTiles
            if defTiles:
                cnt2=0
                while intersection== set() or cnt2 <10:
                    if intersection != set():
                        cnt2+=1
                    if len(defTiles)==0:
                        determiner+='deftiles sa vyprazdnilo, '
                        break
                    BFSstart=defTiles.pop()
                    intersection= intersection | self.BFS_from_one_coord( {}, availableShapes, isInOpen, BFSstart )
            else:
                determiner+='neboli ziadne defTiles, '
            '''

            cnt2=0
            usedAdj=[]
            while adjTiles and cnt2<40:
                BFSstart=adjTiles.pop()
                usedAdj.append(BFSstart)
                intersection= intersection | self.BFS_from_one_coord( {}, availableShapes, isInOpen, BFSstart )
                cnt2+=1

            print('usedAdj', usedAdj)
            '''
            allscores=[]
            for shape in intersection:
                allscores.append(isInOpen[shape][1])
            print('max skore', max(allscores))
            '''

            if intersection:
                bestScore=-100
                for shape in intersection:
                    if isInOpen[shape][1]> bestScore:
                        winner= shape
                        bestScore= isInOpen[shape][1]


            #if nothing is found through enemytiles and deftiles, just throw there something
            if intersection==set(): #or (bestScore<0):
                determiner+='zacalo sa tupe prehladavanie'
                print(determiner)
                freeIndexes= []
                for i in range( len(self.freeStones)):
                    if self.freeStones[i]==True:
                        freeIndexes.append(i)
        

                for idx in freeIndexes:
                    shapes=[]
                    avalist=list(availableShapes.items())
                    
                    for i in range( len( avalist)):
                        for j in range( len(avalist[i][1][1] )):
                            tempIndex= avalist[i][1][1][j][0]
                            if tempIndex == idx:
                                shapes.append(avalist[i][1][0])

                    coordslists= [ ArrayToCoordslist(a) for a in shapes ]
                    for stone in coordslists:
                        position= self.ValidPosition(stone, idx)
                        if position==None:
                            continue
                        else:
                            print('Pokladam:')
                            print(position )
                            print('farba',self.stones[idx][0])
                            print('determiner',determiner)
                            print('-------------------------------------------------------------------------------------------')
                            return [idx, position]

                    if position==None:
                        continue


            #4.) Try to pick something from intersection and place it
            if intersection:

                print('voslo do do 4.)')

                forbidden_colours= self.forb_colours(isInOpen[winner][0])
                print('forbidden_colours',forbidden_colours)
                index= FindIndexBasedOnColour(winner, availableShapes, forbidden_colours)  

                print('Pokladam:')
                print(availableShapes[winner][0])
                print('so skore', isInOpen[ winner ][1])
                print('na', BFSstart)
                print('determiner',determiner)
                print('do returnu vchadza', [index , isInOpen[ winner ][0] ])
                print('-------------------------------------------------------------------------------------------')

                return [index , isInOpen[ winner ][0] ]
            else:            
                #now check badpositions:
                if badPositions:
                    print('return z badPositions', badPositions[0])
                    print('-------------------------------------------------------------------------------------------')
                    return badPositions.pop()
                else: 
                    print('-------------------------------------------------------------------------------------------')           
                    return []
            
        else:
            print('-------------------------------------------------------------------------------------------')
            return []


if __name__ == "__main__":

    #load stones from file
    stones = base.loadStones("stones3.txt")
    #stones=[[1, [[-6, 4], [-5, 4], [-5, 3], [-5, 5], [-4, 4]]], [3, [[13, -4], [13, -3], [13, -5], [13, -2]]], [1, [[15, -1], [15, 0], [15, -2]]], [1, [[-10, -8], [-10, -9], [-10, -7], [-9, -7]]], [2, [[-11, 10], [-11, 9], [-11, 8], [-10, 9]]], [3, [[-9, 1], [-8, 1], [-9, 0], [-9, -1], [-8, -1]]], [1, [[14, 12], [14, 11], [15, 12]]], [3, [[9, 13], [9, 12], [9, 14], [10, 14]]], [2, [[13, -15], [13, -16], [13, -14], [14, -14]]], [1, [[-12, 7], [-12, 6], [-12, 5], [-11, 6]]], [3, [[13, 10], [13, 9], [13, 8], [14, 9]]], [3, [[2, 3], [3, 3], [3, 2], [3, 4], [4, 3]]], [2, [[-4, -4], [-4, -5], [-4, -6], [-3, -5], [-2, -5]]]]
    print("stones are", stones)

    #prepare board and marks
    board, marks = base.makeBoard10();
    #board=[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 1, 1, 0], [0, 1, 0, 0, 0, 1, 0], [1, 1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    #marks=[[1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0], [-1, -1, -1, -1, -1, -1, -1], [0, 0, 0, 0, 0, 0, 0], [-1, -1, -1, -1, -1, -1, -1], [0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1]]

    #create both players    
    p1 = Player("pepa", board, marks, stones, -1)
    p2 = Player("franta", board, marks, stones, 1)  

    #not necessary, only if you want to draw board to png files
    d = Drawer()
    d.draw(p1.board, p1.marks, "init.png");

    moveidx = 0
    while True:
        p1play = True
        p2play = True

        m = p1.move()  #first player, we assume that a corrent output is returned

        #the following if/else is simplified. On Brute, we will check if return value
        #from move() is valid ...
        if len(m) == 0:
            p1play = False
        else:
            stoneIdx, stone = m
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor) #write stone to player1's board
            base.writeBoard(p2.board, stone, stoneColor) #write stone to player2's board
            p1.freeStones[ stoneIdx ] = False #tell player1 which stone is used
            p2.freeStones[ stoneIdx ] = False #tell player2 which stone is used
                    
        d.draw(p2.board, p2.marks, "move-{:02d}a.png".format(moveidx)) #draw to png

        #now we call player2 and update boards/freeStones of both players
        m = p2.move()  
        if len(m) == 0:
            p2play = False
        else:
            stoneIdx, stone = m
            stoneColor = stones[stoneIdx][0]
            base.writeBoard(p1.board, stone, stoneColor)
            base.writeBoard(p2.board, stone, stoneColor)
            p1.freeStones[ stoneIdx ] = False
            p2.freeStones[ stoneIdx ] = False
        
        d.draw(p1.board, p1.marks, "move-{:02d}b.png".format(moveidx))

        #if both players return [] from move, the game ends
        if p1play == False and p2play == False:
            print("end of game")
            break
    
        moveidx+=1
        print(" -- end of move ", moveidx, " score is ", p1.score(p1.player), p1.score(-p1.player) )
