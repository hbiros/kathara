# entry code for package
# when python -m kathara_net_creator first __init__ is executed then __main__
from src.banner import banner
from src.net_topology import *
# from code.banner import banner

if __name__ == "__main__":
    banner()
    create_adj_matrix()