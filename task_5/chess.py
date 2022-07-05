import sys
m=[]            #chessboard matrix

with open(sys.argv[1], 'r') as f:
    for line in f:
        row=line.strip()
        row=row.split()
        m.append(row)
        row=[]

'''
with open('chess.txt', 'r') as f:
    for line in f:
        row=line.strip()
        row=row.split()
        m.append(row)
        row=[]
'''

for r in range(8):
    for s in range(8):
        m[r][s]= int(m[r][s])

#Find exactly one black chess piece in temp
def find_black_in_temp(r, s, temp):
    values=[ m[j[0]][j[1]] for j in temp]
    if ( values.count(0)==len(values)-1 ) and ( sum(values)<=0 ):
        for value in values:
            if value<0:
                ind= values.index(value)
                return r, s, temp[ind][0], temp[ind][1]
    return False

#Return TRUE if ALL values are equal to ZERO, otherwise FALSE
def all_zeros(values):
    for value in values:
        if value!=0:
            return False
    return True

#Return elligible tiles, star-shaped around given piece
q_dir_r=[-1, -1, -1, 0, 1, 1, 1, 0]
q_dir_s=[-1, 0, 1, 1, 1, 0, -1, -1]
def star(r, s):
    star_tiles=[]
    for y in range(8):
        acc=1
        cond=True
        while ( 0<=(r+acc*q_dir_r[y])<=7 ) and ( 0<=(s+acc*q_dir_s[y])<=7 ) and cond==True:
            if m[r+acc*q_dir_r[y]][s+acc*q_dir_s[y]]==0:
                star_tiles.append( [ r+acc*q_dir_r[y] , s+acc*q_dir_s[y] ] )
                acc+=1
            elif m[r+acc*q_dir_r[y]][s+acc*q_dir_s[y]]<0:
                star_tiles.append( [ r+acc*q_dir_r[y] , s+acc*q_dir_s[y] ] )
                cond=False
                acc+=1
            else:
                cond=False
    return star_tiles

#Find coords of the black king:
def bk_coords(m):                                                  
    for l in range(8):
        for j in range(8):
            if int(m[l][j])==-1:
                global bk
                global bkr
                global bkc
                bkr=l           #black king ROW
                bkc=j           #black king COLUMN
                bk= [bkr, bkc]
                return bkr, bkc, bk

bk_coords(m)

white_pieces=[]
for r in range(8):
    for s in range(8):
        if ( m[r][s] > 0 ) and ( m[r][s] not in white_pieces ):
            white_pieces.append(m[r][s])

k_dir_r=[-2, -2, -1, 1, 2, 2, 1, -1]
k_dir_c=[-1, 1, 2, 2, 1, -1, -2, -2]

def knight(m):        #jazdec / kon
    x=[]              #possible coords to score check from
    for i in range(8):
        if (0<= bkr + k_dir_r[i] <=7) and (0<= bkc + k_dir_c[i] <=7):
            if (m[bkr + k_dir_r[i]][bkc + k_dir_c[i]]) <=0:
                x.append( [bkr + k_dir_r[i], bkc + k_dir_c[i]] ) 
    #print('x=', x)

    pos=[]              #possible positions of knights
    for j in range( len(x) ):
        coord_=[0,0]
        for i in range(8):
            r= x[j][0] + k_dir_r[i]
            s= x[j][1] + k_dir_c[i]
            if (0<= r <=7) and (0<= s <=7) and ( [r, s] not in pos) and ( [r,s]!=[bkr, bkc] ) :
                pos.append( [r, s, x[j][0], x[j][1] ] )
    #print('pos=', pos)

    for n in range( len(pos) ):         #check if there are knights at positions in pos[]
        r= pos[n][0]
        s= pos[n][1]
        if m[r][s] == 5:
            return r, s, pos[n][2], pos[n][3]
    return False

