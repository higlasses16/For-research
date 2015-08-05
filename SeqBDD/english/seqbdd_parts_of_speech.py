
# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys, time, nltk, copy, shutil
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
from node_arrange import *
from get_example import *
from get_example_corpus import *
global cache, mode
cache = {}
mode = 'a'

def getnode(data, left, right, f0, f1):
	if right.data == '0':
		return left
	elif cache.has_key("<%s,%s,%s>" % (data, f0, f1)):
		# print "cache exist\n"
		return cache["<%s,%s,%s>" % (data, f0, f1)]
	
	new_node = Node('%s(%s)' %(data[0], data[1]))
	new_node.left = left
	new_node.right = right
	cache["<%s,%s,%s>" %(data, f0, f1)] = new_node

	return new_node


def seqbdd(f):
	
	# f0_word = u''
	# f1_word = u''
	
	f.sort()
	# print 'f = %s' %f
	f0 = []
	f1 = []
	if f == [[]]:	
		return Node('1')
	if f == []:		
		return Node('0')
	if f[0] == []:
		del f[0]
	x = f[0][0]

	for i in range(len(f)):
		if f[i][0] == x:
			f1.append(f[i][1:])
		else:
			f0.append(f[i][:])

	# for w in f0:
	# 	f0_word += '%s, ' %w
	# for w in f1:
	# 	f1_word += '%s, ' %w

	# print 'Getnode(%s, f0[%s], f1[%s])' %(x, f0_word, f1_word)

	r  = getnode(x, seqbdd(f0), seqbdd(f1), f0, f1)

	# global num
	# num += 1
	# r.test_print()
	# r.print_tree(num)
	return r

def nltk_tagger(file):
	f = codecs.open(file, 'r', 'utf-8')
	word_tagged = []
	for line in f.readlines():
		line = nltk.word_tokenize(line)
		word_tagged.append(nltk.pos_tag(line))
	f.close()
	return word_tagged

def remove_word(sentences):
	for words in sentences:
		for w in words:
			del w[0]
	return sentences

def set_list(nest):
	temp = []
	for words in nest:
		if words not in temp:
			temp.append(words)
	return temp



def numbering(sentences, mode):
	for words in sentences:
		for i in range(len(words)):
			words[i] = list(words[i])
			if words[i][1] == ':':
				words[i][1] = 'ETC'
			if mode == 'a':
				words[i].append(u'%s' %i)
			else:
				words[i].append(u'%s' %(len(words) - i - 1))
	return sentences
def reset(w):
	global cache
	cache = {}
	if mode == 'a':
		after_tree = None
	else:
		before_tree = None
	"""
	try:
		shutil.move('%s.txt' %u'_'.join(w[0].split(' ')), 'Result/%s' %u'_'.join(w[0].split(' ')))
	except shutil.Error:
		os.remove('Result/%s/%s.txt' %(u'_'.join(w[0].split(' ')), u'_'.join(w[0].split(' '))))
		shutil.move('%s.txt' %u'_'.join(w[0].split(' ')), 'Result/%s' %u'_'.join(w[0].split(' ')))
	"""

def answer_output(text):
	f = codecs.open('get-patterns_2.txt', 'a', 'utf-8')
	f.write(text)
	f.close()

# if __name__ == '__main__':
def main(w):
	"""
	ctr_dic = load_contractions()
	# print ctr_dic
	split_text('sample_afraid.txt', u'afraid')
	sys.exit()
	"""
	"""
	words = get_word('answer_word_1.txt')
	for w in words:
	"""
	# w = unicode(raw_input("query >> "), 'utf-8')	
	# sample_words = get_ex_sentence(w)
	print 'Query : %s' %u''.join(w[0])

	# if get_sentence_filter(w):
	if get_sentence_from_corpus(w):

		s = time.clock()
		query = u'%s' %w[0].split(' ')[0]
		word_with_tag = nltk_tagger('/Users/piranon/Documents/lab_report/Data/test_set/%s.txt' %u'_'.join(w[0].split(' ')))
		before_query = []
		after_query = []
		for i in range(len(word_with_tag)):
			for j in range(len(word_with_tag[i])):
				if word_with_tag[i][j][0] == query:
					after_query.append(word_with_tag[i][j:])
					before_query.append(word_with_tag[i][:j])

		cache = {}
		if mode == 'a':
			after_numed = numbering(after_query, 'a')
			rank_a = copy.deepcopy(after_numed)
			after = set_list(remove_word(after_numed))
			after_tree = seqbdd(after)
		else:
			before_numed = numbering(before_query, 'b')
			rank_b = copy.deepcopy(before_numed)
			before = set_list(remove_word(before_numed))
			before_tree = seqbdd(before)
		e = time.clock()
		print "\nseqbdd make:%.3f [sec]" %(e - s)

		s = time.clock()
		if mode == 'a':
			graph =	after_tree.make_graph(query)
			graph =	after_tree.print_tree(graph)
			# after_tree.test_output('%s_test.jpeg' %query)
			for sentence in rank_a:
				graph = after_tree.rank(sentence, graph)
			graph_com = after_tree.remove_rank1(graph, query)
			graph_com = after_tree.node_compress(graph_com)
			
			pattern = [query]
			# text = 	u'\nQuery : %s\npattern : %s\nanswer : %s\n\n-------------------------------------------------------------\n' %(u''.join(w[0]), after_tree.pattern_extract(graph_com, query), w[1])
			after_tree.get_patterns(graph_com, query, pattern, [], 0)
			text = 	u'Query : %s\nanswer : %s\n' %(u''.join(w[0]), w[1])
			print text
			# answer_output(text)

			# after_tree.output('/Users/piranon/Documents/lab_report/Data/test_set/Result2/%s/%s_after.jpeg' %(u'_'.join(w[0].split(' ')) ,query), graph_com)
			after_tree.test_output(graph_com)
			after_tree.reset_graph()
		else:
			before_tree.print_tree()
			for sentence in rank_b:
				before_tree.rank(sentence)
			before_tree.remove_rank1()
			before_tree.node_compress()
			before_tree.output('%s_before.jpeg' %query)
			before_tree.reset_graph()

		e = time.clock()
		print "output seqbdd image:%.3f [sec]" % (e - s)
		reset(w)
		return 1

	else:
		return 0


"""
if __name__ == '__main__':

	words = get_word('answer_word_1.txt')
	for w in words:
		main(w)
"""