import sys
import getopt
import string


####
#    given a raw sentence, export
#    [arg1, tac_rel, arg2, doc_info, s1_str, e1_str, s2_str, e2_str, sentence]
#    or
#    arg1 \t arg2 \t relation \t 1
####


def replace_by_sentence(line,vocab,rel_extr):
    cand_row=[]
    sen=line.translate(None, string.punctuation).lower()
    for v in vocab:
            #only one occurence of v! Note: v could be a phrase
        if (sen.find(v) != -1):
            tokenized_sen=sen.split()
            v_tokens=v.split()
            try:
                start_pos=tokenized_sen.index(v_tokens[0])
                end_pos=tokenized_sen.index(v_tokens[-1])+1
                cand_row.append([v,start_pos,end_pos,line])
            except (ValueError):
                pass
    #check on overlaps, e.g. "register"vs."commercial register"
    to_remove=[]
    for i in cand_row:
        for j in cand_row:
            if (i[1]==j[1] and i[2]<j[2]) or (i[1]>j[1] and i[2]==j[2]):
                to_remove.append(i)
    cand_row=[x for x in cand_row if x not in to_remove]

    if len(cand_row)>1:
        #[arg1, tac_rel, arg2, doc_info, s1_str, e1_str, s2_str, e2_str, sentence]
        res=['\t'.join([cand_row[i][0],'raw text',cand_row[i+1][0],'doc',str(cand_row[i][1]),
                        str(cand_row[i][2]),str(cand_row[i+1][1]),str(cand_row[i+1][2]),cand_row[i][3]])
                       for i in range(len(cand_row)-1)]
        #[arg1,arg2,rel,1]
        if rel_extr:
            res=[]
            for i in range(len(cand_row)-1):
                try:
                    triple ='\t'.join([cand_row[i][0],cand_row[i+1][0],define_relations(cand_row[i][1],
                                                                                    cand_row[i][2],cand_row[i+1][1],cand_row[i+1][2],cand_row[i][3]),'1','\n'])
                    res.append(triple)
                except (TypeError):
                    pass
                            
    else:
       res=[]

    return res


def define_relations(s1,e1,s2,e2,sentence):
    #bring into entity1 \t entity2 \t relation \t 1
    if s1 < s2:
        arg1_str = '$ARG1'
        arg2_str = '$ARG2'
    else:
        arg1_str = '$ARG2'
        arg2_str = '$ARG1'
        s1, s2, e1, e2 = s2, s1, e2, e1

    tokens = sentence.split(' ')
    left = tokens[:s1]
    middle = tokens[e1:s2]
    right = tokens[e2:]

    if len(middle)>1 and len(middle)<20:
        wild_card_sentence = ' '.join([arg1_str] + middle + [arg2_str])
    else:
        wild_card_sentence = None

    return wild_card_sentence
    

def main(argv):
    in_file = ''
    out_file = ''
    voc_file = ''
    extract = True

    help_msg = 'FromRawTextToRelation.py -i <inFile(Sentence per line)> -o <outputfile> -v <entity_vocabulary(Enitity per line)> -x extract candidates if false'
    try:
        opts, args = getopt.getopt(argv, "hi:o:v:x", ["inFile=", "outFile=","vocFile="])
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
        elif opt in ("-v", "--vocFile"):
            voc_file = arg
        elif opt in ("-x", "--extract"):
            extract = arg

    with open(voc_file,"rb") as saved_vocabulary:
        vocab=saved_vocabulary.read().splitlines()
    #clean up duplications
    vocab=list(set(vocab))
    print ('Processing lines from ' + in_file)
    data = [replace_by_sentence(line, vocab, extract) for line in open(in_file, 'r')]

    print ('Exporting lines to ' + out_file )
    out = open(out_file, 'w')
    [[out.write(units) for units in line] for line in data]
    out.close()

    

if __name__ == "__main__":
    main(sys.argv[1:])