# Build Graph
# graphframe
sc.addPyFile('/usr/local/Cellar/apache-spark/2.4.1/libexec/jars/graphframes-0.7.0-spark2.4-s_2.11.jar')

# modules
import sys
from graphframes import *
import pyspark.sql.functions as f
from pyspark.sql.functions import lit

# library 
sys.path.append("project/library")
import get_answer_types_from_questions as gtQType
import get_all_subjects_predicates_from_questions as gtQSub
from stanfordcorenlp import StanfordCoreNLP

# config
verbose = 0
nlp = StanfordCoreNLP(r'/Users/jeanxu/PycharmProjects/QUEST_TerminalTest/Code/stanford-corenlp-full-2018-10-05')
prune = 5
question = 'when is national day of England'

# Extracting potential answer type from question
f1 = 'question_type.txt'
gtQType.get_answer_type_main(question,f1,nlp)

# Extracting query terms from question.
s1 = 'question_subject_predicate.txt'
gtQSub.get_sub_pred_ques_main(question,s1,nlp)
aux_list = set()
for l in open('auxiliary_verb_list.txt'):
    l = l.strip()
    aux_list.add(l.lower())

# Read entities of question
s11 = open(s1, 'r')
q_ent = set()
type_qent = {}
for line in s11:
    line = line.strip()
    line = line.split()
    s = line[0]
    for i in range(1, len(line) - 1):
        s += ' ' + line[i]
    q_ent.add(s.lower())
    type_qent[s.lower()] = line[len(line) - 1]
if verbose:
    print "Query terms ->", len(q_ent), q_ent
if len(q_ent) > prune:
    if verbose:
        print "Pruning.."
    p = frozenset(q_ent)
    for s in p:
        if type_qent[s] == 'P':
            q_ent.remove(s)

if verbose:
    print "Without Predicate Query terms ->", len(q_ent), q_ent

p = frozenset(q_ent)
for s in p:
    if s in aux_list and type_qent[s] == 'P':
        q_ent.remove(s)

if verbose:
    print "Without Auxiliary Query terms ->", len(q_ent), q_ent

# file path
File_verticesTextRDD = "/Users/jeanxu/Documents/UniLU/0_MasterThesis/4_Spark/ReferenceFromPaul/Graph-Small/Vertices/part-*"
File_edgesTextRDD = "/Users/jeanxu/Documents/UniLU/0_MasterThesis/4_Spark/ReferenceFromPaul/Graph-Small/Edges/part-*"

######### load vertices
verticesText0 = spark.read.csv(File_verticesTextRDD, header='false', inferSchema='false', sep='\t')

verticesText1 = verticesText0.select("_c1","_c0","_c2","_c3","_c4")\
.withColumnRenamed("_c0", "nodeType").withColumnRenamed("_c1", "id")\
.withColumnRenamed("_c2", "attr1").withColumnRenamed("_c3", "attr2")\
.withColumnRenamed("_c4", "attr3")

######### load edges
edgesText0 = spark.read.csv(File_edgesTextRDD)
edgesText0 = edgesText0.select(f.translate(f.col("_c0"), "Edge(", "").alias("src"), "_c1", f.translate(f.col("_c2"), ")", "").alias("label"))
edgesText1 = edgesText0.select("*").withColumnRenamed("_c1", "dst")
verticesText1J = verticesText1

edgesText2 = edgesText1.join(verticesText1.select("id","nodeType"), edgesText1.src == verticesText1.select("id","nodeType").id, "inner")
edgesText2 = edgesText2.withColumnRenamed("id", "src_id").withColumnRenamed("nodeType", "src_nodeType")
edgesText3 = edgesText2.join(verticesText1.select("id","nodeType"), edgesText2.dst == verticesText1.select("id","nodeType").id, "inner")
edgesText3 = edgesText3.withColumnRenamed("id", "dst_id").withColumnRenamed("nodeType", "dst_nodeType")

######### documnet vertice & edges
### documnets---attributes
doc_verticesText = verticesText1.filter("nodeType = 'Document'")
doc_verticesText = doc_verticesText.withColumn("did", doc_verticesText.id).withColumn("dtitle", doc_verticesText.attr1).drop("attr1").drop("attr2").drop("attr3")

