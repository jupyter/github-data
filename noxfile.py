import nox
from shlex import split
from os.path import realpath

nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "uv"

@nox.session(name="docs-live")
def docs_live(session):
    for ii in ["requirements.txt"]:
        session.run("uv", "pip", "install", "-U", "-r", ii, silent=True)
    session.chdir("book")
    session.run(*"myst start --execute".split(),*session.posargs)

@nox.session
def docs(session):
    for ii in ["requirements.txt"]:
        session.run("uv", "pip", "install", "-U", "-r", ii, silent=True)
    session.chdir("book")
    session.run(*"myst build --html --execute".split(),*session.posargs)

@nox.session
def lab(session):
    for ii in ["requirements.txt"]:
        session.run("uv", "pip", "install", "-U", "-r", ii, silent=True)
    session.run(*split("jupyter lab ."))

@nox.session(name="download")
def download(session):
    """Download GitHub data for Jupyter organizations.

    Usage:
        nox -s download           # Download all orgs
        nox -s download -- jupyter-book  # Download specific org
    """
    session.run("uv", "pip", "install", "-U", "-r", "requirements.txt", silent=True)

    # Default organizations to download
    orgs = ["jupyter", "jupyterlab", "jupyter-book", "jupyter-server", "jupyterhub"]

    # Allow override from command line
    if session.posargs:
        orgs = session.posargs

    print(f"\n{'='*60}")
    print(f"Downloading data for organizations: {', '.join(orgs)}")
    print(f"{'='*60}\n")

    for org in orgs:
        print(f"\n{'='*60}")
        print(f"Processing organization: {org}")
        print(f"{'='*60}\n")
        session.run("python", "scripts/download_issues.py", org)
