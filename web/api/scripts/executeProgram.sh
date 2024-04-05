#!/bin/bash

source ./api/files/adaptation/user.sh

FLAVOR="$1"
IMAGE="$2"
KEY_NAME="$3"
INSTANCE_NAME="$4"
VOL_NAME="$5"
UNIQUE_NAME="$6"
OUTPUT="$7"
MPI="$8"
OPENMP="$9"
THREADS=${10}

IP=$(openstack server list | grep $INSTANCE_NAME| cut -f 5 -d "|" | cut -f 2 -d "=" | cut -f 1 -d " ")

cd ./output/$UNIQUE_NAME/program
chmod 777 *
programname=$(ls)
cd ~/TFGInformaticaWeb/web
scp -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem -r ./output/$UNIQUE_NAME/program/* debian@$IP:~/prg

if [[ $MPI = "False" && $OPENMP = "False" ]]; then
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "gcc ./prg/$programname -o ./prg/exe"
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "chmod 777 ./prg/exe"
    start_time=$(date +%s.%N)
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "./prg/exe"
    echo "./prg/exe"
    end_time=$(date +%s.%N)
    duration=$(python -c "print($end_time - $start_time)")  
elif [[ $MPI = "True" && $OPENMP = "True" ]]; then
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "mpicc -fopenmp -o ./prg/exe ./prg/$programname"
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "chmod 777 ./prg/exe"
    start_time=$(date +%s.%N)
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "mpirun -np $THREADS ./prg/exe"
    echo "mpirun -np $THREADS ./prg/exe"
    end_time=$(date +%s.%N)
    duration=$(python -c "print($end_time - $start_time)")
elif [[ $MPI = "True" ]]; then
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "mpicc -o ./prg/exe ./prg/$programname"
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "chmod 777 ./prg/exe"
    start_time=$(date +%s.%N)
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "mpirun -np $THREADS ./prg/exe"
    echo "mpirun -np $THREADS ./prg/exe"
    end_time=$(date +%s.%N)
    duration=$(python -c "print($end_time - $start_time)")
else
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "gcc ./prg/$programname -o ./prg/exe -fopenmp"
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "chmod 777 ./prg/exe"
    start_time=$(date +%s.%N)
    ssh -o StrictHostKeyChecking=no -i ./api/files/key_testsystem.pem debian@$IP "./prg/exe $THREADS"
    echo "./prg/exe $THREADS"
    end_time=$(date +%s.%N)
    duration=$(python -c "print($end_time - $start_time)")  
fi

echo "$duration" >> $OUTPUT