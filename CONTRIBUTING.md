# CONTRIBUTING

We welcome new contributors. This document will guide you
through the process.

## FORK

Fork the project and check out your copy.

```bash
git clone https://github.com/<your-username>/perprof-py.git
cd perprof-py
git remote add upstream https://github.com/abelsiqueira/perprof-py.git
```

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

```bash
git checkout -b my-feature-branch -t origin/master
```

## COMMIT

Make sure git knows your name and email address:

```bash
git config --global user.name "J. Random User"
git config --global user.email "j.random.user@example.com"
```

Writing good commit logs is important.  A commit log should describe what
changed and why.  Follow these guidelines when writing one:

1. The first line should be 50 characters or less and contain a short
   description of the change.
2. Keep the second line blank.
3. Wrap all other lines at 72 columns.

## REBASE

Use `git rebase` (not `git merge`) to sync your work from time to time.

```bash
git fetch upstream
git rebase upstream/master
```

## PUSH

```bash
git push origin my-feature-branch
```

Go to your fork and select your feature branch.  Click
the 'Pull Request' button and fill out the form.

Pull requests are usually reviewed within a few days. If there are comments
to address, apply your changes in a separate commit and push that to your
feature branch.

## RELEASE

- Branch into `release-vx.y.z`.
- Update `CHANGELOG.md` (create a new release from the unreleased changes).
- Update `x.y.z`in `pyproject.toml`, `perprof/__init__.py`.
- Run the tests and the pre-commit for all files: `pytest -v` and `pre-commit run -a`.
- Commit.
- Create a pull request.
- Merge the pull request after the tests pass.
- Create a GitHub tag and release. It should trigger the deployment.
- Check <https://pypi.org/project/perprof-py>.

### Manual package deployment

If the PyPI deployment did not work, these are the instructions to do it manually:

```bash
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
```

Visit <https://test.pypi.org/project/perprof-py> to check that it was uploaded.

Then, in another terminal (don't close the old one):

```bash
cd $(mktemp -d)
python -m venv env
source env/bin/activate
pip install --upgrade pip setuptools
pip -v install --no-cache-dir \
    --index-url https://test.pypi.org/simple \
    --extra-index-url https://pypi.org/simple perprof-py
```

Finally, upload to pypi org, by going back to the first terminal and running:

```bash
twine upload -u __token__ -p THETOKEN dist/*
```

You also have to manually create a GitHub release.
After the release on GitHub, the Docker image should be uploaded automatically
to <https://hub.docker.com/r/abelsiqueira/perprof-py>.
