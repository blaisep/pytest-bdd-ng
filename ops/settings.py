"""
Settings for CI, test, build, etc.

Consolidate the settings into a single python file from the various existing file formats.
from .github/workflows/release.yaml
"""
import os
# from dotenv import dotenv_values
# env_vars = dotenv_values(".env")   # Keep our secrets out of source control
dir_source = os.path.abspath("../src")
dir_tests = os.path.abspath("../tests")

# Git copies these repos for each action, no caching from one run to another
ci_environment = dict(url="https://github.com/cucumber/ci-environment.git",
                      commit="e6acaf0b83d8eab649eb0bdc9ef2d6e18c14324e"),
compatibility = dict(url="https://github.com/cucumber/compatibility-kit.git",
                     commit="2fd68be7be09eadee05a02badbf3191be9a27270"),
gherkin = dict(url="https://github.com/cucumber/gherkin.git",
               commit="5ec532537888e41c77dd1dd6ace25a72a44cdf0e"),
messages = dict(url="https://github.com/elchupanebrej/messages",
                commit="cecd1fed3d47d59af7f0623f148f6752c9e93ee2")

gitmodules = [ci_environment,
              compatibility,
              gherkin,
              messages]
# github creates this matrix from scratch for each action.
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

os = dict(ubuntu="latest",
    windows="latest",
    macos="latest")

# let's make it easy for legacy references to {{ matrix.python_version }}' etc
matrix = [os, python_version]
