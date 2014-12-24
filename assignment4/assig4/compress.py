import gzip
import sys
filename = sys.argv[1]
zipfilename = filename + ".gz"

f_in = open(filename, 'rb')
f_out = gzip.open(zipfilename, 'wb')
f_out.writelines(f_in)
f_out.close()
f_in.close()

