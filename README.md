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

## Prerequisite

You should have `node ionic cordova` installed globally for SI 669. It's best to have `Visual Studio Code` installed, but you can also use your own editor of preference.

# Quickstart

1. At proejct root, run `. ./setup-project.sh`
2. Setup Google Sheet API - download `credentials.json`.
  - [Go to Sheet API Doc](https://developers.google.com/sheets/api/quickstart/python) and press "Enable the google sheets api" to download. After you have the `json` credential, place in folder `python-script`.
  - ~~Prepare a google spreadsheet where you'll use it to store your grading and comments.~~
  - ~~Copy the spreadsheet ID and put it in `python-script/credentials.py` as `os.environ['SPREADSHEET_ID'] = 'YOUR SPREADSHEET ID'`~~
3. Enter your github account/password in `python-script/credentials.py`. This file is for github API that can search and get repo info. Not needed if the assignment you are working on does not use Github Classroom (in such case, you'll have to feed the repo info using a google spreadsheet).
  - Don't worry - all your credentials are gitignored and won't be pushed to the repo.
4. `cd python-script` and turn on the virtual environment by `. ./venv/bin/activate`
5. `python main.py` to run the program.

# Configuration

- There're two config files, `python-script/settings_local.py` and `python-script/script-session/local-config.json`. `local-config.json` has higher priority and will overwrite the settnigs in `settings_local.py`.
- `settings_local.py` provides a setting base for default. On the other hand, `local-config.json` lets you preserve and reuse settings for each assignment.
- The recommended workflow will be to test your settings in `settings_local.py` for the assignment you're workin on first. When you feel comfortable with that setting, you can copy that setting to `local-config.json` and specify the assingment prefix accordingly.

- The default setting assume you have `vscode` installed. See `python-script/settings_local.py`, there's a `"grade_additional_command": "open -a Visual\ Studio\ Code .",` line. If you want to use your own editor, change the name of the last argument.

- ~~(Optional) Using `iterm2` if you want to use `grade_additional_command`, which lets you run command that will be executed in the repo directory when you're grading submits.~~
  - ~~otherwise won't open iterm2 for you even when you set `grade_additional_command`~~


# Future TODOs

- Late penalty. Since for Github Classroom we already have a late boolean and hook for late delta, we can apply penalty based on the duration over due date.
- Read record from google spreadsheet instead of local cache. This can let us be machine-indenpedent and easier to grade using public computer.
  - Set dynamic for main sheet range, expose range to config.
  

#### Lab 2 Part A Grading Insights

- [Ramdom] sometimes node toss warning about not using `catch()`. onrejected vs catch in Promise?
- [Case D] Reject immediately even before loop.
- [Case C] `setTimeout(resolve(), bignum);` is wrong use of `setTimeout` since the 1st arg should be a function instead of a value! See [this SO post](https://stackoverflow.com/questions/39538473/using-settimeout-on-promise-chain)
- [Case B] some student's loop is blocking and not using Promise async feature.
- [Case A] reject in the first loop round, but the loop still keeps going. (`resolve()` and `reject()` will not stop loop? Should instead explicitly do `return` after `resolve()` or `reject()`. [See this post](https://stackoverflow.com/questions/32536049/do-i-need-to-return-after-early-resolve-reject))
- [Performance] `countBig()`: putting `resolve()` outside of `while` is much faster (10ms). If you put `if` in `while` then do `resolve()`, you have to keep checking for each round, which is much slower (500-1200ms).

# ~~Run On A Public Computer~~

## TL;DR

- Download [this script](https://raw.githubusercontent.com/SI669-internal/mass_clone/master/install-env-lrc-and-run.sh), or see `install-env-lrc-and-run.sh` in the project root folder.

- Run the script
- Download `mass-clone-local-needs.zip`
- Wait for installation to complete

## What does the script do?

1. Run in user permission, no need for sudo.
1. Install brew
1. Install python3 and venv
1. Prompt you to prepare some of the dependencies.
1. Start the script for you at the end.