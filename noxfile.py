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
def lab(session):
    for ii in ["requirements.txt"]:
        session.run("uv", "pip", "install", "-U", "-r", ii, silent=True)
    session.run(*split("jupyter lab ."))
