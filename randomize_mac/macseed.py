import binascii
import hashlib

from . import *

macseed_exec = [ str(PROJECT_ROOT / 'etc/macseed.sh') ]

def reseed():
    proc = run(macseed_exec+['reseed'])

def get_seed():
    proc = run(macseed_exec+['raw'], stdout=subprocess.PIPE)
    return proc.stdout

class MAC:
    __slots__ = [ 'raw' ]
    def __init__(self, arg):
        if isinstance(arg, bytes): # NOT ascii characters, 0-255-valued bytes
            assert len(arg) == 6, "%s improper length" % arg
            self.raw = arg
        elif isinstance(arg, str):
            arg = arg.replace(':', '')
            assert len(arg) == 12, "%s improper length" % arg
            self.raw = binascii.unhexlify(arg)
        else: # presume some iterable
            assert len(arg) == 6, "%s improper length" % arg
            self.raw = binascii.unhexlify(''.join(arg))
    def hex(self):
        return binascii.hexlify(self.raw).decode()
    def __str__(self):
        s = self.hex()
        p = []
        while s:
            p += [s[:2]]
            s = s[2:]
        return ':'.join(p)
    def __repr__(self):
        return str(self)


def _get_macs(*args, seed=None, hasher='SHA256', **kwargs):
    seed = seed or get_seed()
    args = args or [None]
    if args:
        if isinstance(hasher, str):
            hasher = hashlib.new(hasher)
        assert callable(hasher.update)
        hasher.update(seed)
        for arg in args:
            if arg is None:
                yield None, MAC('02' + binascii.hexlify(seed[-5:]).decode())
            else:
                h = hasher.copy()
                assert isinstance(arg, bytes), "'%s' invalid input" % arg
                h.update(arg)
                yield arg, MAC('02'+h.hexdigest()[-10:])
def get_macs(*args, n_type=None, **kwargs):
    hasher = hashlib.sha256()
    if n_type:
        hasher.update(n_type.encode())
    return list(_get_macs(*args, hasher=hasher, **kwargs))
def get_mac(*args, **kwargs):
    ms = get_macs(*args, **kwargs)
    assert len(ms) == 1
    return ms[0][-1]
