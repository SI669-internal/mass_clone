cd python-script

python3 -m venv venv

. ./venv/bin/activate

# if not pip yet, install the follow and follow the instruction on iriversland 1.0 website
# easy_install --user pip

pip install -r requirements.txt && \

cp credentials_example.py credentials.py

cp settings_example.py settings_local.py

cp script-session/recommend-config.json script-session/local-config.json

# https://stackoverflow.com/questions/226703/how-do-i-prompt-for-yes-no-cancel-input-in-a-linux-shell-script

read -p "Please follow the dependency instructions in https://github.com/SI669-internal/mass_clone . Also, we will open the project folder in Finder for you. If this sounds good, hit enter to proceed." yn
open .

read -p "PROMPT: When you finished instructions setting up dependencies, hit enter." yn
case $yn in
    [Yy]* ) python main.py;;
    [Nn]* ) return;;
    * ) python main.py;; # default
esac