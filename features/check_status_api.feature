Feature: JSONBin API - create, read and delete bins

  Background:
    Given the base URL is "https://api.jsonbin.io/v3"

  @tag1
  Scenario Outline: Create a bin with different payloads
    When I create a bin with the payload '<payload>'
    Then the response status code should be 200
    And the response should contain "metadata"
    And the response should contain "<expected_text>"

    Examples:
      | payload                          | expected_text |
      | {"name": "Alice", "age": 30}     | Alice         |
      | {"items": [1, 2, 3]}             | items         |
      | {"active": true, "tags": ["qa"]} | active        |

  @tag1
  Scenario: Read an existing bin
    Given a bin exists with the payload '{"hello": "world"}'
    When I read the bin
    Then the response status code should be 200
    And the response should contain "world"

  @tag2
  Scenario: Delete an existing bin
    Given a bin exists with the payload '{"temp": true}'
    When I delete the bin
    Then the response status code should be 200

  @tag2
  Scenario: A deleted bin can no longer be read
    Given a bin exists with the payload '{"temp": true}'
    And I delete the bin
    When I read the bin
    Then the response status code should be 404