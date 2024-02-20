#!/bin/bash

source ./api/files/adaptation/user.sh
IPUSED=($(openstack floating ip list --network public| grep "10.*"| cut -f 3 -d "|" | cut -f 2 -d " "))
IPLIST=($(openstack floating ip list --network public | grep "10.*" | grep "None" | cut -f 3 -d "|" | cut -f 2 -d " "))
if [ ${#IPUSED[@]} -eq 2 ] && [ ${#IPLIST[@]} -eq 0 ]; then
    echo "No hay direcciones IP disponibles."
    exit 1
fi

if [ ${#IPLIST[@]} -eq 0 ]; then
    # Reservo IP
    openstack floating ip create public
    IP=$(openstack floating ip list --network public | grep "10.*" | grep "None" | cut -f 3 -d "|" | cut -f 2 -d " ")
elif [ ${#IPLIST[@]} -eq 1 ]; then
    IP=$IPLIST
else
    IP=${IPLIST[1]}
fi
openstack volume create --image $2 $5 --size 4
sleep 15
openstack server create --flavor $1 --volume $5 --key-name $3  --wait $4
ssh-keygen -R $IP
openstack server add floating ip $4 $IP
sleep 30
ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "sudo apt update -y"
ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "sudo apt install build-essential -y"
ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "mkdir prg" 
ssh -o StrictHostKeyChecking=no -i ./api/files/miClave.pem debian@$IP "chmod 777 prg" 

cd ~/TFGInformaticaWeb/TFGInformaticaWeb/web/output/$6/program
chmod 777 *
programname=$(ls)
scp -o StrictHostKeyChecking=no -i ~/TFGInformaticaWeb/TFGInformaticaWeb/web/api/files/miClave.pem -r ~/TFGInformaticaWeb/TFGInformaticaWeb/web/output/$6/program/* debian@$IP:~/prg
ssh -o StrictHostKeyChecking=no -i ~/TFGInformaticaWeb/TFGInformaticaWeb/web/api/files/miClave.pem debian@$IP "gcc ./prg/$programname -o ./prg/exe"
ssh -o StrictHostKeyChecking=no -i ~/TFGInformaticaWeb/TFGInformaticaWeb/web/api/files/miClave.pem debian@$IP "chmod 777 ./prg/exe"
start_time=$(date +%s)
ssh -o StrictHostKeyChecking=no -i ~/TFGInformaticaWeb/TFGInformaticaWeb/web/api/files/miClave.pem debian@$IP "./prg/exe"
end_time=$(date +%s)
duration=$(python -c "print($end_time - $start_time)")
echo "$duration"
openstack server delete $4 --wait