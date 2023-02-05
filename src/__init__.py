# Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

import sys

def historic_data():
    pass

def live_data():
    pass

if __name__ == '__main__':
    
    if sys.argv[1]=='historic':
        historic_data()

    if sys.argv[1]=='live':
        live_data()
