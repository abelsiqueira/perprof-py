# CONTRIBUTING

We welcome new contributors. This document will guide you
through the process.

## FORK

Fork the project and check out your copy.

    $ git clone https://github.com/<your-username>/perprof-py.git
    $ cd perprof-py
    $ git remote add upstream https://github.com/abelsiqueira/perprof-py.git

## BRANCH

Create a feature or bug-fix branch and start hacking:

    $ git checkout -b my-feature-branch -t origin/master

## COMMIT

Make sure git knows your name and email address:

    $ git config --global user.name "J. Random User"
    $ git config --global user.email "j.random.user@example.com"

Writing good commit logs is important.  A commit log should describe what
changed and why.  Follow these guidelines when writing one:

1. The first line should be 50 characters or less and contain a short
   description of the change.
2. Keep the second line blank.
3. Wrap all other lines at 72 columns.

## REBASE

Use `git rebase` (not `git merge`) to sync your work from time to time.

    $ git fetch upstream
    $ git rebase upstream/master

## PUSH

    $ git push origin my-feature-branch

Go to https://github.com/username/perprof-py and select your feature branch.  Click
the 'Pull Request' button and fill out the form.

Pull requests are usually reviewed within a few days. If there are comments
to address, apply your changes in a separate commit and push that to your
feature branch.
