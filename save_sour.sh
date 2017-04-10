#!/bin/bash
ph="/jenkins/test/workspace/dygraphs_try"
cp fuselog/*.py ${ph}
cp report/*.py ${ph}
cp readme ${ph}
cp *.sh ${ph}
cd ${ph}&&git add *
cd ${ph}&&git commit -m "$1"

