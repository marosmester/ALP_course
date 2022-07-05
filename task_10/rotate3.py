c= list( map(int, input().split() ) )
z= list( map(int, input().split() ) )
m= list( map(int, input().split() ) )
 
class State():
    def __init__(self, r1, r2, r3):
        self.r1= r1[:]
        self.r2= r2[:]
        self.r3= r3[:]
        self.content= str(self.r1)+str(self.r2)+str(self.r3)
        self.action=()
        self.prev= None
 
    def __repr__(self):
        return str(self.r1)+ '\n'+ str(self.r2)
 
    def expand(self):
        newstates=[]
 
        #(0,p)
        c0p=[ self.r1[5] ] + self.r1[:5]
        z0p, m0p= self.r2[:], self.r3[:]
        z0p[0]=c0p[0]
        z0p[2]=c0p[2]
        m0p[1]=c0p[1]
        m0p[5]=c0p[3]
        State1= State(c0p, z0p, m0p)
        State1.action=(0,'p')
        newstates.append(State1)
 
        #(0,m)
        c0m=self.r1[1:] + [self.r1[0]]
        z0m, m0m= self.r2[:], self.r3[:]
        z0m[0]= c0m[0]
        z0m[2]= c0m[2]
        m0m[1]= c0m[1]
        m0m[5]= c0m[3]
        State2= State(c0m, z0m, m0m)
        State2.action=(0,'m')
        newstates.append(State2)
 
        #(1,p)
        c1p, m1p= self.r1[:], self.r3[:] 
        z1p=[self.r2[5]]+ self.r2[:5]
        c1p[0]= z1p[0]
        c1p[2]= z1p[2]
        m1p[0]= z1p[1]
        m1p[2]= z1p[3]
        State3= State(c1p, z1p, m1p)
        State3.action=(1,'p')
        newstates.append(State3)
 
        #(1,m)
        c1m, m1m= self.r1[:], self.r3[:]
        z1m= self.r2[1:] + [ self.r2[0] ]
        c1m[0]= z1m[0]
        c1m[2]= z1m[2]
        m1m[0]= z1m[1]
        m1m[2]= z1m[3]
        State4= State(c1m, z1m, m1m)
        State4.action=(1,'m')
        newstates.append(State4)
 
        #(2,p)
        c2p, z2p= self.r1[:], self.r2[:]
        m2p= [ self.r3[5] ] + self.r3[:5]
        c2p[1]= m2p[1]
        c2p[3]= m2p[5]
        z2p[1]= m2p[0]
        z2p[3]= m2p[2]
        State5=State(c2p, z2p, m2p)
        State5.action=(2,'p')
        newstates.append(State5)
 
        #(2,m)
        c2m, z2m= self.r1[:], self.r2[:]
        m2m= self.r3[1:]+ [ self.r3[0] ]
        c2m[1]= m2m[1]
        c2m[3]= m2m[5]
        z2m[1]= m2m[0]
        z2m[3]= m2m[2]
        State6=State(c2m, z2m, m2m)
        State6.action=(2,'m')
        newstates.append(State6)
 
        return newstates
 
start= State(c, z, m)
goal= '[1, 2, 0, 0, 0, 0][1, 1, 0, 2, 1, 1][1, 2, 2, 2, 2, 0]'
 
openList=[]
openList.append(start)
isInOpen={}
 
#file=open('debugDU10.txt','w')
 
while openList:
    current= openList.pop(0)
    '''
    print(current.content)
    file.write(current.content)
    file.write(str(current.action))
    if current.prev != None:
        file.write((current.prev).content)
    file.write('\n')
    '''
    if current.content== goal:
        res=[]
        while current != None:
            res.append(current.action)
            current= current.prev
        break
 
 
    newstates= current.expand()
 
    for state in newstates:
        if state.content not in isInOpen:
            state.prev= current
            openList.append(state)
            isInOpen[state.content]=1            
 
res.pop()
#file.close()
 
resString=""
for action in res[::-1]:
    resString+=str(action)
 
resString= resString.replace(" ","")        #odstranit medzery z vysledneho stringu
resString= resString.replace("'","")        #odstranit jednoduche uvodzovky z vysledneho stringu
print(resString)
