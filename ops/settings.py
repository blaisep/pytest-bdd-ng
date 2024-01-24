"""
Settings for CI, test, build, etc.

Consolidate the settings into a single python file from the various existing file formats.
"""

from dotenv import dotenv_values
env_vars = dotenv_values(".env")

# from .github/workflows/release.yaml

# Submodules from other git repos:
ci_environment = client.git("https://github.com/cucumber/ci-environment.git").commit(
    "e6acaf0b83d8eab649eb0bdc9ef2d6e18c14324e").tree()
compatibility = client.git("https://github.com/cucumber/compatibility-kit.git").commit(
    "2fd68be7be09eadee05a02badbf3191be9a27270").tree()
gherkin = client.git("https://github.com/cucumber/gherkin.git").commit(
    "5ec532537888e41c77dd1dd6ace25a72a44cdf0e").tree()
messages = client.git("https://github.com/elchupanebrej/messages").commit(
    "cecd1fed3d47d59af7f0623f148f6752c9e93ee2").tree()

# from .github/workflows/main.yml

python_version = [
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "pypy3.8",
    "pypy3.9",
    "pypy3.10",
    ]

os = {
    "ubuntu" : "latest",
    "windows" : "latest",
    "macos" : "latest",
    }

# let's make it easy for legacy references to {{ matrix.python_version }}' etc
matrix = (python_version, os)
