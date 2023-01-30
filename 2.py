import sys

if len(sys.argv) > 1:
    try:
        s, z = 0, 1
        for a in sys.argv[1:]:
            s += int(a) * z
            z *= -1
        print(s)
    except Exception as ex:
        print(ex.__class__.__name__)
else:
    print('NO PARAMS')