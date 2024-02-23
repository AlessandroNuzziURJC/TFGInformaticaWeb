#!/bin/bash

source ./api/files/adaptation/user.sh

FLAVOR="$1"
IMAGE="$2"
KEY_NAME="$3"
INSTANCE_NAME="$4"
VOL_NAME="$5"
UNIQUE_NAME="$6"

IP=$(openstack server list | grep $INSTANCE_NAME| cut -f 5 -d "|" | cut -f 2 -d "=" | cut -f 1 -d " ")

cd ./output/$UNIQUE_NAME/program
chmod 777 *
programname=$(ls)
cd ~/TFGInformaticaWeb/web
scp -o StrictHostKeyChecking=no -i ./api/files/miClave.pem -r ./output/$UNIQUE_NAME/program/* debian@$IP:~/prg

ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "gcc ./prg/$programname -o ./prg/exe"
ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "chmod 777 ./prg/exe"
start_time=$(date +%s.%N)
ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "./prg/exe"
end_time=$(date +%s.%N)
duration=$(python -c "print($end_time - $start_time)")
echo "$duration" > ./output/$UNIQUE_NAME/results/$FLAVOR.txt