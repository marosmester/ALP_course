import sys
#f= open('rat5.txt','r')
 
#Kodovanie:  OBRAZOK ---> KOD  ****************************************************
def toNibble(line, dict):
    nibbleLine=''
    length= len(line)
    for i in range(length//4):
        a=i*4
        b=a+4
        nibbleLine+= str(dict[line[a:b]])
     
    return nibbleLine
 
'''
def hexToBin(hex):                  #hex je hexadecimalny symbol vo forme STRINGU
    if ord(hex)<60:
        b= bin(hex)
        b=b[2:]
        while len(b)<4:
            b='0'+b
        return b
    else:
        b= bin( ord(hex)-55 )
        b=b[2:]
        return b
'''
 
def betterBin(hexinteger):
    b= bin(hexinteger)
    b=b[2:]
    while len(b)<4:
        b='0'+b
 
    return b
 
def ComprBinToComprHex(longbin):
    lst=[int(i) for i in longbin]
    longhex=''
    if len(lst)%4 ==0:
        length=len(lst)//4
    else:
        length=(len(lst)//4)+1
 
    #if cond==True:
        #length+=1
 
    for i in range( length ):
        nibble=lst[i*4:i*4+4]
         
        #check if theere is a need to add some zeros
        while len(nibble) !=4:
            nibble.append(0)
        #-------------------------------------------
 
        suma=0
        for j in range(4):
            suma+= nibble[3-j]* (2**j)
         
        if suma<10:
            longhex+=str(suma)
        else:
            longhex+= chr(55+suma)
 
    return longhex
 
 
hexdict={}
hexdict['    ']= 0
hexdict['   *']= 1
hexdict['  * ']= 2
hexdict['  **']= 3
hexdict[' *  ']= 4
hexdict[' * *']= 5
hexdict[' ** ']= 6
hexdict[' ***']= 7
hexdict['*   ']= 8
hexdict['*  *']= 9
hexdict['* * ']= 'A'
hexdict['* **']= 'B'
hexdict['**  ']= 'C'
hexdict['** *']= 'D'
hexdict['*** ']= 'E'
hexdict['****']= 'F'
 
nibbles=''
for rawline in sys.stdin: 
    line= rawline.strip('\n')
    nibbledLine= toNibble(line, hexdict)
    nibbles+= nibbledLine
 
nibbles_list=[i for i in nibbles] 
 
#work with buffer, pure strings
buffer=''
testseq=nibbles[0:5]
compressedBIN=''
#compressedBIN2=''
cond=False
 
while testseq:
    if len(buffer)<2:
        testseq_list=[int(i) if ord(i) < 60 else ord(i)-55 for i in testseq]
        compressedBIN+='0'
        compressedBIN+=betterBin(testseq_list[0])
 
        '''
        compressedBIN2+=str(buffer)+' '+str(testseq)+' | '        
        compressedBIN2+='0 '+betterBin(testseq_list[0])
        compressedBIN2+='_'+str(len(compressedBIN)//4)+'\n'
        '''
        #prepare for next iteration
        buffer+=testseq[0]
        nibbles=nibbles[1:]
        testseq=nibbles[0:5]
 
    else:
        #print(buffer, testseq)
        #find maxseq and its offset (if there is one)
        offset=0
        maxlength=0
         
        seq=testseq[:2]
        if seq in buffer:
            for i in range( len(testseq)-2 ):
                seq+=testseq[i+2]
                if seq in buffer:
                    continue
                else:
                    seq=seq[:-1]
                    break
             
            offset=buffer.index(seq)
        else:
            seq=''
         
        #write result into compressedBIN
        if len(seq)<2:
            testseq_list=[int(i) if ord(i) < 60 else ord(i)-55 for i in testseq]
            compressedBIN+=('0'+betterBin(testseq_list[0]))
             
            '''
            compressedBIN2+=str(buffer)+' '+str(testseq)+' | ' 
            compressedBIN2+=('0 '+betterBin(testseq_list[0]))
            compressedBIN2+='_'+str(len(compressedBIN)//4)+' '+str(ComprBinToComprHex(compressedBIN)[-10:])+'\n'
            '''
            #print('0 '+betterBin(max(testseq_list)))
        else:
            compressedBIN+=('1'+betterBin(offset)+ betterBin( len(seq)-2 )[2:] )
            '''
            compressedBIN2+=str(buffer)+' '+str(testseq)+' | ' 
            compressedBIN2+=('1 '+betterBin(offset)+' '+ betterBin( len(seq)-2 )[2:] )
            compressedBIN2+='_'+str(len(compressedBIN)//4)+' '+str(ComprBinToComprHex(compressedBIN)[-10:])+'\n'
            '''
            #print('1 '+betterBin(offset)+ ' '+ betterBin( len(maxseq)-2 )[2:] )
        #print('-----------------------------------------------')
 
 
        #prepare for next iteration
        maxlength=len(seq)
 
        if maxlength==0:
            if len(buffer) <= 15:
                buffer+=testseq[0]
                #check if NEW length of the buffer isnt over 16
                if len(buffer)>16:
                    diff=len(buffer)-16
                    buffer=buffer[diff:]
            else:
                buffer=buffer[1:] + testseq[0]
 
            nibbles=nibbles[1:]
            testseq=nibbles[0:5]
        else:
            if len(buffer) <= 15:
                buffer+=testseq[0:maxlength]
                #check if NEW length of the buffer isnt over 16
                if len(buffer)>16:
                    diff=len(buffer)-16
                    buffer=buffer[diff:]
            else:
                buffer=buffer[maxlength:] + testseq[0:maxlength]
 
            nibbles=nibbles[maxlength:]
            testseq=nibbles[0:5]
     
    if len(testseq)==1:
        cond=True
             
 
#print('len of compressedBin/4= ', len(compressedBIN)/4)
#print(compressedBIN2)
res=ComprBinToComprHex(compressedBIN)
print(res)
#print(len(res))
