package com.graph.scala_process1
import java.text.SimpleDateFormat
import java.util
import java.util.Calendar

import de.mpii.clausie.{ClausIE, ClausIEApp}

//import de.mpii.clausie.ClausIE

import org.apache.spark.rdd.RDD

import org.apache.spark.{SparkConf, SparkContext}

import jnerd.server._

import mpi.aidalight.rmi.{AIDALight_App}

import org.apache.spark.storage.StorageLevel


import scala.collection.JavaConversions._
import scala.collection.mutable.{ArrayBuffer, ListBuffer}

object test1 {
  def main(args: Array[String]) {

    println("*** Printing out input parameters ... ***")
    for(a <- args){
      println(a)
    }
    println("*****************************************")

    //Create a SparkContext to initialize Spark
    val conf = new SparkConf()

    //conf.setMaster("local[*]") //comment out for HPC
    conf.setAppName("BigText")


    val sc = new SparkContext(conf)
    println("Default Parallelism: "+ sc.defaultParallelism)
    println("Default MinPartitions: "+ sc.defaultMinPartitions)
    println("Local? " + sc.isLocal )
    println("Master: "+ sc.master)
    println("*** Printing out Spark Config ... ***")
    sc.getConf.getAll.foreach(println)
    println("*************************************")

    process(sc,args)


    System.exit(0)

  }

  abstract class VertexProperty () {
    def getContentShort : String
    def getContent : String
    def getVertexType : String
    def getNumber : Int
    def getEntity : String
    def getLinks : List[(String,String,String)]
    def getClauseType : String
    def getSubject : String
    def getRelation : String
    def getArgument : String
    def getAdditional : List[String]
    def getEntityType : String
    def getRoot : String
  }

  case class DocumentProperty ( val title: String, val url: String, val domain: String, val tweets : List[String] ) extends VertexProperty
  {
    override def getEntity : String = {
      ""
    }
    override def getContentShort : String = {
      title
    }

    override def getContent : String = {
      title
    }

    override def getVertexType: String = {
      "Document"
    }

    override def getNumber : Int = {
      -1
    }

    override def getLinks : List[(String,String,String)] = {
      null
    }

    override def getClauseType : String = {
      ""
    }

    override def getSubject : String = {
      ""
    }

    override def getRelation : String = {
      ""
    }

    override def getArgument : String = {
      ""
    }

    override def getAdditional: List[String] = {
      null
    }

    override def getEntityType : String = {
      ""
    }

    override def getRoot : String = {
      title
    }
  }

  case class SentenceProperty ( val nr : Int, val content: String, val links : List[(String,String,String)], val root: String) extends VertexProperty
  {
    override def getEntity : String = {
      ""
    }
    override def getContentShort : String = {
      content
    }

    override def getContent : String = {
      content
    }

    override def getVertexType: String = {
      "Sentence"
    }

    override def getNumber : Int = {
      nr
    }

    override def getLinks : List[(String,String,String)] = {
      links
    }

    override def getClauseType : String = {
      ""
    }

    override def getSubject : String = {
      ""
    }

    override def getRelation : String = {
      ""
    }

    override def getArgument : String = {
      ""
    }

    override def getAdditional: List[String] = {
      null
    }

    override def getEntityType : String = {
      ""
    }

    override def getRoot : String = {
      root
    }
  }

  case class ClauseProperty ( val content: String, val clauseType : String, val subject : String, val relation: String, val argument : String, val root : String, val additional : List[String]) extends VertexProperty
  {
    override def getEntity : String = {
      ""
    }
    override def getContentShort : String = {
      content
    }
    override def getContent : String = {
      content
    }

    override def getVertexType: String = {
      "Clause"
    }

    override def getNumber : Int = {
      -1
    }

    override def getLinks : List[(String,String,String)] = {
      null
    }

    override def getClauseType : String = {
      clauseType
    }

    override def getSubject : String = {
      subject
    }

    override def getRelation : String = {
      relation
    }

    override def getArgument : String = {
      argument
    }


    override def getAdditional: List[String] = {
      additional
    }


    override def getEntityType : String = {
      ""
    }

    override def getRoot : String = {
      root
    }

  }

