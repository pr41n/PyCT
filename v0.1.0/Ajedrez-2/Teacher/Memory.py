import os
import cv2

_proc_status = '/proc/%d/status' % os.getpid()
_scale = {
    'kB': 1024.0, 'mB': 1024.0*1024.0,
    'KB': 1024.0, 'MB': 1024.0 * 1024.0,
         }


def _VmB(VmKey):
    global _proc_status, _scale

    try:
        t = open(_proc_status)
        v = t.read()
        t.close()

    except:
        return 0.0      # non Linux?

    i = v.index(VmKey)
    v = v[i:].split(None, 3)
    if len(v) < 3:
        return 0.0

    return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    return _VmB('VmSize:') - since


def resident(since=0.0):
    return _VmB('VmRSS:') - since


def stackSize(since=0.0):
    return _VmB('VmStk:') - since

since_memory = memory()
since_resident = resident()
since_stackSize = stackSize()


def main():
    print 'Memory: {} Mb'.format(memory(since_memory)/1000000)
    print 'Resident memory: {} Mb'.format(resident(since_resident)/1000000)
    print 'Stack size: {} Mb'.format(stackSize(since_stackSize)/1000000)
    print

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.imshow('cam', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 10:
            main()
        if k == ord('q') or k == 27:
            cv2.destroyAllWindows()
            exit(11)
