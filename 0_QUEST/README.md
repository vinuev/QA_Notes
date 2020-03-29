
### 0. Extract SPO Triples
		0.0 Retrieve
			1.0 Relavented documents:10 docs ( Crawl Data from Google with ``requests``, ``beautiful soup``)
			1.1 Entire question: key words from question
			1.2 Indentify cues in match docs & join them across multiple documents: 
				 Patter-based extraction: POS tagging & NER on setences from documents.
				 - V-p triple: NE/NP, X V Y, POS patter V / V + proposition
				 - N-p triple: NE/NP, X N Y, POS patter N / N + proposition

		0.1 Scoring S-P-O
			- d1: 1 / distance(S, P)
			- d2: 1 / distance(P, O) 

### 1. Build KG 
		1.0 Nodes 
			- Entity Nodes: S/O
			- Ralation Nodes: P
			- Type Nodes: method - Hearst pattern
			
		1.1 Edges
			- Triple Edges: S-P, P-O
			- Type Edges: entity - "type" - correspoding type
			
		1.2 Alignment:
			( Entity-mention dictionary / Parapharase DB / Word, Phrase embedding )
			- Entity alignment: silimarity
			- Relation alignment:
			
		1.3 Weight
			1.3.0 Nodes Weight: ( similarity score with token )
				- Entity Nodes: threshold similarity ( 5.3 )
				- Type / Relation Nodes: Higest score with questions' tokens ( Word2Vector / Glove / BERT embedding	)
				
			1.3.1 Edges Weight
				- Triple Edges: Confindence score ( see ``0.1 Scoring S-P-O``)
				- Alignment Edges: Similarity between two Entity Nodes / Relation Nodes (5.3)
				- Type Edges: 1.0
					
			
### 2. Graph Algorithm
[Steiner Tree in Graph — Explained](https://medium.com/@rkarthik3cse/steiner-tree-in-graph-explained-8eb363786599)

[Efficient and Progressive Group Steiner Tree Search](https://ronghuali.github.io/paper/sigmod2016gst.pdf)

		2.0 Compute GST
			2.0.0 Cornerstones 
			Indentify the pivotal nodes by similarity ( Compare with the word/ parase in Questions, Score >= threshold) 
				- Entity Node: method - lexicons
				- Relation Nodes: method - Word2Vector
				
			2.0.1 GST ( compare answer with many cornerstones )
				- Factors: answer lie on path / short path / path with higer weight
			
			2.0.2 Algorithm
				- Start from terminal, tree is grown by adding leatest cost from neibor
				- Trees are mergerd whrn common vertices
				- Priority queue ( Fibonacci heap ) holds all trees in increase order of tree cost, process stop when a tree is found cover all terminals. 
				- ( GST-k )

### 3. Filter & Ranking Answer
		3.0 Answer filter
			- Remove not irrelevant entities （ type checking ）
			- Infer expected-answer type ( compare cosine similarity between two Word2Vector embedding - nodes )
		3.1 Answer aggregation
			- Token 
			- Allignment
		3.2 Answer Scoring
			- Sum weight ( sec. 7 )
			 
### 3. Evaluation