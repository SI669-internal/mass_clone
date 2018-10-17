##### Env Setup
cd $HOME && \
git clone https://github.com/mxcl/homebrew.git
echo 'export PATH=$HOME/homebrew/bin:$PATH' >> ~/.bash_profile
brew update # in order to proceed, mxay need to do brew update. See instruction prompted

xcode-select --install

read -p "You should see a prompt asking you to install software (xcode command line tools), please do so by pressing 'install' button. When you finish, proceed by hitting enter." yn

brew install python3 node && npm i -g ionic cordova # will take a while
if [[ $? -eq 0 ]];
    then
    :
else
    echo "ERROR: Failed to brew install python 3. See error message above."
    return
fi





##### Project Setup

cd $HOME
cd Downloads

git clone https://github.com/SI669-internal/mass_clone.git

cd mass_clone

python3 -m venv venv

. ./venv/bin/activate

# if not pip yet, install the follow and follow the instruction on iriversland 1.0 website
# easy_install --user pip

pip install -r requirements.txt && \

cd python-script

cp credentials_example.py credentials.py

cp settings_example.py settings_local.py

# https://stackoverflow.com/questions/226703/how-do-i-prompt-for-yes-no-cancel-input-in-a-linux-shell-script

read -p "Please follow the dependency instructions in https://github.com/SI669-internal/mass_clone . Also, we will open the project folder in Finder for you. If this sounds good, hit enter to proceed." yn
open .

read -p "When you finished instructions setting up dependencies, hit enter." yn
case $yn in
    [Yy]* ) python3 main.y;;
    [Nn]* ) exit;;
    * ) echo "Please answer by y or n."
esac