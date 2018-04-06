#! /usr/bin/env python3
"""MAC address randomizer

Usage:
    randomize_mac [options] [--]

Options:
    -t TYPE --type=TYPE     Interface type as regular expression [default: wireless]
    -v --verbose
"""
import itertools

from docopt import docopt

from . import *
from .macseed import get_mac, get_macs
from .networks import get_networks


def randomize_networks():
    options = docopt(__doc__, version='1.0a1')
    verbose = options.pop('--verbose')
    if verbose:
        info = print
    else:
        def info(*args, **kwargs):
            pass

    ns = get_networks(network_type=options.pop('--type'))
    mac_lookup = {}
    for n_type, _ in itertools.groupby(ns, key=lambda n: n.type):
        uuids = [ n.uuid.bytes for n in _ ]
        info("%d %s networks" %(len(uuids), n_type))
        mac_lookup.update(get_macs(*uuids, n_type=n_type))
    for n in ns:
        info("%s -> %s" %(n, mac_lookup[n.uuid.bytes]))
        n.set_local_mac(mac_lookup.pop(n.uuid.bytes))

if __name__ == '__main__':
    import sys
    sys.exit(randomize_networks())
