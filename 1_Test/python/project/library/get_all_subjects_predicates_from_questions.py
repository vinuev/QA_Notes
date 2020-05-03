import sys
from stanfordcorenlp import StanfordCoreNLP



def get_entities(sent,verbose):
	line=sent	

	#Replacing Personal and Possesive pronouns by nearest NE at their left. If no match, go to the previous lines
	pro_list=set()
	for l in open('pronoun_list.txt'):
		l=l.strip()
		pro_list.add(l.lower())

	if verbose:
		print "\nPronoun List--->",pro_list	

	
	line1=[]
	i=0
	while i<len(line):
		#if line[i][1]=='PRP' or line[i][1]=='PRP$': #Matching pronouns from the POS tags
		if line[i][0].lower() in pro_list:
			j=i-1
			flag1=0
			flag2=0
			while j>=0:
				if line[j][1]=='NE' and line[j][2]=='PERSON' and flag1==0: #First NE at left which is Person
					flag1=1
					s=line[j]
					break
				if line[j][1]=='NE' and flag2==0: #First NE at left
					flag2=1
					s1=line[j]	
				j=j-1
				
				
			
			if flag1==1:	#Found NE
				line1.append(s)
			else:
				if flag2==1:
					line1.append(s1)	
				else:			
					line1.append(line[i])
		else:		
			line1.append(line[i])		
		i+=1		
	if verbose:	
		print "\nGiven Sentence with POS tags, merged NE, merged consequtive nouns and pronouns replaced by nearest preceeding NEs--->", line1
	line=line1



	#Find X...V...Y type of triples where X, Y are NE or noun phrases; V is verb or verb+preposition. If V is auxiliary verb like be, am, being, been, is, are, was, were, has, have, had, do, did, done, 
	#doing, having, will, shall,..., do the Following - (a) if only auxiliary verb, then consider as predicate , (b) if followed immediately by main verb, then drop auxiliary verb
	#Get complete list of auxiliary verbs from:  https://en.wikipedia.org/wiki/Auxiliary_verb#List_of_auxiliaries_in_English

	aux_list=set()
	for l in open('auxiliary_verb_list.txt'):
		l=l.strip()
		aux_list.add(l.lower())

	if verbose:
		print "\nAuxiliary Verb List--->",aux_list	


	#Mark the terms as predicates (P) and subjects (S) and other terms as Unimportant (U)

	entities=set()
	line1=[]
	i=0
	while i <len(line):
		if line[i][1]=='NE':
			line1.append((line[i][0],line[i][1],line[i][2],'S'))
			entities.add((line[i][0],'NE'))
		else:
			if line[i][1][0]=='N':
				if i+1<len(line) and line[i+1][1]=='IN': #predicate N+P
					s=line[i][0]+' '+line[i+1][0]
					new_type=line[i][1]+'_'+line[i+1][1]
					line1.append((s,new_type,line[i][2],'P'))
					entities.add((s,'P'))
					i+=1
				
				else:
					line1.append((line[i][0],line[i][1],line[i][2],'S'))	
					entities.add((line[i][0],'S'))			
			else:
				if line[i][1][0]=='V':
					if line[i][0].lower() in aux_list: #IF it is an auxiliary verb
						s=line[i][0]
						new_type=line[i][1]
						j=i+1
						while j<len(line) and line[j][1][0]=='V' and line[j][0].lower() in aux_list:
							s=s+' '+line[j][0]
							new_type=line[j][1] 		
							j+=1
						
						if j<len(line) and line[j][1][0]=='V': #Got a main verb, use that in stead of auxiliaries
							s=line[j][0]	
							new_type=line[j][1]
							j+=1
					else:
						s=line[i][0]
						new_type=line[i][1]
						j=i+1
					
					if j<len(line) and line[j][1]=='IN': #Checking for following preposition				
						s+=' '+line[j][0]
						new_type+='_'+line[j][1]
						line1.append((s,new_type,line[i][2],'P'))
						entities.add((s,'P'))
						j+=1
					else:
						line1.append((s,new_type,line[i][2],'P'))
						entities.add((s,'P'))

					i=j-1
			
				else:
					line1.append((line[i][0],line[i][1],line[i][2],'U'))		
		i+=1
	if verbose:
		print "\n\nSentence with marked Subjects (S), Predicates (P) and Unimportants (U) --->",line1	
					
	return entities	




def process_NE_NN(sentence,verbose,nlp):
	#pos=nlp.pos_tag(sentence)
	try:
		pos=nlp.pos_tag(sentence)
	except:
		print "Pos not found for ",sentence
		return []
		
	try:
		ne=nlp.ner(sentence)
		ne_flag=1
	except:
		ne_flag=0
		
	line=[]
	for term in range(0,len(pos)):
		if ne_flag==1:
			line.append((pos[term][0],pos[term][1],ne[term][1]))
		else:
			line.append((pos[term][0],pos[term][1],'O'))
		#print ne[term][1],str(ne[term][1])
		#for c in ne[term][1]:
		#	print ord(c)

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
			
			if j>=len(line):
				line1.append((s,'NE',ne_type))
				i+=skip
					 
			#print '\nNE ',s,ne_type,skip,i	
		i+=1
		#print '\nNE ',		

	if verbose:
		print "\nGiven Sentence with POS tags and MERGED NE--->", line1
	line=line1
	
	#Merging Consequtive Nouns,NE,CD,JJ
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
				if (line[j][1][0]=='N' or line[j][1][0]=='J' or line[j][1]=='CD'):# and line[j][1][0]!='NE':
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
			if j>=len(line):
				if nflag==1:
					line1.append((s,line[nindex][1],line[nindex][2])) #Dropping adjective and CD only compounds, marking as NE compound if it has an NE, otherwise noun compound
				i+=skip		
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
	s3=get_entities(s2,verbose)
	
			
	for ent in s3:
		f22.write(ent[0].encode('utf-8')+' '+ent[1]+'\n')
	
	return	
	
					
def get_sub_pred_ques_main(question,f2,nlp):
	verbose=0
	f22=open(f2,'w')
		
	process_all_questions(question,f22,verbose,nlp)	
		
	f22.close()				
	return
	
	
		
	
	






































