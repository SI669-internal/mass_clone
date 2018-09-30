# How to use

1. Setup dependency following the section below.
1. Edit main.py setting for your needs. Inline explanation provided.
1. Run `python3 main.py`

# Dependency

- `pip -r requirements.txt`
- Make sure you have `vscode` and `Path` setup, so when you run `code .` in terminal, vscode will open the current directory.
- (Optional) Using `iterm2` if you want to use `grade_additional_command`, which lets you run command that will be executed in the repo directory when you're grading submits.
  - otherwise won't open iterm2 for you even when you set `grade_additional_command`
- Setup Google Sheet API - download `credentials.json`.
  - [Go to Sheet API Doc](https://developers.google.com/sheets/api/quickstart/python) and press "Enable the google sheets api" to download.
- Create a `credentials.py` file that provides values for `os.environ['GITHUB_USER']` and `os.environ['GITHUB_PASSWORD']`. This is for github API that can search and get repo info. Not needed if the repos for the assignment does not come from Github Classroom.

### Lab 2 Part A Grading Insights

- [Ramdom] sometimes node toss warning about not using `catch()`. onrejected vs catch in Promise?
- [Criteria] `setTimeout(resolve(), bignum);` is wrong use of `setTimeout` since the 1st arg should be a function instead of a value! See [this SO post](https://stackoverflow.com/questions/39538473/using-settimeout-on-promise-chain)
- [Criteria] some student's loop is blocking and not using Promise async feature.
- [Criteria] got rejected in the first loop round.
- [Performance] `countBig()`: putting `resolve()` outside of `while` is much faster (10ms). If you put `if` in `while` then do `resolve()`, you have to keep checking for each round, which is much slower (500-1200ms).