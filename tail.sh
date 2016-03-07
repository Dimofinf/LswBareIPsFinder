regex1='Finished: SUCCESS'
regex2='No Match Found'
tail logs.txt -F | while read line; do
    echo $line
    if [[ $line =~ $regex1 ]]; then
        pkill -9 -P $$ tail
    fi
    if [[ $line =~ $regex2 ]]; then
        pkill -9 -P $$ tail
    fi
done
