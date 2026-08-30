# Section 5 — the three suites

This is the section. The drills were the tool; this is the work.

## What you are doing

`programs/` holds three small programs. All three work. None of them has a single test written
for it.

You are writing a `pytest` suite for each one. Not a token test each — a suite that would tell
somebody, without them reading the program, whether it still does what it is supposed to do.

## The programs

**`receipt.py`** — costs a depot run. Reads a manifest of comma-separated lines, works out what
each row costs, applies a bulk discount, prints a receipt. Run it against
`samples/manifest.csv` and `samples/manifest-short.csv` and read what it prints.

**`logsweep.py`** — summarises a directory of log files. Counts levels per file, prints a line
for each, prints a total. Run it against `samples/logs`.

**`depotwatch.py`** — reports on what the depot API is holding. It talks to the section 4
sandbox server, which you already have: start `python/http/sandbox/depot_api.py` in another
terminal the same way you did in section 4, then run `depotwatch.py`.

Run all three, several times, with different inputs, before you write a single test. You cannot
test a program you have not watched behave.

## What each suite has to do

Common to all three:

- Cover what the program is **supposed to do**, including the edges — the empty case, the
  boundary value, the input that should be rejected. Not just the happy path you saw when you
  ran it.
- Every test asserts something real about a result. A test that runs code without checking the
  answer is not a test, however green it goes.
- Test names say what is being checked. `test_total_applies_the_bulk_discount` is a name;
  `test_2` is not.
- Where the program is supposed to reject something, prove that it does.

Three further conditions, one per program. These are conditions on the suite, not hints about
the code — meeting them is part of the brief:

- **`receipt.py`** — your suite must pin down the arithmetic exactly, not approximately. Every
  rule the program applies should have a test that would notice if the rule changed.
- **`logsweep.py`** — your suite must not read anything in `samples/`, must not depend on any
  file that already exists on your machine, and must leave nothing behind when it finishes. It
  must also check what the program *prints*, not only what it returns, because most of what
  this program does is printing.
- **`depotwatch.py`** — your suite must pass with the depot server **not running**. All of it,
  including the parts that report on shipments, and including each of the ways the program can
  fail to get an answer. Run it with the server off; if anything in your suite needs the server,
  it is not finished.

That last condition is the one to start thinking about early. It is the whole reason
`depotwatch.py` is in this set, and it is the box on your checklist that says you know roughly
what mocking is.

## Where the tests go

Make a new repository. Copy the three programs into it, write the suite there, and deliver it
as a pull request from a feature branch — the same way as section 4. Do not open a pull request
against this material repository.

Lay it out like this, because the marking depends on it:

```
your-repo/
    receipt.py
    logsweep.py
    depotwatch.py
    tests/
        test_receipt.py
        test_logsweep.py
        test_depotwatch.py
    requirements.txt
```

The three programs sit at the top, unchanged, imported by name. `pytest`, run from the root of
your repository with no arguments and no flags, must find and run everything.

Getting `tests/` to import a module sitting at the root is its own small problem and it is not
the subject of this section. An empty `conftest.py` at the root of your repository is one way to
solve it; there are others; any of them is fine. If you lose more than a few minutes to an
`ImportError` that has nothing to do with testing, that is the thing you have hit — say so on
Discord rather than grinding at it.

`requirements.txt` pins `pytest` and anything else you need, exactly, the same way section 4
asked you to pin `requests`.

## Do not change the programs

Not to make them easier to test, not to fix anything you think is wrong with them, not at all.
They go into your repository as they came out of this one.

If you find yourself wanting to change one, write that down instead — what you wanted to change
and why — and bring it to the session. That note is worth more than the change would have been,
and this is the only part of the brief where "I could not do it without changing the program"
is a genuinely interesting answer rather than a problem.

## The note you hand in with it

Three short paragraphs, one per program, in a `NOTES.md` at the root of your repository. For
each one:

- what you had to set up before you could assert anything
- anything about how the program is written that decided how you wrote its tests
- anything you wanted to test and could not

Three or four sentences each is plenty. This is the fourth column again, in prose: not what you
did, but what the program's shape made you do.

## How this is marked

Your suite is run against a copy of each program in which something has been changed. Your suite
should fail. A suite that passes against both copies has not tested anything.

You are told this up front because it is not a trick — it is the only honest way to check a test
suite, and it should change how you write one. It should not change what you write tests *for*.
Aim at what each program is supposed to do and the changed copies look after themselves; aim at
the marking instead, and you will miss, because you do not know what was changed.

## What you are not doing

- No coverage tooling, no test-runner configuration beyond what you need, no plugins.
- No `unittest`, no `assertEqual`. Plain `assert`, the way the drills did it.
- No rewriting the programs.
- No testing the section 4 build. That part is done live, in the session, and doing it in
  advance costs you the bit that is worth being there for.

## How long this should take

An evening or two, in total, for all three. If one of them alone is eating a weekend, stop and
say so — that is information, and it is the useful kind.

## What to submit

The pull request link, in your section 5 update on Discord, plus the filled prediction sheet
brought to your session.

Bring your section 4 build to the session as well, whatever state it is in.
