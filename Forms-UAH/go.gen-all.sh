#!/bin/bash

FILES=`ls GEF[0-9][0-9].pdf`

for f in $FILES
do
	echo "---------------------------------------------------------------------------"
	echo "Identifying fields for [$f]..."
	python ../pdf-form-identify-fields.py $f
done
