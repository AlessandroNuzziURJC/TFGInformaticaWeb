sudo apt update -y
sudo apt install -y build-essential 
sudo apt install -y git
sudo apt install -y virtualenv
sudo apt-get install jq -y
sudo timedatectl set-timezone Europe/Madrid
virtualenv venv
source venv/bin/activate
pip install python-openstackclient
pip install django

git clone https://github.com/AlessandroNuzziURJC/TFGInformaticaWeb.git
cd TFGInformaticaWeb/web

pip install -r requirements.txt
chmod 777 /home/debian/TFGInformaticaWeb/web/api/scripts/*
#python manage.py runserver 0.0.0.0:8080