import re
from typing import Literal

from src.catalog import Book, Catalog

from messages import DataTable, Step  # type:ignore[attr-defined]
from pytest_bdd import given, step, then, when
from pytest_bdd.compatibility.pytest import FixtureLookupError, FixtureRequest


def get_books_from_data_table(data_table: DataTable):
    step_data_table_titles = [cell.value for cell in data_table.rows[0].cells]
    assert step_data_table_titles == ["Author", "Title"]

    author_and_title_list = [[cell.value for cell in row.cells] for row in data_table.rows[1:]]

    books = [Book(author, title) for author, title in author_and_title_list]
    return books


@given("these books in the catalog", target_fixture="catalog")
def these_books_in_the_catalog(step: Step):
    catalog = Catalog()

    books = get_books_from_data_table(step.data_table)
    catalog.add_books_to_catalog(books)
    yield catalog


@when(
    re.compile('a (?P<search_type>name|title) search is performed for "(?P<search_term>.+)"'),
    target_fixture="search_results",
)
def a_search_type_is_performed_for_search_term(
    request: FixtureRequest, search_type: Literal["name", "title"], search_term: str, catalog: Catalog
):
    try:
        search_results = request.getfixturevalue("search_results")
    except FixtureLookupError:
        search_results = []

    if search_type == "title":
        search_results.extend(catalog.search_by_title(search_term))
    elif search_type == "name":
        search_results.extend(catalog.search_by_author(search_term))
    else:
        assert False, "Unknown"

    yield search_results


@then("only these books will be returned")
def only_these_books_will_be_returned(step: Step, catalog: Catalog):
    expected_books = get_books_from_data_table(step.data_table)
    assert all([book in catalog.storage for book in expected_books])