#cp *.py ${ph}
ph="dygraphs_try"
cp fuselog/*.py ${ph}
cp report/*.py ${ph}
cp report/test* ${ph}
cp readme ${ph}
cp *.sh ${ph}
cd ${ph}&&git add *
git commit -m "$1"
cd ../

