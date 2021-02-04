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
