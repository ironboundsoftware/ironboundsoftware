#
# datareader.py
#
# Reads in the data.
#


def readFromCSVFile(filename):
    '''This Function reads in CSV files like what are downloaded from
    finance.yahoo.com'''
    import csv, time
    f = csv.reader(open(filename, 'rb'))
    output = []
    max_val = 0
    min_val = 10000000000
    max_d = 0
    min_d = 999999999999
    for line in f:
        d = time.mktime(time.strptime(line[0], '%d-%b-%y'))
        val = float(line[6])
        output.append((d, val))
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val
        if d > max_d:
            max_d = d
        if d < min_d:
            min_d = d
        
    return output, max_val, min_val, max_d, min_d

def readFromInternet(url):
    pass


if __name__ =='__main__':
    output = readFromCSVFile('data/xom.csv')
    for item in output:
        print item