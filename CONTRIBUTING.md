# Contributing to match-recommendation-service
Just a few things to keep in mind.
* Fork and create a new branch from `main`. Make changes and open a pull request.
* Follow PEP guidelines for Python code.
* We do not like tabs here. Please use 2 spaces instead.
* When creating automatic migrations with Alembic, please check the following:
    * Renaming of a table/column is treated as deleting one in autogenerated code. Please refactor it accordingly before pushing.
    * It is better to name your constraints for Alembic to handle it properly.
