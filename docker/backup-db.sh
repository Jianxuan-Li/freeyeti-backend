#!/bin/sh

# Backup postgis in Kubernetes cluster
# Author: JIANXUAN LI<liujin834@gmail.com>

# Caveat: these variable is mention in backup ymal file of k8s job.
# 			 	Don't change them if you are not sure. 
backupstoredir=/data 
prefix=backend_app
max_keeps=7 # Keep 7 days backup
host=postgis
port=5432
user=postgres
dbname=boilerplate
password=postgres

# Define filename of database backup file
datetime=$(date +"%Y%m%d%H%M%S")
filename=$backupstoredir/$prefix_$datetime.backup

# Define list file
list=$backupstoredir/$prefix.list

# Use pg_dump to create backup file
/usr/bin/pg_dump \
		--host $host \
		--port $port \
		--username $user \
  	--format=c \
	  --no-owner \
	  --no-privileges \
    --file=$filename \
		$dbname

echo $filename >> $list
echo $filename
echo "^^^^ CREATED BACKUP FILE ABOVE ^^^^"

# Save list file and clean backup dir
linecount=`/usr/bin/wc -l $list | /usr/bin/awk '{print $1}'`

echo $linecount backup files

if [ $linecount -lt $max_keeps ]
then
	echo lack backup files
else
	toremove=$(expr $linecount - $max_keeps)

	echo "$toremove backup file(s) will removed"

	if [ $toremove -lt 1 ]
		then
		echo nothing to remove
		exit 0
	fi

	head -$toremove $list | while read line
	do
		file=$(basename $line)
		fullpath=$backupstoredir/$file
		if [ ! -f $fullpath ]
		then
			echo $fullpath not exists, remove from list!
		else
			rm $fullpath
			echo $fullpath removed
		fi
	done
fi

filelist=`ls $backupstoredir`
for filename in $filelist
do
	echo $filename >> $list.tmp
done
sed -i '/^\s*$/d' $list.tmp
mv $list.tmp $list