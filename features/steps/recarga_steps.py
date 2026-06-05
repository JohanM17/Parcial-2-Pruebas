"""
Steps de BDD - RecargaYa S.A.S.
Implementacion de los pasos Gherkin con behave
"""
from behave import given, when, then
from app.recarga import calcular_recarga


@given("un usuario no premium")
def step_usuario_no_premium(context):
    context.premium = False


@given("un usuario premium")
def step_usuario_premium(context):
    context.premium = True


@given("un usuario {tipo}")
def step_usuario_tipo(context, tipo):
    context.premium = (tipo.strip() == "premium")


@when("realiza una recarga de {monto:d} pesos")
def step_realizar_recarga(context, monto):
    context.resultado = calcular_recarga(monto, context.premium)


@then("la recarga es aceptada")
def step_recarga_aceptada(context):
    assert context.resultado["valido"] is True, (
        f"Se esperaba recarga aceptada pero fue: {context.resultado['mensaje']}"
    )


@then("la recarga es rechazada")
def step_recarga_rechazada(context):
    assert context.resultado["valido"] is False, (
        "Se esperaba recarga rechazada pero fue aceptada"
    )


@then("la bonificacion es del {porcentaje:d} porciento")
def step_bonificacion(context, porcentaje):
    actual = context.resultado["bonificacion_porcentaje"]
    assert actual == porcentaje, (
        f"Se esperaba bonificacion {porcentaje}% pero fue {actual}%"
    )
