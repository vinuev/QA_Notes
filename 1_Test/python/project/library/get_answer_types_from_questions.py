# from stanfordcorenlp import StanfordCoreNLP
import sys


verbose=1

def check_pattern1(line,tid):
	flag=0
	s=''
	
	if verbose:
		print "pattern 1 line ",line, len(line), tid
	
	while tid<len(line):
		if line[tid][0].lower()!='which' and line[tid][0].lower()!='what':
			tid+=1
		else:
			break
			
	if tid>=len(line):
		return flag,s,tid		
	
	tid+=1

	
	if verbose:
		print "Which|what ", len(line), tid
	
	be_flag=0
	if tid<len(line) and (line[tid][0]=='is' or line[tid][0]=='are' or line[tid][0]=='was' or line[tid][0]=='were'):
		tid+=1
		be_flag=1
		
	if verbose:
		print "lemma 'be' ", len(line), tid	
					
	if tid<len(line) and line[tid][1]=='DT':
		tid+=1		
	
	if verbose:
		print "[DET]? ", len(line), tid
	
	if tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
		while tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
			tid+=1			 		
	
	if verbose:
		print "[ADJ|ADV]* ", len(line), tid
	
	if tid<len(line) and line[tid][1].startswith('N'):
		if verbose:
			print "[noun] ", len(line), tid, line[tid][1]
		if (tid+1)==len(line) or ((tid+1) < len(line) and line[tid+1][0].lower()!='of' and line[tid+1][1]!='POS'): #not (be_flag==1 and line[tid+1][1]=='POS')):
			s=line[tid][0]
			flag=1		
			return flag, s, tid	
		else:
			return flag, s, tid	 
	else:
		return flag,s,tid

						
def check_pattern2(line,tid):
	flag=0
	s=''
	
	#if verbose:
		#print "pattern 2 line ",line, len(line), tid
	
	while tid<len(line):
		if line[tid][0].lower()!='which' and line[tid][0].lower()!='what':
			tid+=1
		else:
			break
			
	if tid>=len(line):
		return flag,s,tid		
	
	tid+=1
	
	if tid<len(line) and (line[tid][0]=='is' or line[tid][0]=='are' or line[tid][0]=='was' or line[tid][0]=='were'):
		tid+=1
					
	if tid<len(line) and line[tid][1]=='DT':
		tid+=1		
	
	if tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
		while tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
			tid+=1			 		
	
	if tid<len(line) and line[tid][1].startswith('N'):
		s=line[tid][0]
		tid+=1
	else:
		return flag,s, tid
	
	if tid<len(line) and line[tid][0] =='of':
		s+=' '+line[tid][0]
		tid+=1
	else:
		return flag, s, tid	
	
	
	if tid<len(line) and line[tid][1]=='DT':
		tid+=1	
	
	if tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
		while tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
			tid+=1
							
	if tid<len(line) and line[tid][1].startswith('N'):
		s+=' '+line[tid][0]
		#s=line[tid][0]
		flag=1
		return flag, s, tid
	else:	
		return flag, s, tid	


def check_pattern3(line,tid):
	flag=0
	s=''
	
	#if verbose:
		#print "pattern 3 line ",line, len(line), tid
	
	while tid<len(line):
		if line[tid][0].lower()!='which' and line[tid][0].lower()!='what':
			tid+=1
		else:
			break
			
	if tid>=len(line):
		return flag,s, tid		
	
	tid+=1

	#MAking [be] optional
	if tid<len(line) and (line[tid][0]=='is' or line[tid][0]=='are' or line[tid][0]=='was' or line[tid][0]=='were'):
		tid+=1
	#else:
	#	return flag, s, tid	
					
	if tid<len(line) and line[tid][1]=='DT':
		tid+=1		
	
	
	if tid<len(line) and line[tid][1].startswith('N'):
		tid+=1
	else:
		return flag,s, tid
	
	if tid<len(line) and line[tid][1] =='POS':
		tid+=1
	else:
		return flag, s, tid	
	
	
	if tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
		while tid<len(line) and (line[tid][1].startswith('JJ') or line[tid][1].startswith('RB')):
			tid+=1				
	
	if tid<len(line) and line[tid][1].startswith('N'):
		s=line[tid][0]
		flag=1
		return flag,s,tid
	else:
		return flag,s,tid
	
		
