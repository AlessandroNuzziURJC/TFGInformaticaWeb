#!/bin/bash

source ./api/files/adaptation/user.sh

FLAVOR="$1"
IMAGE="$2"
KEY_NAME="$3"
INSTANCE_NAME="$4"
VOL_NAME="$5"
UNIQUE_NAME="$6"

IP=$(openstack server list | grep $INSTANCE_NAME| cut -f 5 -d "|" | cut -f 2 -d "=" | cut -f 1 -d " ")

openstack server delete $INSTANCE_NAME --wait
openstack volume delete $VOL_NAME

# Mostrar información del volumen y obtener los datos de attachments
attachments_info=$(openstack volume show "$VOL_NAME" -c attachments -f json)

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
            openstack volume delete "$VOL_NAME"
        else
            echo "No se encontró el servidor $server_id. No se realizará ninguna acción."
        fi
    else
        echo "No se pudo extraer server_id del JSON. Verifica el formato de la salida."
    fi
else
    echo "No hay attachments para el volumen $VOL_NAME. No se realizará ninguna acción."
fi

sleep 15