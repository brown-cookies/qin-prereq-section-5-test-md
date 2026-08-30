# testing/

Section 5 is about proving your code works without you being there to check. Everything
before this section you verified by running it and looking. That does not scale, it does not
survive you forgetting, and it is not what section 8 will run on every push. Tests are the
thing that does.

This section has three parts, and they are not the same kind of work:

1. **Four short drills**, predict-before-run, on a sandbox that is already written for you.
   They teach you how `pytest` behaves, which is mostly convention and not something you can
   reason your way to.
2. **Three programs, and the test suites you write for them.** This is the bulk of the
   section and the thing you hand in. Nobody has written any tests for these; that is your job.
3. **One thing done live in your session**, described at the bottom of this file. Do not do
   it in advance.

## Why the drills come first, and why they are short

Sections 1 to 4 all asked you to predict the output of something. That still works here, but
only for a narrow slice: how the tool itself behaves. Whether a broken test is reported as a
*failure* or an *error*, how many times a fixture actually runs, what `pytest` does with a
test that asks for something that does not exist. That slice is real, it is genuinely
surprising, and you cannot derive it — it is a set of decisions the people who wrote `pytest`
made, the same way status codes were.

But predicting output stops being the right exercise the moment you are the one writing the
tests. So the drills are four, not five, and then the section changes shape.

## The order of work

1. Read `DRILLS.md`, including the reading block at the top. It has the vocabulary you cannot
   derive.
2. Work the four drills, alone, in order, filling in `prediction-sheet.md` as you go rather
   than afterward.
3. Read `TESTS.md` and write the three suites.
4. Bring the sheet and the suites to your session, and bring your section 4 build with you.

## Getting set up

This is the first section that needs something installed, which means it is the first section
where the `venv` and `requirements.txt` boxes from section 1 stop being theoretical.

From `python/testing`, in Git Bash:

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pytest --version
```

That last line should print a version. If it prints nothing, or prints an error about
`pytest` not being found, your virtual environment is not active — that is the usual cause and
it is worth recognising now rather than in section 8.

Every command in this section assumes that environment is active. When you come back to this
after a break, activate it again before anything else.

## Run each drill from inside its own directory

```
cd sandbox/drill1
pytest
```

Not from `python/testing`, and not from the repository root. Each drill is a self-contained
little project, and running `pytest` from a directory above them will collect all four at
once and give you a mess that has nothing to teach you. `cd` into the drill, run `pytest`,
`cd` back out.

## Git Bash, not PowerShell

Same as sections 2, 3 and 4, and the same reasoning. Use Git Bash.

## The fourth column, again

`prediction-sheet.md` has four columns and the fourth is still the one that counts. Here it is
"which mechanism produced the difference" — not "I was wrong". `pytest` behaved the way it did
for a reason, and naming the reason is the entire exercise. "Don't know yet" is a real entry
and a better one than a guess written after you saw the answer.

## How the three suites get marked

Your suites are run against a copy of each program in which something has been changed. A
suite that passes against both copies has not tested anything, whatever it looks like on the
page.

You are told this in advance on purpose, because it is not a trick — it is the only honest way
to check a test suite, and knowing it should change how you write one. It should not change
what you write tests *for*: aim at what each program is supposed to do, and the changed copies
take care of themselves. Writing tests aimed at the marking rather than at the program is the
one approach that reliably fails this.

`TESTS.md` has the rest of the brief.

## The live part

Bring your section 4 build to the session — the GitHub tool from `http/BUILD.md`, whatever
state it is in. Part of this session is done together, on your own code, the same way the
conflict drill in section 3 was. Do not try to get ahead of it by testing that tool
beforehand; there is nothing to gain and the session is where it is useful.

If you do not have a section 4 build, say so on Discord before the session rather than on the
day. There is a version of this that works without one.

## If nothing works

If `pytest` will not install, will not run, or does something no part of this file describes,
that is not a sign you are not ready for the section. It is almost always small. Say so on
Discord on the day it happens.
