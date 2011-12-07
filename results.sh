#!/bin/bash

FILE_NAME=$1
PROTOCOL=$2

if [ -z "$FILE_NAME" ] || [ -z "$PROTOCOL" ]; then
  echo "./results <classification_file> <protocol>"
fi

TOTAL=`grep "^$PROTOCOL|" $FILE_NAME | wc -l`
CORRECT=`grep "^$PROTOCOL|\['$PROTOCOL'\]" $FILE_NAME | wc -l`
DETECTED=`grep "|\['$PROTOCOL'\]" $FILE_NAME | wc -l`

RECALL=`echo "scale=10; $CORRECT/$TOTAL" | bc`
PRECISION=`echo "scale=10; $CORRECT/$DETECTED" | bc`

echo "RECALL: $RECALL"
echo "PRECISION: $PRECISION"
