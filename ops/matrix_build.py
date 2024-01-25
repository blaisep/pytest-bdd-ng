import os
import sys
import anyio
import itertools
import dagger
import settings

sys.path.append("/ops")
async def main():
    """ main.yaml workflow

            APIs:   minus one API: tox-gh-actions
            Files: minus two file (main.yml, release
            Extra: custom error handling
            Submodules: minus 4
    """

    print("Starting")
    # initialize dagger client:
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project source
        src = client.host().directory(os.path.abspath(settings.dir_source))
        tests = client.host().directory(os.path.abspath(settings.dir_tests))
        python = (
        for settings.os, settings.python_version in itertools.product(settings.matrix.os_version,
                                                                      settings.matrix.python_version):
            client.container()
            # pull container
            .from_("python:3.11-slim-buster")
            .with_directory("/host", client.host().directory(
                client.git(settings.ci_environment.url).commit(settings.ci_environment.commit).tree(),
                client.git(settings.compatibility.url).commit(settings.compatibility.commit).tree(),
                client.git(settings.gherkin.url).commit(settings.gherkin.commit).tree(),
                client.git(settings.messages.url).commit(settings.messages.commit).tree()
                ) )  # and voila, no more .gitmodules file
            .with_directory("/host", client.host().directory(src, tests)
            .with_exec(["python", "-m", "pip", "install", "--upgrade", "pip"])
            .with_exec(["pip", "install", "--upgrade", "setuptools"])
            .with_exec(["pip", "install", "--upgrade", "tox~=4.0", "codecov"]) # minus one API: tox-gh-actions
            .with_exec(["tox"])
            .with_exec(["codecov"])
            .with_exec(["pip", "install", "--upgrade", "pip"])
                            )
        )
        await python

        # except exceptions.DaggerError as exc:
        #     raise exc

if __name__ == "__main__":
    anyio.run(main)
    """
    Refactor this workflow into python...
              python -m pip install --upgrade pip
              pip install -U setuptools
              pip install "tox~=4.0" "tox-gh-actions~=3.0" codecov
          - name: Test with tox
            run: |
              tox
              codecov
          - name: Build checking
            if: "matrix.python-version == '3.12'"
            env:
              TWINE_USERNAME: __token__
              TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
            run: |
              python -m pip install --upgrade build twine
              python -m build
              twine check dist/*
    """
