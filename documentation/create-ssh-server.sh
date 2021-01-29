 
sudo apt-get update
sudo apt-get install openssh-server
#Check ssh server state
sudo systemctl status sshd

#Enable ssh connections in ufw firewall
sudo ufw allow ssh
sudo ufw status

#Enable firewall
sudo ufw enable
#sudo ufw allow 2654

#Check if ssh server starts through a service at boot time
sudo systemctl list-unit-files | grep enabled | grep ssh
#If not -> enable
sudo systemctl enable ssh

sudo nano /etc/ssh/sshd_config

echo -e "Port 2654\n" | sudo tee -a /etc/ssh/sshd_config

#Restarting server for config changes to take effect
sudo systemctl restart sshd
sudo systemctl status sshd

#Check if service is listening on port 2654
netstat -tulpn | grep 2654

#Show network adapter and ip info
sudo ifconfig

#Add host to ssh config
sed -i '1s/^/HostName 127.0.0.1\n\tUser pmarkus\n/' ~/.ssh/config

#Ssh into localhost to test server
ssh -v -p 2654 pmarkus@127.0.0.1

#Get ip
#192.168.0.102
#192.168.0.101
# -> ssh -v -p 2654 pmarkus@192.168.0.102 -i ~/.ssh/id_rsa
# -verbose (logs) -port - identityfile


#Stop ssh server
sudo systemctl stop sshd
sudo systemctl status sshd



#Termux
#apt install openssh
#sshd
#whoami
#ifconfig
#nmap localhost
#ssh u0_a278@192.168.0.107 -p 8022