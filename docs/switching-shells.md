# Ways to switch between available shell implementations (zsh, bash, fish, etc.)

## Temporarily switch to bash in current terminal session

Bash has to be in the system PATH, if not "/bin/bash" should be used instead.

```bash
exec bash
```

## Temporarily switch to zsh in current terminal session

Zsh has to be in the system PATH, if not "/bin/bash" should be used instead.

```bash
exec zsh
```

## Permanently switch default shell

List all available shells:

```bash
cat /etc/shells
```

Select one shell as default shell from the options above - here for "bash":

```bash
chsh -s /bin/bash
```

Close and restart your terminal emulator.
If that does not work a reboot is required to finalize the switching of shells.

## Attention

After switching to a new shell the configurations and settings of your old shell are not included anymore.  
So some applications (for instance those which are installed via snap or flatpak) are not discoverable anymore.  
And as the system uses the shell for various tasks these missing link can appear systemwide.  
<br>
**Examples:**  

- If you have installed the "chromium-browser" through "snap" it won't show up in your "application menu" anymore.  
- Opening some applications through xdg-open will not work anymore, so no default-application

- To fix this the profile of the old shell can be included in the new configuration.

### Example ( from bash -> zsh )

```bash
sudo nano /etc/zsh/zprofile
```

- Then add following line to the configuration.  

```bash
emulate sh -c 'source /etc/profile'
```

- Which includes you bash profile configuration into your zsh configuration.  
- Then log out of your system and log in again  
- Now you should be able to see all your applications in the application menu again and be able to open default application

#### If you like the article consider dropping me a coffee

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate?hosted_button_id=BSFX8LCPHW2AE)
  
<br>  
<br>  