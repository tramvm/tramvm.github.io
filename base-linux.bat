timedatectl set-timezone Asia/Ho_Chi_Minh
echo "Go root folder"
cd ..
cd ..
pwd
mkdir webapps
cd webapps/
chmod -R 777 .
echo "Start nginx"
service nginx restart
echo "Install certbot"
sudo apt install certbot python3-certbot-nginx
echo "Install docker"
sudo apt-get installsudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
 "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo service docker start
echo "Install docker compose via pip"
apt install python3-pip
pip install docker-compose
docker network create same-network

