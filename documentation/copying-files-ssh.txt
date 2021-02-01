To copy files over ssh we can either use sftp protocol and mounting the filesystem as a network drive:

ADDING SFTP NETWORK FOLDER DOLPHIN:
1. network
2. add nework folder
3. secure shell ssh

4.  Name = Label of the created drive
    User = username to which to logon on the remote machine
    Server = Local/Remote ip of the remote maching (ifconfig + local ip when on the same network/wlan/lan)
    Port = port on which the ssh server is hosted (22 if not specified differently on /etc/ssh/sshd-config)
    Protocol = sftp (essentially ftp file transfer over ssh connection)
    Folder = Which path to mount as the network storage ("/" = root, "/home/user" = the home folder of user )
    -> Save and connect
5. Network -> new network drive -> right click -> add to places (to add a shortcut to dolphin)


COPYING VIA "SCP"
scp -P targetport path/on/host/machine username@hostip:/guest/path/on/target

Example:
Transfer of bash settings and all alias settings from 1 machine to the remote machine:

scp -P 5555 ~/.bashrc peitl@192.168.0.117:~/.bashrc

Then execute ". ~/.bashrc" on target machine to reload bash settings

REMOTE COMMAND EXECUTION (for the same thing)
ssh -t peitl@192.168.0.117 -p 5555 ". ~/.bashrc"
(Note that the "" are necessary as otherwise ~ is evaluated on the host machine instead of the remote machine, which points to different paths)


COPYING ALTERNATIV "RSYNC":
Powerful copy and sync tool to backup, move and compare files.

rsync -e "ssh -p 5555" -avz ~/.bashrc peitl@192.168.0.117:"~/.bashrc"

-a recursion on the path and preserving everything
-v ouput verbose log (always useful for debugging)
-z compress source before moving (speeds up ssh)

-> compression -> faster than scp -> better for larger files