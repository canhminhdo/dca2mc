#!/bin/sh

echo "~~~~~~~~~~ TESTING ~~~~~~~~~~"
DIR="output"
ls | grep ".maude$" | sort -V | while read -r FILE; do
    NAME=`echo $FILE | cut -d '.' -f1`
    maude < $FILE -no-banner | sed -r '/^(rewrites:|Solution|states:)/d' > "$NAME.out"
    diff "$DIR/$NAME.expected" "$NAME.out"
    rm "$NAME.out"
done
echo "DONE!"

