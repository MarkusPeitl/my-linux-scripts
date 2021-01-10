#DEBUG=true
#touch `dirname $0`/out.txt
#echo $(cat `dirname $0`/alias-collection.txt) >> `dirname $0`/out.txt && . ~/.bashrc

echo $(cat `dirname $0`/alias-collection.txt) >> ~/.bashrc && . ~/.bashrc