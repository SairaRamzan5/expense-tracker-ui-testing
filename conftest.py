import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()

BASE_URL        = os.getenv("BASE_URL")
LOGIN_PATH      = os.getenv("LOGIN_PATH", "/login")
TEST_EMAIL      = os.getenv("TEST_EMAIL")
TEST_PASSWORD   = os.getenv("TEST_PASSWORD")
INVALID_EMAIL   = os.getenv("INVALID_EMAIL")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }


@pytest.fixture
def page(browser, request) -> Page:
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(30000)

    yield page

    # Save screenshot on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("reports", exist_ok=True)
        page.screenshot(path=f"reports/{request.node.name}_FAILED.png", full_page=True)

    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)