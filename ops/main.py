import sys
import anyio
import dagger
import exceptions, settings

try:
    async def stage():
        """ main.yaml workflow

                APIs:   minus one API: tox-gh-actions
                Files: minus two file (main.yml, release
                Extra: custom error handling
                Submodules: minus 4
        """
        async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
            results = (
                client.container()
                # pull container
                .from_("python:3.11-slim-buster") # later do the matrix from settings.python_versions[*]
                .with_directory("/host", client.host().directory(
                    settings.ci_environment,
                    settings.compatibility,
                    settings.gherkin,
                    settings.messages,
                    ) )  # Yay, no more .gitmodules file
                .with_directory("/host", client.host().directory("../src", "../tests")
                .with_exec(["python", "-m", "pip", "install", "--upgrade", "pip"])
                .with_exec(["pip", "install", "--upgrade", "setuptools"])
                .with_exec(["pip", "install", "--upgrade", "tox~=4.0", "codecov"]) # minus one API: tox-gh-actions
                .with_exec(["tox"])
                .with_exec(["codecov"])
                .with_exec(["pip", "install", "--upgrade", "pip"])))
            await results

        # except exceptions.DaggerError as exc:
        #     raise exc

if __name__ == "__main__":
    anyio.run(stage)
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