def check_pattern4(line,tid):
	flag=0
	s=''
	
	while tid<len(line):
		if line[tid][0].lower()!='when':
			tid+=1
		else:
			break
	if tid>2:#=len(line): #when after position 1 is not allowed
		return flag,s, tid				
	else:
		flag=1
		s='date'
		return flag,s,tid+1
	
def check_pattern5(line,tid):
	flag=0
	s=''
	
	while tid<len(line):
		if line[tid][0].lower()!='where':
			tid+=1
		else:
			break
	if tid>=2:#len(line): #where after position 1 is not allowed
		return flag,s, tid				
	else:
		flag=1
		s='location'
		return flag,s,tid+1

def check_pattern6(line,tid):
	flag=0
	s=''
	#if verbose:
		#print 'tid at pattern 6',tid
	while tid<len(line):
		if line[tid][0].lower()!='who':
			tid+=1
		else:
			break
	if tid>=2:#len(line): #who after position 1 is not allowed
		return flag,s, tid				
	else:
		flag=1
		s='person'
		return flag,s,tid+1			
			
def get_answer_type(line,verbose):
	# Pattern 1 [.*]* [which|what] [lemma: be]? [det]? [adj|adv]* [noun]+ [.*]*      (E.g.: What is the current currency in Germany?)
	# Pattern 2 [.*]* [which|what] [lemma: be]? [det]? [adj|adv]* [noun] [of ] [det]?[adj|adv]* [noun]+ [.*]*     (E.g.: What kind of currency does Germany have?)
	# Pattern 3 [.*]* [which|what] [lemma: be] [det]? [noun]+ [poss] [adj|adv]*[noun]+ [.*]*     (E.g.: What is Germany's currency?)
	
	#On 4th Feb
	# Pattern 1 [.*]* [which|what] [lemma: be]? [det]? [adv]* [adj|noun|CD]+ [.*]*      (E.g.: What is the current currency in Germany?)
	# Pattern 2 [.*]* [which|what] [lemma: be]? [det]? [adv]* [adj|noun|CD] [of ] [det]?[adj|adv]* [noun]+ [.*]*     (E.g.: What kind of currency does Germany have?)
	# Pattern 3 [.*]* [which|what] [lemma: be] [det]? [noun]+ [poss] [adj|adv]*[noun]+ [.*]*     (E.g.: What is Germany's currency?)
	# Pattern 4 When ---> Date        #only in positions 0 or 1 in the sentence
	# Pattern 5 Where --> Location    #only in positions 0 or 1 in the sentence
	# Pattern 6 Who ----> Person      #only in positions 0 or 1 in the sentence
	
	
	tid=0
	type_set=set()
	
	while tid<len(line):
		p1_flag=0
		p2_flag=0
		p3_flag=0
		p4_flag=0
		p5_flag=0
		p6_flag=0
		
		p1_flag, s1, tid1=check_pattern1(line,tid)
		p2_flag, s2, tid2=check_pattern2(line,tid)
		p3_flag, s3, tid3=check_pattern3(line,tid)
		p4_flag, s4, tid4=check_pattern4(line,tid)
		p5_flag, s5, tid5=check_pattern5(line,tid)
		p6_flag, s6, tid6=check_pattern6(line,tid)
	
		if p1_flag==1:
			if verbose:
				print "matched pattern 1"
			type_set.add(s1)
			tid=tid1
		if p2_flag==1:
			if verbose:
				print "matched pattern 2"
			type_set.add(s2)
			tid=tid2
		if p3_flag==1:
			if verbose:
				print "matched pattern 3"
			type_set.add(s3)
			tid=tid3
		
		if p4_flag==1:
			if verbose:
				print "matched pattern 4"
			type_set.add(s4)
			tid=tid4

		if p5_flag==1:
			if verbose:
				print "matched pattern 5"
			type_set.add(s5)
			tid=tid5

		if p6_flag==1:
			if verbose:
				print "matched pattern 6", line,s6,tid6
			type_set.add(s6)
			tid=tid6

		if p1_flag==0 and p2_flag==0 and p3_flag==0 and p4_flag==0 and p5_flag==0 and p6_flag==0:
			#if verbose:
			#	print "No pattern"
			break	
	
	if verbose:
		print "Set of types", type_set
	return type_set		

