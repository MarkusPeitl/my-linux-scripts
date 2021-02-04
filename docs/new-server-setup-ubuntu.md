# Some basic setup steps, when setting up a clean Debian or Ubuntu VPS server, from a linux distribution

## SSH ACCESS SETUP

Open up you terminal "CTRL + ALT + T".

```bash
mkdir -p ~/.ssh/
cd ~/.ssh/
```

Generate 1 private and 1 public key for you ssh connection:

```bash
ssh-keygen -t rsa -b 4096
# -> Enter data for the keypair (name + password)
```

After these steps your new key pair is generated in the current directory.

Print out the public key file's contents and the select the contents in your terminal and copy them.
(you could also open it in an editor and copy the contents there, or use xclip to do this inside of the terminal)

```bash
cat key_name.pub
```

Insert as ssh public key on your hosters side if that option is available. (probably the best and securest option)
If not your hoster might provide you with a login password to your root account, then you can omit setting the  
-i (identityfile) option in the next terminal step.
(TODO add description for how to add pub key files manually)  

Then find out the public ip of you server from your hoster (your.public.ip.address)  
Usually findable somewhere on your dashboard or in your server settings/info  

<br>
Ssh into your server as root user (to take control over it), with the info from your hoster.

```bash
ssh root@your.public.ip.address -i ~/ssh/key_name
```

Now you can use the server as you would an normal ubuntu/debian machine from the terminal
and continue to the next section.

## INITIAL USER SETUP

- Create new Password for root (you definitely want to root user to protected by a strong password)

```bash
passwd
```

<br>
- Check admin users (if some of them already exist) - root will be in there
  
```bash
cat /etc/sudoers
```

<br>
- Add your everyday user (you don't want to use root, even if you know what you are doing, as breaking your system with root is way too easy)

```bash
adduser yournewusername
```

Then enter your new Password for the user and other user info in the prompts that follow.

<br>
- Add your user to the sudo group (if you want the user to have admin priviledges).  
  By prepending sudo to a command you can execute it with root priviledges (you can still break your system with it, but it is more effort).  
  Advice: Don't use sudo if you can avoid it (be especially careful when executing "rm -r" as sudo).  

```bash
usermod -G sudo yournewusername
```

Yay now your user "yournewusername" can use "sudo"

<br>
- Switch to you newly created user (su = switch user)

```bash
su yournewusername
```

<br>
- Make sure you can access sudo and therefore have admin access ~~before continuing !!!~~

```bash
sudo -v
```

Should print out nothing.  
If you do not have sudo priviledges "Sorry, user testuser may not run sudo on machine" is printed.  

You could also print out sudoers to check if your user is in the list:

```bash
cat /etc/sudoers
```

<br>
- If your user now has sudo priviledges there is no reason to use your root account to login via ssh anymore.  

```bash
sudo nano /etc/ssh/sshd_config
```

1. -> Go to  
PermitRootLogin yes
2. and set it to
PermitRootLogin no
3. Save:ctrl + x	->	y	->	,Enter

<br>
- Reload the sshd server for the configuration changes to take effect

```bash
sudo systemctl restart sshd
```

<br>
- Close ssh session (repeat until session is closed)

```bash
exit
```

<br>
- Check if disabling root ssh logon worked

```bash
ssh root@your.public.ip.address -i ~/ssh/key_name
```

If you enter your correct root password and it says "Permission denied, please try again" it worked.

<br>
- Check if ssh access with your new user works

```bash
ssh yournewusername@your.public.ip.address -i ~/ssh/key_name
```

After entering your password you should be able to access the server using your new user

## Configuring a SSH-shortcut to speed up and simplify the ssh connection process

To permanently save your ssh logon info you can use the config file.

<br>
- Create a ssh config file if it does not exist yet and start editing it:

```bash
touch ~/.ssh/config
nano ~/.ssh/config
```

<br>
- Now paste following credentials and replace the entries with your configuration

```bash
Host myserver
	HostName your.public.ip.address
	User pmarkus
	PORT 22
	IdentityFile ~/.ssh/hostinger_rsa
```

- **Host:** is any label with which you want to use ssh to connect to the machine ( use short ones if you want to ssh often)  
- **HostName:** Url to you maching or a public ip address point to your machine (be carful as if you have a dynamic ip address this can change)  
therefore its better to use a static ip (ipv6 addresses are usually easier to get) or have a domain ready that you can point to your server.
Usually there is also some kind of free DNS url to your server provided by you hosting service, which you can use.  
so for quick checking -> use public dyncamic ip, for a permanent link -> use the static url provided by your hoster, for something easy to remember  
-> use a domain that dns resolves to your server  
- **User:** As which user do you want to log onto the machine  
- **PORT:** Which port (default is 22 can be changed on you server in /etc/ssh/sshd_config + restart service)  
- **IdentityFile:** Which private Keyfile to use for connecting (server should have public keyfile)  

<br>
- You can then very easily ssh connect into your server by typing
```bash
ssh myserver
```

#### If you like the article consider dropping me a coffee

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=BSFX8LCPHW2AE)
  
<br>  
<br>  