from os import getpid


class Memory:
    def __init__(self):
        self.__proc_status = '/proc/%d/status' % getpid()
        self.__scale = {'kB': 1024.0, 'mB': 1024.0 * 1024.0,
                        'KB': 1024.0, 'MB': 1024.0 * 1024.0}

        self.since_memory = self._memory()
        self.since_resident = self._resident()
        self.since_stackSize = self._stackSize()

    def _VmB(self, VmKey):
        try:
            t = open(self.__proc_status)
            v = t.read()
            t.close()

        except (OSError, IOError):
            return 0.0      # non Linux

        i = v.index(VmKey)
        v = v[i:].split(None, 3)
        if len(v) < 3:
            return 0.0

        return float(v[1]) * self.__scale[v[2]]

    def _memory(self, since=0.0):
        return self._VmB('VmSize:') - since

    def _resident(self, since=0.0):
        return self._VmB('VmRSS:') - since

    def _stackSize(self, since=0.0):
        return self._VmB('VmStk:') - since

    def print_used_memory(self):
        print 'Memory: {} Mb'.format(self._memory(self.since_memory)/1000000)
        print 'Resident memory: {} Mb'.format(self._resident(self.since_resident)/1000000)
        print 'Stack size: {} Mb'.format(self._stackSize(self.since_stackSize)/1000000)
        print

if __name__ == '__main__':
    memory = Memory()
    memory.print_used_memory()
