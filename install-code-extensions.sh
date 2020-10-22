# ----------------- Installing vscode extensions

#vscode-extensions.txt xargs -I % code --install-extension %
cat vscode-extensions.txt | xargs -L1 code --install-extension