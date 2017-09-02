import os

_proc_status = '/proc/%d/status' % os.getpid()
_scale = {'kB': 1024.0, 'mB': 1024.0*1024.0,
          'KB': 1024.0, 'MB': 1024.0 * 1024.0}


def _VmB(VmKey):
    global _proc_status, _scale

    try:
        t = open(_proc_status)
        v = t.read()
        t.close()

    except (OSError, IOError):
        return 0.0      # non Linux

    i = v.index(VmKey)
    v = v[i:].split(None, 3)
    if len(v) < 3:
        return 0.0

    return float(v[1]) * _scale[v[2]]


def _memory(since=0.0):
    return _VmB('VmSize:') - since


def _resident(since=0.0):
    return _VmB('VmRSS:') - since


def _stackSize(since=0.0):
    return _VmB('VmStk:') - since

since_memory = _memory()
since_resident = _resident()
since_stackSize = _stackSize()


def main():
    print 'Memory: {} Mb'.format(_memory(since_memory)/1000000)
    print 'Resident memory: {} Mb'.format(_resident(since_resident)/1000000)
    print 'Stack size: {} Mb'.format(_stackSize(since_stackSize)/1000000)
    print
