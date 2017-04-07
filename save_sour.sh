#cp *.py /jenkins/test/workspace/load_L2/cluster
cp fuselog/*.py /jenkins/test/workspace/load_L2/cluster
cp report/*.py /jenkins/test/workspace/load_L2/cluster
cp readme /jenkins/test/workspace/load_L2/cluster
cp *.sh /jenkins/test/workspace/load_L2/cluster
cd /jenkins/test/workspace/load_L2/cluster&&git add *
cd /jenkins/test/workspace/load_L2/cluster&&git commit -m "$1"

