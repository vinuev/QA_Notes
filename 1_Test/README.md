`MacOS`,`Anaconda 3`,`Jupyter Nootbook`, `python 2.7`, `hadoop 3.1.2`, `scala 2.12.8`, `apache-spark 2.4.1`, 

- 1. Install spark, scala hadoop
      ```
      brew install apache-spark
      brew install scala
      brew install hadoop
      ```
- 2. enviroment variables

  - 1. Open `.zshrc`

    `vim ~/.zshrc`

  - 2. write & save
    ```
    #JAVA_HOME
    export JAVA_HOME=$(/usr/libexec/java_home)

    #Hadoop
    export HADOOP_HOME=/usr/local/Cellar/hadoop/3.1.2
    export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin

    #SCALA_HOME
    export SCALA_HOME=/usr/local/Cellar/scala/2.12.8
    export PATH=$PATH:$SCALA_HOME/bin

    #SPARK_HOME
    #export SPARK_HOME=/usr/local/Cellar/apache-spark/2.4.1
    #export PATH=$PATH:$SPARK_HOME/bin

    #pyspark
    export PYSPARK_DRIVER_PYTHON="jupyter"
    export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
    export PYSPARK_PYTHON=python2

    # Launch the jupyter server.
    pyspark --jars graphframes-0.7.0-spark2.4-s_2.11.jar

    #python
    #export PATH="/usr/local/anaconda3/bin:$PATH"
    ```
  - 3. execute `.zshrc`
    `source ~/.zshrc`

- 3. Build the anoconda virtual environment `python 2.7`
[Reference](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)

- 4. Install packages 
      ```
      pip install requests
      pip install BeautifulSoup`
      pip install networkx
      pip install matplotlib
      pip install numpy
      pip install stanfordcorenlp
      pip install gensim
      pip install graphframes
      ```
- 5. Download corresponding GraphFrame `jar` 
from [jar](https://dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/)
And save it at corresponding spark file. In my computer: "/usr/local/Cellar/apache-spark/2.4.1/libexec/jars"

- 6. type `pyspark` in terminal and start to test using jupyter
