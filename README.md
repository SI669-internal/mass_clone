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

- Should have `node ionic cordova` with you.
  - To test in browser, run `ionic serve --platform ios`

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

# Run On A Public Computer

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