import stl
import timecode
import getopt
import sys


def usage():
    print "Usage: adjusttc.py [OPTION] [FILE]..."
    print "Modify the initial and final timecode of a STL subtitle"
    print ""
    print "Options:"
    print "-i, --input=\tInput STL file"
    print "-o, --output=\tOutput STL file"
    print "-a, --add=\tTimecode that need to be added for each TCI/TCO"
    print "-s, --sub=\tTimecode that need to be substracted for each TCI/TCO"
    print "\t\tTimecode Format:\tHH:MM:SS:FF | HH:MM:SS;FF\n"
    print "-n, --number\tOptional Argument: From that subtitle makes changes"
    print "-h, --help\tDisplay this help"
    print "-d, --dump\tOnly dumps Subtitle Number, TCI, TCO"
    print "\n"
    print "Report bugs to <ebilli@claxson.com>"

def main():
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hdi:o:a:s:n:", [ "help", "dump", "input=","output=","add=", "sub=", "number="])
    except getopt.GetoptError as err:
	# print help information and exit:
        print str(err) # will print something like "option -a not recognized"
	usage()
        sys.exit(2)     
        
    inp = None
    out = None
    tc  = None 
    add = None
    num = 0
    dump = False
    
    
    for o,a in opts:
	if o == '-h':
	    usage()
	    sys.exit()
	elif o in ('-d', '--dump'):
	    dump = True
	elif o in ('-i', '--input'):
	    inp = a
	elif o in ('-o', '--output'):
	    out = a
	elif o in ('-a', '--add'):
	    tc = timecode.fromString(a)
	    add = True
	elif o in ('-s', '--sub'):
	    tc = timecode.fromString(a)
	    add = False
	elif o in ('-n', '--number'):
	    num = a
	else:
	    assert False, "unhandled option"

    if dump == True and inp is not None:
	subtitle = stl.STL()
	subtitle.load(inp)
	for tf in subtitle.tti:
	    print ("%d: %s -> %s") % (tf.sn, tf.tci, tf.tco)
    else:
	if inp is not None and out is not None and tc is not None:
	    subtitle = stl.STL()
	    subtitle.load(inp)
	    i = 0
	    for tf in subtitle.tti:
		if ( i >= num ):
		    if add:
			tf.tci = tf.tci + tc
	    	        tf.tco = tf.tco + tc
		    else:
			tf.tci = tf.tci - tc
		        tf.tco = tf.tco - tc
		    
	    subtitle.save(out)
	else:
	    usage()
	    sys.exit()	    
    
if __name__ == "__main__":
    main()