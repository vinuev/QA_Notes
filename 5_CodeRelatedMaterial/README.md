## Run process.scala on HPC
### 0. Run AIDA Server
1. Upload AIDA Server file on HPC by `rsync -avzu <source file path> iris-cluster:<destination path>`
2. Modify the path to openning the path of AIDA in `launcher.Server.sh` "cd ..."
3. `sbatch launcher.Server.sh`

### 1. Install EasyBuild on HPC (if you have easybuild in HPC, ignore this step)
Find the steps at [EasyBuild](https://ulhpc-tutorials.readthedocs.io/en/latest/tools/easybuild/)

### 2. Run Install Spark (if you have Spark in HPC, ignore this step)
	##apply nodes
	srun -p interactive -N 1 -n 1 -c 28 -t 1:00:00 --pty bash
	
	##check spark version and install
	eb -S Spark
	time eb Spark-2.3.0-Hadoop-2.7-Java-1.8.0_162.eb -r
	
	##Check the installed software:
	module av Spark
	module spider Spark

### 3. Run `process.scala`
1. Upload .jar files to HPC(find it at 'lib' file)
2. Check the `protobuf-java.jar` file in `/home/users/jxu/.local/easybuild/software/Spark/2.3.0-Hadoop-2.7-Java-1.8.0_162/jars/`, replace it with `protobuf-java-3.2.0.jar`
3. Find `IP` address at the `.out` file of AIDA Serve, modify the `arguments` and `IP` in `process.scala` file

		#apply for nodes
		srun -p interactive -N 1 -n 1 -c 28 -t 4:00:00 --pty bash
		
		#load Spark
		module use $LOCAL_MODULES
		module load devel/Spark/2.3.0-Hadoop-2.7-Java-1.8.0_162
		
		#run with command
		spark-shell --conf spark.driver.memory=30g \
		--conf spark.executor.memory=100g \
		--conf spark.default.parallelism=55 \
		--jars lib/ClausIE.jar,lib/aidalight-backup.jar,lib/jnerd.jar,lib/stanford-corenlp-3.9.2-sources.jar,lib/stanford-corenlp-3.9.2.jar,lib/jopt-simple-4.4.jar,lib/protobuf-java-3.2.0.jar \
		-i ./process_test1.scala



