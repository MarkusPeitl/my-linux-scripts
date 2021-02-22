# Install docker from ubuntu registry

```bash
#Install docker from default ubuntu repository
sudo apt install docker.io
```

Add user to docker group (to run docker from user without permission denied)

```bash
#Add docker group
sudo groupadd docker
```

```bash
# mod user -add -group username
sudo usermod -aG docker pmarkus
```

```bash
# enable service at startup
sudo systemctl enable docker
```

```bash
# restart to update configuration
sudo systemctl restart docker
```

Restart your current terminal or ssh session for permission changes to take effect
