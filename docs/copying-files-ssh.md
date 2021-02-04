# Copying files using a ssh connection

To copy files over ssh we can either use sftp protocol and mounting the filesystem as a network drive:

## Adding sftp network folder dolphin

**1.** Go to network item in places navigation  
**2.** add nework folder  
**3.** secure shell ssh  
**4.** Name = Label of the created drive  

- **User** = username to which to logon on the remote machine  
- **Server** = Local/Remote ip of the remote maching (ifconfig + local ip when on the same network/wlan/lan)  
- **Port** = port on which the ssh server is hosted (22 if not specified differently on /etc/ssh/sshd-config)  
- **Protocol** = sftp (essentially ftp file transfer over ssh connection)  
- **Folder** = Which path to mount as the network storage ("/" = root, "/home/user" = the home folder of user )  
    -> **Save and connect** \

**5.** - Network -> new network drive -> right click -> add to places (to add a shortcut to dolphin)

## Copying files via "scp"

```shell
scp -P targetport path/on/host/machine username@hostip:/guest/path/on/target
```

### Example:

Transfer of bash settings and all alias settings from 1 machine to the remote machine:

```shell
scp -P 5555 ~/.bashrc peitl@192.168.0.117:~/.bashrc
```

Then execute ". ~/.bashrc" on target machine to reload bash settings

**remote command execution** (for the same thing)  

```shell
ssh -t peitl@192.168.0.117 -p 5555 ". ~/.bashrc"
```

(Note that the "" are necessary as otherwise ~ is evaluated on the host machine instead of the remote machine, which points to different paths)

## Alternative copying procedure "rsync"

Powerful copy and sync tool to backup, move and compare files.

```shell
rsync -e "ssh -p 5555" -avz ~/.bashrc peitl@192.168.0.117:"~/.bashrc"
```

**-a** recursion on the path and preserving everything  
**-v** ouput verbose log (always useful for debugging)  
**-z** compress source before moving (speeds up ssh)

### Advantage

-> compression -> faster than scp -> better for larger files

#### If you like the article consider dropping me a coffee

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=BSFX8LCPHW2AE)
  
<br>  
<br>  