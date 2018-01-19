#!/bin/bash

echo ""
echo " Running default Debian installs ..."
echo "****************************************************************************************************"
echo ""

if [ "$1" == "-x" ]; then

    echo "Skipping download of third party .deb packages ..."
    echo ""

else

    # Somewhere to store Downloads
    cd $HOME/Downloads

    # Chrome
    echo "Installing Google Chrome ..."
    echo ""
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    dpkg -i google-chrome-stable_current_amd64.deb
    echo "****************************************************************************************************"

    # VSCode
    echo "Installing Visual Studio Code ..."
    echo ""
    wget https://go.microsoft.com/fwlink/?LinkID=760868 -O code_latest_amd64.deb
    dpkg -i code_latest_amd64.deb
    echo "****************************************************************************************************"
    echo ""

    # Fix Dependencies
    apt -f install
    echo "****************************************************************************************************"
    echo ""
    
    rm -v google-chrome-stable_current_amd64.deb
    rm -v code_latest_amd64.deb

fi

# Main Packages
echo "Installing default packages ..."
echo ""
apt update
apt install -y \
    geany geany-plugins git meld \
    gnome-shell-extension-dashtodock gnome-shell-extension-pixelsaver \
    gnome-shell-extension-system-monitor gnome-shell-extension-weather \
    texlive-full thunderbird thunderbird-l10n-nb-no keepass2 zim terminator \
    build-essential autotools-dev automake cmake pkg-config gfortran gcc g++ \
    python3 ipython ipython3 python3-matplotlib python3-numpy python-matplotlib python-numpy python3-gi \
    libboost-all-dev libopenmpi-dev libssl-dev \
    typecatcher vlc gimp inkscape calibre \
    rar unrar p7zip curl apt-transport-https rsync secure-delete \
    libreoffice-style-breeze \
    lm-sensors aptitude system-config-printer
echo "****************************************************************************************************"
echo ""

# Syncthing
if [ ! -f /etc/apt/sources.list.d/syncthing.list ]; then
    echo "Installing Syncthing ..."
    echo ""
    curl -s https://syncthing.net/release-key.txt | sudo apt-key add -
    echo "deb https://apt.syncthing.net/ syncthing stable" | tee /etc/apt/sources.list.d/syncthing.list
    apt update
    apt install syncthing
    apt -f install
    systemctl enable syncthing@vkbo.service
    systemctl start syncthing@vkbo.service
    echo "****************************************************************************************************"
    echo ""
fi

# Spotify
if [ ! -f /etc/apt/sources.list.d/spotify.list ]; then
    echo "Installing Spotify ..."
    echo ""
    apt install -y dirmngr
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0DF731E45CE24F27EEEB1450EFDC8610341D9410
    echo deb http://repository.spotify.com stable non-free | tee /etc/apt/sources.list.d/spotify.list
    apt update
    apt install spotify-client
    apt -f install
    echo "****************************************************************************************************"
    echo ""
fi
