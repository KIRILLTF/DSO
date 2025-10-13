Feature: Authorization and Security NFR

  Scenario: Пользователь без токена пытается получить item
    Given пользователь не авторизован
    When он делает GET /items/1
    Then сервер возвращает 401 Unauthorized

  Scenario: Пользователь с валидным токеном получает item
    Given пользователь авторизован и имеет токен
    When он делает GET /items/1
    Then сервер возвращает 200 OK и данные item

  Scenario: Пользователь пытается изменить чужой item
    Given пользователь авторизован
    And item принадлежит другому пользователю
    When он делает PATCH /items/2
    Then сервер возвращает 403 Forbidden

  Scenario: Пароль не соответствует требованиям
    Given пользователь вводит пароль "123"
    When он регистрируется
    Then сервер возвращает 422 Validation Error

  Scenario: JWT токен истёк
    Given пользователь имеет устаревший JWT
    When он делает GET /items/1
    Then сервер возвращает 401 Unauthorized
