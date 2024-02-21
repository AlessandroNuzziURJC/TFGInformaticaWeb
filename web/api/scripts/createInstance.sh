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
#IP=$(openstack server list | grep $4| cut -f 5 -d "|" | cut -f 2 -d "=" | cut -f 1 -d " ")
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
openstack volume delete $5

nombre_volumen="$5"

# Mostrar información del volumen y obtener los datos de attachments
attachments_info=$(openstack volume show "$nombre_volumen" -c attachments -f json)

# Verificar si hay attachments
if [ "$(echo "$attachments_info" | jq '.attachments | length')" -gt 0 ]; then
    # Extraer el server_id del primer attachment si hay attachments
    server_id=$(echo "$attachments_info" | jq -r '.attachments[0].server_id')

    # Verificar que server_id no sea null o vacío
    if [ -n "$server_id" ]; then
        # Verificar si el servidor existe
        server_info=$(openstack server show "$server_id" -f json 2>/dev/null)
        if [ "$server_info" != "No server found for $server_id" ]; then
            # Borrar la attachment y el volumen
            attachment_id=$(echo "$attachments_info" | jq -r '.attachments[0].attachment_id')
            openstack --os-volume-api-version 3.27 volume attachment delete "$attachment_id"
            openstack volume delete "$nombre_volumen"
        else
            echo "No se encontró el servidor $server_id. No se realizará ninguna acción."
        fi
    else
        echo "No se pudo extraer server_id del JSON. Verifica el formato de la salida."
    fi
else
    echo "No hay attachments para el volumen $nombre_volumen. No se realizará ninguna acción."
fi

sleep 15