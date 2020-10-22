#TODO
sudo apt update

## Apt:
## Smaller packages
## Better gui integration
## Auto updates
##
## Snaps:
## Apps isolated -> clean uninstall (att also data and deps)
## Sandboxed
##
## Prefer Apt

#--- DEV
#sudo apt-get install ffmpeg
#sudo apt-get install git

#Anaconda install (miniconda)
#wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
#chmod +x Miniconda3-latest-Linux-x86_64.sh
#./Miniconda3-latest-Linux-x86_64.sh
#export PATH=~/miniconda/bin:$PATH

#--- Photo edit
#sudo apt-get install digikam
#sudo apt-get install darktable

#--- ScreenRec
#sudo apt install kazam

#--- ScreenShot
#sudo apt-get install shutter 

#--- Office
#sudo apt install libreoffice

#--- Gaming
#sudo add-apt-repository multiverse
#sudo apt update
#sudo apt install steam

#sudo apt-get install playonlinux

#--- System
#sudo apt install gnome-tweaks
#sudo apt install gnome-shell-extensions

#--- Internet
#sudo apt install firefox

#cd ~/Downloads
#wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#sudo apt install ./google-chrome-stable_current_amd64.deb


#--- Audio
#sudo apt-get install audacity

#--- Video
#sudo apt install obs-studio

#--- Mail
#sudo apt install thunderbird

#--- Communication


# ----------------- SNAP Programs (UBUNTU)
#--- DEV
#sudo snap install code --classic
#sudo snap install notepad-plus-plus
#sudo snap install node --classic
# --- might fail as npm does not work after installation (can be fixed by making executable and addiding to the right path --> google)
#sudo snap install android-studio --classic

#--- Mail
#sudo snap install thunderbird

#--- Internet
#sudo snap install chromium
#sudo snap install firefox

#--- Audio
#sudo snap install audacity

#--- Screenshot
#sudo snap install shutter

#--- Video
#sudo snap install vlc
#sudo snap install obs-studio
#sudo snap install shotcut
#sudo snap install kdenlive

#--- Communication
#sudo snap install skype --classic
#sudo snap install slack
#sudo snap install discord

#--- Misc
#sudo snap install canonical-livepatch
#sudo snap install ffmpeg
#sudo snap install simplenote

#--- Android
#sudo snap install anbox --beta


# ----------------- Flatpack Programs similar to snap (but can share deps)
#sudo apt install flatpak
#flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

#flatpak install flathub com.valvesoftware.Steam
#flatpak run com.valvesoftware.Steam

#flatpak install flathub org.libreoffice.LibreOffice
#flatpak run org.libreoffice.LibreOffice

#flatpak install flathub org.kde.kdenlive
#flatpak run org.kde.kdenlive

#flatpak install flathub com.github.carlos157oliveira.Calculus
#flatpak run com.github.carlos157oliveira.Calculus

#flatpak install flathub io.atom.Atom
#flatpak run io.atom.Atom


# --++--- Installing misc packages
#cd ~
#curl -O https://www.reaper.fm/files/6.x/reaper615_linux_x86_64.tar.xz
