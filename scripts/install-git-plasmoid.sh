#Usage bash install-git-plasmoid.sh https://github.com/paju1986/PlasmaConfSaver
cd ~/Downloads
git clone "$1"

GITDIRNAME=$(echo "$1" | rev | cut -d'/' -f 1 | rev)

echo "Opening directory: $GITDIRNAME"

cd ~/Downloads/$GITDIRNAME

INSTALLABLEDIR=$(find . -type f -name 'metadata.desktop' | sed -r 's|/[^/]+$||' |sort -u)

plasmapkg2 --install "$INSTALLABLEDIR"
cd ~/Downloads
rm -r ~/Downloads/$GITDIRNAME