import stl
import timecode
import getopt
import sys


def usage():
    print "Not help yet"


def main():
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hdi:o:t:", [ "help", "dump", "input=","output=","timecode="])
    except getopt.GetoptError as err:
	# print help information and exit:
        print str(err) # will print something like "option -a not recognized"
	usage()
        sys.exit(2)     
        
    inp=None
    out=None
    tc=None 
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
	elif o in ('-t', '--timecode'):
	    tc = timecode.fromString(a)
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
	    for tf in subtitle.tti:
		tf.tci = tf.tci + tc
	        tf.tco = tf.tco + tc
	    subtitle.save(out)
	    
    
if __name__ == "__main__":
    main()