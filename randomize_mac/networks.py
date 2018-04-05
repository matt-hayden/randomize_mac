import binascii
import hashlib

from . import *
from .macseed import get_mac, get_macs


class Network():
    def __init__(self, n_device, n_type, n_name, n_uuid):
        self.device = None
        if n_device != '--':
            self.device = n_device
        self.type = n_type
        self.name = n_name
        self.uuid = UUID('{%s}' % n_uuid)
    def __repr__(self):
        u_node = self.uuid.fields[5]
        return "<'%s' (%x)>" %(self.name, u_node)
    def set_local_mac(self, mac_address):
        proc = run(['nmcli', 'connection', 'modify', str(self.uuid), 'wifi.cloned-mac-address', str(mac_address)])
    def is_virtual(self):
        return bool(self.device)


def _get_networks(network_type=None, splitter=regex('(?<!\\\\)[:]').split):
    if isinstance(network_type, str):
        def network_type(arg, text=network_type):
            return arg and regex(text).search(arg)
    proc = run(['nmcli', '-t', '--fields', 'device,type,name,uuid', 'connection', 'show'], stdout=subprocess.PIPE)
    for line in proc.stdout.decode().split('\n'):
        line = line.rstrip()
        if line:
            n = Network(*splitter(line))
            if network_type(n.type):
                yield n

def get_networks(*args, **kwargs):
    return list(_get_networks(*args, **kwargs))
