import json
import os

import requests
from behave import given, when, then


@given('the base URL is "{base_url}"')
def step_impl(context, base_url):
    context.base_url = base_url
    context.bin_id = None
    # JSONBin needs your master key on every request (set it as an environment variable)
    master_key = os.getenv("JSONBIN_MASTER_KEY")
    assert master_key, "Set the JSONBIN_MASTER_KEY environment variable"
    context.headers = {"Content-Type": "application/json", "X-Master-Key": master_key}


@given("a bin exists with the payload '{payload}'")
def step_impl(context, payload):
    full_url = f"{context.base_url}/b"
    context.response = requests.post(full_url, headers=context.headers, data=payload, timeout=30)
    assert context.response.status_code == 200, context.response.text
    context.bin_id = context.response.json()["metadata"]["id"]


@when("I create a bin with the payload '{payload}'")
def step_impl(context, payload):
    full_url = f"{context.base_url}/b"
    context.response = requests.post(full_url, headers=context.headers, data=payload, timeout=30)
    if context.response.status_code == 200:
        context.bin_id = context.response.json()["metadata"]["id"]


@when('I send a GET request to "{endpoint}"')
def step_impl(context, endpoint):
    full_url = f"{context.base_url}{endpoint}"
    # Store the response in the context to use in the 'then' step
    context.response = requests.get(full_url, headers=context.headers, timeout=30)


@when("I read the bin")
def step_impl(context):
    full_url = f"{context.base_url}/b/{context.bin_id}/latest"
    context.response = requests.get(full_url, headers=context.headers, timeout=30)


@given("I delete the bin")
@when("I delete the bin")
def step_impl(context):
    full_url = f"{context.base_url}/b/{context.bin_id}"
    context.response = requests.delete(full_url, headers=context.headers, timeout=30)
    if context.response.status_code == 200:
        context.bin_deleted = True  # tells environment.py not to delete it again


@then('the response should contain "{expected_text}"')
def step_impl(context, expected_text):
    # Assert that the expected text is in the response body
    assert expected_text in context.response.text, \
    f"Response text did not contain '{expected_text}'. Actual text: '{context.response.text}'"


@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    # Assert the HTTP status code
    assert context.response.status_code == status_code, \
    f"Expected status code {status_code} but got {context.response.status_code}"