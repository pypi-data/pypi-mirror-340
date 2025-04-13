code = """
from scipy.stats import f # type: ignore

number = int(input("Enter the number of sample : "))
size = list(map(int, input("Enter the sizes of each sample : ").split()))

lists = [[] for _ in range(number)]

for i in range(number):
    lists[i] = list(map(int, input(f"Enter for sample {i} : ").split()))

N = sum(size)

Ti = [sum(i) for i in lists]
Ti_2 = [i ** 2 for i in Ti]

G = sum(Ti)

CF = round((G ** 2) / N , 2)

summation = 0
for i in range(number):
    summation += Ti_2[i] / size[i]

T = round(summation - CF, 2)

summation = 0
for i in lists:
    for j in i:
        summation += j ** 2
TSS = round(summation - CF, 2)

E = TSS - T

MSS = [T / (number - 1) , E / ((N - 1) - (number - 1))]

F_val = round(MSS[0] / MSS[1], 2)

alpha = 0.05
F_Table_val = round(f.ppf(1 - alpha, (number - 1), ((N - 1) - (number - 1))), 2)

if F_val > F_Table_val:
    print("Reject the null hypothesis: Significant difference exists.")
else:
    print("Accept the null hypothesis: No significant difference.")
Output : 
Z:\Y23CM012\work_cs> python .\1wayclassification.py
Enter the number of sample : 3                      
Enter the sizes of each sample : 6 7 5
Enter for sample 0 : 90 82 79 98 83 91
Enter for sample 1 : 105 89 93 104 89 95 86
Enter for sample 2 : 83 89 80 94 94
Accept the null hypothesis: No significant difference.

---------------------------------------------------------------------------
Question_2 

from scipy.stats import f # type: ignore
import numpy as np


number = int(input("Enter the number of samples: "))
size = list(map(int, input("Enter the sizes of each sample: ").split()))

lists = [[] for _ in range(number)]
for i in range(number):
    lists[i] = list(map(int, input(f"Enter for sample {i}: ").split()))

N = sum(size)
t = len(lists)  
b = len(lists[0])  

Ti = [sum(i) for i in lists]  
Ti_2 = [i ** 2 for i in Ti]  

Bi = np.sum(lists, axis=0)  
Bi_2 = [i ** 2 for i in Bi]  

G = sum(Ti)

CF = round((G ** 2) / N , 2)

summation = sum(Ti_2)
T = round((summation / b) - CF, 2)

summation = sum(Bi_2)
B = round((summation / t) - CF, 2)

summation = 0
for i in lists:
    for j in i:
        summation += j ** 2
TSS = round(summation - CF, 2)

E = TSS - T - B

MSS = [B / (b - 1), T / (t - 1), E / ((N - 1) - (b - 1) - (t - 1))]

F_val1 = round(MSS[0] / MSS[2], 2)  
F_val2 = round(MSS[1] / MSS[2], 2)  

alpha = 0.05

df_treatment = b - 1
df_block = t - 1
df_error = (N - 1) - (b - 1) - (t - 1)

F_Table_val1 = round(f.ppf(1 - alpha, df_treatment, df_error), 2)
F_Table_val2 = round(f.ppf(1 - alpha, df_block, df_error), 2)

def check(F_val, F_Table_val, typ):
    if F_val > F_Table_val:
        print(f"Reject the null hypothesis for {typ}: Significant difference exists.")
    else:
        print(f"Accept the null hypothesis for {typ}: No significant difference.")


check(F_val1, F_Table_val1, "Treatment")
check(F_val2, F_Table_val2, "Block")

Output: 
Z:\Y23CM012\work_cs> python .\2wayclassification.py
Enter the number of samples: 4
Enter the sizes of each sample: 5 5 5 5
Enter for sample 0: 75 73 59 69 84
Enter for sample 1: 83 72 56 70 92
Enter for sample 2: 86 61 53 72 88
Enter for sample 3: 73 64 62 79 95
Reject the null hypothesis for Treatment: Significant difference exists.
Accept the null hypothesis for Block: No significant difference.        

"""


def getCode():
    global code
    print(code)
