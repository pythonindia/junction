"""Automation using nox.
"""

import nox

nox.options.sessions = ["dev"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True


@nox.session(python="3.5")
def dev(session):
    session.install("-r", "requirements.txt")

    session.run("python", "manage.py", *session.posargs)


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "tools/requirements-test.txt")

    session.run("pytest", "--cov", "--cov-report=xml", "-v", "--tb=native")
    session.run("coverage", "report", "-m")


@nox.session(python=["3.5", "3.6", "3.7", "3.8"])
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python="3.5")
def docs(session):
    session.install("-r", "tools/requirements-docs.txt")

    def get_sphinx_build_command(kind):
        return [
            "sphinx-build",
            "-W",
            "-d",
            "docs/build/_doctrees/" + kind,
            "-b",
            kind,
            "docs/source",
            "docs/build/" + kind,
        ]

    session.run(*get_sphinx_build_command("html"))
