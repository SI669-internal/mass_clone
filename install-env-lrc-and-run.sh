##### Env Setup
cd $HOME && \
git clone https://github.com/mxcl/homebrew.git && \
export PATH=$HOME/homebrew/bin:$PATH && \

# in order to proceed, mxay need to do brew update. See instruction prompted
brew update

xcode-select --install

brew install python3 # will take a while

cd $HOME
cd Downloads

git clone https://github.com/SI669-internal/mass_clone.git

cd mass_clone

## Install And Run On LRC Machine





##### Project Setup

python3 -m venv venv

. ./venv/bin/activate

# if not pip yet, install the follow and follow the instruction on iriversland 1.0 website
# easy_install --user pip

pip install -r requirements.txt && \

cd python-script

cp credentials_example.py credentials.py

cp settings_example.py settings_local.py

# https://stackoverflow.com/questions/226703/how-do-i-prompt-for-yes-no-cancel-input-in-a-linux-shell-script

read -p "Please follow the config instruction in https://github.com/SI669-internal/mass_clone . We will open the folder in Finder for you. Sounds good? (Y)" yn
open .

read -p " Finished following instructions? (Y/n)" yn
case $yn in
    [Yy]* ) python3 main.y;;
    [Nn]* ) exit;;
    * ) echo "Please answer by y or n."
esac