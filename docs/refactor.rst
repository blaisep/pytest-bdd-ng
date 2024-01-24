:slide-numbers: true

.. title:: Desert Island Daggerization

----

Desert Island Daggerization
===========================

An opinionated guide to refactoring legacy projects.


----

Why are you here?
=================

We want to offer you an opinionated guide to refactor existing projects.
Opinionated in the sense that propose a structure to help you get "80% of the bang for 20% of the buck"

----

What will talk about?
=====================

    * The project today
    * Challenges
    * Goals & Indicators
    * Hypothesis & Strategy
    * Results

----

The project today
=================

    * Pytest-BDD-NG is a refactor of a pytest plugin for Cucumber.
    * Upstream does not have an official release of the python implementation.
    * Pytest-BDD has fallen behind the Upstream

----

Challenges
==========

    * External dependencies pinned as repos in ``.Gitmodules``
    * Local build and test is cumbersome and difficult to reproduce
    * Depending on github actions means commit/push to github for every iteration.
    * Cycle time casn be as long as 29 minutes.

----

Goals & Indicators
==================

Find the opportunities for improvement, starting with the **quick wins**
    * Reduced cycle time
    * Reduced number of APIs
    * Consolidated settings management
    * Accelerated iterations

----

Hypothesis
==========

Refactoring the automation using Dagger will achieve the goals and improve developer experience.

----

Step 0
========

Begin with a local clone on a machine with the Dagger Engine and Python SDK

----


Step 1 Reverse engineer the workflow
-------------------------------------

    * Test
    * Build
    * Release
    * Settings


----

Create the dagger client
------------------------

``main.py`` to set up a basic scaffold. Run a simple "Hello World".

----

Consolidate settings
--------------------

``settings.py`` for variables which you can then ``import`` into python.

----


Install the airbags
-------------------

Plan for failure; custom exceptions will signal where your automation breaks.

----

Run tests
---------

    * ``hello.py`` to make sure the client is working
    * ``test.py`` to run unit tests and do the workflow

----

Build the project
-----------------

``build.py`` to run build the project and run matrix tests.

----

Release a version
-----------------

``release.py`` to create packages for external consumption.

----

Conclusion
==========

    * Faster Cycle time
    * Fewer APIs
    * Fewer Hosts
    * Zero gitmodules
    * Custom Error Handling
