### Dependency

- `pip -r requirements.txt`
- Install vscode and `Path` so `code .` will work.
- Setup Google Sheet API - download `credentials.json`.

### Lab 2 Part A Grading Insights

- [Ramdom] sometimes node toss warning about not using `catch()`. onrejected vs catch in Promise?
- [Criteria] `setTimeout(resolve(), bignum);` is wrong use of `setTimeout` since the 1st arg should be a function instead of a value! See [this SO post](https://stackoverflow.com/questions/39538473/using-settimeout-on-promise-chain)
- [Criteria] some student's loop is blocking and not using Promise async feature.
- [Criteria] got rejected in the first loop round.
- [Performance] `countBig()`: putting `resolve()` outside of `while` is much faster (10ms). If you put `if` in `while` then do `resolve()`, you have to keep checking for each round, which is much slower (500-1200ms).