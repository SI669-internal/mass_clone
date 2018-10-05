# Batch Clone

1st version automation tool that integrates three things:
- Github API: Batch clone repo
- Google Sheet API: Display grades / Read roster
- Interactive Terminal: run code, grade and comment all in one place

# How it works

- Batch clone student repos
  - Support late detection when using Github classroom.
  - You can also provide a list of github repo names in your Google spreadsheet, but no late detection.
- Interactive grading and commenting on students' repo submits.
  - Can batch apply terminal commands on each repo.
  - Can open code editor or run code for you when you are grading students' submits.
  - TODO: late penalty
- Can keep track of multiple assignments, and show all the grades and comments you made in your Google spreadsheet.
- Will clone student repos next to the `mass_clone` directory as follows:

```

/mass_clone
/<generated assignment prefix here>
---/<generated repo clones for the assignment>
---/<generated repo clones for the assignment>
---/<generated repo clones for the assignment>
---/...

```

# How to use

1. Clone this repo.
1. Setup dependency following the section below.
1. Run `python3 main.py`

# Dependency

- `pip install -r requirements.txt`
- Setup Google Sheet API - download `credentials.json` and place in folder `python-script`.
  - [Go to Sheet API Doc](https://developers.google.com/sheets/api/quickstart/python) and press "Enable the google sheets api" to download.
  - Prepare a google spreadsheet where you'll use it to store your grading and comments.
  - Copy the spreadsheet ID and put it in `credentials.py` as `os.environ['SPREADSHEET_ID'] = 'YOUR SPREADSHEET ID'`
- Follow the instructions in `credentials_example.py`. This file is for github API that can search and get repo info. Not needed if the repos for the assignment does not come from Github Classroom.
- Follow the instructions in `settings_example.py` to setup your local setting.

- (Optional) Make sure you have `vscode` and `Path` setup, so when you run `code .` in terminal, vscode will open the current directory. [See this page for how to setup](https://code.visualstudio.com/docs/setup/mac).
- (Optional) Using `iterm2` if you want to use `grade_additional_command`, which lets you run command that will be executed in the repo directory when you're grading submits.
  - otherwise won't open iterm2 for you even when you set `grade_additional_command`

# Future TODOs

- Late penalty. Since for Github Classroom we already have a late boolean and hook for late delta, we can apply penalty based on the duration over due date.
- Read record from google spreadsheet instead of local cache. This can let us be machine-indenpedent and easier to grade using public computer.

#### Lab 2 Part A Grading Insights

- [Ramdom] sometimes node toss warning about not using `catch()`. onrejected vs catch in Promise?
- [Case D] Reject immediately even before loop.
- [Case C] `setTimeout(resolve(), bignum);` is wrong use of `setTimeout` since the 1st arg should be a function instead of a value! See [this SO post](https://stackoverflow.com/questions/39538473/using-settimeout-on-promise-chain)
- [Case B] some student's loop is blocking and not using Promise async feature.
- [Case A] reject in the first loop round, but the loop still keeps going. (`resolve()` and `reject()` will not stop loop? Should instead explicitly do `return` after `resolve()` or `reject()`. [See this post](https://stackoverflow.com/questions/32536049/do-i-need-to-return-after-early-resolve-reject))
- [Performance] `countBig()`: putting `resolve()` outside of `while` is much faster (10ms). If you put `if` in `while` then do `resolve()`, you have to keep checking for each round, which is much slower (500-1200ms).

# Run On A LRC Machine

Download [this script](https://raw.githubusercontent.com/SI669-internal/mass_clone/master/install-env-lrc-and-run.sh).

## Prepare Environment

```shell

cd $HOME && \
git clone https://github.com/mxcl/homebrew.git && \
export PATH=$HOME/homebrew/bin:$PATH && \


# in order to proceed, mxay need to do brew update. See instruction prompted
brew update

xcode-select --install

read -p "You should see a prompt asking you to install software (xcode command line tools), please do so by pressing 'install' button. When you finish, proceed by hitting enter." yn

brew install python3 # will take a while

if [[ $? -eq 0 ]]; then
    ;
else
    echo "ERROR: Failed to brew install python 3. See error message above."
    return
fi

```

## Install And Run

```shell

# Project Setup

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

read -p "Please follow the config instruction in https://github.com/SI669-internal/mass_clone . We will open the folder in Finder for you. Sounds good? (Y)" yn
open .

read -p " Finished following instructions? (Y/n)" yn
case $yn in
    [Yy]* ) python3 main.y;;
    [Nn]* ) exit;;
    * ) echo "Please answer by y or n."
esac


```