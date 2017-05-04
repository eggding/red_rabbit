import cProfile
import time, StringIO, pstats

pr = cProfile.Profile()
pr.enable()


def fun(a, b):
    c = 0
    while True:
        time.sleep(0.1)
        c += 1
        print(a + b)
        if (c > 100):
            break

        if (c % 10 == 0):
            s = StringIO.StringIO()
            # sortby = 'cumulative'
            ps = pstats.Stats(pr, stream=s)
            ps.print_stats()
            aa = s.getvalue()
            print(aa)
            return


fun(10, 2)

pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print s.getvalue()
