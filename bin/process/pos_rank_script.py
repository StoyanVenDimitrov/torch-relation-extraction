from position_rank import position_rank
from tokenizer import StanfordCoreNlpTokenizer


with open('text1', 'r') as f:
    abstract=f.read()
tokenizer = StanfordCoreNlpTokenizer("/home/stoyan/stanford-corenlp-full-2017-06-09")
pos_rank = position_rank(abstract, tokenizer,num_keyphrase=200)
out = open("/home/stoyan/uschema/rel_vocab", 'w+')
[out.write(unit.replace('_', ' ')+'\n') for unit in pos_rank]
out.close()

