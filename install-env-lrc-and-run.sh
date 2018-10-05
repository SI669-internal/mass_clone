cd $HOME && \
git clone https://github.com/mxcl/homebrew.git && \
export PATH=$HOME/homebrew/bin:$PATH && \


#
# in order to proceed, mxay need to do brew update. See instruction prompted
brew update

xcode-select --install

brew install python3 # will take a while

cd $HOME
cd Downloads

git clone https://github.com/SI669-internal/mass_clone.git

cd mass_clone

python3 -m venv venv

. ./venv/bin/activate

cd python-script

# https://stackoverflow.com/questions/226703/how-do-i-prompt-for-yes-no-cancel-input-in-a-linux-shell-script
read -p "Please follow the config instruction in https://github.com/SI669-internal/mass_clone . Finished? (Y/n)" yn
case $yn in
    [Yy]* ) python3 main.y;;
    [Nn]* ) exit;;
    * ) echo "Please answer by y or n."
esac

