m=[]
with open('mojtest.txt', 'r') as f:
    for line in f:
        row=line.strip()
        row=row.split()
        m.append([int(i) for i in row ])
        row=[]

print(m)

def max_area_histogram(histogram):   
    stack = []
    max_area = 0
    index = 0

    while index < len(histogram):
 
        if len(stack)==0 or (histogram[stack[-1]] <= histogram[index]):
            stack.append(index)
            index += 1

        else:
            top_of_stack = stack.pop()
            area = (  histogram[top_of_stack] *( (index - stack[-1] - 1) if len(stack)!=0 else index)  )
            max_area = max(max_area, area)

    while len(stack)!=0:
        top_of_stack = stack.pop()
        area = (  histogram[top_of_stack] * ((index - stack[-1] - 1) if len(stack)!=0 else index)  )
        max_area = max(max_area, area)

    return max_area

MAX=0
for i in range(len(m)):
    if i==0:
        hist_riadok= max_area_histogram(m[i])
        if hist_riadok > MAX:
            MAX= hist_riadok
    else:
        for j in range(len(m[i])):
            if m[i][j]!=0:
                m[i][j]= m[i-1][j] + m[i][j]
        hist_riadok= max_area_histogram(m[i])
        if hist_riadok > MAX:
            MAX= hist_riadok
        
print(MAX)
