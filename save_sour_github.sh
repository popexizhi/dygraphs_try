#!/bin/bash
ph1="/jenkins/test/workspace/dygraphs_try" #github use
ph2="/jenkins/test/workspace/load_L2/cluster" #gitlab use
file_list="${ph1} ${ph2}"
for ph in ${file_list}
do
    echo "github*${ph}*************************************"
    cp fuselog/*.py ${ph}
    cp report/*.py ${ph}
    cp ue_rtt/*.py ${ph}
    cp ue_rtt/*.sh ${ph}
    cp readme ${ph}
    cp *.sh ${ph}
    cur=`pwd`
    cd ${ph}&&git add *
    cd ${ph}&&git commit -m "$1"
    cd ${cur}
    echo "gitlab**************************************"
done
#./save_sour.sh $1
