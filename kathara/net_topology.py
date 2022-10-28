import ipaddress
import numpy
import os
from datetime import date
from getkey import getkey

def create_adj_matrix():
    router_num = int(input("How many routers are needed?: "))
    pc_num = int(input("How many PCs are needed?: "))
    router_names = ["r"+str(i) for i in range(0,router_num)]
    pc_names = ["pc"+str(i) for i in range(0,pc_num)]
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
    return adj_matrix, dev_names

def addresses_setup(adj_matrix, dev_names):
    size = len(dev_names)
    ip_pools = list()
    if adj_matrix.size == 0:
        return       
    for i in range(0, size-1):
        row = adj_matrix[i,:]
        for j in range(i+1, size):
            if row[j] == 1:
                ip_pool = get_ip('IP pool for devices '+dev_names[i]+'--'
                                        +dev_names[j])
                while True:        
                    if ip_pool not in [ip.with_prefixlen for ip in ip_pools]:
                        try:
                            ip_addr = ipaddress.IPv4Network(ip_pool)
                        except Exception as e:
                            print(e)
                            ip_pool = input('\n')
                            continue
                        else:
                            ip_pools.append(ip_addr)
                            break
                    else:
                        ip_pool = get_ip("Specified network already exists")
    return ip_pools

def get_ip(text=None):
    if text:
        print(text)
    while True:
        try:
            ip_pool = ipaddress.ip_network(input())
        except Exception as e:
            print(e)
        else:
            if ip_pool.prefixlen > 30:
                print("You shall specify network with mask of " 
                                        "maximum length of 30")
                continue
            else:
                return ip_pool.with_prefixlen

def create_lab_config(ip_pools, adj_matrix, dev_names):
    if os.path.exists('lab.conf'):
        print("File lab.conf already exists."
        "Are you sure you want to overwrite it?")
        ans = input("y/n: ").upper()
        if ans != 'Y':
            return -1
    with open('lab.conf', 'w') as f:
        f.write("# DATE: {}\n".format(date.today()))
        f.write("LAB_NAME=\"{}\"\n".format('Example'))
        f.write("LAB_DESCRIPTION=\"{}\"\n".format('Example description'))
        f.write("LAB_VERSION={}\n".format('1.0'))
        f.write("LAB_AUTHOR={}\n".format('test'))
        f.write("LAB_EMAIL={}\n\n".format('test@test.com'))
        dev_count = len(dev_names)   
        net_count = len(ip_pools)
        net_names = [chr(65 + i) for i in range(0, net_count)]
        net_names.reverse()
        for i in range(0, dev_count-1):
            int_num=0
            # row = adj_matrix[i,:]
            row=adj_matrix[i,:].tolist()
            for j in range(i+1, dev_count):
                if row[j] == 1:
                    col=adj_matrix[:,j].tolist()
                    f.write('{0}[{1}]={2}\n'.format(dev_names[i], 
                                                        row[0:j].count(1), 
                                                        net_names[-1]))
                    f.write('{0}[{1}]={2}\n\n'.format(dev_names[j], 
                                                        col[0:i].count(1), 
                                                        net_names.pop()))

def create_lab_startups(ip_pools, adj_matrix, dev_names):
    ip_pools.reverse()
    dev_count = len(dev_names)   
    # net_count = len(ip_pools)
    for i in range(0, dev_count-1):
        row=adj_matrix[i,:].tolist()
        for j in range(i+1, dev_count):
            if row[j] == 1:
                ip=ip_pools.pop()
                ip_addr=ip.hosts()
                ip_netmask=ip.netmask
                startup_file="{0}.{1}".format(dev_names[i],"startup")
                with open(startup_file, 'a') as f:
                    f.write('ifconfig eth{0} {1} netmask {2} up\n'.format(
                                                        row[0:j].count(1),
                                                        next(ip_addr, 1),
                                                        ip_netmask
                    ))
                startup_file="{0}.{1}".format(dev_names[j],"startup")
                with open(startup_file, 'a') as f:
                    f.write('ifconfig eth{0} {1} netmask {2} up\n'.format(
                                                        row[0:i].count(1),
                                                        next(ip_addr, 1),
                                                        ip_netmask
                    ))