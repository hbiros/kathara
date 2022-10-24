import numpy
from getkey import getkey

def create_adj_matrix():
    router_num = int(input("How many routers are needed?: "))
    pc_num = int(input("How many PCs are needed?: "))
    router_names = ["R"+str(i) for i in range(0,router_num)]
    pc_names = ["PC"+str(i) for i in range(0,pc_num)]
    dev_names = router_names + pc_names
    matrix_len = router_num + pc_num
    adj_matrix = numpy.zeros((matrix_len, matrix_len), dtype=int)
    # print("\t", *["R"+str(i) for i in range(0,router_num)], *["PC"+str(i) for i in range(0,pc_num)])
    print("\n    ", *dev_names)
    row=0
    while row < matrix_len:
        print(dev_names[row], end=" "*(5-len(dev_names[row])), flush=True)
        col = row
        for i in range(row):
            print(" " + str(adj_matrix[i][row]), end=" "*(len(dev_names[i])-1), flush=True)
            adj_matrix[row][i]=adj_matrix[i][row]
        while col < matrix_len:
            if row == col:
                print(" 0", end=" "*(len(dev_names[col])-1), flush=True)
                col+=1
                continue
            key = getkey()
            if key == '1':
                print(" 1", end=" "*(len(dev_names[col])-1), flush=True)
                adj_matrix[row][col] = 1
            elif key == '0':
                print(" 0", end=" "*(len(dev_names[col])-1), flush=True)
            else:
                print('', end='', flush=True)
                continue
            col+=1
        print()
        row+=1
    return adj_matrix
