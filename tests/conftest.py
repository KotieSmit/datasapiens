# conftest.py
import pytest
from playwright.sync_api import BrowserType, Playwright, sync_playwright
from typing import Dict, Generator
import os
import time
from datetime import datetime
import os


# @pytest.fixture(scope="session")
# def playwright() -> Generator[Playwright, None, None]:
#     pw = sync_playwright().start()
#     yield pw
#     pw.stop()


# @pytest.fixture(scope="session")
# def browser_type(playwright: Playwright, browser_name: str) -> BrowserType:
#     return getattr(playwright, browser_name)


@pytest.fixture(scope="session")
def context(
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
    base_url,
):
    """Instantiate a browser context, and load state"""
    os.system("rm -rf ./browser_state")
    os.system("cp -r ./browser_states/signed-up ./browser_state ")
    # browser_type = BrowserType()
    if base_url == "":
        base_url = "http://localhost:3567"
    context = browser_type.launch_persistent_context(
        "./browser_state",
        **{
            **browser_type_launch_args,
            **browser_context_args,
            "locale": "de-DE",
            "base_url": base_url,
            "chromium_sandbox": True,
            "args": ["--no-sandbox"],
        },
    )
    # context = browser_type.launch( **{
    #     **browser_type_launch_args,
    #     **browser_context_args,
    # })
    # context = browser_type.chromium.launch(
    #     **{
    #     **browser_type_launch_args,
    #     **browser_context_args,}
    # )
    # pw = sync_playwright().start()
    # context = pw.chromium.launch(**{
    #     **browser_type_launch_args,
    #     **browser_context_args,})
    yield context

    # context.close()


@pytest.fixture(autouse=True)
def resource(context):
    """Close the current tab"""
    yield "resource"
    context.pages[-1].close()


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs["context"]

            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# make a screenshot with a name of the test, date and time
def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace(
        "/", "_"
    ).replace("::", "__")
    # driver.save_screenshot(file_name)
    driver.pages[1].screenshot(path=f"/tmp/images/{file_name}", full_page=True)