  case class MentionProperty (val mention: String, val entitytype: String, val entity : String) extends VertexProperty
  {

    override def getEntity : String = {
      entity
    }
    override def getContentShort : String = {
      mention
    }
    override def getContent : String = {
      "\"" +mention + "\" which has been disambiguated as \"" +  entitytype+":"+entity + "\""
    }

    override def getVertexType: String = {
      "Mention"
    }

    override def getNumber : Int = {
      -1
    }

    override def getLinks : List[(String,String,String)] = {
      null
    }

    override def getClauseType : String = {
      ""
    }

    override def getSubject : String = {
      ""
    }

    override def getRelation : String = {
      ""
    }

    override def getArgument : String = {
      ""
    }

    override def getAdditional: List[String] = {
      null
    }


    override def getEntityType : String = {
      entitytype
    }

    override def getRoot : String = {
      ""
    }
  }


  case class EntityProperty (val entity: String) extends VertexProperty
  {
    override def getEntity : String = {
      entity
    }

    override def getContentShort : String = {
      entity
    }
    override def getContent : String = {
      "\"" +entity + "\" "
    }

    override def getVertexType: String = {
      "Entity"
    }

    override def getNumber : Int = {
      -1
    }

    override def getLinks : List[(String,String,String)] = {
      null
    }

    override def getClauseType : String = {
      ""
    }

    override def getSubject : String = {
      ""
    }

    override def getRelation : String = {
      ""
    }

    override def getArgument : String = {
      ""
    }

    override def getAdditional: List[String] = {
      null
    }


    override def getEntityType : String = {
      ""
    }

    override def getRoot : String = {
      ""
    }
  }


  def getStringRepresentation(id: Long, vertex: VertexProperty) : String = {
    val vertexType = vertex.getVertexType
    vertexType match {
      case "Document" =>
        val title = vertex.getContent
        val url = ""
        val domain = ""
        val tweets = List()
        vertexType + "\t" + id + "\t" + title + "\t" + url + "\t" + domain + "\t" + tweets + " $END$"
      case "Sentence" =>
        val content = vertex.getContent
        val sentenceNr = vertex.getNumber
        val links = vertex.getLinks
        val root = vertex.getRoot
        var s = vertexType + "\t" + id + "\t" + sentenceNr + "\t" + content + "\t" + root +"\t"
        links.foreach(link => s = s + link._1 + "\t" + link._2 + "\t" + link._3 + "\t")
        s + " $END$"
      case "Clause" =>
        val content = vertex.getContent
        val clauseType = vertex.getClauseType
        val subject = vertex.getSubject
        val relation = vertex.getRelation
        val argument = vertex.getArgument
        val root = vertex.getRoot
        val additional = vertex.getAdditional
        var s = vertexType + "\t" + id + "\t" + content + "\t" + clauseType + "\t" + subject + "\t" + relation + "\t" + argument + "\t" + root + "\t"
        additional.foreach(argument => s = s + argument + "\t")
        s +" $END$"
      case "Mention" =>
        val mention = vertex.getContentShort
        val entityType = vertex.getEntityType
        val entity = vertex.getEntity
        vertexType + "\t" + id + "\t" + mention + "\t" + entityType + "\t" + entity + " $END$"
      case "Entity" =>
        val entity = vertex.getContentShort
        vertexType + "\t" + id + "\t" + entity + " $END$"

    }
  }


  def parseHeader(line: String): Array[String] = {
    try {
      var s = line.substring(line.indexOf("id=\"") + 4)
      val id = s.substring(0, s.indexOf("\""))
      s = s.substring(s.indexOf("url=\"") + 5)
      val url = s.substring(0, s.indexOf("\""))
      s = s.substring(s.indexOf("title=\"") + 7)
      val title = s.substring(0, s.indexOf("\""))
      Array(id, url, title)
    } catch {
      case e: Exception => Array("", "", "")
    }
  }

  def parse(lines: Array[String]): Array[(String, String)] = {
    var docs = ArrayBuffer.empty[(String, String)]
    var title = ""
    var content = ""
    for (line <- lines) {
      try {
        if (line.startsWith("<doc ")) {
          title = parseHeader(line)(2)
          content = ""
        } else if (line.startsWith("</doc>")) {
          if (title.length > 0 && content.length > 0) {
            docs += ((title, content))
          }
        } else {
          content += line + "\n"
        }
      } catch {
        case e: Exception => content = ""
      }
    }
    docs.toArray
  }



  def getReadableTime(nanos: Long): String = {
    val tempSec = nanos/(1000*1000*1000)
    val sec = tempSec % 60
    val min = (tempSec /60) % 60
    val hour = (tempSec /(60*60)) % 24
    val day = (tempSec / (24*60*60)) % 24
    day + " d "+ hour + " h " + min + " m " + sec +" s"
  }


