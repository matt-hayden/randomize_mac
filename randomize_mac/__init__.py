from functools import lru_cache
from pathlib import Path
import re
import subprocess
import uuid

PROJECT_ROOT = Path(__file__).parent

@lru_cache()
def regex(*args, **kwargs):
    return re.compile(*args, **kwargs)

def run(*args, **kwargs):
    proc = subprocess.run(*args, **kwargs)
    assert (proc.returncode == 0)
    return proc

@lru_cache()
def UUID(*args, **kwargs):
    return uuid.UUID(*args, **kwargs)
