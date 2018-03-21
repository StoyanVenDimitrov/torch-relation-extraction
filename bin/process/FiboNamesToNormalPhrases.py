#!/usr/bin/python

import sys, getopt, re, string

def readFromTSV(read_line):
   formatted=[]
   ent1,rel,ent2 = read_line.split('\t')
   e1 = re.search('vocabulary#(.+?)>', ent1)
   if e1:
      ent1 = e1.group(1)

      ent1 = re.findall(r'([A-Z]{2,}(?=[A-Z]|$)|[A-Z][a-z]*)', ent1)
      print (ent1)
      ent1 = ' '.join(ent1)
   m = re.search('#(.+?)>', rel)
   if m:
      rel = 'rel:' + m.group(1)
   e2 = re.search('vocabulary#(.+?)>', ent2)
   if e2:
      ent2 = e2.group(1)
      ent2 = re.findall('[A-Z][^A-Z]*', ent2)
      ent2 = ' '.join(ent2).lower()
   return '\t'.join((ent1,rel,ent2))


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   print ('Processing lines from ' + inputfile)
   data = [readFromTSV(line) for line in open(inputfile, 'r')]

   print ('Exporting lines to ' + outputfile )
   out = open(outputfile, 'w+')
   [out.write(line) for line in data]
   out.close()

if __name__ == "__main__":
   main(sys.argv[1:])
