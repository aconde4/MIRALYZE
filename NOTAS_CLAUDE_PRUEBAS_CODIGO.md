# Nota para Claude: pruebas de codigo incorporadas

Se han incorporado pruebas automaticas de codigo con `pytest` para complementar
las pruebas funcionales y de interfaz ya previstas en la memoria.

Archivos creados:

```text
tests/test_loader.py
tests/test_validator.py
tests/test_calculator.py
```

Dependencia anadida:

```text
pytest==8.3.4
```

## Alcance de las pruebas

Las pruebas no dependen de Streamlit ni de Supabase. Se centran en la logica
critica del sistema:

1. `etl/loader.py`

   - Comprueba que una exportacion SABI en formato wide se transforma a formato
     long empresa-anio.
   - Verifica el uso de `Last available year`, `Last avail. yr` y `Year - 1`.
   - Comprueba que `n.a.` se transforma en `None`.
   - Verifica que los CSV se rechazan como formato no soportado.

2. `etl/validator.py`

   - Comprueba que se aceptan negativos en campos donde son financieramente
     validos: `working_capital`, `net_income` y `cash_flow`.
   - Comprueba que se rechazan duplicados empresa-anio dentro del fichero.
   - Comprueba que se rechazan importes negativos en campos que no deben serlo,
     como `revenue`.

3. `metrics/calculator.py`

   - Comprueba deuda bruta, deuda neta, margenes, crecimiento interanual,
     productividad por empleado, cash conversion y equity ratio.
   - Comprueba la regla de deuda parcial:
     - si una deuda existe y la otra es nula, se usa la existente;
     - si ambas deudas son nulas, la deuda bruta queda nula;
     - si no hay caja, no se calcula deuda neta.

## Resultado de ejecucion

Comandos ejecutados:

```powershell
python -m compileall app.py database etl metrics utils views tests
python -m pytest tests -q
```

Resultado:

```text
6 passed in 7.54s
```

## Como reflejarlo en la memoria

En el Capitulo 6 o en el Anexo C se puede anadir una frase similar:

```text
Ademas de las pruebas funcionales con datos reales, se incorporaron pruebas
automaticas con pytest sobre los modulos criticos del pipeline: carga,
validacion y calculo de metricas. Estas pruebas verifican la conversion del
formato SABI wide-to-long, las reglas de validacion de filas y el calculo de
indicadores financieros como deuda neta, margenes, crecimiento y cash
conversion.
```

Tabla breve para Anexo C:

```text
ID  | Prueba de codigo                  | Resultado esperado                         | Resultado obtenido | Estado
TC01| Loader SABI wide-to-long          | Genera filas empresa-anio correctas        | Correcto           | OK
TC02| Rechazo de CSV                    | CSV no soportado                           | Correcto           | OK
TC03| Validator campos negativos        | Permite negativos financieros validos      | Correcto           | OK
TC04| Validator duplicados/negativos     | Rechaza duplicados y revenue negativo      | Correcto           | OK
TC05| Calculator metricas financieras    | Calcula deuda, margenes y productividad    | Correcto           | OK
TC06| Calculator regla deuda parcial     | Respeta reglas de deuda y caja nula        | Correcto           | OK
```
