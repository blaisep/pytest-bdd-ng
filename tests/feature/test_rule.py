"""Test feature background."""

# language=gherkin
FEATURE = '''\
    Feature: Some rules
        """
        Feature description
        """

      Background:
        """
        Background description
        """
        Given fb
          """
          Step description
          """

      Rule: A
        The rule A description

        Background:
          Given ab

        Example: Example A
          Given a

      Rule: B
        The rule B description

        Example: Example B
          Given b

      Rule: C
        The rule C description

        Example: Example CA
          Given c

        Rule: CB
            Example: CBA
              Given caa

            Example: CBB
              Given cab

            Example: CBC
              Given ca<key>

              Examples:
              | key |
              |  c  |
              |  d  |
              |  e  |
'''

# language=python
STEPS = """\
    from pytest_bdd import given

    @given("{}")
    def step():
        pass
"""


def test_background_basic(testdir):
    """Test feature background."""
    testdir.makefile(".feature", rule=FEATURE)

    testdir.makeconftest(STEPS)

    result = testdir.runpytest()
    result.assert_outcomes(passed=8)
