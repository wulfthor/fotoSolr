
find . -type f > /home/drupal/foto/globuslist &
sed 's/^\./\/mnt\/cifs\/Globus\/globus/g' globuslist2 > globuslist3
identify -verbose > textfiles-containing info
ls textfiles | while read x; do prepFotoForSolr.py "$x"; done

############################################################ 
#
# this will create a number of json-files ready for import
#
# curl http://localhost:8983/solr/foto/update?commit=true -H 
# 'Content-type:application/json ' --data  @globus_40412628_img0446.json
############################################################ 


perl -lane 'print "mv \"" . join(" ",@F) . "\""; print join("_",@F)' listoffiles
sed 's/\(.*\)txt\"[_]*/ \1txt" /' cpcmd > cpcmd2
curl http://localhost:8983/solr/globus/update?commit=true -H 'Content-type:text/xml' --data-binary  "<delete><query>id:*</query></delete>"

grep "Image Name\[2,5\]" *txt  | awk '{FS=":"}{print $NF}' | sort | uniq -c | sort -k1n | awk '{ if ($1 > 1) { print $2}}'  > doublkms
cat doublkms | while read x; do cnt=$(( cnt + 1 )); egrep  "${x}$" *txt | grep Image |x=`echo $cnt` awk 'BEGIN {FS=":"}{print "egrep modify "$1 >> "test"ENVIRON["x"]}'; done
chmod 775 test*
ls test* | while read x; do ./$x | while read y; do echo $y; cnt=$(( cnt + 1));sed "${cnt}q;d" $x | awk '{print $3}'; done > ${x}_out; done
ls test*out | while read x; do paste -s -d' \n' $x > ${x}_concat;done
ls *concat | while read x; do doDateSort.py $x > mvcmd; done



############################################################ 
# how to delete all records
#
# curl http://localhost:8983/solr/globus/update?commit=true -H 
# 'Content-type:text/xml' --data-binary  "<delete><query>id:*</query></delete>"
#
############################################################ 

############################################################ 
#  TODO
# - handle date-clock-timestamp (,2015-08-20T08:02:56Z,1)
# cat newtest2.csv |  perl -n -e 'if (m/(.*),([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9:Z]+),(.*)/g) { print "$1,$2,$4\n";}' > newtest2-1.csv 
# should be handled in prep-script
# - handle all quality-cases ("unknown")
# - handle resolution-cases (300x300, 72.000)
#    sed -i 's/resolution": "\(72\)[.x0-9]*",/resolution": "\1",/g' *json
#    (this for all cases found by:)
#    ls *json | while read x; do cat $x | jq '.[] | {res: .resolution}';done | grep res | cut -d\" -f4 | sort | uniq -c | sort -k1n
# 
#
############################################################ 

############################################################ 
# VIDEOS
# will be imported via csv
#
# Running find on film-02 and then
#
# stat -f "%N%%%a%%%m%%%B%%%z%%%HT" <file>
# output: ./FilmProd/Jack/Elmgreen Dragset/Kunstrazzia ProRes.mov%1411056694%1410426950%1410425895%11527027824%Regular File
#
# N:Name
# a:accesstime
# m:modify
# B:birth
# z:size in bytes
# HT:Type
#
#
# see if escaped chars in filename:
# awk -F\% '{if ((NF-1)>5) {print $0}}' ProdStat.txt
# 
# import to solr:
# curl http://172.20.1.107:8983/solr/video/update/csv --data-binary 
# @arkivStat.txt.csv -H 'Content-type:text/plain; charset=utf-8'
############################################################ 