def bishop(m):       #strelec
    x1, x2=[], []             #possible coords to score check from         
    for i in range(-7, 8, 1):
        if (i!=0) and (0<=(bkr+i)<=7) and (0<=(bkc-i)<=7):
            x1.append([bkr+i, bkc-i])
        if (i!=0) and (0<=(bkr+i)<=7) and (0<=(bkc+i)<=7):
            x2.append([bkr+i, bkc+i])

    #If bishop is already somewhere in x[]
    for coords in x1:
        r= coords[0]
        s= coords[1]
        if m[r][s]==4:
            temp=[]
            cnt=1
            for i in range (min(bkc, s)+1, max(bkc, s)):
                temp.append( [max(bkr, r)-cnt, i] )
                cnt+=1
            cnt=0
            result=find_black_in_temp(r, s, temp)
            if result!=False:
                return result
    
    for coords in x2:
        r= coords[0]
        s= coords[1]
        if m[r][s]==4:
            temp=[]
            cnt=1
            for i in range (min(bkr, r)+1, max(bkr, r)):
                temp.append( [i, min(bkc, s)+cnt] )
                cnt+=1
            cnt=0
            result=find_black_in_temp(r, s, temp)
            if result!=False:
                return result

    #if bishop is not located in x1[] or x2[]
    x=x1+x2
    bishops=[]
    for r in range(8):
        for s in range(8):
            if m[r][s]==4:
                bishops.append([r, s])
    
    for piece in bishops:
        br= piece[0]
        bs= piece[1]
        diagonal_tiles=[]        
        for i in range(-7, 8, 1):
            if (i!=0) and (0<=(br+i)<=7) and (0<=(bs-i)<=7):
                diagonal_tiles.append([br+i, bs-i])
            if (i!=0) and (0<=(br+i)<=7) and (0<=(bs+i)<=7):
                diagonal_tiles.append([br+i, bs+i])
        #print('diagonal tiles=', diagonal_tiles)
        #print('x=', x)
        shared_tiles=[]
        for tile in diagonal_tiles:
            if tile in x:
                shared_tiles.append(tile)
        #print('shared tiles=', shared_tiles)
        for tile in shared_tiles:
            tr=tile[0]
            ts=tile[1]
            if m[tr][ts]<=0:
                routeBT=[]
                if tr<br and ts<bs:
                    for u in range(br-(tr+1)):
                        routeBT.append( [tr+1+u, ts+1+u] )
                elif tr<br and ts>bs:
                    for u in range(ts-(bs+1)):
                        routeBT.append( [br-1-u, bs+1+u] )
                elif tr>br and ts<bs:
                    for u in range(tr-(br+1)):
                        routeBT.append( [tr-1-u, ts+1+u] )
                elif tr>br and ts>bs:
                    for u in range(tr-(br+1)):
                        routeBT.append( [br+1+u, bs+1+u] )
                routeTK=[]
                if bkr<tr and bkc<ts:
                    for u in range(tr-(bkr+1)):
                        routeTK.append( [bkr+1+u, bkc+1+u] )
                elif bkr<tr and bkc>ts:
                    for u in range(bkc-(ts+1)):
                        routeTK.append( [tr-1-u, ts+1+u] )
                elif bkr>tr and bkc<ts:
                    for u in range(bkr-(tr+1)):
                        routeTK.append( [bkr-1-u, bkc+1+u] )
                elif bkr>tr and bkc>ts:
                    for u in range(bkr-(tr+1)):
                        routeTK.append( [tr+1+u, ts+1+u] )
                
                #print('strelec routeBT=', routeBT)
                #print('strelec routeTK=', routeTK)
                route= routeBT + routeTK
                values=[ m[j[0]][j[1]] for j in route ]
                #print('strelec values=', values)
                if all_zeros(values)==True:
                    return br, bs, tr, ts
    return False