def process_NE_NN(sentence,verbose,nlp):
	pos=nlp.pos_tag(sentence)
	ne=nlp.ner(sentence)
	line=[]
	for term in range(0,len(pos)):
		line.append((pos[term][0],pos[term][1],ne[term][1]))
		#if verbose:
			#print ne[term][1],str(ne[term][1])
		#for c in ne[term][1]:
		#	if verbose:
				#print ord(c)

	#if verbose:
		#print "Given Sentence --->", sentence
	if verbose:
		print "\nGiven Sentence with POS tags and NE --->",line
	

	
	#Merging NEs as single term

	line1=[]
	i=0
	while i<len(line):
		if str(line[i][2])=='O':
			line1.append(line[i])
		else:
			ne_type=line[i][2]
			s=line[i][0]
			j=i+1
			skip=0
			while j<len(line):
				if str(line[j][2])=='O' or line[j][2]!=ne_type:
					line1.append((s,'NE',ne_type))
					i+=skip
					break
				else:
					s=s+' '+line[j][0]
					skip+=1
					j+=1
			#if verbose:
				#print s,ne_type,skip,i	
		i+=1		

	if verbose:
		if verbose:
			print "\nGiven Sentence with POS tags and MERGED NE--->", line1
	line=line1
	
	'''
	#Merging Consequtive Nouns not NE
	line1=[]
	i=0
	while i<len(line):
		if line[i][1][0]=='N' and line[i][1]!='NE':
			s=line[i][0]
			j=i+1
			skip=0
			while j<len(line):
				if line[j][1][0]=='N' and line[j][1]!='NE':
					s=s+' '+line[j][0]
					skip+=1
					j+=1
				else:	
					line1.append((s,line[i][1],line[i][2]))
					i+=skip
					break
		else:		
			line1.append(line[i])		
		i+=1		
	'''
	#Merging Consequtive Nouns not NE
	line1=[]
	i=0
	while i<len(line):
		if (line[i][1][0]=='N' or line[i][1][0]=='J' or line[i][1]=='CD'):# and line[i][1]!='NE':
			nflag=0
			nindex=0
			if line[i][1]=='NE':
				nflag=1
				nindex=i
			else:
				if line[i][1][0]=='N' and nflag==0:
					nflag=1
					nindex=i
			s=line[i][0]
			j=i+1
			skip=0		
						
			while j<len(line):
				if (line[j][1][0]=='N' or line[j][1][0]=='J' or line[j][1]=='CD'):# and line[j][1][0]!='':
					if line[j][1]=='NE':
						nflag=1
						nindex=j
					else:
						if line[j][1][0]=='N' and nflag==0:
							nflag=1
							nindex=j
					s=s+' '+line[j][0]
					skip+=1
					j+=1		
				else:	
					if nflag==1:
						line1.append((s,line[nindex][1],line[nindex][2])) #Dropping adjective and CD only compounds, marking as NE compound if it has an NE, otherwise noun compound
					i+=skip
					break
		else:		
			line1.append(line[i])		
		i+=1		
	if verbose:
		print "\nGiven Sentence with POS tags, merged NE and MERGED CONSEQUTIVE NOUNS--->", line1
	
	line=line1
	
	return line	

def replace_symbols(s):
	s=s.replace('(',' ')
	s=s.replace(')',' ')
	s=s.replace('[',' ')
	s=s.replace(']',' ')
	s=s.replace('{',' ')
	s=s.replace('}',' ')
	s=s.replace('|',' ')
	s=s.replace('"',' ')
	s=s.strip()
	return s	
	
def process_all_questions(ques,f22,verbose,nlp):
	s1=replace_symbols(ques)
	s2=process_NE_NN(s1,verbose,nlp)
	s3=get_answer_type(s2,verbose)
	
			
	for tp in s3:
		f22.write(str(tp.encode('utf-8'))+'\n')
	
	return	
		
					
def get_answer_type_main(question,f2,nlp):
	global verbose
	verbose=0
	f22=open(f2,'w')
		
	process_all_questions(question,f22,verbose,nlp)	
		
	f22.close()				
	return
	








































