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

select_list = ['nsubj','nsubjpass','dep','advmod','amod','acl:relcl','npadvmod','num','vmod','compound','nmod:for','nmod:poss','nmod:of','nmod:in','nmod:to','nmod:on','nmod:from','nmod:with','nmod:at','nmod:next','nmod:under']

file_name = open("/Users/songchangheon/Desktop/what_be_nlq.txt")
output_file = open("/Users/songchangheon/Desktop/extract.txt","w")

lines = file_name.readlines()
tuple_lines = tuple(lines)

print "file read is done."

sentences = dependency_parser.raw_parse_sents(tuple_lines)

i = 0
for line in sentences:
    print tuple_lines[i]
    print ""

    Focus = ""
    answer = ""
    Modifier = []
    flag = False

    for element in list(line.next().triples()):

        print element[1],element[0],element[2]
        # process 'dobj' to pick focus
        if flag == False and (element[1] == 'dobj'):
            if u'NN' in element[0][1] :
                Focus += element[0][0]
            elif u'NN' in element[2][1]:
                Focus += element[2][0]

        # process 'nsubj' and 'nsubjpass' to pick focus
        if flag == False and (element[1] == 'nsubj' or element[1] == 'nsubjpass'):
            if u'NN' in element[0][1]:
                Focus += element[0][0]
                if element[2][1] != u'WP' and u'VBP' not in element[2][1]:
                    Modifier.append(element[2][0])
            elif u'NN' in element[2][1]:
                Focus += element[2][0]
                if element[0][1] != u'WP' and u'VBP' not in element[0][1]:
                    Modifier.append(element[0][0])
            else:
                Focus += element[0][0] if element[0][1] != u'WP' else element[2][0]
            flag = True
        # processing Focus compound
        if element[1] == 'compound':
            if element[0][0] in Focus or element[2][0] in Focus:
                Focus = Focus + " " +element[0][0] if element[0][0] not in Focus else Focus + " " + element[2][0]
            if element[0][0] in Modifier or element[2][0] in Modifier:
                Modifier.append(element[0][0] if element[0][0] not in Modifier else element[2][0])

        if u'mod' in element[1] or u'acl' in element[1] or u'obj' in element[1] or u'advcl' in element[1]:           ## need to get modifier method
            if (element[0][0] in Focus or element[0][0] in Modifier) and element[2][1] != u'DT':
                mod = element[2][0]
            elif (element[2][0] in Focus or element[0][0] in Modifier) and element[2][1] != u'DT':
                mod = element[0][0]
            else:
                mod = ""
            if mod is not "":
                Modifier.append(mod)
        answer = Focus

    print "Focus : ",Focus
    for mod in Modifier:
        answer += (" " + mod)
    answer += "\n"
    output_file.write(answer)
    print "Modifier :", Modifier
    print ""
    i += 1

file_name.close()
output_file.close()
'''
What is required to open an account with Chevy Chase Bank Online?


nsubjpass (u'required', u'VBN') (u'What', u'WP')
compound (u'Online', u'NNP') (u'Chevy', u'NNP')
compound (u'Online', u'NNP') (u'Chase', u'NNP')
compound (u'Online', u'NNP') (u'Bank', u'NNP')
Focus :  required
Modifier : []



What are some banking tools that give a person access to their accounts?


nsubj (u'What', u'WP') (u'tools', u'NNS')
compound (u'tools', u'NNS') (u'banking', u'NN')
nsubj (u'give', u'VBP') (u'that', u'WDT')
compound (u'access', u'NN') (u'person', u'NN')
nmod:poss (u'accounts', u'NNS') (u'their', u'PRP$')
Focus :  give
Modifier : []

giving a flag to get first nsubj to get focus.

What is the minimum amount needed to open a checking account with Compass Bank Online?


dep (u'needed', u'VBN') (u'What', u'WP')
nsubjpass (u'needed', u'VBN') (u'amount', u'NN')
amod (u'amount', u'NN') (u'minimum', u'JJ')
amod (u'account', u'NN') (u'checking', u'VBG')
compound (u'Online', u'NNP') (u'Compass', u'NNP')
compound (u'Online', u'NNP') (u'Bank', u'NNP')
Focus :  needed
Modifier : []

How can I handle this problem.
Which one is a real focus in this sentence, if 'minimum amount', I have to change upper algorithm.
However 'needed' is focus, it will be okay to stay like this.
'''