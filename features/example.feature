Feature: load testing data

  Scenario: load Redis and Postgres fixtures
    Given postgres "pg-01-int" command
      """
      TRUNCATE users;
      INSERT INTO users (id, version)
      VALUES
        (1, 0),
        (2, 0),
        (3, 0);
      """
    And redis "redis-01-int" command "PING"
    And redis "redis-01-int" command "FLUSHALL"

    When redis "redis-01-int" command "SET hello world"
    And redis "redis-01-int" command "SET world hello"
    And redis "redis-01-int" command "GET hello"

    Then redis "redis-01-int" KEYS *