
find . -type f > /home/drupal/foto/globuslist &
sed 's/^\./\/mnt\/cifs\/Globus\/globus/g' globuslist2 > globuslist3
identify -verbose > textfiles-containing info
ls textfiles | while read x; do prepFotoForSolr.py "$x"; done
cat fillist3 | awk '{ print "cp "$0" newfiles/"$1"_"$2"_"$3"_"$4"_"$5"_"$6"_"$7"_"$8"_"$9}' > cpcmd
sed 's/\(.*\)txt\"[_]*/ \1txt" /' cpcmd > cpcmd2

grep "Image Name\[2,5\]" *txt  | awk '{FS=":"}{print $NF}' | sort | uniq -c | sort -k1n | awk '{ if ($1 > 1) { print $2}}'  > doublkms
cat doublkms | while read x; do cnt=$(( cnt + 1 )); egrep  "${x}$" *txt | grep Image |x=`echo $cnt` awk 'BEGIN {FS=":"}{print "egrep modify "$1 >> "test"ENVIRON["x"]}'; done
chmod 775 test*
ls test* | while read x; do ./$x | while read y; do echo $y; cnt=$(( cnt + 1));sed "${cnt}q;d" $x | awk '{print $3}'; done > ${x}_out; done
ls test*out | while read x; do paste -s -d' \n' $x > ${x}_concat;done
ls *concat | while read x; do doDateSort.py $x > mvcmd; done
