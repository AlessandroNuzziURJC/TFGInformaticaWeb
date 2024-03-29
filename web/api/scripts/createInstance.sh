#!/bin/bash

source ./api/files/adaptation/user.sh

FLAVOR="$1"
IMAGE="$2"
KEY_NAME="$3"
INSTANCE_NAME="$4"
VOL_NAME="$5"
UNIQUE_NAME="$6"
MPI="$7"
OPENMP="$8"
OUTPUT="$9"

openstack volume create --image $IMAGE $VOL_NAME --size 4
sleep 15
openstack server create --flavor $FLAVOR --volume $VOL_NAME --key-name $KEY_NAME  --wait $INSTANCE_NAME
IP=$(openstack server list | grep $INSTANCE_NAME| cut -f 5 -d "|" | cut -f 2 -d "=" | cut -f 1 -d " ")

sleep 30
start_time=$(date +%s.%N)
ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "sudo apt update -y"
ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "sudo apt install build-essential -y"
ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "mkdir prg" 
ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "chmod 777 prg" 

if [ $MPI = "True" ]; then
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "sudo apt-get install openmpi-bin openmpi-doc libopenmpi-dev -y"
fi
end_time=$(date +%s.%N)
duration=$(python -c "print($end_time - $start_time)")
echo "$duration" >> $OUTPUT