def rook(m):        #veza
    x=[]            #possible coords to score check from
    for i in range(-7, 8, 1):
        if (bkc+i <=7) and (bkc+ i >=0 ) and ( i!=0 ):
            x.append([bkr, bkc+i])
        if (bkr+i <=7) and (bkr+ i >=0 ) and ( i!=0 ):
            x.append( [bkr+i, bkc] )

    #If rook is already somewhere in x[]
    for coords in x:
        r= coords[0]
        s= coords[1]
        if m[r][s]==3:
            temp=[]
            if bkr==r:
                for i in range( min(bkc, s)+1, max(bkc, s) ):
                    temp.append( [bkr, i] )
                
                result=find_black_in_temp(r, s, temp)
                if result!=False:
                    return result

            elif bkc==s:
                for i in range( min(bkr, r)+1, max(bkr, r) ):
                    temp.append( [i, bkc] )

                result=find_black_in_temp(r, s, temp)
                if result!=False:
                    return result
    
    #if rook is not located in x[]
    rooks=[]
    for r in range(8):
        for s in range(8):
            if m[r][s]==3:
                rooks.append([r, s])

    for piece in rooks:
        vr= piece[0]
        vs= piece[1]
        if m[bkr][vs] <= 0:
            temp=[]
            if vr<bkr:
                for i in range(bkr-vr-1):
                    temp.append([vr+i+1, vs])
            else:
                for i in range(vr-bkr-1):
                    temp.append([vr-1-i, vs])
            if vs<bkc:
                for i in range(bkc-vs-1):
                    temp.append( [bkr, vs+i+1] )
            else:
                for i in range(vs-bkc-1):
                    temp.append( [bkr, bkc+1+i] )

            values=[ m[j[0]][j[1]] for j in temp ]      
            if all_zeros(values)==True:
                return vr, vs, bkr, vs
        
        if m[vr][bkc] <= 0:
            temp=[]
            if vr<bkr:
                for i in range(bkr-vr-1):
                    temp.append([bkr-1-i, bkc])
            else:
                for i in range(vr-bkr-1):
                    temp.append([bkr+1+i, bkc])
            if vs<bkc:
                for i in range(bkc-vs-1):
                    temp.append( [vr, vs+i+1] )
            else:
                for i in range(vs-bkc-1):
                    temp.append( [vr, bkc+i+1] )

            values=[ m[j[0]][j[1]] for j in temp ]      
            if all_zeros(values)==True:
                return vr, vs, vr, bkc
            

    return False

def pawn(m):        #pesiak
    counter=0
    for i in range(2):
        if ( (bkr+1)<=7 ) and ( (bkc-1)>=0 ) and counter==0:
            tr=bkr+1
            ts=bkc-1
            counter+=1
            if m[tr][ts] < 0:
                if ( (tr+1)<=7 ) and ( (ts-1)>=0 ) and m[tr+1][ts-1]==6:
                    return tr+1, ts-1, tr, ts
                if ( (tr+1)<=7 ) and m[tr+1][ts+1]==6:
                    return tr+1, ts+1, tr, ts
            elif m[tr][ts] == 0:
                if ( (tr+1)<=7 ) and m[tr+1][ts]==6:
                    return tr+1, ts, tr, ts
                elif (tr==4) and (m[tr+1][ts]==0) and m[tr+2][ts]==6:
                    return tr+2, ts, tr, ts

        elif ( (bkr+1)<=7 ) and ( (bkc+1)<=7 ):
            tr=bkr+1
            ts=bkc+1
            if m[tr][ts] < 0:
                if ( (tr+1)<=7 ) and ( 7>=(ts+1)>=0 ) and m[tr+1][ts+1]==6:
                    return tr+1, ts+1, tr, ts
                if ( (tr+1)<=7 ) and m[tr+1][ts-1]==6:
                    return tr+1, ts-1, tr, ts
            elif m[tr][ts] == 0:
                if ( (tr+1)<=7 ) and m[tr+1][ts]==6:
                    return tr+1, ts, tr, ts
                elif (tr==4) and (m[tr+1][ts]==0) and m[tr+2][ts]==6:
                    return tr+2, ts, tr, ts

        else:
            continue
    
    return False

def queen(m):       #dama
   for i in range(8):
       for j in range(8):
           if m[i][j]==2:
               qr=i
               qs=j

   bk_list=star(bkr, bkc)
   q_list=star(qr, qs)
   for polozka in bk_list:
       if polozka in q_list:
            return qr, qs, polozka[0], polozka[1]
    
   return False

for num in white_pieces:
    if num==3:
        res=rook(m)
        if res!=False:
            #print('veza3:')
            print(res[0], res[1], res[2], res[3])
    elif num==4:
        res=bishop(m)
        if res!=False:
            #print('strelec4:')
            print(res[0], res[1], res[2], res[3])
    elif num==5:
        res=knight(m)
        if res!=False:
            #print('jazdec5:')
            print(res[0], res[1], res[2], res[3])
    elif num==6:
        res=pawn(m)
        if res!=False:
            #print('pesiak6:')
            print(res[0], res[1], res[2], res[3])
    elif num==2:
        res=queen(m)
        if res!=False:
            #print('dama6:')
            print(res[0], res[1], res[2], res[3])
