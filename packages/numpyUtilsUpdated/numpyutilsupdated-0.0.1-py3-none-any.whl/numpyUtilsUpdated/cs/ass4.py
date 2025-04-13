code = '''
import numpy as np


y = list(map(int, input("Enter the values of Y : ").split()))

n = int(input("Enter no.of samples to take : "))
lists = [[] for _ in range(n)]

N = len(y)
lists[0] = [1] * N

for i in range(1, n):
    lists[i] = list(map(int, input(f"Enter the values of sample {i + 1} : ").split()))

x = np.transpose(lists)
xT = np.transpose(x)
xT_x = np.dot(xT, x)
xT_xI = np.linalg.inv(xT_x)
xT_y = np.dot(xT, y)
beta = np.dot(xT_xI, xT_y)

output = f"{beta[0]:.2f}"

for i in range(1, len(beta)):
    if beta[i] >= 0:
        output += f" + {beta[i]:.2f} x{i}"
    else:
        output += f" - {-beta[i]:.2f} x{i}"
print(output)

Output: 
Z:\Y23CM012\work_cs> python .\multiple_lenear_regression_model.py
Enter the values of Y : 100 110 105 94 95 99 104 108 105 98 105 110
Enter no.of samples to take : 3
Enter the values of sample 2 : 9 8 7 14 12 10 7 4 6 5 7 6
Enter the values of sample 3 : 62 58 64 60 63 57 55 56 59 61 57 60
133.46 - 1.25 x1 - 0.35 x2

----------------------------------------------------------------------
Question_2

import numpy as np

y = []
for i in range(2):
    y.append(list(map(int, input("Enter the values of Y : ").split())))

n = int(input("Enter no. of samples to take : "))
lists = [[] for _ in range(n)]

N = len(y[0])

lists[0] = [1] * N

for i in range(1, n - 1):  
    lists[i] = list(map(int, input(f"Enter the values of sample {i + 1} : ").split()))

lists[n - 1] = list(map(float, input(f"Enter the values of sample {n} : ").split()))

x = np.transpose(lists)
xT = np.transpose(x)
xT_x = np.dot(xT, x)
xT_xI = np.linalg.inv(xT_x)
xT_y = np.dot(xT, np.transpose(y))
beta = np.dot(xT_xI, xT_y)
beta = np.transpose(beta)

output_1 = f"Y1 : {beta[0][0]:.2f}"  
output_2 = f"Y2 : {beta[1][0]:.2f}"  

for i in range(1, len(beta[0])):
    if beta[0][i] >= 0:
        output_1 += f" + {beta[0][i]:.2f} x{i}"
    else:
        output_1 += f" - {-beta[0][i]:.2f} x{i}"

for i in range(1, len(beta[1])):
    if beta[1][i] >= 0:
        output_2 += f" + {beta[1][i]:.2f} x{i}"
    else:
        output_2 += f" - {-beta[1][i]:.2f} x{i}"

print(output_1)
print(output_2)

Output:
Z:\Y23CM012\work_cs> python .\multivariate_linear_regression_model.py
Enter the values of Y : 10 12 11 9 9 10 11 12 11 10 11 12
Enter the values of Y : 100 110 105 94 95 99 104 108 105 98 103 110
Enter no. of samples to take : 4
Enter the values of sample 2 : 9 8 7 14 12 10 7 4 6 5 7 6
Enter the values of sample 3 : 62 58 64 60 63 57 55 56 59 61 57 60
Enter the values of sample 4 : 1 1.3 1.2 0.8 0.8 0.9 1 1.2 1.1 1 1.2 1.2
Y1 : 10.90 - 0.04 x1 - 0.09 x2 + 5.04 x3
Y2 : 91.10 - 0.06 x1 - 0.29 x2 + 27.84 x3

'''

def getCode():
    global code
    print(code)

