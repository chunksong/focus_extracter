'''
    This program takes question from file input,
    and extracts Focus from that Natural Language Question,
    actually, at first, writer takes examples that have "What be" question.

'''
import os
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = '/Users/songchangheon/stanford_NLP/stanford-parser-full-2017-06-09/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '/Users/songchangheon/stanford_NLP/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'

parser = stanford.StanfordParser(model_path="/Users/songchangheon/stanford_NLP/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
dependency_parser = stanford.StanfordDependencyParser(os.environ['STANFORD_PARSER'],os.environ['STANFORD_MODELS'],)

select_list = ['nsubj','nsubjpass','dep','advmod','amod','npadvmod','num','vmod','compound','nmod:for','nmod:poss','nmod:of','nmod:in','nmod:to','nmod:on','nmod:from','nmod:with','nmod:at','nmod:next','nmod:under']

file_name = open("/Users/songchangheon/PARALEX/web_crawl/question.txt")

lines = file_name.readlines()
tuple_lines = tuple(lines)

print "file read is done."

sentences = dependency_parser.raw_parse_sents(tuple_lines)

i = 0
for line in sentences:
    print tuple_lines[i]
    print ""

    Focus = ""
    Modifier = []
    for element in list(line.next().triples()):
        if element[1] in select_list:
            print element[1],element[0],element[2]
            if element[1] == 'nsubj' or element[1] == 'nsubjpass':
                Focus = element[0][0] if element[0][1] != u'WP' else element[2][0]


    print "Focus : ",Focus
    print "Modifier :", Modifier
    print ""
    i += 1