  def process(sc: SparkContext, args : Array[String]): Unit = {
    val t0 = System.nanoTime()

    val sampleSize = args(1).toDouble

    //Server & Port
    val host = args(2)
    val port = args(3).toInt

    println(host + " --- "+port)

    //Number of partitions
    val numberPartitions = args(4).toInt

    //Job ID
    val jobId = args(5)
    //Document path
    val docpath = args(6)

    val textFiles = sc.wholeTextFiles(docpath,numberPartitions).sample(false, sampleSize)


    val DocSentences = textFiles.flatMap{ case (url,text) => parse(text.split("\n"))}
    //rdd of the form [VertexProperty, List[VertexProperty]]
    //    //in this case the 1st value is DocumentProperty(which extends VertexProperty)
    //    //the 2nd value is a list of SentenceProperty (Representing the sentences of the document)
    val rddDocSentences = DocSentences.map(x => {
      val docProp = DocumentProperty(x._1,"","",List.empty[String])
      val listSentenceProperty = new ListBuffer[SentenceProperty]
      var sentenceNumber = 1
      val content = x._2
      val contentWithOutTitle = content.substring(x._2.indexOf("\n"),content.length)

      val sentences = new edu.stanford.nlp.simple.Document(contentWithOutTitle).sentences()
      for(sentence <- sentences){
        //replaceAll is to remove linebreaks in a sentence.
        listSentenceProperty.append(SentenceProperty(sentenceNumber, sentence.text().replaceAll("[\n\r]", " "), List.empty[(String,String,String)],x._1))
        sentenceNumber += 1
      }
      (docProp,listSentenceProperty.toList)
    }).repartition(numberPartitions)


    //FlatMap the value of DocSentences and repartition the data
    //( (Doc1, [S1,S2,S3]) , .... ) => ( (Doc1,S1), (Doc1,S2), (Doc1, S3), ...)
    val rddDocSentencesPartitioned = rddDocSentences.flatMapValues(x => x.map(s => s)).repartition(numberPartitions)

    rddDocSentencesPartitioned.persist(StorageLevel.MEMORY_AND_DISK)

    //Disambiguation Tool
    // 0 = JNERD, 1 = AIDALight
    val tool = 1

    //Context range parameter
    val contextRange = 3

    //Export the GraphRDD
    val exportGraphRDD = true

    //Selection of KB
    //0 : KB used by AIDALIGHT
    val kbSelection = 0

    //DocumentProperties
    //rdd of the form [VertexProperty, List[VertexProperty]]
    //in this case the 1st value is DocumentProperty(which extends VertexProperty)
    //the 2nd value is an empty List since a Document node does not have any parent nodes
    val rddDocumentPropertiesParentNodes: RDD[(VertexProperty, List[VertexProperty])] = rddDocSentences.map(x => (x._1, List()))

    //SentenceProperties
    //rdd of the form [VertexProperty, List[VertexProperty]]
    //in this case the 1st value is a SentenceProperty(which extends VertexProperty)
    //the 2nd value is a list containing 1 DocumentProperty (representing the Document containing this sentence)
    val rddSentencePropertiesParentNodes: RDD[(VertexProperty, List[VertexProperty])] = rddDocSentences.flatMap(x => x._2.map(s => (s, List(x._1))))

    //ClauseProperties
    //Initialize a new ClauseIE application
    val clauseIE = new ClausIEApp
//    val clauseIE = new ClausIE
    //rdd of the form (SentenceProp,List[ClauseProp])
    //1st value is a SentenceProperty
    //2nd value is a list containing ClauseProperties (representing the extracted clauses from this sentence)
    val rddSentenceToClauses: RDD[(VertexProperty, List[VertexProperty])] =
    rddDocSentencesPartitioned.map(
      element => {
        val sentenceContent = element._2.getContent
        val clauses = clauseIE.getClauses(sentenceContent)
        val clauseProperties = new ListBuffer[ClauseProperty]
        clauses.foreach(proposition => {
          val clauseType = proposition.getType
          val subject = proposition.subject().replace(" '", "'")
          val relation = proposition.relation().replace(" '", "'")
          var argument = ""
          val additional = new ListBuffer[String]

          if (proposition.noArguments() >= 1) {
            argument = proposition.argument(0).replace(" '", "'")
            for(i <- 1 to proposition.noArguments()-1){
              additional += proposition.argument(i).replace(" '", "'")
            }

          }
          clauseProperties.append(ClauseProperty(proposition.toString.replace(" '", "'"), clauseType, subject, relation, argument, element._2.getRoot+"-"+element._2.getNumber, additional.toList))
        })
        (element._2, clauseProperties.toList.distinct) //Remove duplicate clauses
      })

    rddSentenceToClauses.persist(StorageLevel.MEMORY_AND_DISK)

    //rddSentenceToClauses.foreach(println(_))

    //Pair RDD, Key : Clause-Vertex, Value : List of Parent Vertices (Parent is a single Sentence Vertex)
    //1st value is a ClauseProperty
    //2nd value is a list containing 1 SentenceProperty (representing the sentence that contains this clause)
    val rddClausePropertiesParentNodes: RDD[(VertexProperty, List[VertexProperty])]
    = rddSentenceToClauses.flatMap(x => x._2.map(clause => (clause, List(x._1))))
    //persist this RDD since it will be used for the next transformation
    rddClausePropertiesParentNodes.persist(StorageLevel.MEMORY_AND_DISK)


    //Initialize a new AIDALIGHT application
    val aidaLightApp = new AIDALight_App


    //Mentions RDD : [(SentenceProp1, [MentionProp1, MentionProp2]), (SentenceProp2, [MentionProp3]), ... ]
    //RDD of the form (SentenceProp,List[MentionProp])
    //1st value is a SentenceProperty
    //2nd value is a list containing MentionProperties (representing the mentions contained in a sentence)

    val rddSentenceToMentions: RDD[(VertexProperty, List[VertexProperty])] =
    //sc.parallelize(Seq((new SentenceProperty(1, "hi", List.empty[(String,String,String)]),List(new MentionProperty("a","b","c")))))
      rddDocSentences.map(x => {
        var contextCounter = 1
        var contextMap: java.util.Map[Integer, String] = new util.HashMap()
        val sentencePropContextMap = new ListBuffer[VertexProperty]
        val listSentEntities: util.List[BigTextSentence] = new util.ArrayList[BigTextSentence]
        val listSentPropEntities: util.List[(VertexProperty, List[VertexProperty])] = new util.ArrayList[(VertexProperty, List[VertexProperty])]

        //Create Variable to store the first sentence of a document (Used in order to add some context for the disambiguation)
        var firstSentence = SentenceProperty(0,"",null,"")
        //Check if the document contains a sentence
        if(x._2.filter(x => x.getNumber == 1).length != 0){
          //Assign the first sentence to the variable
          //firstSentence = x._2.filter(x => x.getNumber == 1).last
          firstSentence = SentenceProperty(0,"This document is about "+x._1.title+".",null,"")
        }

        sentencePropContextMap.append(SentenceProperty(0, firstSentence.getContent, firstSentence.getLinks,firstSentence.getRoot))
        x._2.foreach(element => {
          if (contextCounter < contextRange && (element != x._2.last)) {
            contextCounter += 1
            sentencePropContextMap.append(element)
          } else {
            sentencePropContextMap.append(element)

            sentencePropContextMap.foreach(element => contextMap += ((element.getNumber, element.getContent)))

            contextMap.foreach(println(_))


            tool match {
              case 0 => //listSentEntities = jnerdApp.callJNERD(contextMap, null)
              case 1 =>
                aidaLightApp.callAIDALight(contextMap,null, host, port).foreach(element => listSentEntities.add(element))
            }

            listSentEntities.foreach(element => {
              val sentenceNumber = element.getSentenceNumber
              val sentenceContent = element.getSentenceContent
              sentencePropContextMap.foreach(sentence => {
                if (sentence.getNumber == sentenceNumber && sentence.getContent.equals(sentenceContent)) {
                  val mentions = element.getEntities
                  val mentionPropertyList = new ListBuffer[VertexProperty]
                  mentions.foreach(e => {
                    val mention = e.getMention
                    val entityType = e.getType
                    val entity = e.getEntity
                    mentionPropertyList.append(MentionProperty(mention, entityType, entity))
                  })
                  listSentPropEntities.append((sentence, mentionPropertyList.toList))
                }
              })
            })

            contextCounter = 1
            contextMap.clear()
            sentencePropContextMap.clear()
            sentencePropContextMap.append(SentenceProperty(0, firstSentence.getContent, firstSentence.getLinks,firstSentence.getRoot))

          }
        })
        listSentPropEntities.toList
      }).flatMap(element => element.map(x => x))

    rddSentenceToMentions.persist(StorageLevel.MEMORY_AND_DISK)

    //From : RDD = [(SentenceProp1, [MentionProp1, MentionProp2]), (SentenceProp2, [MentionProp3]), ... ]
    //To : RDD = [(MentionProp1, [SentenceProp1]), (MentionProp2, [SentenceProp1]), (MentionProp3, [SentenceProp2])]
    //1st value is a MentionProperty
    //2nd value is a list containing 1 SentenceProperty (representing the sentence that contains this mention)
    val rddMentionPropertiesAndSentenceProp: RDD[(VertexProperty, List[VertexProperty])] = rddSentenceToMentions.flatMap(x => x._2.map(mention => (mention, List(x._1))))

    //Pair RDD, Key : Mention-Vertex, Value : List of Parent Vertices (Parent is a single Clause Vertex)
    //1st value is a MentionProperty
    //2nd value is a list containing 1 ClauseProperty (representing the clause that contains this mention)
    val rddMentionPropertiesParentNodes: RDD[(VertexProperty, List[VertexProperty])] = rddClausePropertiesParentNodes.map(x => (x._2, x._1))
      .join(rddMentionPropertiesAndSentenceProp.map(x => (x._2, x._1)))
      .map(x => x._2)
      .filter(x => {
        var inAdditional = false
        for(i <- 0 until x._1.getAdditional.size){
          if(x._1.getAdditional(i).contains(x._2.getContentShort)){
            inAdditional = true
          }
        }
        x._1.getSubject.contains(x._2.getContentShort) || x._1.getRelation.contains(x._2.getContentShort) || x._1.getArgument.contains(x._2.getContentShort) || inAdditional
      })
      .map(x => (x._2, List(x._1)))


    rddSentenceToMentions.unpersist()

    //Persist this RDD, because its is needed for a couple of times
    rddMentionPropertiesParentNodes.persist(StorageLevel.MEMORY_AND_DISK)

    //Entity Properties
    //Pair RDD, Key : Entity-Vertex, Value : List of Parent Vertices (Parents are multiple Mention Vertices)
    //1st value is a EntityProperty
    //2nd value is a list containing MentionProperties (representing the mentions that are resolved to that entity)
    val rddEntityPropertiesParentNodes: RDD[(VertexProperty, List[VertexProperty])]
    = rddMentionPropertiesParentNodes.map(x => (EntityProperty(x._1.getEntity), x._1))
      .combineByKey(x => List(x), (acc : List[VertexProperty],x) => acc.::(x) , (acc1 : List[VertexProperty],acc2 : List[VertexProperty]) => acc1.union(acc2))      //.groupByKey().
      .filter(x => !x._1.getContentShort.equals("--NME--")).map(x => (x._1, x._2.toList.distinct))



    var rddAllPropertiesParentNodes: RDD[(VertexProperty, List[VertexProperty])] = null

    kbSelection match {
      case 0 =>
        rddAllPropertiesParentNodes = rddDocumentPropertiesParentNodes.union(rddSentencePropertiesParentNodes)
          .union(rddClausePropertiesParentNodes).union(rddMentionPropertiesParentNodes).union(rddEntityPropertiesParentNodes)

    }


    rddClausePropertiesParentNodes.unpersist()
    rddMentionPropertiesParentNodes.unpersist()
    rddAllPropertiesParentNodes.persist(StorageLevel.MEMORY_AND_DISK)//.foreach(println(_))


    val today:java.util.Date = Calendar.getInstance.getTime
    val timeFormat = new SimpleDateFormat("yyyy-MM-dd-HH-mm-ss")
    val now:String = timeFormat.format(today)
    rddAllPropertiesParentNodes.map(element => {
      val child = element._1
      val parents = element._2

      val childString = getStringRepresentation(0,child)
      var parentsString = ""
      parents.foreach(f => parentsString = parentsString + getStringRepresentation(0,f)+ " ")
      (childString,parentsString)

    })//.saveAsTextFile("/home/users/pmeder/BigText_alpha/output/RDDtoString"+now+"-"+jobId+"/")
      .saveAsTextFile("./output/RDDtoString"+now+"-"+jobId+"/")
    //Save the RDD as  text file


    val t1 = System.nanoTime()
    println("Elapsed time: " + (t1 - t0) + "ns")
    println(getReadableTime(t1-t0))
  }

}


