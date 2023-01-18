#!/home/karmel/coding/kathara/venv/bin/python

from operator import add
from sre_constants import CH_UNICODE
from banner import *
from net_topology import *

if __name__ == "__main__":
    # banner()
    adj_matrix, dev_names = create_adj_matrix()
    ip_pools = addresses_setup(adj_matrix, dev_names)
    create_lab_config(ip_pools, adj_matrix, dev_names)
    create_lab_startups(ip_pools, adj_matrix, dev_names)
    choices = create_device_configs(dev_names)   
