# CONTRIBUTING

We welcome new contributors. This document will guide you
through the process.

## FORK

Fork the project and check out your copy.

    $ git clone https://github.com/<your-username>/perprof-py.git
    $ cd perprof-py
    $ git remote add upstream https://github.com/abelsiqueira/perprof-py.git

## DEVELOPMENT INSTALL

We use Python 3. Your system might require that you write `python3` to be explicit.

```bash
python -m venv env
. env/bin/activate
pip install --upgrade pip setuptools
pip install --no-cache-dir --editable .
pip install --no-cache-dir --editable '.[dev]'
```

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

## RELEASE

Make sure that

- <CHANGELOG.md> is updated (create a new release from the unreleased changes)
- The version have been updated in <pyproject.toml>, <doc/conf.py>, <perprof/__init__.py>.
- Tests pass (run with `pytest -v`)
- You have a commit with the new version pushed.

Then, in a new terminal

    cd $(mktemp -d)
    git clone https://github.com/abelsiqueira/perprof-py .
    python -m venv env
    source env/bin/activate
    pip install --upgrade pip setuptools
    pip install --no-cache-dir .
    pip install --no-cache-dir '.[dev]'
    pip install --no-cache-dir '.[publishing]'
    python -m build
    twine upload -u __token__ -p THETOKEN -r testpypi dist/*

Visit <https://test.pypi.org/project/perprof-py> to check that it was uploaded.

Then, in another terminal (don't close the old one):

    cd $(mktemp -d)
    python -m venv env
    source env/bin/activate
    pip install --upgrade pip setuptools
    pip -v install --no-cache-dir \
        --index-url https://test.pypi.org/simple \
        --extra-index-url https://pypi.org/simple perprof-py

Finally, upload to pypi org, by going back to the first terminal and running:

    twine puload -u __token__ -p THETOKEN dist/*

You also have to manually create a GitHub release.
After the release on GitHub, the Docker image should be uploaded automatically to <https://hub.docker.com/r/abelsiqueira/perprof-py>.
