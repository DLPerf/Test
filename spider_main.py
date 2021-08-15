# from scrapy.cmdline import execute
#
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# execute(["scrapy", "crawl", "Haichuan"])


from scrapy import cmdline
import sys
sys.setrecursionlimit(1000000)

# cmdline.execute(["cd","Bysj_SE"])
cmdline.execute(["scrapy", "crawl", "Haichuan"])