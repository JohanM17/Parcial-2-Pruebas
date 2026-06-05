Feature: Calculo de recargas celulares - RecargaYa S.A.S.
  Como usuario del sistema de recargas
  Quiero calcular el valor final de mi recarga
  Para conocer mi bonificacion en datos

  Scenario: Recarga con monto minimo valido
    Given un usuario no premium
    When realiza una recarga de 1000 pesos
    Then la recarga es aceptada
    And la bonificacion es del 0 porciento

  Scenario: Recarga rechazada por monto menor al minimo
    Given un usuario no premium
    When realiza una recarga de 500 pesos
    Then la recarga es rechazada

  Scenario: Recarga rechazada por monto mayor al maximo
    Given un usuario no premium
    When realiza una recarga de 60000 pesos
    Then la recarga es rechazada

  Scenario: Recarga con bonificacion del 25 por ciento para monto alto
    Given un usuario no premium
    When realiza una recarga de 30000 pesos
    Then la recarga es aceptada
    And la bonificacion es del 25 porciento

  Scenario: Usuario premium recibe 5 por ciento adicional sobre bonificacion base
    Given un usuario premium
    When realiza una recarga de 10000 pesos
    Then la recarga es aceptada
    And la bonificacion es del 15 porciento

  Scenario: Usuario premium sin bonificacion base recibe solo 5 por ciento
    Given un usuario premium
    When realiza una recarga de 5000 pesos
    Then la recarga es aceptada
    And la bonificacion es del 5 porciento

  Scenario Outline: Particion de equivalencia para distintos montos y tipos de usuario
    Given un usuario <tipo>
    When realiza una recarga de <monto> pesos
    Then la recarga <resultado>
    And la bonificacion es del <bonificacion> porciento

    Examples:
      | tipo        | monto | resultado    | bonificacion |
      | no premium  | 999   | es rechazada |            0 |
      | no premium  | 1000  | es aceptada  |            0 |
      | no premium  | 9999  | es aceptada  |            0 |
      | no premium  | 10000 | es aceptada  |           10 |
      | no premium  | 29999 | es aceptada  |           10 |
      | no premium  | 30000 | es aceptada  |           25 |
      | no premium  | 50000 | es aceptada  |           25 |
      | no premium  | 50001 | es rechazada |            0 |
      | premium     | 10000 | es aceptada  |           15 |
      | premium     | 30000 | es aceptada  |           30 |
