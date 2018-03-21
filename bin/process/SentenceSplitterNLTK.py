import sys
import getopt
import nltk.data

def sentence_splitter(in_file):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(in_file)
    data = fp.read()
    return ('\n'.join(tokenizer.tokenize(data)))

def main(argv):
    in_file = ''
    out_file = ''

    help_msg = 'SentenceSplitterNLTK.py -i <inFile> -o <outFile>'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["inFile=", "outFile="])
    except getopt.GetoptError:
        print (help_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (help_msg)
            sys.exit()
        elif opt in ("-i", "--inFile"):
            in_file = arg
        elif opt in ("-o", "--outFile"):
            out_file = arg

 
    print ('Processing text from ' + in_file)
    data = sentence_splitter(in_file)

    print ('Exporting lines to ' + out_file )
    out = open(out_file, 'w+')
    out.write(data)
    out.close()

    

if __name__ == "__main__":
    main(sys.argv[1:])
