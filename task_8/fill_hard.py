import sys
#filename=sys.argv[1]
filename='hard3.txt'

#pisanie= open('proces.txt','w')

#FUNCTIONS--------------------------------------------------------------------------------------------------------------
def readStones(filename):
    stones = []            #vystup funkce - seznam nactenych kamenu
    f = open(filename,"r")
    numRows = int(f.readline().strip())  #precti 1. radek ze souboru
    numCols = int(f.readline().strip())  #precti 2. radek ze souboru
    for line in f:
        numbers = list(map(int, line.strip().split()))  #precti vsechna cisla na dalsich radcich
        color = numbers[0]                              #prvni z nich je barva kamene
        coords = numbers[1:]                            #zbyle jsou souradnice r1 c1 ... rn cn
        cells = []                                      #prevedeme [r1,c1 ... rn,cn] na pole cells = [[r1,c1], ... [rn,cn]]
        for i in range(len(coords)//2):
            cells.append( [ coords[2*i+0], coords[2*i+1] ] )
        stones.append( [ color, cells ] )
    f.close()
    return numRows, numCols, stones


def write(file, pole, nko):
    global cnt
    cnt+=1
    file.write('po iteracii funckie fill() cislo '+str(cnt)+'\n')
    file.write('idem skusat kamen n='+str(nko) +'\n')
    for i in range(len(pole)):
        line=''
        for j in range(len(pole[i])):
            line+=str(pole[i][j])+' '
        file.write(line)
        file.write('\n')
    file.write('\n')


def print_matrix(a):
    if type(a)==type([]):
        for r in range( len(a) ):
            for s in range( len(a[0])):
                print(a[r][s], end=' ')
            print()
    else:
        print(a)

def print_stone(stone):
    farba=stone[0]
    coords=stone[1]
    rozm=stone[2]
    for i in range(M):
        for j in range(N):
            if [i, j] in coords:
                print(farba, end=' ')
            else:
                print('-', end=' ')
        print()
    print('rozm=', rozm)
    print()

def toOrigin(stones):           #argumentom je cely zoznam kamenov
    niceStones=[]
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
        movedStone=[kamen[0], [ [ k[0]+rowdif, k[1]+coldif ] for k in coords], [sirka, vyska] ]
        niceStones.append(movedStone)
    niceStones.sort(key=lambda x: len(x[1]), reverse=True)
    return niceStones

def toOriginAfterRotation(stone):        #argumentom je 1 kamen
    coords=stone[1]
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
    movedStone=[stone[0], [ [ k[0]+rowdif, k[1]+coldif ] for k in coords], [sirka, vyska] ]
    return movedStone

def StonesPrint(stones):
    for kamen in stones:
        print(kamen, 'pocet blokov=', len(kamen[1]))

def CheckIfStoneCanBePlaced(m, suter):
    kamen=suter[1]
    acc=0
    stop=False
    num_of_blocks= len(kamen)
    while ( acc<num_of_blocks ) and ( stop==False): 
        br=kamen[acc][0]
        bc=kamen[acc][1]
        if not (br<M) or not (br>=0):
            stop=True
            break
        if not (bc<N) or not (bc>=0):
            stop=True
            break
        if m[br][bc]==0:
            acc+=1
            continue
        else:
            stop=True
    if stop==True:
        return False
    else:
        return True

def rotateStone(stone, cnt):
    coords=stone[1]
    rotatedStone=[]
    if cnt==0:
        return stone
    elif cnt==1:
        for block in coords:
            rotatedStone.append([-1*block[1], block[0]])
    elif cnt==2:
        for block in coords:
            rotatedStone.append([-1*block[0], -1*block[1]])
    elif cnt==3:
        for block in coords:
            rotatedStone.append([block[1], -1*block[0]])

    rotatedStone=[stone[0], rotatedStone]
    rotatedStone= toOriginAfterRotation(rotatedStone)
    return rotatedStone

def NewValidPosition(m, suter, coordsList, rotcnt):     #l... chceme l-tu moznu poziciu kamena
    um=[i for i in m]
    l=len(coordsList)

    f=suter[0]
    coords=suter[1]          #list of coords
    rozm=suter[2]
    
    if rozm[0]> N:
        return False
    if rozm[1]> M:
        return False

    x= l%( N-rozm[0]+1 )
    y= l//( N-rozm[0]+1 )
    
    newcoords=[]
    for block in coords:
        newbr= block[0] + y
        newbc= block[1] + x
        if newbr>= len(m) or newbc>= len(m[0]):           #test whether newcords arent outside of desk
            return False
        newcoords.append([newbr, newbc])

    newStone= [f, newcoords, rozm]

    '''
    print('DOSKA:')
    print_matrix(m)
    print('rotcnt=', rotcnt)
    print('KAMEN:')
    print_stone(newStone)
    '''

    if CheckIfStoneCanBePlaced(m, newStone):           #check if other tiles aren't blocking the placement of the stone
        for block in range(len(newcoords)):
            br=newcoords[block][0]
            bc=newcoords[block][1]
            um[br][bc]=f
        coordsList.append(newStone)
        return um, coordsList
    else:
        coordsList.append([])
        return NewValidPosition(m, suter, coordsList, rotcnt)


def removeStone(board, kamen):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==kamen[0]:
                board[i][j]=0
    return board

def fill(board, n, kamene, rotcnt):          #board= mat, n= number of stones used, kamene= niceStones
    #write(pisanie, board, n)
    global max_n
    if n>max_n:
        max_n=n

    #base case
    if n==len(kamene):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]==0:
                    return board, n-1, kamene, 0
        #write(pisanie, board)
        return board
    
    #non-base cases
    else:
        #PART 1: Calculate result
        farba=kamene[n][0]
        result=NewValidPosition(board, rotateStone(kamene[n], rotcnt), ListOfAllCoords[farba][rotcnt], rotcnt)

        #PART 2: Do something based on result
        if (n==0) and (result==False) and (rotcnt>=3):
            return ('NOSOLUTION')
        elif (result==False) and (rotcnt<=2):
            rotcnt= rotcnt +1
            return board, n, kamene, rotcnt
        elif (result==False) and (rotcnt>2):
            if n>0:
                board=removeStone(board, kamene[n-1])
            if n<= max_n-1:
                for i in range(n+1, max_n+1):
                    ListOfAllCoords[kamene[i][0]]={0: [], 1: [], 2: [], 3: []}
            return board, n-1, kamene, 0
        else:
            if n<= max_n-1:
                for i in range(n+1, max_n+1):
                    ListOfAllCoords[kamene[i][0]]={0: [], 1: [], 2: [], 3: []}
            return result[0], n+1, kamene, 0
#-----------------------------------------------------------------------------------------------------------------------
M,N, stones = readStones(filename)
niceStones= toOrigin(stones)

cnt=0

ListOfAllCoords={}
for kamen in niceStones:
    farba=kamen[0]
    ListOfAllCoords[farba] = {}
    for i in range(4):
        ListOfAllCoords[farba][i]=[]

max_n=0
mat= [[0] * N for i in range(M)]


output=(mat, 0, niceStones, 0)
while type(output)==tuple:
    output=fill(output[0], output[1], output[2], output[3])
print(output)

#pisanie.close()
