"""
scope="function" -> Default
Lifetime: The fixture is created and torn down for each individual test function.

scope="class"
Lifetime: The fixture is created once per test class and shared across all methods in that class.

scope="session"
Lifetime: The fixture is created once per entire pytest session and shared across all tests, even in different test modules.

scope="module"
Lifetime: The fixture is created once per test module (file) and shared across all tests in that module.

autouse=True
Autouse enables your test functions to automatically utilize a fixture without explicitly requesting it.
example : @pytest.fixture(autouse=True)

@pytest.mark.skip(reason = " Optional message")
If You want to skip a test , mark it as skipped with this.

@pytest.mark.test_clean_old_entries
If you want to run only this test. CMD : pytest -m test_clean_old_entries



Monkey Patching :
https://docs.pytest.org/en/stable/how-to/monkeypatch.html

Teardown/Cleanup (AKA Fixture finalization) :
https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization

PyTest Debug :
https://pypi.org/project/pytest-vscodedebug/

In order to run unit tests -> "pytest tests/unit"
In order to run integration tests -> "pytest tests/integration"
"""
