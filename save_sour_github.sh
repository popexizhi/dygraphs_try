#!/bin/bash
ph="/jenkins/test/workspace/dygraphs_try"
cp fuselog/*.py ${ph}
cp report/*.py ${ph}
cp readme ${ph}
cp *.sh ${ph}
cur=`pwd`
cd ${ph}&&git add *
cd ${ph}&&git commit -m "$1"
cd ${cur}
./save_sour.sh $1
