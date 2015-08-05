# -*- coding: utf-8 -*-

# Python2.X encoding wrapper
import codecs,sys, time
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
from get_example import *
from subprocess import Popen, PIPE
from seqbdd_parts_of_speech import *

if __name__ == '__main__':
	adopt_rate = {'y' : 0, 'n' : 0}
	# f = codecs.o 'utf-8')
	# f.close()
	"""
	s = time.clock()
	f1 = codecs.open('/Users/piranon/Documents/corpus/bnc/raw/bnc.txt', 'r', 'utf-8')
	l = f1.readline()
	print l
	f1.close()
	e = time.clock()
	print "%.3f [sec]" % (e - s)
	sys.exit()
	"""
	words = get_word('answer_word_2.txt')
	for w in words:
		w = [u"represent as",u"represent  someone or something  as  something"] #テスト用
		main(w)
		sys.exit()		#テスト用
		"""
		if main(w):
			adopt_rate['y'] += 1
		else:
			adopt_rate['n'] += 1
		print 'adopt_rate : %.3f\n' %(adopt_rate['y'] / sum(adopt_rate.values()))
		"""
	"""
		p = Popen(["python", "/Users/piranon/Documents/lab_report/Data/seqbdd (parts)/seqbdd_parts_of_speech.py"], stdin=PIPE, stdout=PIPE)
		p.stdin.write(w[0])
		while True:
			line = p.stdout.readline()
			if not line:
				break
			print line
		p.wait()
		print 'end :%s' %w
	"""

