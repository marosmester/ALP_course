base= int ( input() )       #desired base
num = float( input() )    #number in decimal base
anum= int( abs(num) )
frac=abs(num) - int(abs(num))   #digits after decimal point

#INTEGER PART
exp=0   #exponent
product=0
while product < abs(anum):
    exp+= 1
    product= base**exp
exp-=1

nasobky=[]
anum_= anum
while exp>=0:
    result=  anum_//(base**exp) 
    anum_= anum_ - (base**exp) * result
    exp-=1
    nasobky.append( int(result) )

output=''
symbols='abcdefghijklmnopqrstuvwxyz'
for i in nasobky:
    if i<10:
        output+= str(i)
    else:
        output+= symbols[i-10]

if output=='':
    output+='0'

#FRACTION PART
output+='.'

if frac!=0:
    digits= []
    for i in range(6):
        prod= frac * base                   #prod = product of multiplication
        integ_part= int( prod//1 )          #integer part of the number, integ_part is always < base
        splitted= str(prod).split('.')     
        #remain= float('0.'+splitted[1])     #remain= digits after the decimal point
        remain=abs(prod) - int(abs(prod))

        digits.append(integ_part)
        frac=remain
        if remain==0:
            break

    for i in digits:
        if i<10:
            output+= str(i)
        else:
            output+= symbols[i-10]

splitted_output=output.split('.')
test=splitted_output[1]
if len(test)<6:
    add= 6 - len(test)
    for i in range(add):
        output+='0'

if num<0:
    output='-'+ output
elif num==0:
    output+='0'

print(output)