### sentence---attributes
# sen_verticesText = verticesText1.filter("nodeType = 'Sentence'")
sen_edges = edgesText3.filter("label = 'contains the sentence'")
sen_verticesTextJ_test = verticesText1.filter("nodeType = 'Sentence'")
sen_edgesJ = sen_edges.select("src_id","src_nodeType","dst_id","dst_nodeType")
# conbine src_id
sen_edgesJ_test1 = sen_edgesJ.join(doc_verticesText, sen_edgesJ.src_id==doc_verticesText.id,"inner")
sen_edgesJ_test1 = sen_edgesJ_test1.drop("id").drop("nodeType")
# conbine dst_id
sen_verticesTextJ_test1 = sen_edgesJ_test1.join(sen_verticesTextJ_test,sen_edgesJ_test1.dst_id==sen_verticesTextJ_test.id,"inner")
sen_verticesTextJ_test2 = sen_verticesTextJ_test1.drop("attr2").drop("attr3")
sen_verticesText = sen_verticesTextJ_test2.drop("src_id").drop("src_nodeType").drop("dst_id").drop("dst_nodeType")
sen_verticesText = sen_verticesText.withColumnRenamed("attr1","sid")
sen_verticesText = sen_verticesText.select("id","nodeType","did","dtitle","sid")


### clause---attributes
clause_verticesText_test = verticesText1.filter("nodeType = 'Clause'")
clause_edges = edgesText3.filter("label = 'contains the clause'")
# combine dst_id
clause_verticesTextJ_test = clause_verticesText_test.join(clause_edges.select("src_id","src_nodeType","dst_id","dst_nodeType"), clause_verticesText_test.id==clause_edges.dst_id, "inner")
clause_verticesTextJ_test = clause_verticesTextJ_test.drop("src_nodeType").drop("dst_id").drop("dst_nodeType")
# combine src_id
clause_verticesText_test1 = clause_verticesTextJ_test.join(sen_verticesTextJ.select("senid","did","dtitle","sid"), clause_verticesTextJ_test.src_id==sen_verticesTextJ.senid, "inner")
clause_verticesText_test2 = clause_verticesText_test1.drop("attr2").drop("attr3").drop("src_id").drop("sen_id")
clause_verticesText = clause_verticesText_test2
## change clause to predicate
clause_verticesText1 = clause_verticesText.withColumn("attr1", f.split(clause_verticesText['attr1'], ","))
predicate_verticesText = clause_verticesText.withColumn("predicate", f.split("attr1", ",")[1])
predicate_verticesText1 = predicate_verticesText.select("*", f.translate(f.col("predicate"), "[\"()]", "").alias("predicate1"))
predicate_verticesText2 = predicate_verticesText1.withColumn("nodeType1",f.lit("Predicate"))
predicate_verticesText = predicate_verticesText2.select("id","nodeType1","did","dtitle","sid","predicate1")
#add predicate alignment edge (to do)





### mention---mention edges
entity_edges = edgesText3.filter("label = 'is disambiguated as'")
NewMentionEdges = entity_edges.groupBy("dst_id").agg(f.collect_list('src_id').alias('NewMentionEdges'))
NewMentionEdges = NewMentionEdges.withColumnRenamed("NewMentionEdges","Mention")
NewMentionEdges = NewMentionEdges.select("Mention")
NewMentionEdges = NewMentionEdges.withColumn("Mention1",NewMentionEdges.Mention)
NewMentionEdgesJ = NewMentionEdges.withColumn("Mention1", f.explode("Mention1"))

NewMentionEdgesJ1 = NewMentionEdgesJ.withColumn("Mention", f.explode("Mention"))
NewMentionEdgesJ2 = NewMentionEdgesJ1.filter(NewMentionEdgesJ1.Mention!=NewMentionEdgesJ1.Mention1)

# add type by HP (couldn't find it use sentence, drop this type temporarily)
# add mention NE_type by NER (to do)
# mention alignment

# add weight and maxword (to do)
# generate cornerstone (to do)


