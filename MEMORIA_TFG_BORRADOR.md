# MEMORIA TFG — MIRALYZE
## Herramienta de Deal Screener con Dashboard y Scoring para Search Funds
### Trabajo de Fin de Grado — Ingeniería Informática
### ETSI Informáticos — Universidad Politécnica de Madrid

**Autor:** Alejandro Conde Uceda  
**Tutor:** Alberto Tejero  
**Curso académico:** 2025-2026

---

# Nota para redaccion: pruebas y capturas que deben incorporarse

Esta seccion recoge decisiones acordadas antes del despliegue para que la
redaccion final de la memoria distinga correctamente entre capturas de
implementacion y evidencias de validacion.

## 1. Diferencia entre capturas del Capitulo 4 y capturas del Anexo C

En el **Capitulo 4 (Implementacion)** deben aparecer capturas del frontend con
funcion explicativa. Su objetivo es ensenar que se ha construido y como se
organiza la interfaz de usuario.

En el **Anexo C (Catalogo de pruebas de validacion)** deben aparecer capturas
con funcion probatoria. Su objetivo es demostrar que una prueba concreta se ha
ejecutado y que el resultado obtenido coincide con el esperado.

Por tanto, puede haber capturas visualmente parecidas, pero su uso narrativo es
distinto:

- Capitulo 4: explica la funcionalidad.
- Anexo C: evidencia que la funcionalidad funciona.

## 2. Capturas recomendadas para el Capitulo 4

Estas capturas deben insertarse en el cuerpo principal de la memoria, dentro de
la explicacion de la implementacion de la interfaz:

```text
Figura 4.1 Dashboard general de Miralyze
Figura 4.2 Vista de carga de datos
Figura 4.3 Listado de empresas
Figura 4.4 Ficha historica de empresa
Figura 4.5 Screener financiero
Figura 4.6 Analisis sectorial por CNAE
Figura 4.7 Mapa geografico de distribucion provincial
```

Ejemplo de redaccion para estas figuras:

```text
La Figura 4.X muestra la vista de Screener, desde la que el usuario puede
aplicar filtros financieros y sectoriales para reducir el universo de companias
candidatas y acceder directamente a la ficha individual de cada empresa.
```

## 3. Capturas recomendadas para el Anexo C

Estas capturas deben utilizarse como evidencia de pruebas concretas:

```text
Figura C.1 Resultado de importacion correcta
Figura C.2 Validacion de errores en fichero Excel
Figura C.3 Conteo de tablas en Supabase
Figura C.4 Aplicacion de filtros en Screener
Figura C.5 Navegacion desde Screener a ficha de empresa
Figura C.6 Mapa geografico filtrado por CNAE
Figura C.7 Aplicacion desplegada en Streamlit Community Cloud
```

La captura de despliegue se debe incorporar cuando la aplicacion ya este subida
a Streamlit Community Cloud.

## 4. Pruebas recomendadas antes del despliegue

Se acuerda realizar pruebas realistas y defendibles, evitando un catalogo
excesivamente artificial. El objetivo es validar que Miralyze arranca, conecta,
importa, persiste, calcula y visualiza correctamente.

Pruebas propuestas:

```text
P01 - Arranque local
Objetivo: comprobar que la aplicacion abre sin errores.
Entrada: streamlit run app.py.
Resultado esperado: dashboard cargado correctamente.

P02 - Conexion con Supabase
Objetivo: comprobar que la aplicacion no depende de SQLite local.
Entrada: consulta de conteo sobre tablas cloud.
Resultado esperado: la app lee empresas, financieros y metricas desde Supabase.

P03 - Persistencia de datos financieros
Objetivo: comprobar que existen registros empresa-anio.
Entrada: consulta sobre financials.
Resultado esperado: registros financieros persistidos en PostgreSQL.

P04 - Calculo de metricas
Objetivo: comprobar que existe una fila de metricas por empresa-anio.
Entrada: consulta sobre metrics.
Resultado esperado: metricas calculadas para los registros financieros.

P05 - Importacion de Excel SABI
Objetivo: comprobar que un Excel compatible se valida e importa.
Entrada: fichero Excel SABI.
Resultado esperado: empresas, financials y metricas actualizadas.

P06 - CSV deshabilitado
Objetivo: comprobar que ya no se permite subir CSV.
Entrada: intento de carga de CSV.
Resultado esperado: la interfaz solo acepta .xlsx/.xls.

P07 - Tratamiento de valores no disponibles
Objetivo: comprobar que valores como n.a. no se guardan como texto.
Entrada: Excel con valores n.a.
Resultado esperado: valores guardados como NULL.

P08 - Tratamiento de fechas antiguas
Objetivo: comprobar que fechas tipo 21/10/1870 no rompen PostgreSQL.
Entrada: Excel con fecha antigua de constitucion.
Resultado esperado: fecha parseada correctamente o tratada de forma segura.

P09 - Screener
Objetivo: comprobar filtros y ranking.
Entrada: filtros de revenue, deuda, CNAE u otros.
Resultado esperado: tabla de resultados coherente.

P10 - Navegacion desde Screener a ficha
Objetivo: comprobar que seleccionar una empresa abre su ficha.
Entrada: click sobre una fila del Screener.
Resultado esperado: navegacion a Ficha de empresa con la empresa seleccionada.

P11 - Ficha de empresa
Objetivo: comprobar visualizacion historica.
Entrada: seleccion de una empresa.
Resultado esperado: datos historicos, metricas y graficos visibles.

P12 - Analisis sectorial
Objetivo: comprobar comparacion CNAE vs mercado.
Entrada: seleccion de un CNAE.
Resultado esperado: KPIs y graficos sectoriales renderizados correctamente.

P13 - Mapa geografico
Objetivo: comprobar distribucion territorial.
Entrada: todos los sectores y un CNAE concreto.
Resultado esperado: mapa provincial y ranking regional correctos.

P14 - Despliegue en Streamlit Community Cloud
Objetivo: comprobar que la app funciona en entorno cloud.
Entrada: repositorio GitHub + secrets configurados.
Resultado esperado: app accesible desde URL de Streamlit.
Estado: pendiente hasta realizar despliegue.
```

## 5. Resultados reales ya comprobados

Antes del despliegue se realizo una comprobacion no destructiva contra Supabase.
Resultado:

```text
Empresas: 9.132
Registros financieros: 60.112
Metricas calculadas: 60.112
Anios cubiertos: 1995-2025
Provincias detectadas: 52
Importaciones registradas: 7
```

Estos datos deben usarse en el Capitulo 6 como evidencia cuantitativa del estado
final de la base de datos.

## 6. Tabla base para el Anexo C

```text
ID  | Prueba                           | Resultado esperado                         | Resultado obtenido                         | Estado
P01 | Arranque local                   | La app abre sin errores                    | Dashboard cargado correctamente            | OK
P02 | Conexion Supabase                | La app lee datos cloud                     | 9.132 empresas detectadas                  | OK
P03 | Persistencia financials          | Existen registros financieros              | 60.112 registros                           | OK
P04 | Metricas calculadas              | Una metrica por empresa-anio               | 60.112 metricas                            | OK
P05 | Importacion Excel                | El Excel SABI se valida e importa          | Pendiente de documentar con captura        | Pendiente
P06 | CSV deshabilitado                | CSV no permitido                           | Solo se aceptan .xlsx/.xls                 | OK
P07 | Valores n.a.                     | Se guardan como NULL                       | Pendiente de documentar con captura        | Pendiente
P08 | Fechas antiguas                  | No rompe PostgreSQL                        | Correccion implementada                    | OK
P09 | Screener                         | Filtra empresas y muestra ranking          | Pendiente de captura                       | Pendiente
P10 | Navegacion Screener -> ficha      | Click en empresa abre ficha                | Pendiente de captura                       | Pendiente
P11 | Ficha empresa                    | Muestra historico y metricas               | Pendiente de captura                       | Pendiente
P12 | Analisis sectorial               | Compara CNAE vs mercado                    | Graficos corregidos                        | OK
P13 | Mapa geografico                  | Muestra distribucion provincial            | 52 provincias detectadas                   | OK
P14 | Despliegue Streamlit Cloud       | App funciona en URL cloud                  | Pendiente de despliegue                    | Pendiente
```

## 7. Indicacion de redaccion

En el Capitulo 6 no se debe decir simplemente que "se hicieron pruebas". Debe
explicarse que la validacion se estructuro en tres niveles:

1. Validacion tecnica: arranque, dependencias, conexion y compilacion.
2. Validacion de datos: persistencia, importacion, limpieza y metricas.
3. Validacion funcional: navegacion, filtros, graficos, mapa y despliegue.

Esta estructura permite defender que el sistema no solo se implemento, sino que
se verifico sobre datos reales y con flujos representativos de uso.

> **Nota de redacción:**  
> Este archivo es el borrador de trabajo de la memoria del TFG. Se redacta en
> Markdown para maximizar la velocidad de escritura y la revisión iterativa. Una
> vez aprobado el contenido se formateará en LaTeX (plantilla ETSIINF-UPM) o Word.  
> - Las citas bibliográficas se marcan como `[N]`. Las referencias completas están
>   al final de este documento en la sección **Referencias**.  
> - Los marcadores `[FIGURA X — descripción]` indican dónde irá cada imagen o
>   diagrama en la versión final.  
> - Los marcadores `[TABLA X — descripción]` indican tablas que se exportarán
>   desde la aplicación o se construirán al formatear.  
> - Las secciones marcadas con `[TODO]` requieren revisión o completado posterior.

---

## Estado de redacción

*(Estructura según indicaciones del tutor — mayo 2026)*

| Capítulo | Estado |
|---|---|
| Cap 1. Introducción | ✅ Primer borrador completo |
| Cap 2. Estado del arte | ✅ Primer borrador completo |
| Cap 3. Objetivos | ✅ Primer borrador completo |
| Cap 4. Metodología | ✅ Primer borrador completo |
| Cap 5. Desarrollo | ✅ Primer borrador completo |
| Cap 6. Resultados | ✅ Primer borrador completo |
| Cap 7. Conclusiones | ✅ Completo |
| Bibliografía | 🔄 Referencias base definidas, revisar formato final |
| Anexos (A, B, C) | ✅ Completos |

---

---

# Capítulo 1. Introducción

## 1.1 Motivación y contexto

El modelo de *search fund* es un vehículo de inversión privada en el que uno o
dos emprendedores —denominados *searchers*— recaudan capital de un grupo reducido
de inversores institucionales o individuales para financiar una búsqueda
estructurada de una única empresa privada susceptible de ser adquirida y
gestionada directamente por ellos [1]. Introducido en la década de 1980 en la
Graduate School of Business de Stanford, el modelo ha experimentado un crecimiento
sostenido en las dos últimas décadas: según el estudio bienal de Stanford sobre
search funds, el número de fondos activos en el mundo se ha más que triplicado
entre 2010 y 2022, con una aceleración especialmente pronunciada en Europa e
Iberia [2].

El ciclo de vida de un search fund se articula en tres fases claramente
diferenciadas:

1. **Búsqueda (*sourcing*):** período de entre 18 y 24 meses en el que el
   *searcher* identifica y preselecciona empresas objetivo evaluando criterios de
   sector, tamaño, rentabilidad, crecimiento y perfil de endeudamiento.
2. **Adquisición:** proceso de *due diligence*, valoración financiera y cierre
   de la operación.
3. **Gestión:** operación directa de la empresa adquirida, con un horizonte
   típico de cuatro a ocho años.

La fase de búsqueda es la más intensiva en análisis de información. Un *searcher*
activo evalúa sistemáticamente entre 50 y 200 empresas a lo largo del proceso,
con revisiones periódicas a medida que aparecen nuevos candidatos o se actualiza
la información financiera disponible [1]. Esta intensidad analítica contrasta con
la escasez de herramientas diseñadas específicamente para el contexto de las
empresas privadas en el mercado ibérico.

## 1.2 El problema: análisis financiero de empresas privadas en España

A diferencia de las empresas cotizadas, cuya información financiera es pública y
está disponible en tiempo real a través de plataformas especializadas, las
empresas privadas españolas presentan sus cuentas únicamente en el Registro
Mercantil, con periodicidad anual y un formato que varía según el tamaño de la
empresa (cuentas abreviadas, normales o consolidadas).

La principal fuente de datos financieros para empresas privadas ibéricas es
**SABI** (*Sistema de Análisis de Balances Ibéricos*), una base de datos
comercial que agrega las cuentas anuales depositadas en el Registro Mercantil [3].
SABI es una herramienta de consulta y exportación: permite localizar empresas,
aplicar filtros básicos y descargar sus datos financieros en Excel. Sin embargo,
sus capacidades de análisis son limitadas: la interfaz no permite calcular
indicadores personalizados, construir rankings multivariable, visualizar
evoluciones históricas interactivas ni filtrar por criterios financieros
compuestos. En la práctica, los equipos de *search funds* usan SABI para extraer
los datos y resuelven el análisis en hojas de cálculo externas. Es decir, SABI
es el punto de partida, no la solución. Su descripción completa —formato, cobertura,
limitaciones y alternativas disponibles— se desarrolla en el Capítulo 2.

El flujo de trabajo habitual de un *search fund* ibérico combina exportaciones de
esta fuente con hojas de cálculo manuales para realizar cuatro tareas recurrentes:
limpiar y unificar los datos procedentes de distintas fuentes, calcular indicadores
financieros clave (*KPIs*) como márgenes, ratios de endeudamiento y tasas de
crecimiento compuesto, filtrar y ordenar las empresas según criterios de inversión
configurables, y compartir listas de candidatos con los inversores del fondo.

Este proceso presenta cuatro problemas estructurales que limitan su eficiencia y
reproducibilidad:

**Herramienta de análisis insuficiente.** SABI está diseñada para consultar y
exportar datos, no para analizarlos. No calcula KPIs financieros, no genera
rankings configurables, no muestra evoluciones históricas interactivas y no
permite comparar empresas entre sí con criterios compuestos. El análisis real
ocurre fuera de SABI, en hojas de cálculo, lo que traslada toda la complejidad
al analista.

**Heterogeneidad de datos.** Los datos proceden de fuentes con formatos distintos
e incompatibles entre sí. Unificarlos en cada ciclo de análisis consume tiempo
y es propenso a errores.

**Escalabilidad limitada.** Una hoja de cálculo con 100 empresas y 10 años de
historia supera el millar de filas de datos financieros. Cuando se añaden
múltiples indicadores calculados y filtros cruzados, el rendimiento y la
mantenibilidad se degradan rápidamente [4].

**Reproducibilidad insuficiente.** Cada nuevo ejercicio anual requiere actualizar
manualmente los cálculos. Si dos analistas aplican fórmulas ligeramente diferentes
—lo que ocurre habitualmente en equipos de búsqueda pequeños—, los resultados no
son comparables entre sí.

**Alternativas comerciales inaccesibles o inadecuadas.** Las plataformas de
análisis institucional (Bloomberg Terminal, S&P Capital IQ) están optimizadas
para empresas cotizadas y tienen un coste superior a 20.000 dólares por usuario
y año [5], inasumible para un fondo en fase de búsqueda. Las herramientas de BI
genéricas (Power BI, Tableau) carecen de lógica de dominio financiero integrada
y siguen requiriendo preparación manual de datos [6]. Una comparativa exhaustiva
de todas estas alternativas se desarrolla en el Capítulo 2.

## 1.3 Propuesta de solución: Miralyze

Este Trabajo de Fin de Grado presenta **Miralyze**, una plataforma web de
análisis financiero diseñada específicamente para el proceso de *sourcing* de
*search funds* ibéricos. El nombre es un portmanteau de *mirar* y *analyze* y
refleja el objetivo central de la herramienta: permitir visualizar y analizar
datos financieros de empresas privadas de forma rápida, sistemática y
reproducible, reduciendo el tiempo dedicado a tareas operativas de bajo valor
durante la fase de búsqueda.

Miralyze permite a un analista cargar exportaciones de SABI en formato Excel,
persistirlas en una base de datos relacional en la nube, calcular automáticamente
un conjunto de indicadores financieros y explorar el universo de empresas a través
de seis vistas interactivas:

- **Dashboard general:** métricas agregadas del universo de empresas cargadas,
  con distribuciones por sector y provincia.
- **Listado de empresas:** tabla filtrable con los indicadores principales de
  cada empresa y acceso directo a la ficha individual.
- **Ficha de empresa:** historial financiero completo con gráficos de evolución
  anual de ingresos, EBITDA, deuda y métricas derivadas.
- **Screener:** filtrado multivariable con umbrales cuantitativos configurables
  por el usuario, orientado a identificar empresas que cumplan criterios de
  inversión específicos.
- **Análisis sectorial:** comparativa de sectores económicos clasificados por
  CNAE-2009, con distribuciones de márgenes, ingresos y crecimiento.
- **Mapa geográfico:** distribución territorial de las empresas del universo
  y sus métricas financieras principales por provincia española.

La herramienta está construida íntegramente en Python, con Streamlit como
*framework* de interfaz web [7], Supabase/PostgreSQL como base de datos
persistente en la nube [8] y Plotly para las visualizaciones interactivas [9].
Se despliega en Streamlit Community Cloud como aplicación web accesible desde
cualquier dispositivo con navegador, sin requerir instalación local.

## 1.4 Objetivos del trabajo

El objetivo general de este TFG es diseñar e implementar una aplicación web que
permita a un equipo de *search fund* importar exportaciones de SABI, persistirlas
en la nube y analizarlas mediante cuadros de mando, filtros, fichas individuales,
análisis sectorial y visualización geográfica; reduciendo así el tiempo dedicado
al análisis manual durante la fase de *sourcing*. A partir del análisis del estado
del arte se han derivado siete objetivos específicos que articulan ese propósito
general, descritos con detalle en el Capítulo 3.

## 1.5 Contribuciones principales

Este trabajo realiza las siguientes contribuciones originales:

1. **Herramienta de *sourcing* específica para el mercado ibérico.** No existe,
   según el conocimiento del autor, ninguna herramienta de código abierto que
   integre la importación de exportaciones SABI, el cálculo automático de KPIs
   financieros y la visualización de empresas privadas ibéricas en un único flujo
   de trabajo.

2. **Pipeline ETL reproducible para datos SABI.** El módulo de importación
   desarrollado normaliza las diferencias de formato entre distintas versiones de
   SABI, convierte el formato *wide* al modelo relacional empresa-año y gestiona
   la actualización incremental de datos sin duplicar registros.

3. **Modelo de datos orientado al análisis de *deal flow*.** El esquema relacional
   diseñado —tablas `companies`, `financials`, `metrics` e `import_log`— permite
   consultas analíticas eficientes sobre universos de cientos de empresas con
   series históricas de hasta diez años.

4. **Validación con datos reales de escala industrial.** A diferencia de pruebas
   de concepto con datos sintéticos, Miralyze ha sido validado con exportaciones
   reales de SABI que contienen más de 1.000 empresas.

## 1.6 Estructura del documento

El resto de esta memoria se organiza en seis capítulos adicionales, una sección
de bibliografía y tres anexos técnicos.

El **Capítulo 2** analiza el estado actual del problema: las fuentes de datos
disponibles para empresas privadas ibéricas —con especial atención a SABI y sus
limitaciones como herramienta de análisis—, las soluciones existentes en el
mercado y el hueco que ninguna de ellas cubre.

El **Capítulo 3** define los objetivos del trabajo. A partir de las brechas
identificadas en el estado del arte, se formula el objetivo general y los siete
objetivos específicos que guían el desarrollo, junto con el alcance y las
limitaciones asumidas.

El **Capítulo 4** describe la metodología adoptada: el *stack* tecnológico
seleccionado y su justificación frente a alternativas, la arquitectura del
sistema, el modelo de datos, el enfoque de importación ETL y el modelo de
*scoring* financiero.

El **Capítulo 5** detalla el desarrollo: la implementación del *pipeline* de
importación SABI, el motor de cálculo de indicadores, las seis vistas de la
interfaz y el despliegue en Streamlit Community Cloud.

El **Capítulo 6** presenta los resultados obtenidos y las conclusiones del
trabajo: grado de cumplimiento de los objetivos, limitaciones identificadas y
líneas de trabajo futuro.

El **Capítulo 7** analiza el impacto del proyecto desde las perspectivas
económica, social y de sostenibilidad, incluyendo las implicaciones de la
dependencia de datos privados y los requisitos para una eventual comercialización.

Los **Anexos** recogen el esquema SQL de la base de datos (Anexo A), el mapeo
completo de columnas SABI al modelo relacional (Anexo B) y el catálogo de pruebas
de validación con sus resultados (Anexo C).

---

---

# Capítulo 2. Estado del arte

Este capítulo analiza el estado actual del problema que Miralyze aborda. En
primer lugar se describe el ecosistema de fuentes de datos para empresas privadas
en España, con especial atención a SABI como principal proveedor y a las
limitaciones que presenta como herramienta de análisis. A continuación se revisan
las soluciones existentes en el mercado —plataformas institucionales, herramientas
de BI y hojas de cálculo— y se identifican las brechas que ninguna de ellas cubre.
Las decisiones tecnológicas adoptadas para resolver esas brechas se desarrollan
en el Capítulo 4.

## 2.1 Fuentes de datos de empresas privadas en España

### 2.1.1 El Registro Mercantil como fuente primaria

El Registro Mercantil español es el repositorio oficial de cuentas anuales de
las sociedades mercantiles domiciliadas en España. Por ley, las sociedades de
capital (sociedades anónimas, de responsabilidad limitada y comanditarias por
acciones) están obligadas a depositar sus cuentas anuales en el plazo de un mes
desde su aprobación en junta, que debe producirse en los seis primeros meses de
cada ejercicio [19]. Esto convierte al Registro Mercantil en la única fuente
exhaustiva y legalmente obligatoria de información financiera de empresas privadas
en España.

Sin embargo, acceder a los datos del Registro Mercantil de forma estructurada y
masiva presenta dos dificultades relevantes. En primer lugar, la consulta
individual tiene coste por empresa y se realiza a través de un portal web con
interfaz manual. En segundo lugar, los depósitos en formato digital (XBRL desde
2018) requieren un procesamiento técnico específico para extraer los datos
financieros de forma automatizable [TODO-REF: referencia a normativa XBRL
registros mercantiles]. Estas barreras justifican la existencia de agregadores
comerciales como SABI.

### 2.1.2 SABI: la principal fuente agregada de datos financieros privados ibéricos

**SABI** (*Sistema de Análisis de Balances Ibéricos*) es una base de datos
comercial distribuida por Bureau van Dijk, empresa del grupo Moody's Analytics,
y comercializada en España también a través de Informa D&B [3]. SABI agrega las
cuentas anuales depositadas en los registros mercantiles de España y Portugal,
ofreciendo cobertura sobre más de tres millones de empresas ibéricas con series
históricas de hasta diez años.

La plataforma de SABI permite al usuario realizar búsquedas por criterios
financieros básicos —rango de ingresos, sector CNAE, provincia, forma jurídica,
número de empleados— y exportar los resultados en formato Excel. El fichero
exportado adopta un **formato *wide***: cada empresa ocupa una fila, y las
columnas representan las magnitudes financieras para cada ejercicio disponible
(por ejemplo, `Operating revenue (Turnover) 2023`, `Operating revenue (Turnover) 2022`,
etc.). Los valores monetarios se expresan en miles de euros.

Esta estructura de exportación es el punto de partida de Miralyze. El pipeline
ETL desarrollado lee estos ficheros Excel, detecta automáticamente las columnas
de cada magnitud para cada año, y los transforma al modelo relacional
empresa-año (*long format*) adecuado para el análisis.

### 2.1.3 Limitaciones de SABI como herramienta de análisis

Conviene distinguir entre las capacidades de SABI como **base de datos y
motor de exportación** y sus capacidades como **herramienta de análisis
financiero**. En el primer rol, SABI es sólida: su cobertura es amplia, su
actualización es periódica y la calidad de los datos del Registro Mercantil es
razonablemente fiable. En el segundo rol, sin embargo, presenta limitaciones
importantes que explican por qué los equipos de *search funds* no pueden apoyarse
en ella exclusivamente para el proceso de *sourcing*.

**Interfaz de análisis anticuada.** La plataforma web de SABI está orientada a
la consulta y la exportación, no al análisis interactivo. Los filtros disponibles
operan sobre los datos brutos del Registro Mercantil (ingresos declarados, número
de empleados) pero no sobre indicadores calculados como el margen EBITDA, la
deuda neta o el crecimiento compuesto anual.

**Ausencia de KPIs calculados.** SABI expone las magnitudes contables primarias
(ingresos, EBIT, resultado neto, activo total, fondos propios), pero no calcula
de forma nativa los indicadores derivados de mayor utilidad para la valoración de
empresas: margen EBITDA, ROE, ROA, CAGR de ingresos, ratio deuda neta/EBITDA o
cobertura de intereses. Estos cálculos deben realizarse manualmente por el
analista.

**Sin visualización histórica interactiva.** La plataforma no dispone de gráficos
de evolución temporal para una empresa concreta ni de comparativas sectoriales
visuales. El análisis de tendencias requiere exportar los datos y trabajar con
ellos externamente.

**Sin ranking multivariable configurable.** SABI no permite ordenar un universo
de empresas según una función de puntuación compuesta que combine múltiples KPIs
con pesos ajustables. Esta funcionalidad —central en el proceso de *sourcing*— no
existe en la herramienta.

**Dependencia de proveedor y consideraciones de licencia.** SABI es un servicio
de suscripción con coste significativo, accesible principalmente a través de
universidades e instituciones. Para el uso personal o comercial fuera del entorno
académico se requiere una licencia específica. Cualquier explotación comercial de
un producto basado en datos de SABI/Informa requeriría, previsiblemente, un
acuerdo comercial con el proveedor que autorice dicho uso [3].

En resumen: **SABI resuelve el problema del acceso a los datos, pero no el
problema del análisis**. Miralyze está diseñado para operar en ese espacio: toma
las exportaciones de SABI como entrada y proporciona todas las capacidades de
análisis que la plataforma no ofrece.

### 2.1.4 Otras fuentes de datos financieros de empresas privadas ibéricas

**Informa D&B.** Distribuida por Informa, empresa del grupo D&B (Dun & Bradstreet),
cubre las mismas fuentes primarias que SABI —Registro Mercantil español y
portugués— con una nomenclatura de columnas diferente y un portal de acceso
distinto. Su cobertura y calidad son comparables. Miralyze ha sido diseñado
principalmente para exportaciones SABI, aunque el módulo de importación podría
adaptarse a Informa D&B con ajustes en el mapeo de columnas.

**Axesor.** Proveedor español de información empresarial con origen en el
análisis de riesgo crediticio. Ofrece datos del Registro Mercantil con énfasis
en el perfil de riesgo y la solvencia. Su cobertura de series históricas es menor
que SABI para los fines de análisis de *deal flow*.

**Registro Mercantil Central.** Permite la descarga individual de cuentas en
formato XBRL o PDF a través de su portal. No es viable para análisis masivos sin
desarrollo técnico adicional y sin coste por consulta [19].

**Ficheros ad hoc de empresa.** En el contexto de un *search fund*, el propio
propietario o asesor de la empresa objetivo puede facilitar información financiera
directamente en Excel. Miralyze está diseñado para procesar exportaciones SABI,
pero este tipo de ficheros puede incorporarse manualmente una vez que se
estandariza su formato.

---

## 2.2 Herramientas de análisis financiero: panorama y brecha existente

### 2.2.1 Plataformas institucionales de datos financieros

Las plataformas institucionales de referencia —**Bloomberg Terminal**, **S&P
Capital IQ** y **Refinitiv Eikon** (ahora LSEG Workspace)— son los estándares
del sector financiero profesional para el análisis de inversiones [5]. Ofrecen
datos en tiempo real, series históricas largas, modelos de valoración integrados,
alertas y capacidades de *screening* avanzadas.

Sin embargo, presentan tres limitaciones determinantes para el caso de uso de
los *search funds* ibéricos:

1. **Cobertura de empresas privadas limitada.** Estas plataformas están
   optimizadas para empresas cotizadas en mercados regulados, donde la información
   es pública y fluye de forma estandarizada. La cobertura de empresas privadas
   españolas de tamaño mediano —que son el objetivo habitual de un *search fund*—
   es escasa o inexistente.

2. **Coste prohibitivo.** El acceso al Bloomberg Terminal supera los 27.000
   dólares por usuario y año [5]. S&P Capital IQ y Refinitiv tienen estructuras
   de precio similares. Estos importes son inasumibles para un equipo de búsqueda
   antes de completar la adquisición.

3. **Formato no adaptado al flujo de trabajo de *sourcing*.** Aunque permiten
   filtros avanzados y *screening*, no están diseñadas para integrar exportaciones
   de SABI ni para el proceso específico de identificación de empresas privadas
   ibéricas.

### 2.2.2 Herramientas de *Business Intelligence* genéricas

**Microsoft Power BI** y **Tableau** son las plataformas de BI más extendidas en
el ámbito corporativo [6]. Permiten construir cuadros de mando interactivos,
conectar con múltiples fuentes de datos y aplicar filtros visuales sobre los
resultados. En entornos con datos ya preparados, son herramientas muy potentes.

Su limitación principal para este caso de uso es que **no incorporan lógica de
dominio financiero**. Power BI o Tableau no calculan automáticamente el margen
EBITDA, la deuda neta o el CAGR: el analista debe preparar esos campos antes de
cargar los datos en la herramienta, lo que implica resolver el problema de la
transformación de datos de SABI externamente, generalmente en Excel o con código
adicional. En la práctica, el uso de BI genérico para este caso de uso desplaza
el problema en lugar de resolverlo.

Además, la integración con exportaciones de SABI no está contemplada de forma
nativa, y la configuración de un cuadro de mando financiero completo desde cero
requiere un esfuerzo de implementación significativo que va más allá del perfil
de un equipo de *search fund*.

### 2.2.3 Hojas de cálculo

Microsoft Excel y Google Sheets son las herramientas más utilizadas en la
práctica para el análisis de *deal flow* en *search funds* [4]. Su ventaja es la
ubicuidad y la flexibilidad: cualquier analista con conocimientos financieros
puede construir un modelo de evaluación de empresas con fórmulas estándar.

Las limitaciones son bien conocidas. Los estudios sobre errores en hojas de
cálculo estiman que entre el 88 y el 94 % de las hojas utilizadas en entornos
profesionales contienen al menos un error [4]. A esto se añaden problemas de
escalabilidad —el rendimiento se degrada a partir de pocas decenas de empresas
con series históricas—, de reproducibilidad —distintos analistas aplican fórmulas
ligeramente distintas— y de colaboración —la gestión de versiones en Excel es
propensa a inconsistencias.

### 2.2.4 Análisis de brechas (*gap analysis*)

La tabla siguiente sintetiza las capacidades de cada herramienta analizada frente
a los requisitos del proceso de *sourcing* de un *search fund* ibérico:

[TABLA 2.1 — Comparativa de herramientas de análisis financiero para empresas
privadas ibéricas]

| Capacidad | SABI | Bloomberg/CapIQ | Power BI | Excel | **Miralyze** |
|---|:---:|:---:|:---:|:---:|:---:|
| Datos de empresas privadas ibéricas | ✅ | ❌ | ❌ | Manual | ✅ |
| Importación automática desde exportación SABI | — | ❌ | ❌ | Manual | ✅ |
| Cálculo automático de KPIs financieros | ❌ | ✅ | ❌ | Manual | ✅ |
| *Screening* por KPIs compuestos configurables | ❌ | ✅ | Parcial | Manual | ✅ |
| Visualización histórica interactiva por empresa | ❌ | ✅ | ✅ | Parcial | ✅ |
| Análisis sectorial CNAE | ❌ | ❌ | ❌ | Manual | ✅ |
| Mapa geográfico por provincia | ❌ | ❌ | Parcial | ❌ | ✅ |
| Persistencia cloud entre sesiones | — | ✅ | ✅ | ❌ | ✅ |
| Coste accesible para un *search fund* | Alto | Muy alto | Medio | Bajo | Bajo |
| Despliegue web sin instalación local | — | ✅ | ✅ | ❌ | ✅ |

La tabla sugiere que, para el caso de uso definido, ninguna de las herramientas
analizadas cubre el flujo completo que requiere un *search fund* ibérico:
importar datos de SABI, calcular KPIs de forma automática, filtrar el universo
de empresas con criterios configurables y visualizar los resultados de forma
integrada. Miralyze está diseñado específicamente para cubrir esta brecha.

> **Nota de estructura:** Las tecnologías seleccionadas para cubrir este hueco
> (Streamlit, PostgreSQL/Supabase, Plotly, pandas) y la clasificación sectorial
> CNAE-2009 se describen en el **Capítulo 4 (Metodología)**, donde corresponde
> explicar *cómo* se va a resolver el problema identificado aquí.

---

---

# Capítulo 3. Objetivos

El análisis del estado del arte realizado en el capítulo anterior permite
delimitar con precisión el problema que este trabajo aborda. Las herramientas
existentes cubren partes del proceso de análisis de empresas privadas ibéricas,
pero ninguna integra en un único flujo la importación de exportaciones SABI, el
cálculo automático de indicadores financieros y la exploración interactiva de los
resultados. Esa brecha, documentada en la Tabla 2.1, define el espacio de diseño
de Miralyze y sirve de punto de partida para formular los objetivos de este
trabajo.

## 3.1 Objetivo general

Diseñar e implementar una plataforma web que automatice el flujo completo de
análisis financiero de empresas privadas ibéricas para equipos de *search funds*:
desde la importación de datos exportados de SABI hasta la exploración interactiva
del universo de empresas mediante indicadores calculados, filtros configurables y
visualizaciones geográficas y sectoriales, con persistencia de datos en la nube
y despliegue accesible desde cualquier dispositivo.

## 3.2 Objetivos específicos

Los siguientes cinco objetivos específicos articulan el camino hacia el objetivo
general. Cada uno corresponde a un bloque funcional independiente cuya realización
contribuye de forma directa al resultado final.

**OE1 — Adquisición e integración de datos.**
Conseguir que la plataforma sea capaz de leer exportaciones en formato Excel
generadas por SABI, interpretar correctamente su estructura heterogénea y
trasladar la información a un modelo de datos relacional persistente en la nube.
Este objetivo es el cimiento del sistema: sin una ingesta fiable y reproducible
de datos, el resto de funcionalidades carece de base.

**OE2 — Cálculo automático de indicadores financieros.**
Derivar de forma automática, a partir de los datos importados, el conjunto de
indicadores financieros necesarios para evaluar el atractivo de una empresa en
un proceso de *sourcing*: márgenes de rentabilidad, ratios de endeudamiento, tasas
de crecimiento histórico y métricas de estabilidad. El analista no debe calcular
ningún indicador manualmente; el sistema debe proporcionárselos ya calculados.

**OE3 — Interfaz web de análisis multidimensional.**
Ofrecer al usuario una interfaz con seis vistas complementarias que permitan
analizar el universo de empresas desde ángulos distintos: visión agregada del
portfolio, listado filtrable, historial individual de empresa, *screening*
configurable por criterios cuantitativos, comparativa sectorial y distribución
geográfica. Cada vista debe ser coherente con las demás y responder a los
patrones de uso real de un equipo de búsqueda.

**OE4 — Persistencia en la nube y despliegue accesible.**
Garantizar que los datos cargados en la plataforma persistan entre sesiones y
sean accesibles desde cualquier dispositivo con navegador, sin requerir
instalación local ni gestión de infraestructura por parte del usuario. Esto
implica tanto la elección de un proveedor de base de datos cloud adecuado como
el despliegue de la aplicación en una plataforma web de acceso público.

**OE5 — Validación con datos reales a escala.**
Verificar que el sistema funciona correctamente con exportaciones SABI reales de
escala significativa —universos de cientos o miles de empresas con series
históricas de varios años—, comprobando la integridad de la importación, la
corrección de los cálculos y el comportamiento de la interfaz bajo condiciones
reales de uso.

## 3.3 Alcance y limitaciones

### 3.3.1 Alcance del trabajo

El presente trabajo abarca el diseño, la implementación y la validación de una
primera versión funcional de Miralyze. Quedan dentro del alcance:

- La importación de ficheros Excel exportados por SABI con la estructura de
  columnas habitual en sus versiones recientes.
- El cálculo de indicadores financieros derivables de las magnitudes contables
  que SABI exporta del Registro Mercantil.
- Las seis vistas de análisis descritas en el objetivo OE3.
- La persistencia en Supabase/PostgreSQL y el despliegue en Streamlit Community
  Cloud.
- La validación con datos reales de exportaciones SABI proporcionadas en el
  contexto del trabajo.

### 3.3.2 Limitaciones asumidas

Las siguientes limitaciones son decisiones de diseño deliberadas, no carencias
técnicas. Quedan identificadas como posibles líneas de evolución futura:

**Fuente de datos única.** El sistema está diseñado para exportaciones SABI.
No contempla la integración con otras fuentes (Informa D&B, Axesor, ficheros
ad hoc de empresa) sin adaptación del módulo de importación.

**Sin actualización automática de datos.** Cada nuevo ejercicio fiscal requiere
una nueva exportación SABI y su carga manual en la plataforma. El sistema no
dispone de conexión directa a la API de SABI ni de mecanismos de actualización
automática.

**Sin sistema de autenticación de usuarios.** La primera versión asume un
entorno de uso privado y controlado por un único equipo. No se implementan
roles, permisos ni gestión de múltiples usuarios.

**Uso no comercial de los datos.** El sistema trabaja con exportaciones SABI
autorizadas para uso académico e interno. Cualquier explotación comercial del
producto que implique redistribuir o reutilizar datos de SABI/Informa requeriría
revisar las condiciones de licencia del proveedor y, previsiblemente, formalizar
un acuerdo comercial específico.

---

---

# Capítulo 4. Metodología

Este capítulo describe las decisiones metodológicas que hacen posible el sistema.
Se presentan en primer lugar el enfoque de desarrollo adoptado y el conjunto de
tecnologías seleccionadas, con justificación de cada elección frente a las
alternativas evaluadas. A continuación se describe la arquitectura del sistema,
el modelo de datos que la sustenta, el proceso de importación de datos desde SABI,
el motor de cálculo de indicadores financieros y la clasificación sectorial
utilizada.

## 4.1 Enfoque metodológico

El desarrollo de Miralyze siguió un enfoque iterativo organizado en dos fases
sucesivas, donde los resultados de cada fase condicionaron las decisiones de la
siguiente.

La primera fase se centró en validar el modelo de dominio con datos reales. Se
construyó una versión local de la aplicación con persistencia en SQLite, que
permitió comprobar que el esquema de datos elegido, las fórmulas de cálculo de
indicadores y el diseño de las vistas respondían a las necesidades reales del
proceso de *sourcing*. Trabajar primero en local redujo la fricción de iteración:
cualquier cambio en el modelo de datos o en la lógica de cálculo se podía probar
sin depender de conectividad ni de configuración de servicios externos.

La segunda fase abordó los requisitos de accesibilidad y persistencia cloud. Una
vez estabilizado el modelo de dominio, se migró la capa de datos de SQLite a
Supabase/PostgreSQL y se configuró el despliegue en Streamlit Community Cloud.
Esta secuencia evitó enfrentar simultáneamente la complejidad del dominio
financiero y la complejidad de la infraestructura cloud.

Durante ambas fases se emplearon asistentes de inteligencia artificial generativa
(Claude de Anthropic y Codex de OpenAI) como herramientas de apoyo al desarrollo,
especialmente para la generación y revisión de código, la resolución de problemas
técnicos y la elaboración de documentación. Su uso se integró de forma natural en el flujo de trabajo del proyecto, en línea
con las prácticas habituales del desarrollo de software actual.

La validación se realizó con datos reales a lo largo de todo el proceso, no como
etapa final. En cada iteración se cargaban exportaciones SABI con cientos o miles
de empresas para comprobar el comportamiento del sistema bajo condiciones reales
antes de continuar con el desarrollo.

## 4.2 Herramientas y tecnologías

La Tabla 4.1 recoge el conjunto de tecnologías seleccionadas para cada componente
del sistema.

[TABLA 4.1 — Stack tecnológico de Miralyze]

| Componente | Tecnología | Versión |
|---|---|---|
| Lenguaje de programación | Python | 3.11 |
| Framework de interfaz web | Streamlit | 1.41.1 |
| Base de datos | PostgreSQL vía Supabase | 3.2.3 (psycopg) |
| Visualización | Plotly | 5.24.1 |
| Manipulación de datos | pandas | 2.2.3 |
| Lectura de Excel | openpyxl | 3.1.5 |
| Clasificación sectorial | CNAE-2009 | INE, 2009 |

### 4.2.1 Python

Python 3.11 es el lenguaje sobre el que se construye toda la aplicación. La
elección no requiere justificación extensa: Python es el estándar de facto en el
desarrollo de aplicaciones de análisis de datos, con un ecosistema de librerías
maduro que cubre la totalidad de los requisitos del proyecto, desde la lectura de
Excel hasta el acceso a PostgreSQL [18]. Su compatibilidad directa con Streamlit,
Plotly y pandas eliminó la necesidad de capas de integración adicionales.

### 4.2.2 Streamlit frente a Dash y Flask

La elección del framework de interfaz web fue la decisión técnica con mayor
impacto en la velocidad de desarrollo. Se evaluaron tres alternativas.

Dash, desarrollado por Plotly Inc., construye aplicaciones analíticas web mediante
un sistema de callbacks explícitos que conectan cada componente de entrada con las
salidas que debe actualizar. El modelo es potente y ofrece control fino sobre el
comportamiento de la interfaz, pero resulta verboso: definir un único filtro
interactivo requiere declarar el componente, el callback y el decorador
correspondiente. En una aplicación con tantos filtros simultáneos como el
screener de Miralyze, gestionar el grafo de dependencias entre callbacks añade
una complejidad que no contribuye al valor funcional del producto.

Flask, combinado con un framework de frontend como React, representa la
arquitectura web clásica con backend y frontend separados. Es la opción con mayor
control sobre la experiencia de usuario y el rendimiento, pero exige desarrollo
en dos lenguajes distintos, gestión de una API REST entre ambas capas y un
tiempo de implementación considerablemente mayor.

Streamlit [7] adopta un modelo de programación diferente. Cualquier elemento de
la interfaz, ya sea un selector, un filtro, una tabla o un gráfico, se declara
en una única línea de código Python. Cuando el usuario modifica cualquier
componente, el script completo se re-ejecuta de arriba a abajo y todos los
elementos se actualizan automáticamente. No hay callbacks que declarar ni estado
que gestionar de forma explícita.

Esta simplicidad tiene un coste: el control sobre el diseño y el comportamiento
visual es menor que en Dash o React. Para compensarlo, Miralyze implementa una
capa de CSS personalizado centralizada en `utils/theme.py` que aplica la identidad
visual corporativa a todos los componentes nativos de Streamlit y a los gráficos
Plotly, logrando una apariencia coherente sin renunciar al modelo reactivo de
Streamlit.

La razón de fondo de la elección es pragmática: para un proyecto de esta escala,
orientado al prototipado rápido y a la validación con usuarios reales, la
velocidad de desarrollo que ofrece Streamlit supera a las ventajas de control que
ofrecen las alternativas.

### 4.2.3 Supabase/PostgreSQL frente a SQLite y otras alternativas

El sistema de persistencia evolucionó a lo largo del desarrollo. La primera
versión utilizó SQLite, que pertenece a la biblioteca estándar de Python y no
requiere ningún servidor. SQLite es adecuado para desarrollo local monousuario:
almacena todos los datos en un único fichero y soporta SQL estándar. Sin embargo,
tiene una limitación que lo hace inviable para el despliegue en la nube: en
plataformas como Streamlit Community Cloud, el sistema de ficheros es efímero.
Cada vez que la aplicación se reinicia, el fichero de base de datos desaparece y
con él todos los datos cargados. Esto hace imposible cualquier tipo de persistencia
entre sesiones.

La migración a PostgreSQL fue, por tanto, una consecuencia directa del requisito
de despliegue web, no una preferencia técnica. Entre las alternativas disponibles
se descartaron Firebase y MongoDB Atlas por su modelo documental NoSQL, que no
se adapta bien a datos financieros relacionales donde las consultas SQL de
agregación por empresa, año o sector son el patrón de acceso dominante. PlanetScale,
una base de datos MySQL serverless, era compatible con SQL pero no ofrecía las
ventajas específicas de PostgreSQL y su modelo de precios resultaba más complejo
para la escala del proyecto.

Supabase [8] proporciona una instancia PostgreSQL gestionada en la nube con plan
gratuito suficiente para los volúmenes de datos del proyecto. La conexión desde
Miralyze se realiza mediante `psycopg` [16], el adaptador PostgreSQL estándar
para Python, usando SQL directo sin ORM. Esta decisión preservó el mismo patrón
de consultas que existía con SQLite y evitó introducir una capa de abstracción
adicional que habría complicado la migración.

### 4.2.4 Plotly frente a Matplotlib, Altair y Bokeh

Miralyze necesita gráficos interactivos: el usuario debe poder hacer zoom sobre
una serie temporal, desactivar series concretas, ver los valores exactos al pasar
el cursor, y explorar un mapa geográfico con filtros dinámicos. Matplotlib, la
librería de visualización más extendida en Python, genera gráficos estáticos de
alta calidad para publicaciones, pero no es adecuada para este caso de uso.

Altair, basada en la gramática de Vega-Lite, produce gráficos declarativos e
interactivos con una sintaxis elegante. Su integración con Streamlit es funcional,
pero su soporte para mapas coropléticos y gráficos financieros específicos es más
limitado. Bokeh genera gráficos HTML interactivos con gran flexibilidad, pero su
API es más verbosa y su integración con Streamlit introduce algunas restricciones
en el renderizado.

Plotly [9] fue la elección por dos razones. Primera, su integración nativa con
Streamlit mediante `st.plotly_chart` es directa y sin fricciones. Segunda, cubre
todos los tipos de gráfico necesarios en Miralyze: líneas temporales, barras
agrupadas, diagramas de caja, mapas de burbujas, gráficos de dispersión y mapas
coropléticos provinciales mediante `choropleth_mapbox`. No se necesitó ninguna
librería adicional para ninguna de las visualizaciones.

### 4.2.5 pandas y openpyxl

pandas [10] es la librería central para la manipulación de datos a lo largo de
todo el pipeline: lectura del Excel de SABI, detección y parseo de columnas,
transformación de formato wide a long, preparación de los datos para las
visualizaciones y cálculo de estadísticas agregadas.

Para la lectura de ficheros Excel se utiliza openpyxl, que da soporte al formato
`.xlsx` que utilizan las exportaciones actuales de SABI. Se descartó `xlrd` porque
desde su versión 2.0 solo soporta el formato `.xls` anterior. Se valoró también
polars, una librería de manipulación de datos con un motor en Rust que ofrece
mejor rendimiento en datasets muy grandes. Para el volumen de trabajo de Miralyze,
universos de hasta varios miles de empresas, la diferencia de rendimiento no
justificaba el cambio de API ni la pérdida de compatibilidad con el resto del
ecosistema.

## 4.3 Arquitectura del sistema

Miralyze sigue una arquitectura en tres capas con flujo de datos unidireccional.
La capa de presentación no accede nunca directamente a la base de datos; lo hace
siempre a través de la capa de lógica. Esto separa las responsabilidades de cada
módulo y facilita modificar cualquiera de las tres capas sin afectar a las demás.

[FIGURA 4.1 — Diagrama de arquitectura en tres capas de Miralyze]

```
Capa de presentación
  app.py, views/ (home, upload, company_list, company_detail,
                  screener, sector, geo_map), utils/theme.py
         |
         v (llamadas a funciones de lógica)
Capa de lógica
  etl/ (loader, validator, transformer)
  metrics/calculator.py
  utils/ (helpers, geography)
         |
         v (consultas SQL)
Capa de datos
  database/db_manager.py → Supabase / PostgreSQL
```

**Capa de presentación.** El fichero `app.py` actúa como punto de entrada: configura
la página, aplica el CSS corporativo, carga el logo del sidebar y delega el
renderizado a la vista seleccionada. Cada una de las siete vistas vive en un
módulo independiente dentro del directorio `views/`. La identidad visual se
centraliza en `utils/theme.py`, que expone la paleta de colores corporativa y los
helpers de layout para los gráficos Plotly.

**Capa de lógica.** El directorio `etl/` contiene los tres módulos del pipeline de
importación. El módulo `metrics/calculator.py` implementa el cálculo de indicadores
financieros a partir de los datos almacenados. El directorio `utils/` agrupa
funciones auxiliares de formateo, consulta de catálogos y normalización geográfica.

**Capa de datos.** El módulo `database/db_manager.py` encapsula todas las
operaciones sobre PostgreSQL: inicialización del esquema, consultas de lectura y
escritura mediante `psycopg`. Ningún otro módulo del sistema ejecuta SQL
directamente; todas las operaciones pasan por este módulo.

## 4.4 Modelo de datos

### 4.4.1 De formato wide a modelo relacional

Las exportaciones de SABI tienen una estructura de datos conocida como formato
*wide*: cada empresa ocupa una única fila, y sus datos financieros para distintos
ejercicios se distribuyen en columnas con nombres que incluyen el año
(`Operating revenue (Turnover) 2023`, `Operating revenue (Turnover) 2022`, etc.).
Este formato es práctico para exportar y visualizar en Excel, pero no es adecuado
para el análisis en base de datos.

Miralyze transforma esa estructura al modelo relacional *long format*: una fila
por empresa y año. Esto permite escribir consultas SQL sobre series temporales,
calcular CAGR entre dos años cualesquiera, filtrar por año concreto o agregar por
sectores, todo con las mismas consultas independientemente de cuántos ejercicios
tenga disponibles cada empresa.

### 4.4.2 Cinco tablas y sus responsabilidades

El esquema de la base de datos está formado por cinco tablas. El DDL completo
se recoge en el Anexo A.

**`companies`** almacena los datos maestros de cada empresa: identificadores
(NIF/CIF y BvD ID de SABI), nombre, sector CNAE, provincia, país, fecha de
constitución, descripción de actividad y URL web. Una fila por empresa. Cuando se
reimportan datos de una empresa ya existente, esta fila se actualiza en lugar de
duplicarse.

**`financials`** contiene las cifras contables anuales por empresa: ingresos,
coste de ventas, EBITDA, resultado neto, flujo de caja, activo total, capital
circulante, fondos propios, deuda a largo plazo, deuda a corto plazo, caja y
equivalentes y número de empleados. Una fila por combinación empresa-año. Es la
tabla de mayor volumen del sistema; con el conjunto de datos validado durante el
desarrollo, supera los 60.000 registros.

**`metrics`** guarda los indicadores financieros derivados por empresa y año:
márgenes de rentabilidad, ratios de deuda, tasas de crecimiento, métricas de
productividad por empleado y ratios de solidez patrimonial. Se mantiene separada
de `financials` para no mezclar datos brutos con datos derivados. Si las fórmulas
de cálculo cambian, basta con recalcular `metrics` sin modificar `financials`. La
puntuación compuesta del screener no se persiste en esta tabla; se calcula de
forma dinámica en la vista de Screener en el momento de la consulta.

**`import_log`** registra cada importación ejecutada: fecha, modo de importación
(append o replace), número de empresas afectadas, número de registros financieros
insertados o actualizados, y número de errores detectados. Proporciona trazabilidad
completa del histórico de cargas.

**`import_errors`** recoge los errores detectados durante cada importación, con
referencia al nombre de la empresa afectada, el campo problemático y el mensaje de
error. Esta tabla alimenta la tabla de errores visible en la vista de carga de
datos.

### 4.4.3 Decisiones sobre campos financieros de SABI

SABI exporta las magnitudes contables con nombres en inglés que no siempre
corresponden de forma directa a las partidas contables más utilizadas en el
análisis financiero. Las decisiones de mapeo más relevantes son las siguientes.

**Deuda neta.** SABI no exporta la deuda neta como magnitud directa. Se calcula
internamente a partir de dos campos: la deuda bruta como suma de `Long-term debts`
y `Short-term debts`, y la deuda neta como deuda bruta menos `Cash and
equivalents`. Si alguno de los dos componentes de deuda es nulo para un año
concreto, se utiliza el componente disponible. Si la caja es nula, no se calcula
la deuda neta para ese año.

**Fondos propios.** Entre los campos de SABI relacionados con el patrimonio neto,
se optó por `Shareholders' equity` como representación de los fondos propios,
utilizada en el ratio de equity y en los indicadores de apalancamiento. Se
descartó `Total equity and liabilities`
porque representa el total del pasivo del balance, no los fondos propios aislados,
y `Equity-accounted companies` porque recoge participaciones valoradas por el
método de puesta en equivalencia.

**Resultado neto.** El campo `P/L for period` de SABI se interpreta como el
resultado neto del ejercicio y se almacena internamente como `net_income`.

**Flujo de caja.** Se incorporó el campo `Cash flow` como dato financiero adicional
porque enriquece el análisis de la conversión del resultado contable en caja real,
uno de los indicadores que los equipos de *search funds* consultan habitualmente
en las fichas individuales de empresa.

## 4.5 Pipeline de importación: del Excel de SABI a PostgreSQL

La importación de datos sigue un pipeline de cuatro etapas secuenciales. Cada
etapa está implementada en un módulo independiente, lo que permite probar y
modificar cada paso de forma aislada.

[FIGURA 4.2 — Diagrama del pipeline ETL de importación SABI]

```
Fichero Excel SABI (.xlsx)
        |
        v
   loader.py          Detecta columnas y años disponibles
        |
        v
   validator.py       Valida campos, limpia valores, gestiona fechas
        |
        v
   transformer.py     Wide to long, calcula deuda, normaliza provincias
        |
        v
   db_manager.py      Upsert en PostgreSQL (companies, financials, metrics)
```

**Etapa 1: carga (`loader.py`).** El módulo lee el fichero Excel con pandas y
detecta automáticamente qué columnas corresponden a qué magnitud financiera para
qué año. Las exportaciones de SABI utilizan sufijos relativos al año base: el
ejercicio más reciente se identifica con el sufijo `Last avail. yr`, y los
ejercicios anteriores con sufijos como `Year - 1`, `Year - 2`, hasta `Year - 6`.
El año base de referencia se lee del campo `Last available year`, que llega en
formato `YYYY-MM-DD`. El cargador aplica expresiones regulares sobre los nombres
de columna, extrae el nombre de la magnitud y el sufijo de año, y construye un
diccionario de mapeo que relaciona cada columna con su campo interno y su
ejercicio calendario.

**Etapa 2: validación (`validator.py`).** Sobre los datos cargados se aplican
tres tipos de comprobaciones. Primero, se verifica que existen los campos
obligatorios mínimos: `company_name`, `cif`, `cnae_code` y `year`. Las empresas
a las que les falta alguno de estos campos se registran en `import_errors` con la
descripción del problema y se omiten del resto del pipeline. Segundo, los valores
no numéricos habituales en las exportaciones de SABI, principalmente `n.a.`, se
convierten a `NULL` para evitar que se almacenen como texto en campos numéricos.
Tercero, las fechas de constitución se parsean explícitamente en Python antes de
enviarse a PostgreSQL, para evitar errores de interpretación de formato en
empresas con fechas de constitución muy antiguas.

**Etapa 3: transformación (`transformer.py`).** El módulo convierte cada empresa
del formato wide al conjunto de registros anuales correspondientes. Por cada
empresa y cada año para el que existen datos, genera un diccionario con los valores
de todos los campos financieros mapeados. En esta etapa se calculan también los
campos derivados: la deuda bruta, la deuda neta y la normalización del nombre de
provincia para el mapa geográfico. Esta última normalización resuelve las
discrepancias entre los nombres de provincia tal como los exporta SABI y los
identificadores que utiliza el fichero GeoJSON del mapa.

**Etapa 4: persistencia (upsert en PostgreSQL).** Los registros transformados se
insertan o actualizan en las tablas `companies` y `financials` usando operaciones
upsert. Para `companies`, la clave de unicidad es el identificador BvD; para
`financials`, la combinación de empresa y año. Esto garantiza que reimportar el
mismo fichero no genera duplicados. El modo de importación queda registrado en `import_log`. En modo *append*, los
registros del fichero se añaden o actualizan sin afectar al resto de los datos
existentes. En modo *replace*, el contenido del fichero se trata como el universo
de referencia de esa carga. Tras la inserción, el sistema recalcula los
indicadores financieros para las empresas afectadas.

## 4.6 Motor de cálculo de indicadores financieros

### 4.6.1 Indicadores calculados y persistidos

Una vez persistidos los datos financieros, el módulo `metrics/calculator.py`
deriva un conjunto de indicadores por cada combinación empresa-año y los almacena
en la tabla `metrics`. La Tabla 4.2 recoge los indicadores, agrupados por
categoría.

[TABLA 4.2 — Indicadores financieros calculados por Miralyze]

| Categoría | Indicador | Fórmula |
|---|---|---|
| Estructura de deuda | Deuda bruta | `long_term_debts + short_term_debts` |
| Estructura de deuda | Deuda neta | `gross_debt − cash_and_equivalents` |
| Estructura de deuda | Ratio ND/EBITDA | `net_debt / ebitda` |
| Márgenes | Margen EBITDA | `ebitda / revenue` |
| Márgenes | Margen neto | `net_income / revenue` |
| Márgenes | Margen cash flow | `cash_flow / revenue` |
| Crecimiento | Crecimiento de ingresos interanual | `(revenue_t / revenue_{t-1}) − 1` |
| Crecimiento | Crecimiento de EBITDA interanual | `(ebitda_t / ebitda_{t-1}) − 1` |
| Crecimiento | CAGR ingresos 3 años | `(revenue_t / revenue_{t-3})^(1/3) − 1` |
| Crecimiento | CAGR ingresos 5 años | `(revenue_t / revenue_{t-5})^(1/5) − 1` |
| Productividad | Ingresos por empleado | `revenue / employees` |
| Productividad | EBITDA por empleado | `ebitda / employees` |
| Productividad | Cash flow por empleado | `cash_flow / employees` |
| Calidad | Cash conversion | `cash_flow / ebitda` |
| Solidez | Ratio de equity | `equity / total_assets` |

El cálculo gestiona explícitamente los casos en los que el denominador es nulo,
cero o desconocido. Si una empresa no tiene ingresos para un ejercicio, los
márgenes de ese año quedan como nulo en lugar de propagar un error de división.
Para los ratios de crecimiento, si no existen datos del año de referencia, el
indicador queda como nulo y el sistema continúa con el resto de ejercicios.

### 4.6.2 Modelo de puntuación compuesta: WSM

La vista de Screener calcula de forma dinámica una puntuación compuesta que
permite ordenar el universo de empresas. Esta puntuación no se persiste en la
tabla `metrics`; se recalcula en cada consulta sobre los indicadores disponibles
en ese momento. El método utilizado es el *Weighted Sum Model* (WSM), ampliamente
empleado en screening financiero por su interpretabilidad [11].

La fórmula es la siguiente:

```
Puntuación = Σ (w_i × score_i) × 100
```

donde `w_i` es el peso asignado a cada indicador, con la restricción de que la
suma de todos los pesos sea igual a 1, y `score_i` es el valor normalizado del
indicador en el intervalo [0, 1].

En la versión actual del screener, la puntuación se construye sobre cuatro
indicadores con pesos ajustables por el usuario:

[TABLA 4.3 — Indicadores del modelo WSM en el Screener]

| Indicador | Campo de `metrics` | Peso por defecto |
|---|---|---|
| Margen EBITDA | `ebitda_margin` | Configurable |
| Crecimiento de ingresos interanual | `revenue_growth_yoy` | Configurable |
| Ratio de equity | `equity_ratio` | Configurable |
| EBITDA por empleado | `ebitda_per_employee` | Configurable |

El usuario puede ajustar los pesos desde la interfaz del screener antes de
ejecutar una búsqueda. La restricción de que la suma de pesos sea igual a 1 se
aplica automáticamente, sin necesidad de intervención manual.

### 4.6.3 Normalización min-max

Para que los indicadores, que tienen escalas y unidades distintas, sean
comparables en el modelo WSM, cada uno se normaliza al intervalo [0, 1] mediante
min-max sobre el universo de empresas con datos disponibles para ese indicador:

```
score = (x - x_min) / (x_max - x_min)
```

Para los indicadores donde un valor mayor representa una situación peor, como el
ratio deuda neta sobre EBITDA, la fórmula se invierte:

```
score = 1 - (x - x_min) / (x_max - x_min)
```

Antes de normalizar, los valores extremos superiores al percentil 99 se recortan
al valor de ese percentil. Esto evita que un único valor atípico muy elevado
comprima al resto del universo hacia la zona baja de la escala, distorsionando
el ranking. La normalización es relativa al universo cargado en cada momento,
no a benchmarks sectoriales externos. Una puntuación de 80 significa que la
empresa se sitúa en el percentil 80 del universo actualmente analizado.

## 4.7 Clasificación sectorial: CNAE-2009

La **Clasificación Nacional de Actividades Económicas 2009** (CNAE-2009) es el
sistema oficial de referencia para la clasificación sectorial de empresas en
España, equivalente a la clasificación europea NACE Rev. 2 [12]. Todas las
empresas inscritas en el Registro Mercantil están clasificadas con este código,
que SABI exporta en el campo `CAE Rev.3 Primary Code`.

CNAE-2009 organiza las actividades económicas en cuatro niveles jerárquicos:
sección (una letra, de la A a la U, 21 secciones en total), división (dos dígitos,
88 divisiones), grupo (tres dígitos, 272 grupos) y clase (cuatro dígitos, 615
clases). Miralyze almacena el código de cuatro dígitos en la tabla `companies`
y lo usa en tres contextos distintos del sistema.

En la vista de análisis sectorial, las empresas se agrupan por división de dos
dígitos para calcular y comparar los indicadores financieros entre sectores
mediante distribuciones estadísticas. En el screener, el usuario puede restringir
el universo de búsqueda a uno o varios códigos CNAE concretos. En el mapa
geográfico, el filtro por CNAE combina la dimensión sectorial con la territorial,
permitiendo visualizar cómo se distribuye un sector concreto por provincias.

Se descartaron otros sistemas de clasificación, como el SIC norteamericano, porque
no corresponden a los códigos que proporciona SABI ni a los que figuran en el
Registro Mercantil español. Usar CNAE-2009 garantiza coherencia directa entre
los datos de origen y la clasificación utilizada en el análisis, sin necesidad de
tablas de conversión.

---

---

# Capítulo 5. Desarrollo

Este capítulo describe el sistema construido. Se presenta la organización del
repositorio, la implementación de la capa de acceso a datos, el pipeline de
importación con sus decisiones técnicas y el módulo de cálculo de métricas. La
interfaz de usuario y el despliegue se tratan en las secciones 5.5 y 5.6.

## 5.1 Estructura del repositorio

El código fuente de Miralyze se organiza en módulos por responsabilidad. La
raíz del repositorio contiene el punto de entrada de la aplicación y los ficheros
de configuración; cada subdirectorio agrupa los módulos de una capa o un dominio
funcional concreto.

```
tfg_screener/
├── app.py                       Punto de entrada de Streamlit
├── requirements.txt             Dependencias del proyecto
├── DOCUMENTACION.md             Bitácora técnica de desarrollo
├── assets/
│   ├── logo_miralyze_sidebar.png
│   └── geo/
│       └── iberia_regions.geojson
├── database/
│   ├── db_manager.py            Acceso a PostgreSQL/Supabase
│   └── schema.sql               DDL de creación de tablas
├── etl/
│   ├── loader.py                Lectura de Excel SABI
│   ├── validator.py             Validación de datos
│   └── transformer.py           Wide-to-long y upsert
├── metrics/
│   └── calculator.py            Cálculo de indicadores financieros
├── utils/
│   ├── theme.py                 Identidad visual y CSS
│   ├── helpers.py               Funciones de formateo y catálogos
│   └── geography.py             Normalización geográfica y carga de GeoJSON
└── views/
    ├── home.py                  Dashboard
    ├── upload.py                Carga de datos
    ├── company_list.py          Listado de empresas
    ├── company_detail.py        Ficha de empresa
    ├── screener.py              Screener financiero
    ├── sector.py                Análisis sectorial
    └── geo_map.py               Mapa geográfico
```

> **Nota para el formateado final:** el árbol usa caracteres Unicode (├──, │, └──)
> que pueden requerir una fuente monoespaciada compatible (p. ej. Consolas, JetBrains
> Mono). En LaTeX se recomienda envolverlo en un entorno `verbatim` o `lstlisting`
> con `inputencoding=utf8`.

Las dependencias del proyecto, declaradas en `requirements.txt`, son las que ya
se han justificado en el Capítulo 4: Streamlit 1.41.1, pandas 2.2.3, Plotly
5.24.1, openpyxl 3.1.5, psycopg 3.2.3 con binarios precompilados y Pillow para
la carga del logo.

## 5.2 Capa de acceso a la base de datos

Toda la interacción con PostgreSQL se concentra en `database/db_manager.py`. El
resto de módulos del sistema invoca a este módulo y nunca ejecuta SQL por su
cuenta, lo que facilita aislar los cambios cuando se modifica el esquema o se
ajusta el comportamiento de la conexión.

El módulo expone seis funciones principales. `get_connection()` abre una conexión
a Supabase a partir de la URL configurada en los secretos, devolviéndola con un
cursor que entrega los resultados como diccionarios mediante `dict_row` de
psycopg. `execute_query()` ejecuta consultas SELECT y devuelve la lista de filas.
`execute_insert()`, `execute_update()` y `execute_many()` realizan las
operaciones de escritura, esta última optimizada para insertar lotes de
registros como los que produce el pipeline de importación. Por compatibilidad
con la versión SQLite anterior se mantiene `init_db()`, aunque su comportamiento
ha cambiado: ya no crea tablas, porque el esquema se aplica una sola vez sobre
Supabase ejecutando el DDL completo del fichero `database/schema.sql` desde el
SQL Editor del proveedor.

La migración desde SQLite obligó a tres ajustes técnicos en la capa de acceso.
Primero, los placeholders de las consultas pasaron del símbolo `?` que utiliza
SQLite al `%s` que requiere psycopg. Segundo, las filas devueltas ya no son
tuplas indexadas por posición sino diccionarios indexados por nombre de columna,
lo que mejoró la legibilidad del resto del código pero exigió revisar todas las
consultas existentes. Tercero, los valores numéricos que PostgreSQL devuelve con
tipo `Decimal` se convierten a `float` en la propia función de lectura, ya que
los `Decimal` no son directamente compatibles con las operaciones aritméticas de
pandas ni con los gráficos de Plotly.

La cadena de conexión a la base de datos no se almacena en el código fuente. El
módulo busca la URL en tres ubicaciones por orden de prioridad: el objeto
`st.secrets` cuando la aplicación se ejecuta en Streamlit Community Cloud, la
variable de entorno `SUPABASE_DB_URL` cuando se ejecuta en local, y el fichero
`.streamlit/secrets.toml` en desarrollo. Este último fichero está incluido en
`.gitignore` y nunca se sube al repositorio.

## 5.3 Implementación del pipeline de importación

El pipeline ETL descrito en el Capítulo 4 se materializa en tres módulos del
directorio `etl/` más la capa de persistencia ya descrita. Esta sección entra en
los detalles de implementación de cada módulo: los nombres reales de los campos
de SABI, las reglas concretas de validación y las decisiones técnicas adoptadas
ante los problemas encontrados durante el desarrollo.

### 5.3.1 Carga del Excel y detección de columnas (`loader.py`)

Las exportaciones de SABI organizan los datos financieros con un patrón
específico de nombres de columna. El año más reciente disponible para una empresa
se lee del campo `Last available year`, que llega en formato `YYYY-MM-DD`. Los
datos de ese año se identifican con el sufijo `Last avail. yr` en cada columna
financiera. Los ejercicios anteriores se nombran de forma relativa al año base,
desde `Year - 1` hasta `Year - 6`, lo que da hasta siete ejercicios disponibles
por empresa.

El cargador recorre las columnas del fichero, aplica expresiones regulares para
extraer el nombre de la magnitud y el sufijo de año, y construye un diccionario
que mapea cada columna del Excel al campo de la base de datos y al ejercicio
calendario correspondiente. Por ejemplo, si una empresa tiene `Last available year`
igual a `2024-12-31`, su columna `Operating revenue (Turnover) Year - 2` se
mapea al campo `revenue` del año 2022.

Los doce campos numéricos parametrizados por año que el cargador busca en cada
fichero son `Cash & cash equivalent`, `Total assets`, `Working capital`,
`Number of employees`, `Operating revenue (Turnover)`, `Cost of goods sold`,
`EBITDA`, `Long term debts`, `Short term debts`, `Shareholders' equity`,
`P/L for period` y `Cash flow`. Los once campos descriptivos de empresa
(nombre, CIF, BvD ID, fecha de constitución, web, país, provincia, GUO, código
CNAE y las dos descripciones de actividad) se leen de columnas independientes
que no están parametrizadas por año.

Durante el desarrollo se evaluó admitir también ficheros CSV. La opción se
descartó por dos motivos. Las descripciones de actividad económica que SABI
incluye (campos `Native trade description` y `English trade description`) suelen
contener comas, lo que exige un escapado correcto del delimitador. Además, la
configuración regional de Excel altera el separador por defecto entre la coma y
el punto y coma según el sistema del usuario. La combinación de ambos factores
elevaba el riesgo de errores silenciosos durante la importación. La vista de
carga acepta únicamente extensiones `.xlsx` y `.xls`.

### 5.3.2 Validación (`validator.py`)

Sobre los registros extraídos por el cargador se aplican dos bloques de
validación previos a la transformación. El primero verifica que cada empresa
dispone de los campos mínimos requeridos: `company_name`, `cif`, `cnae_code` y
`year`. Las empresas a las que les falta alguno de estos campos se registran en
`import_errors` con la descripción del problema y se omiten del resto del
pipeline. El segundo bloque convierte los valores no numéricos habituales en
SABI, principalmente la cadena `n.a.`, al valor nulo de PostgreSQL para evitar
que se almacenen como texto en columnas de tipo numérico.

El validador permite explícitamente valores negativos en los campos
`net_income`, `cash_flow` y `working_capital`, donde un signo negativo es una
señal financiera legítima (pérdidas, salidas netas de caja, capital circulante
negativo). Tampoco se rechaza una empresa por tener una de las dos partidas de
deuda nula: muchas empresas pequeñas no tienen deuda a largo plazo o no tienen
deuda a corto plazo, y eso no es un error de datos.

A los dos bloques anteriores se añade una etapa específica de parseo de fechas
que se ejecuta antes de cada inserción. El motivo aparece con empresas del
Registro Mercantil que tienen fechas de constitución muy antiguas, como
`21/10/1870`. PostgreSQL podía rechazar estos valores con el mensaje
`date/time field value out of range` cuando interpretaba el formato con un
`datestyle` distinto al esperado. La solución consistió en parsear las fechas
explícitamente como día/mes/año en Python antes del envío a la base de datos,
de modo que PostgreSQL recibe siempre un valor de tipo `date` ya convertido y
no una cadena ambigua.

### 5.3.3 Transformación wide-to-long y upsert (`transformer.py`)

El transformador genera, para cada empresa y para cada año con datos disponibles,
un registro independiente que se inserta o actualiza en la tabla `financials`.
La conversión del formato wide al modelo relacional ya descrita en el Capítulo 4
se materializa aquí mediante la iteración sobre el diccionario de mapeo
producido por el cargador.

La identificación de empresa para el upsert sigue una cadena de prioridad
diseñada para evitar duplicados entre cargas sucesivas. El sistema busca
primero por `bvd_id`, el identificador único de Bureau van Dijk, porque es el
más fiable y persistente entre exportaciones. Si la empresa no tiene `bvd_id`,
se usa el `cif`. En último recurso, se compara por nombre normalizado. Esta
cadena complementa al chequeo del validador: aunque la regla de campos mínimos
exige `cif`, el upsert puede resolver la identidad por `bvd_id` cuando ambos
campos están presentes, que es el caso habitual en las exportaciones de SABI.

A nivel de base de datos, las restricciones de unicidad refuerzan la integridad.
La tabla `companies` impone unicidad sobre `bvd_id`. La tabla `financials`
impone unicidad sobre la combinación `(company_id, year)`, lo que garantiza que
nunca exista más de un registro anual por empresa, independientemente del número
de cargas que se realicen.

El modo de importación queda registrado en `import_log`. En modo *append*, los
registros del fichero se añaden o actualizan sin afectar al resto de los datos
existentes en la base de datos. En modo *replace*, el contenido del fichero se
trata como el universo de referencia de esa carga; el modo queda anotado para
trazabilidad y permite distinguir el tipo de operación realizada. Tras finalizar
la inserción, el transformador invoca al módulo de cálculo de métricas para que
recalcule los indicadores de las empresas afectadas.

## 5.4 Cálculo de indicadores financieros

El módulo `metrics/calculator.py` calcula los indicadores derivados a partir de
los datos almacenados en `financials` y los persiste en la tabla `metrics`. Su
ejecución se dispara automáticamente al final de cada importación exitosa, sobre
las empresas que el pipeline acaba de procesar. Esto mantiene la coherencia
entre las dos tablas sin necesidad de invocaciones manuales.

El módulo calcula quince indicadores financieros derivados que alimentan las
vistas de ficha, screener y análisis sectorial. La tabla 5.1 los recoge agrupados
por categoría. La puntuación compuesta del screener no forma parte de esta tabla;
se calcula dinámicamente en la vista de Screener, tal como se describe en 4.6.2.

[TABLA 5.1 — Indicadores financieros calculados y persistidos en `metrics`]

| Categoría | Indicador | Fórmula |
|---|---|---|
| Estructura de deuda | Deuda bruta | `long_term_debts + short_term_debts` |
| Estructura de deuda | Deuda neta | `gross_debt - cash_and_equivalents` |
| Estructura de deuda | Ratio ND/EBITDA | `net_debt / ebitda` |
| Márgenes | Margen EBITDA | `ebitda / revenue` |
| Márgenes | Margen neto | `net_income / revenue` |
| Márgenes | Margen cash flow | `cash_flow / revenue` |
| Crecimiento | Crecimiento de ingresos interanual | `(revenue_t / revenue_{t-1}) - 1` |
| Crecimiento | Crecimiento de EBITDA interanual | `(ebitda_t / ebitda_{t-1}) - 1` |
| Crecimiento | CAGR ingresos 3 años | `(revenue_t / revenue_{t-3})^(1/3) - 1` |
| Crecimiento | CAGR ingresos 5 años | `(revenue_t / revenue_{t-5})^(1/5) - 1` |
| Productividad | Ingresos por empleado | `revenue / employees` |
| Productividad | EBITDA por empleado | `ebitda / employees` |
| Productividad | Cash flow por empleado | `cash_flow / employees` |
| Calidad | Cash conversion | `cash_flow / ebitda` |
| Solidez | Ratio de equity | `equity / total_assets` |

El cálculo gestiona explícitamente los casos en los que el denominador es nulo,
cero o desconocido. Si una empresa no tiene ingresos para un ejercicio concreto,
los márgenes de ese año se almacenan como nulo en lugar de propagar un error de
división. Para los ratios de crecimiento, si no existen datos del año de
referencia, el indicador queda como nulo y el sistema continúa con el resto de
ejercicios sin interrumpirse.

El cambio de motor de base de datos de SQLite a PostgreSQL provocó un problema
de tipos durante el cálculo. Los valores numéricos almacenados en columnas
`numeric` de PostgreSQL llegan a Python como objetos `Decimal`, mientras que
SQLite los devolvía directamente como `float`. Las operaciones aritméticas de
pandas y los gráficos de Plotly no aceptan `Decimal` de forma directa: las
funciones de agregación lanzaban excepciones y los gráficos no renderizaban las
series. La corrección se aplicó en la capa de lectura, que convierte los valores
numéricos a `float` antes de devolverlos a las capas superiores. Esto preservó
la lógica original del calculador sin propagar el cambio de tipo a otros
módulos.

## 5.5 Interfaz de usuario

La interfaz de Miralyze se reparte en siete vistas independientes accesibles
desde el menú lateral. Cada vista vive en un módulo del directorio `views/` y
se renderiza desde `app.py` cuando el usuario la selecciona en el sidebar. Esta
sección describe el diseño visual común a todas las vistas y la implementación
concreta de cada una.

### 5.5.1 Diseño visual y navegación

El diseño visual de Miralyze parte de tres decisiones que condicionan toda la
interfaz. La primera es el modo oscuro como elección por defecto, adoptada
porque reduce la fatiga visual durante las sesiones largas de análisis y
contrasta mejor con los datos numéricos de los gráficos financieros. La segunda
es el uso de una paleta corporativa propia, registrada en el documento de
identidad visual del proyecto. La tercera es la centralización de toda la lógica
de estilos en un único módulo, `utils/theme.py`, que aplica los colores y la
tipografía tanto a los componentes nativos de Streamlit como a los gráficos
generados con Plotly. La tabla 5.2 recoge la paleta y su uso.

[TABLA 5.2 — Paleta corporativa de Miralyze]

| Elemento | Color | Código hexadecimal |
|---|---|---|
| Fondo principal | Midnight | `#0E1825` |
| Fondo de tarjetas | Navy | `#182639` |
| Color principal | Gold | `#C8A96E` |
| Color secundario | Sapphire | `#1D6FA4` |
| Texto principal | Ivory | `#F5EFE0` |
| Texto secundario | Frost | `#C8D3E0` |
| Acento positivo | Emerald | `#2ECC71` |
| Acento negativo | Crimson | `#E74C3C` |

El sidebar es el elemento de navegación principal. Contiene el logo de Miralyze,
el menú vertical con las siete vistas y un pie de página con la referencia al
TFG. El logo se carga desde `assets/logo_miralyze_sidebar.png`, una versión ya
recortada del fichero original del design sheet. La razón del recorte previo es
que la versión original requería un procesamiento dinámico con Pillow en cada
arranque de la aplicación, lo que provocaba ocasionalmente que la imagen no se
renderizara correctamente en el sidebar. Cargar directamente la versión
preprocesada eliminó la dependencia del procesamiento en tiempo de ejecución.

### 5.5.2 Dashboard

El dashboard es la vista por defecto al abrir la aplicación. Su objetivo es dar
una visión inmediata del estado del universo de empresas cargadas en el sistema.

La parte superior muestra cuatro tarjetas de métricas con el total de empresas,
el número de registros financieros, el número de importaciones realizadas y el
número de países representados. Cada tarjeta consulta una agregación distinta
sobre las tablas `companies`, `financials` e `import_log`.

A continuación aparece un ranking visual del Top 10 de sectores CNAE por número
de empresas. La primera versión del ranking se construyó con un componente
nativo de Streamlit, pero el primer elemento se renderizaba como código HTML
visible en lugar de como barra proporcional. La solución fue cambiar el
renderizado a `streamlit.components.v1.html`, que interpreta correctamente el
marcado. Tras este cambio surgió un segundo problema: el componente solo
mostraba parte de las diez filas porque la altura por defecto era insuficiente.
Se ajustó la altura del componente y se compactó el espaciado interno entre
filas para que las diez entradas resultaran visibles sin scroll.

La parte inferior del dashboard recoge las últimas importaciones registradas en
`import_log`, con su fecha, modo y volumen de registros afectados.

[FIGURA 5.1 — Dashboard general de Miralyze]

### 5.5.3 Carga de datos

La vista de carga gestiona el flujo completo de importación SABI desde la
interfaz. El usuario sube un fichero Excel mediante el componente
`st.file_uploader`, configurado para aceptar exclusivamente las extensiones
`.xlsx` y `.xls` por las razones descritas en el apartado 5.3.1.

Antes del envío, el usuario selecciona el modo de importación entre las dos
opciones definidas en el transformador: *append* para añadir o actualizar sin
afectar al resto del universo, o *replace* para reconstruir el universo desde
el fichero. La operación se inicia con un botón explícito para evitar
importaciones accidentales al cambiar el modo seleccionado.

Durante la ejecución, una barra de progreso informa al usuario del estado del
proceso. La barra distingue dos fases consecutivas: la fase de importación de
datos, que abarca la lectura del Excel, la validación, la transformación y el
upsert en `companies` y `financials`, y la fase de recálculo de métricas, que
recorre las empresas afectadas y reconstruye los registros de `metrics`. Esta
distinción resultó útil durante el desarrollo porque la segunda fase tarda más
de lo que el usuario podría esperar: ver la barra avanzar en la fase correcta
elimina la sensación de bloqueo.

Al finalizar la importación, la vista presenta un resumen con el número de
empresas y registros afectados y, si se han producido errores de validación,
una tabla descargable con el detalle empresa por empresa procedente de
`import_errors`.

[FIGURA 5.2 — Vista de carga de datos]

### 5.5.4 Listado de empresas

La vista de listado proporciona una consulta general sobre las empresas
disponibles en la base de datos. Se construye sobre `st.dataframe` con las
columnas más relevantes para la identificación rápida: nombre, CIF, código
CNAE, provincia, país y año más reciente con datos disponibles.

El usuario dispone de un buscador por nombre o CIF y de filtros por país y por
sector CNAE para acotar el universo mostrado. La tabla soporta selección de
fila, lo que permite saltar directamente a la ficha individual de una empresa
mediante el mismo mecanismo de navegación que se describe en el apartado del
screener.

[FIGURA 5.3 — Listado de empresas]

### 5.5.5 Ficha de empresa

La ficha es la vista de mayor profundidad analítica sobre una empresa
individual. Está organizada en tres secciones verticales.

La cabecera presenta los datos maestros enriquecidos de la empresa: web oficial,
provincia, identificador BvD, nombre del *Global Ultimate Owner* (GUO) cuando
existe, fecha de constitución y descripción de actividad en castellano e inglés.
Los datos descriptivos se leen de los campos `native_trade_description` y
`english_trade_description` de SABI.

La sección intermedia recoge los indicadores financieros clave del último
ejercicio disponible, agrupados en cuatro bloques temáticos: rentabilidad,
crecimiento, apalancamiento y productividad por empleado. Cada bloque se
representa como un conjunto de tarjetas con el valor del indicador y la unidad.
Esta sección incorpora las métricas añadidas durante la migración a la nueva
base de datos: deuda bruta, deuda neta, cash flow y cash conversion, que no
estaban presentes en la versión inicial con SQLite.

La sección inferior contiene los gráficos de evolución histórica. Para cada
magnitud relevante (ingresos, EBITDA, deuda neta, márgenes de rentabilidad) se
genera un gráfico de líneas con todos los ejercicios disponibles para la
empresa. La selección de magnitudes a visualizar se basa en lo que un equipo de
*search fund* consulta habitualmente al revisar una candidata: tendencia de
crecimiento, evolución del margen y trayectoria del endeudamiento.

[FIGURA 5.4 — Ficha histórica de empresa]

### 5.5.6 Screener

El screener es la vista central del proceso de *sourcing*. Permite al usuario
filtrar el universo de empresas según criterios cuantitativos configurables y
ordenar el resultado por la puntuación compuesta del modelo WSM.

La columna izquierda agrupa los filtros: rango de ingresos, rango de deuda
neta, rango de margen EBITDA, código CNAE, provincia y año de referencia. Bajo
los filtros aparece un panel con cuatro deslizadores correspondientes a las
cuatro dimensiones del modelo WSM definido en el Capítulo 4. El usuario puede
ajustar el peso de cada dimensión sin tocar ningún fichero de configuración.
Los pesos se normalizan automáticamente para que sumen uno antes de aplicar la
fórmula del modelo.

La columna principal muestra los resultados en dos elementos coordinados. Arriba
aparece un gráfico de ranking horizontal con las veinte empresas con mayor
puntuación dentro de los filtros activos. Cada barra incluye un *hover*
enriquecido con los valores de empresa, CNAE, puntuación, ingresos, margen
EBITDA, crecimiento de ingresos y ratio ND/EBITDA. Esta visualización sustituye
al gráfico original de la primera versión, que era un *scatter plot* de
crecimiento frente a margen EBITDA con tamaño proporcional al revenue y color
por CNAE. El *scatter* presentaba dos problemas para la finalidad del screener:
los valores atípicos distorsionaban el eje y dificultaban la lectura, y la
leyenda con muchos sectores ocupaba demasiado espacio sin ayudar a priorizar.
El ranking horizontal por puntuación es más alineado con el objetivo real de la
vista, que es seleccionar candidatas, no explorar la dispersión del universo.

Debajo del gráfico aparece la tabla completa de empresas filtradas, con todas
las columnas relevantes y la puntuación numérica. La tabla soporta selección de
fila para abrir directamente la ficha de la empresa elegida. La navegación se
implementa guardando el `company_id` seleccionado en `st.session_state` y
forzando un `st.rerun()` que renderiza la vista de ficha con la empresa cargada.

[FIGURA 5.5 — Screener financiero]

### 5.5.7 Análisis sectorial

La vista sectorial responde a una necesidad distinta del screener: en lugar de
priorizar empresas concretas, ayuda al usuario a entender la posición relativa
de un sector frente al mercado y su evolución temporal.

La parte superior muestra los KPIs sectoriales agregados en formato de tarjetas:
mediana del margen EBITDA, mediana del crecimiento de ingresos, número de
empresas en el sector y años con datos disponibles. Una decisión deliberada del
diseño es usar la mediana en lugar de la media en estos resúmenes. La media
resulta muy sensible a las empresas atípicas y, en sectores con pocas empresas
o con variaciones extremas, producía valores que no representaban el
comportamiento habitual del sector. La mediana ofrece una lectura más estable.

La sección intermedia presenta dos gráficos principales. El primero muestra la
evolución del sector mediante una combinación de barras del revenue total
agregado por año y una línea con el margen EBITDA mediano por año. Esta
visualización sustituye al boxplot original de distribución del EBITDA, que
producía mucho ruido visual sin transmitir una narrativa clara. La nueva
combinación permite ver de un vistazo si el sector crece en volumen y si esa
evolución va acompañada de una mejora del margen.

El segundo gráfico muestra la tendencia de crecimiento del sector frente a la
del mercado. La primera versión calculaba una media simple del crecimiento
interanual, pero los casos extremos (por ejemplo, una empresa que pasa de
ingresos muy bajos a ingresos normales y genera tasas de crecimiento de varios
miles por ciento) hacían que la escala perdiera utilidad. La versión actual
representa la mediana del crecimiento del sector con una banda del rango
intercuartil, junto con la mediana del mercado calculada exclusivamente sobre
los años para los que el sector tiene datos. Antes de calcular las medianas se
descartan los crecimientos fuera del rango [-100 %, +300 %] para mantener el
eje legible sin perder la lectura de tendencia.

La parte inferior incluye los boxplots de distribución de los principales
indicadores financieros entre las empresas del sector y un mapa de burbujas que
combina margen y crecimiento.

[FIGURA 5.6 — Análisis sectorial por CNAE]

### 5.5.8 Mapa geográfico

La vista del mapa geográfico se incorporó durante la fase de migración a la
nube y no formaba parte del diseño inicial. Su objetivo es ofrecer una lectura
territorial del universo de empresas que complementa al análisis sectorial.

La cartografía se carga desde el fichero `assets/geo/iberia_regions.geojson`,
que combina dos fuentes públicas. Las 52 provincias españolas proceden del
proyecto `es-atlas`, basado en los datos del Instituto Geográfico Nacional. Los
18 distritos de Portugal proceden del conjunto de datos abiertos de E-REDES.
El fichero resultante se incluye dentro del repositorio para que la aplicación
no dependa de una conexión a Internet en producción y el primer renderizado del
mapa sea inmediato.

La vista ofrece dos controles principales. Un selector de sector permite
visualizar todas las empresas o filtrar por un código CNAE concreto. Un
selector de vista alterna entre el modo Península, que recorta a la España
peninsular y a Portugal continental, y el modo Completo, que añade Canarias y
Baleares. Bajo los controles aparecen cuatro tarjetas de resumen con el número
de empresas visualizadas, el número de regiones con presencia, la región con
más empresas y el sector activo.

El mapa requirió resolver tres problemas técnicos durante el desarrollo. El
primero apareció con la implementación inicial basada en `go.Choropleth`: el
componente mostraba la barra de color, pero los polígonos no se pintaban en el
mapa. La solución consistió en renderizar cada provincia y cada distrito como
una traza independiente del tipo `go.Scatter` con la opción `fill="toself"`
para rellenar el polígono, manteniendo una traza adicional invisible
exclusivamente para que la barra de color continua se mostrara correctamente.
El segundo problema afectó al *hover*: al pasar el ratón sobre una provincia,
Plotly mostraba el texto `trace` en lugar del nombre de la región. La solución
fue asignar un nombre explícito a cada traza y construir un `hovertemplate`
propio que combina nombre de la región, país, número de empresas y sector
filtrado. El tercero fue la simplificación de la escala cromática a un degradado
de dos extremos, de azul oscuro para las regiones con menos empresas a dorado
para las de mayor concentración, lo que mejoró la legibilidad sobre el fondo
oscuro de la aplicación.

La normalización de los nombres de provincia entre SABI y el GeoJSON se
implementó en `utils/geography.py` mediante una tabla de mapeo. Algunos casos
relevantes son `Vizcaya` a `Bizkaia`, `Guipuzcoa` a `Gipuzkoa`, `Alava` a
`Araba/Alava` y `Baleares` a `Illes Balears`. Tras aplicar el mapeo, las 52
provincias detectadas en el universo cargado quedan correctamente ubicadas en
el mapa, sin discrepancias.

Bajo el mapa aparece una tabla con el ranking de regiones por número de
empresas, el país al que pertenecen y el porcentaje sobre el total visualizado.

[FIGURA 5.7 — Mapa geográfico de distribución provincial]

## 5.6 Despliegue en Streamlit Community Cloud

El despliegue de Miralyze en Streamlit Community Cloud requiere coordinar tres
elementos: el repositorio con el código fuente, la base de datos en Supabase ya
inicializada y los secretos de configuración. El proceso se realiza una sola
vez para la puesta en marcha inicial y, a partir de ahí, cada `git push` sobre
la rama de producción del repositorio dispara un redespliegue automático.

El primer paso consiste en subir el repositorio a GitHub con todos los assets
necesarios incluidos: el logo del sidebar, el fichero GeoJSON de la cartografía
ibérica, el fichero de tema visual y el `requirements.txt` con las dependencias.
El fichero `.streamlit/secrets.toml` queda explícitamente excluido mediante
`.gitignore` para que las credenciales no viajen al repositorio público. El
fichero `requirements.txt` debe declarar las versiones exactas de Streamlit,
pandas, Plotly, openpyxl, psycopg con binarios precompilados y Pillow.

El segundo paso es la inicialización del esquema en Supabase. El DDL completo
del fichero `database/schema.sql` se ejecuta una única vez desde el SQL Editor
del panel de Supabase, lo que crea las cinco tablas del modelo de datos
descrito en el Capítulo 4 con sus restricciones de unicidad e índices. Esta
operación es independiente del despliegue de la aplicación y no se repite con
cada redespliegue: el esquema vive en la base de datos, no en el código.

El tercer paso es la configuración de los secretos en el panel de Streamlit
Community Cloud. La aplicación necesita una única variable, `SUPABASE_DB_URL`,
con la cadena de conexión completa al pooler de Supabase en el formato:

```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@[POOLER_HOST]:5432/postgres?sslmode=require
```

El parámetro `sslmode=require` fuerza la conexión cifrada con la base de datos.
La cadena se introduce en el formulario de secretos del panel web de Streamlit
Cloud, no en ningún fichero del repositorio. La capa de acceso a datos descrita
en el apartado 5.2 lee la URL de `st.secrets` cuando la aplicación se ejecuta
en este entorno.

Una vez completados los tres pasos, Streamlit Community Cloud arranca la
aplicación en una URL pública asignada al proyecto. La plataforma gestiona el
ciclo de vida de la instancia, incluyendo el reinicio automático cuando la
aplicación lleva tiempo sin uso. Como el sistema de ficheros es efímero entre
reinicios, ningún dato de la aplicación reside en local: las cargas SABI, los
registros financieros y las métricas calculadas viven íntegramente en Supabase
y sobreviven a los reinicios.

[FIGURA 5.8 — Aplicación desplegada en Streamlit Community Cloud]

---

# Capítulo 6. Resultados

Este capítulo presenta los resultados obtenidos al término del desarrollo. La
exposición se articula en cinco apartados. El primero recoge el estado final del
sistema entregado, identificando los componentes operativos y las cifras reales
acumuladas en producción. El segundo describe el resultado de la campaña de
validación, organizada en tres niveles complementarios. El tercero contrasta el
sistema entregado con los objetivos específicos definidos en el Capítulo 3. El
cuarto reconoce las limitaciones que la primera versión asume de forma
deliberada. El quinto, por último, traza las líneas de trabajo futuro derivadas
del propio desarrollo.

A diferencia del Capítulo 5, que documentaba el proceso de construcción del
sistema, este capítulo se ocupa exclusivamente del producto resultante y de la
evidencia que respalda su funcionamiento.

## 6.1 Estado final del sistema

Miralyze se entrega como una aplicación web operativa, con persistencia en la
nube y accesible desde cualquier navegador sin instalación local. El sistema
integra un proceso completo de extracción, transformación y carga, una capa de
cálculo automático de indicadores financieros, una base de datos relacional
desplegada en Supabase y una interfaz de análisis multidimensional construida
sobre Streamlit. Cada uno de estos componentes ha pasado de prototipo a versión
funcional durante el desarrollo del trabajo.

La Tabla 6.1 resume los componentes entregados y su estado al cierre del TFG.

**Tabla 6.1.** Componentes del sistema y estado de entrega.

| Componente | Función | Estado |
|---|---|---|
| Pipeline ETL (`loader`, `validator`, `transformer`) | Lectura de Excel SABI, normalización wide-to-long, validación e inserción | Operativo |
| Motor de métricas | Cálculo de 15 indicadores financieros derivados por empresa-año | Operativo |
| Base de datos PostgreSQL en Supabase | Persistencia normalizada en cinco tablas (`companies`, `financials`, `metrics`, `import_log`, `import_errors`) | Operativo |
| Interfaz Streamlit | Siete vistas: Dashboard, Cargar datos, Listado, Ficha, Screener, Análisis sectorial, Mapa | Operativo |
| Assets estáticos | GeoJSON de regiones ibéricas y logo corporativo | Integrados |
| Despliegue en Streamlit Community Cloud | Acceso público a la aplicación | Pendiente de activación |

El sistema entregado se ha probado con datos reales procedentes de
exportaciones SABI suministradas en el contexto del trabajo. La Tabla 6.2
resume el estado cuantitativo de la base de datos en el momento de cierre.

**Tabla 6.2.** Estado cuantitativo de la base de datos al cierre del TFG.

| Métrica | Valor |
|---|---|
| Empresas registradas | 9.132 |
| Registros financieros (`financials`) | 60.112 |
| Métricas calculadas (`metrics`) | 60.112 |
| Importaciones acumuladas | 7 |
| Cobertura temporal | 1995-2025 |
| Cobertura geográfica | 52 provincias españolas |

Estas cifras describen un sistema validado con un volumen de datos superior al de
una prueba mínima. La ratio de un registro financiero por cada empresa-año implica que la pipeline ha
mantenido la integridad referencial bajo la restricción `UNIQUE(company_id,
year)` durante las siete cargas sucesivas. La igualdad exacta entre el número
de filas en `financials` y en `metrics` confirma que el motor de cálculo se ha
ejecutado para la totalidad de los registros financieros persistidos, sin
rezagos ni huecos. La cobertura geográfica de 52 provincias corresponde a la
totalidad del territorio español, incluyendo Ceuta y Melilla.

La interfaz incluye las seis vistas analíticas comprometidas en el objetivo OE3
más una vista administrativa de carga de datos, lo que suma siete vistas en total.
Las seis vistas analíticas operan sobre el mismo conjunto unificado de datos sin
necesidad de recargar la aplicación. La identidad visual aplicada
de forma consistente en todas las vistas, descrita en el apartado 5.5, se
mantiene también en los gráficos generados por Plotly y en el mapa
geográfico.

El despliegue en Streamlit Community Cloud queda como último paso operativo.
La arquitectura está preparada para ello, tal como se documenta en el apartado
5.6: el repositorio se ha estructurado para ser consumido por la plataforma, la
configuración por secretos está externalizada y la dependencia de SQLite local
ha sido eliminada por completo. La activación del despliegue público es una
acción puntual que no requiere modificaciones adicionales del código.

## 6.2 Validación del sistema

La validación del sistema se planteó con un criterio pragmático. En lugar de
construir un catálogo artificial de pruebas unitarias dirigido a demostrar
cobertura, se diseñó un plan compacto de catorce pruebas representativas, cada
una asociada a un riesgo concreto identificado durante el desarrollo. El plan
se estructura en tres niveles de validación que se corresponden con tres
preguntas sucesivas: ¿arranca la aplicación y se conecta a sus dependencias?,
¿procesa correctamente los datos que recibe?, y ¿responde la interfaz de forma
coherente al usuario? Las catorce pruebas se identifican con los códigos P01 a
P14. La Tabla C.1 del Anexo C recoge para cada una de ellas el objetivo, la
entrada empleada, el resultado esperado, el resultado observado y la
documentación gráfica asociada cuando procede. En el cuerpo del capítulo se
resumen los resultados agrupados por nivel.

### 6.2.1 Validación técnica

El primer nivel verifica que el sistema arranca y se comunica correctamente con
sus dependencias externas. Comprende las pruebas P01 (arranque local) y P02
(conexión con Supabase).

La aplicación arranca sin errores mediante el comando `streamlit run app.py` y
presenta el Dashboard cargado en menos de tres segundos en el entorno local de
desarrollo. La conexión con Supabase se establece de forma estable durante el
arranque y se mantiene activa durante la sesión: las consultas iniciales
recuperan las 9.132 empresas registradas en la nube sin que ningún componente
del sistema lea ni escriba en ficheros locales. Esta segunda prueba es
particularmente relevante porque confirma que la migración descrita en el
apartado 5.4 ha sido completa y que no quedan dependencias residuales del
backend SQLite original.

### 6.2.2 Validación de datos

El segundo nivel comprueba que la pipeline de importación se comporta
correctamente frente a los casos representativos del dominio SABI. Comprende
las pruebas P03 a P08.

La persistencia financiera (P03) y el cálculo de métricas (P04) se verificaron
mediante consultas de conteo sobre las tablas `financials` y `metrics`. Los
60.112 registros observados en cada tabla, exactamente coincidentes, demuestran
que la pipeline garantiza una correspondencia uno a uno entre cada par
empresa-año persistido y su métrica derivada. La importación de un Excel SABI
real (P05) reprodujo la transformación wide-to-long descrita en 5.3, la
interpretación correcta del campo `Last available year` y la cadena de upsert
basada en `bvd_id`, sin filas huérfanas ni duplicadas.

La inhabilitación de la carga por CSV (P06) se confirmó comprobando que la
interfaz de carga acepta exclusivamente extensiones `.xlsx` y `.xls`. Esta
restricción responde al problema documentado en 5.3: las descripciones
empresariales que contienen comas pueden corromper un fichero CSV mal escapado
y derivar en filas malformadas en producción.

El tratamiento de valores ausentes (P07) y de fechas históricas anteriores al
rango habitual (P08) se validó con muestras reales en las que los campos
financieros llegan como cadena `n.a.` y donde la fecha de constitución
corresponde a empresas centenarias. En ambos casos el sistema produjo el
comportamiento esperado: los valores `n.a.` se almacenaron como `NULL` en la
base de datos, sin contaminar las columnas numéricas con texto, y las fechas
históricas se parsearon antes de la inserción y llegaron a PostgreSQL en un
formato aceptado por su tipo `DATE`.

### 6.2.3 Validación funcional

El tercer nivel verifica que las vistas de la interfaz responden de forma
coherente a las acciones del usuario. Comprende las pruebas P09 a P13, una por
cada vista analítica que requiere validación funcional.

El Screener financiero (P09) genera un ranking ordenado por la puntuación
compuesta WSM, calculada de forma dinámica sobre el universo de 9.132 empresas
con los pesos configurados por el usuario. Los controles de umbral sobre
revenue, deuda total y CNAE producen subconjuntos coherentes que se actualizan
sin recargar la página. La navegación desde el Screener hacia la ficha individual (P10)
funciona correctamente: la selección de una fila abre la vista de Ficha de
empresa con la entidad correspondiente preseleccionada y sus datos cargados. La
Ficha de empresa (P11) presenta los datos históricos de cuenta de resultados,
los KPIs derivados y los gráficos de evolución plurianual sin discrepancias
respecto a los valores almacenados en base de datos.

El Análisis sectorial (P12) compara el CNAE seleccionado contra el agregado del
mercado y renderiza correctamente el gráfico combinado de revenue total y
margen EBITDA mediano que sustituyó al boxplot original. La sustitución
respondía a una limitación de interpretabilidad detectada durante la
validación. El Mapa geográfico (P13) presenta las 52 provincias españolas como
polígonos pintados con la escala de color asignada al número de empresas, y el
ranking regional acompañante refleja la distribución observada. La
implementación basada en trazas `go.Scatter` con `fill="toself"`, descrita en
5.5, produce el resultado visual esperado tras corregir el comportamiento del
componente `go.Choropleth` original.

### 6.2.4 Incidencias detectadas y resueltas

Durante la validación se identificaron siete incidencias técnicas que afectaban
al funcionamiento o a la presentación del sistema. Todas fueron diagnosticadas,
corregidas y reverificadas antes de la entrega. La Tabla 6.3 las recoge de
forma sintética; el detalle de cada solución se documenta en el Capítulo 5 en
el apartado correspondiente al componente afectado.

**Tabla 6.3.** Incidencias detectadas durante la validación y resolución aplicada.

| Incidencia | Componente afectado | Resolución |
|---|---|---|
| Fechas anteriores a 1900 rechazadas por PostgreSQL | Validador de la pipeline | Parseo previo a la inserción |
| Riesgo de corrupción en ficheros CSV con descripciones | Vista de carga | Inhabilitación de CSV; aceptación exclusiva de Excel |
| Ranking del Dashboard renderizado como código HTML | Dashboard | Uso de `streamlit.components.v1.html` |
| Top 10 CNAE truncado visualmente | Dashboard | Ajuste de altura del componente y compactación interna |
| Logo del sidebar no cargado | Layout general | Asset preprocesado y carga directa |
| Choropleth sin polígonos pintados | Mapa geográfico | Trazas `go.Scatter` con relleno por provincia |
| Hover del mapa con etiqueta `trace` por defecto | Mapa geográfico | `hovertemplate` personalizado por provincia |

En los siete casos, la causa subyacente fue un comportamiento por defecto de las
bibliotecas empleadas que no se ajustaba a los requisitos del sistema, y la
resolución se realizó sin alterar la arquitectura general.

### 6.2.5 Despliegue cloud

La prueba P14, relativa al despliegue en Streamlit Community Cloud, queda
pendiente de ejecución en el momento de cierre del documento. El sistema ha
sido preparado íntegramente para este despliegue, según se describe en el
apartado 5.6, y la activación se planificará en coordinación con el tutor para
realizarla con anterioridad a la defensa del trabajo. Una vez completada, la
captura de la aplicación accesible en su URL pública se incorporará como Figura
C.7 del Anexo C.

## 6.3 Grado de cumplimiento de los objetivos

Este apartado contrasta el sistema entregado con los cinco objetivos específicos
formulados en el Capítulo 3. Para cada objetivo se indica el estado de
cumplimiento y la evidencia concreta que lo respalda, evitando declaraciones
genéricas. La Tabla 6.4 ofrece una visión sintética del balance global; los
párrafos posteriores desarrollan cada caso.

**Tabla 6.4.** Balance de cumplimiento de los objetivos específicos.

| Objetivo | Estado | Evidencia principal |
|---|---|---|
| OE1 — Adquisición e integración de datos | Cumplido | 7 importaciones SABI completadas; 9.132 empresas y 60.112 registros financieros persistidos |
| OE2 — Cálculo automático de indicadores | Cumplido | 60.112 filas en `metrics`; 15 indicadores derivados por empresa-año |
| OE3 — Interfaz web de análisis multidimensional | Cumplido | 6 vistas analíticas + 1 administrativa operativas; pruebas P09-P13 superadas |
| OE4 — Persistencia en la nube y despliegue accesible | Cumplido en persistencia; pendiente la activación del despliegue público | Migración a Supabase/PostgreSQL completada (P02-P03); arquitectura preparada para Streamlit Community Cloud |
| OE5 — Validación con datos reales a escala | Cumplido | 9.132 empresas, 60.112 registros, serie 1995-2025, 52 provincias |

### 6.3.1 OE1 — Adquisición e integración de datos

El objetivo se considera cumplido. La pipeline ETL implementada en los módulos
`loader.py`, `validator.py` y `transformer.py` lee exportaciones Excel reales de
SABI, interpreta correctamente la estructura de columnas basada en sufijos
relativos al año base (`Last avail. yr`, `Year - 1`, …, `Year - 6`) y convierte
el formato wide al modelo relacional empresa-año.

La evidencia cuantitativa es directa: la base de datos en Supabase acumula siete
importaciones completadas, registradas en `import_log`, con un total de 9.132
empresas en `companies` y 60.112 registros en `financials`. Las pruebas P05
(importación Excel SABI) y P07 (tratamiento de valores `n.a.`) confirman que la
pipeline maneja correctamente los casos representativos del dominio sin
introducir filas malformadas. La tabla `import_errors` registra las filas
rechazadas con su motivo, lo que aporta trazabilidad completa del proceso.

### 6.3.2 OE2 — Cálculo automático de indicadores financieros

El objetivo se considera cumplido. El módulo `metrics/calculator.py` deriva
quince indicadores financieros para cada combinación empresa-año a partir de
los datos persistidos en `financials`, agrupados en cinco categorías: estructura
de deuda, márgenes, crecimiento, productividad por empleado y solidez
patrimonial. La invocación es automática al final de cada importación; el
analista no necesita ejecutar ningún cálculo manual.

La evidencia cuantitativa es la igualdad exacta entre el número de filas en
`financials` y el número de filas en `metrics` (60.112 en cada tabla),
verificada en la prueba P04. Esa equivalencia demuestra que el motor se ha
ejecutado para la totalidad de los registros financieros, sin dejar
combinaciones empresa-año sin cubrir. La puntuación compuesta WSM, que
complementa los indicadores individuales para ordenar el universo de
candidatos, se calcula dinámicamente en la vista de Screener con pesos
configurables, tal como se describe en 4.6.2.

### 6.3.3 OE3 — Interfaz web de análisis multidimensional

El objetivo se considera cumplido. La aplicación entrega las seis vistas
analíticas comprometidas en el objetivo (Dashboard, Listado de empresas, Ficha
de empresa, Screener, Análisis sectorial y Mapa geográfico) más una séptima
vista administrativa de Carga de datos. Las seis vistas analíticas operan sobre
el mismo conjunto unificado de datos, comparten la identidad visual descrita
en 5.5 y permiten al analista atacar el universo de empresas desde ángulos
complementarios sin abandonar la aplicación.

La evidencia funcional procede de las pruebas P09 a P13, una por cada vista
analítica que requiere validación de comportamiento ante la interacción del
usuario. Todas se superan con resultado conforme: el Screener filtra y ordena
sobre las 9.132 empresas, la navegación al detalle de cada empresa funciona sin
recargas, la Ficha presenta los históricos coherentes con la base de datos, el
Análisis sectorial compara el CNAE seleccionado contra el agregado del mercado
y el Mapa geográfico pinta correctamente las 52 provincias españolas.

### 6.3.4 OE4 — Persistencia en la nube y despliegue accesible

El objetivo se considera cumplido en su componente de persistencia y pendiente
en su componente de despliegue público. La migración de SQLite a PostgreSQL en
Supabase está completa, validada por las pruebas P02 (conexión cloud) y P03
(persistencia de financials). La aplicación no escribe ni lee datos en local;
toda la información reside en la nube y sobrevive a los reinicios de la
plataforma de despliegue, lo que cumple el requisito de persistencia entre
sesiones.

El despliegue en Streamlit Community Cloud, que corresponde a la prueba P14,
queda pendiente de activación en el momento de cierre del documento. El sistema
está preparado para ello: el repositorio se ha estructurado para ser consumido
por la plataforma, las dependencias están declaradas en `requirements.txt`, la
configuración por secretos está externalizada y la aplicación arranca sin
errores en entorno local replicando las condiciones del entorno cloud. La
activación es una operación puntual que no requiere modificaciones adicionales
del código.

### 6.3.5 OE5 — Validación con datos reales a escala

El objetivo se considera cumplido. El sistema se ha probado con un volumen de
datos significativamente superior al de un prototipo de demostración: 9.132
empresas reales, 60.112 registros financieros con series históricas que cubren
desde 1995 hasta 2025 y una distribución geográfica que abarca las 52
provincias españolas.

La integridad de la importación se ha verificado mediante la coincidencia
exacta entre el número de filas en `financials` y en `metrics`, así como por
la ausencia de filas duplicadas bajo la restricción `UNIQUE(company_id, year)`.
La corrección de los cálculos se ha validado de forma indirecta a través del
funcionamiento coherente de las vistas analíticas, que dependen de las
métricas derivadas: cualquier inconsistencia significativa en los cálculos se
habría manifestado en los gráficos del Análisis sectorial o en los rankings
del Screener. El comportamiento de la interfaz bajo el universo real cargado
se ha verificado en las pruebas P09 a P13 sin observar degradación de
rendimiento perceptible.

### 6.3.6 Síntesis del balance

Los cinco objetivos específicos se consideran cumplidos. El único condicionante
en el momento de cierre del documento es la activación del despliegue público
en Streamlit Community Cloud (P14), que se incluye dentro de OE4 y cuya
ejecución es una acción operativa pendiente de programación previa a la
defensa. Esta circunstancia no afecta al cumplimiento del resto de los
objetivos ni al funcionamiento del sistema en entorno local y cloud
gestionado por la base de datos.

## 6.4 Limitaciones identificadas

El sistema entregado es funcional y cubre los objetivos definidos, pero su
alcance se ha acotado de forma deliberada. Algunas de las restricciones que se
describen a continuación ya se anticiparon en el apartado 3.3.2 como decisiones
de diseño; otras han emergido durante el propio desarrollo y conviene
documentarlas con la misma honestidad. En ningún caso comprometen la utilidad
del sistema dentro del marco para el que fue concebido.

### 6.4.1 Dependencia de SABI como fuente única

La pipeline de importación está calibrada para la estructura de columnas de las
exportaciones SABI: sufijos `Last avail. yr` y `Year - N`, nomenclatura inglesa
de magnitudes contables y formato Excel `.xlsx`. Integrar otra fuente, como
Informa D&B, Axesor o ficheros ad hoc procedentes de la propia empresa
analizada, requeriría adaptar el módulo `loader.py` y, previsiblemente,
introducir una capa de normalización de nombres de campo entre fuentes.

Esta dependencia no compromete el caso de uso central. SABI es la herramienta
estándar para el análisis de empresas privadas en el mercado ibérico y casi
todos los equipos de *search funds* operan a partir de sus exportaciones. Sin
embargo, conviene tenerla presente si se quisiera generalizar el sistema a
otros mercados o combinar SABI con fuentes complementarias.

### 6.4.2 Actualización manual del universo de datos

Los datos del Registro Mercantil se actualizan anualmente, a medida que las
empresas depositan sus cuentas. Miralyze no dispone de conexión directa a la
API de SABI ni de tareas programadas de refresco: cada nuevo ejercicio fiscal
exige al analista exportar el universo desde SABI y cargarlo manualmente desde
la vista de Carga de datos. La actualización es un proceso operativo
controlado, no automatizado.

En el contexto de búsqueda esta limitación es asumible. La frecuencia natural
de actualización de los datos contables es anual y la decisión de qué subuniverso
cargar en cada momento (por sector, por tamaño, por área geográfica) es en sí
misma parte del trabajo del analista. Una automatización ciega contra la API
podría deteriorar esta selección consciente del universo de trabajo.

### 6.4.3 Ausencia de autenticación y de gestión de usuarios

La primera versión opera bajo el supuesto de un entorno controlado por un
único equipo. No se han implementado registro de usuarios, roles, permisos ni
políticas de Row Level Security en Supabase. Cualquier persona con acceso a la
URL desplegada vería los mismos datos y podría ejecutar las mismas
operaciones, incluida la carga de nuevos ficheros.

Para un uso interno de un *search fund* concreto este modelo es suficiente,
pero no para un escenario multi-equipo o comercial. Una versión orientada a
varios usuarios necesitaría añadir, como mínimo, autenticación, segregación
de universos por equipo y un control de auditoría sobre las cargas.

### 6.4.4 Rendimiento no evaluado más allá del volumen probado

El sistema se ha validado con 9.132 empresas y 60.112 registros financieros,
volumen suficiente para el caso de uso real. Las consultas operan dentro de
tiempos de respuesta aceptables sobre este conjunto, pero no se ha medido el
comportamiento ante volúmenes un orden de magnitud superiores. La
arquitectura actual no incluye paginación en las consultas que alimentan el
listado, ni estrategias de caché aplicadas a los agregados sectoriales o
geográficos.

Si en el futuro se cargan universos de varios cientos de miles de empresas o
se incorporan series temporales más profundas, sería previsible la aparición
de cuellos de botella en las vistas que ejecutan agregaciones sobre todo el
universo, especialmente el Análisis sectorial y el Mapa geográfico.

### 6.4.5 Validación con base en revisión funcional, sin tests automatizados

La campaña de validación descrita en el apartado 6.2 se ha apoyado en pruebas
funcionales y en consultas de conteo sobre la base de datos. No se ha
construido una suite de tests unitarios ni de integración automatizados para
los módulos del pipeline ETL ni para el motor de cálculo de métricas. Cada
iteración del desarrollo se ha verificado de forma manual.

Esta decisión es coherente con el alcance de un primer prototipo funcional,
donde el coste de mantener una suite de tests durante la fase de exploración
del modelo de dominio habría sido desproporcionado. Sin embargo, en el momento
en que la aplicación pase a un uso recurrente, la ausencia de cobertura
automatizada se convierte en un riesgo: cualquier cambio en `calculator.py` o
en la pipeline puede introducir regresiones silenciosas que solo se detectarían
al observar resultados anómalos en la interfaz.

## 6.5 Trabajo futuro

Las líneas de trabajo futuro que se proponen a continuación se han identificado
durante el desarrollo del propio sistema. No constituyen una lista genérica de
mejoras posibles, sino una traducción concreta de las limitaciones reconocidas
en 6.4 y de las oportunidades observadas al usar el producto. Se ordenan por
horizonte temporal aproximado, en función del esfuerzo y de la dependencia
respecto al estado actual del sistema.

### 6.5.1 Continuación inmediata del trabajo

Las siguientes mejoras se derivan directamente de las limitaciones documentadas
y pueden abordarse sobre la versión entregada sin cambios estructurales:

- **Autenticación de usuarios en Supabase.** Añadir un proveedor de
  autenticación (correo y contraseña, OAuth) y reglas de Row Level Security
  para segregar lo que cada usuario puede ver y modificar. Es la respuesta
  natural a la limitación 6.4.3.
- **Filtro por provincia en el Screener.** El campo `province` ya está
  poblado en `companies` y se utiliza en el Mapa geográfico, pero no se
  expone como filtro en la vista de Screener. Su incorporación tendría coste
  bajo y aportaría a los analistas una dimensión geográfica adicional para el
  *sourcing*.
- **Informes de importación descargables.** El contenido de `import_log` e
  `import_errors` se muestra en pantalla; convertirlo en un fichero
  descargable (Excel o PDF) facilitaría la trazabilidad del trabajo del
  analista y el reporte interno dentro del equipo.
- **Suite de tests automatizados para el pipeline y el motor de métricas.**
  Cubrir con tests unitarios las funciones de detección de columnas, parseo
  de fechas, conversión `n.a.` a `NULL` y cálculo de cada indicador
  derivado, junto con tests de integración sobre ficheros Excel sintéticos.
  Es la respuesta natural a la limitación 6.4.5.

### 6.5.2 Evolución a medio plazo

Las siguientes líneas requieren un esfuerzo mayor o introducen cambios en la
experiencia de usuario, pero se apoyan sobre la arquitectura existente:

- **Selector de métrica en el Mapa geográfico.** Hoy el mapa presenta el
  número de empresas por provincia. Permitir al usuario elegir la métrica
  representada (revenue total, EBITDA medio, cash flow agregado) ofrecería
  lecturas comparativas adicionales sobre la misma geometría.
- **Personalización de la puntuación compuesta del Screener.** La versión
  actual aplica el modelo WSM sobre cuatro indicadores fijos
  (`ebitda_margin`, `revenue_growth_yoy`, `equity_ratio`,
  `ebitda_per_employee`). Permitir al usuario seleccionar qué indicadores
  participan en el ranking, además de ajustar sus pesos, daría flexibilidad
  para adaptar el screening a tesis de inversión específicas.
- **Procesamiento por lotes de ficheros grandes.** Reescribir la fase de
  upsert para procesar la importación en bloques con seguimiento de
  progreso, lo que facilitaría la carga de exportaciones SABI con decenas
  de miles de empresas sin bloquear la interfaz.
- **Búsqueda por descripción de actividad.** Añadir un buscador textual
  sobre los campos `native_trade_description` y `english_trade_description`
  para complementar la búsqueda por código CNAE, útil cuando el código no
  refleja con precisión la actividad real.

### 6.5.3 Extensión del alcance

Las siguientes líneas amplían el campo del sistema más allá de su propuesta
inicial y requerirían trabajo de diseño adicional antes de su implementación:

- **Integración con fuentes alternativas.** Adaptar el pipeline para
  ingerir datos de Informa D&B, Axesor o ficheros estructurados aportados
  por la propia empresa analizada, con una capa de normalización entre
  fuentes que reduzca la dependencia documentada en 6.4.1.
- **Despliegue multi-tenant.** Una vez resuelta la autenticación,
  evolucionar la base de datos hacia un modelo multi-tenant en el que
  varios *search funds* puedan operar sobre la misma instancia con
  aislamiento estricto de sus datos.
- **Conexión directa a la API de SABI.** Reemplazar la carga manual de
  exportaciones por un proceso programado que mantenga el universo de
  datos sincronizado con la fuente, formalizando previamente las
  condiciones de licencia con el proveedor.
- **Modelos de scoring más sofisticados.** Sustituir o complementar el
  modelo WSM con técnicas de análisis de decisión multicriterio
  alternativas (TOPSIS, ELECTRE, AHP) o, en un horizonte más ambicioso,
  modelos basados en aprendizaje supervisado entrenados con los
  resultados históricos de operaciones cerradas por el equipo.

---

---

# Capítulo 7. Conclusiones

El Capítulo 6 ha presentado los resultados del trabajo: qué se construyó, qué se
validó y qué quedó fuera de alcance. Este capítulo asume esos resultados y se
ocupa de algo distinto: qué significa el conjunto del trabajo una vez terminado.
Se estructura en tres apartados de naturaleza progresivamente más interpretativa.
El apartado 7.1 sintetiza, en términos verificables, el sistema entregado y su
aportación; el apartado 7.2 recoge la lectura del propio autor sobre el proceso
de desarrollo y los aprendizajes obtenidos; el apartado 7.3 sitúa el resultado
en su contexto económico y social.

## 7.1 Conclusiones objetivas

### 7.1.1 El sistema entregado

Miralyze es una aplicación web funcional, desplegable y operativa. Su pipeline
ETL ingiere las exportaciones nativas de SABI, las normaliza al esquema interno
de cinco tablas y persiste el resultado en una base de datos PostgreSQL alojada
en Supabase. Sobre esa base, el módulo `metrics/calculator.py` deriva quince
indicadores financieros y operativos por empresa y ejercicio, y la interfaz
Streamlit los expone a través de seis vistas independientes que cubren la
exploración del universo, el ranking dinámico de candidatas mediante el modelo
WSM, la consulta del histórico de cada compañía, la representación geográfica
por provincia y la trazabilidad del proceso de importación.

Los cinco objetivos específicos formulados en el Capítulo 3 se han alcanzado
con la única salvedad documentada del despliegue público en Streamlit Community
Cloud, cuya activación es una acción operativa pendiente de programación
previa a la defensa y que no afecta al funcionamiento del sistema. La validación
se ha realizado sobre 9.132 empresas reales, 60.112 registros financieros con
métricas calculadas, una serie temporal que se extiende de 1995 a 2025 y la
totalidad de las 52 provincias del territorio español. La conclusión objetiva
de primer orden es directa: existe un artefacto software que cumple la
especificación con la que se concibió.

### 7.1.2 Aportación al proceso de sourcing en search funds

El proceso de sourcing tal como lo describe la literatura de search funds
–y tal como lo practican los equipos consultados durante la fase preliminar
de este trabajo– descansa sobre hojas de cálculo construidas a medida por
cada analista. La exportación de SABI se descarga, se limpia manualmente, se
filtra con criterios definidos en cada iteración, y se ordena con fórmulas
escritas sobre la marcha. El resultado es difícilmente reproducible: dos
analistas del mismo equipo, partiendo de la misma exportación, llegan a
universos comparables pero no idénticos, y la trazabilidad del razonamiento
se pierde con cada nuevo libro de Excel.

Miralyze interviene exactamente sobre la parte mecánica de ese proceso. La
ingestión, la normalización, el cálculo de ratios y la ordenación dejan de
ser tareas que el analista resuelva en cada iteración y pasan a ser
operaciones del sistema. El analista recupera tiempo para lo que la
herramienta no puede hacer: la lectura cualitativa de cada candidata, el
contraste con su tesis de inversión y la decisión de profundizar en una
empresa concreta. El planteamiento del trabajo no ha sido en ningún momento
sustituir el juicio del inversor por un score automático, sino reducir el
coste de llegar al punto en el que ese juicio resulta posible.

### 7.1.3 Aportación como herramienta de referencia abierta

La revisión del estado del arte realizada en el Capítulo 2 no ha localizado,
hasta donde alcanza el alcance bibliográfico de este trabajo, ninguna
herramienta de código abierto orientada al screening financiero de PYMEs
ibéricas para search funds. Los productos comerciales del segmento –Bloomberg,
Capital IQ, Power BI con conectores propietarios– cubren funcionalidades
parciales, pero ninguno encaja con la combinación de fuente de datos (SABI),
caso de uso (sourcing en search funds) y modelo de coste (gratuito) que define
el problema abordado.

El sistema entregado, junto con su documentación técnica y su arquitectura
modular, queda disponible para que otros equipos lo adopten, lo evalúen y lo
extiendan. La elección de un stack tecnológico de uso generalizado –Python,
Streamlit, PostgreSQL, Plotly– y la separación en capas de ingestión, cálculo
y presentación facilitan tanto la lectura del código como la incorporación de
las extensiones identificadas en 6.5. El valor del trabajo, en este sentido,
no se agota en la aplicación instanciada para el ejercicio académico, sino que
se proyecta sobre la posibilidad de que el artefacto sirva de base para
trabajos posteriores.

## 7.2 Conclusiones subjetivas

Las conclusiones que siguen recogen la lectura del autor sobre el desarrollo
del trabajo. Se han redactado tras finalizar el sistema y revisar la
documentación generada durante el curso del proyecto, con el ánimo de
identificar aprendizajes concretos y no de elaborar valoraciones genéricas
sobre la experiencia. Cuando proceda, se utiliza la primera persona.

### 7.2.1 Aprendizajes técnicos

El problema técnico más exigente del proyecto no ha sido ninguno de los
componentes individuales del sistema, sino la transformación inicial de las
exportaciones SABI desde su formato wide al esquema relacional largo en el
que opera la base de datos. El formato de columnas que utiliza SABI –la
combinación del sufijo `Last avail. yr` con la serie `Year - 1`, `Year - 2`
hasta `Year - 6`– carece de documentación pública, varía levemente entre
exportaciones y obliga a deducir el ejercicio de referencia a partir del
encabezado del fichero. Resolver ese desensamblado de forma robusta exigió
varias iteraciones y una lectura cuidadosa de ficheros reales generados en
distintas fechas. El aprendizaje transversal es que la solidez de una
pipeline ETL depende, antes que del código que la implementa, del tiempo
invertido en entender el formato de origen y en aceptar que ese formato
nunca es exactamente lo que la documentación dice que es.

El paso de pandas como mecanismo de persistencia improvisado a una base
PostgreSQL gestionada con `psycopg` v3 y operaciones de upsert por clave
compuesta supuso una segunda curva de aprendizaje significativa. La gestión
explícita de tipos –en particular, la conversión entre `Decimal` de
PostgreSQL y `float` de Python al cruzar la frontera entre la base de datos
y el motor de cálculo– fue origen de los defectos más sutiles del proyecto y
obligó a establecer una norma clara sobre dónde se realiza la conversión.

Streamlit, por su parte, plantea una restricción arquitectónica que no es
evidente en su documentación introductoria: cada interacción del usuario
provoca la re-ejecución completa del script. Diseñar la aplicación bajo esa
premisa –apoyándose en `st.session_state` para preservar estado entre
ejecuciones y en `@st.cache_data` para evitar recargas innecesarias de la
base de datos– es un patrón que requiere asimilarse. La elección final de
Plotly para la visualización añadió un aprendizaje específico: el método
estándar `go.Choropleth` no rendía correctamente los polígonos del GeoJSON
local utilizado, y la solución pasó por construir el mapa con `go.Scatter` y
relleno `fill="toself"`. La conclusión derivada es que la documentación
oficial de las bibliotecas describe el comportamiento esperado, pero no
siempre el comportamiento observado, y que el desarrollo eficiente exige
combinar la lectura de la documentación con la experimentación directa.

### 7.2.2 Aprendizajes de proceso

La decisión metodológica más útil del proyecto fue trabajar con datos reales
desde la primera iteración. La validación sobre exportaciones SABI auténticas
desde el primer sprint reveló problemas –valores `n.a.`, ejercicios contables
desplazados, empresas con series incompletas– que ninguna batería de datos
sintéticos habría anticipado. El coste de incorporar datos reales al ciclo
de desarrollo es bajo cuando se asume desde el principio; intentar
introducirlos al final suele forzar reescrituras costosas.

La acotación del alcance ha sido tan importante como la elección de las
funcionalidades incluidas. Renunciar a la autenticación de usuarios, a una
suite de tests automatizados y al procesamiento por lotes en esta primera
versión fue una decisión deliberada. Cada una de esas líneas tiene su lugar
en el trabajo futuro descrito en 6.5, pero introducirlas en la versión
inicial habría desplazado el esfuerzo desde la construcción del valor central
del sistema –el flujo completo de SABI a interfaz de análisis– hacia
componentes accesorios. En proyectos de duración acotada, la disciplina para
no acometer lo que parece imprescindible pero no lo es resulta tan necesaria
como la capacidad técnica para implementar lo que sí lo es.

Mantener un documento técnico vivo (`DOCUMENTACION.md`) durante el desarrollo,
actualizado iteración a iteración, ha tenido un efecto colateral que no se
había anticipado al inicio: ha reducido sustancialmente el tiempo necesario
para redactar la presente memoria y ha minimizado los errores de descripción
entre lo que el sistema hace y lo que el documento afirma que hace. La
documentación contemporánea al desarrollo es, en términos prácticos, una
inversión que se amortiza en la fase de escritura final.

### 7.2.3 Valor del trabajo en perspectiva personal

El trabajo no parte de un encargo académico desconectado de un interés real.
La elección del modelo de search fund como dominio de aplicación procede de
una atención sostenida del autor a esta clase de activo como vía de inversión
y, eventualmente, como trayectoria profesional. Esa motivación ha condicionado
buena parte de las decisiones de diseño: la negativa a trabajar con datos
sintéticos, la insistencia en cubrir la totalidad del flujo desde la
exportación hasta el ranking, y la atención a los detalles que un analista
real percibiría al usar la herramienta.

El sistema construido es, en su estado actual, algo que el autor podría
utilizar en un proceso real de sourcing. Esa condición –que la herramienta
funcione lo bastante bien como para ser empleada por su creador en su
contexto natural– es, a juicio del autor, el criterio más exigente al que
puede someterse un trabajo de fin de grado de naturaleza aplicada, y constituye
la conclusión personal que cierra el desarrollo del proyecto.

## 7.3 Impacto económico y social

Las conclusiones de los apartados anteriores describen el sistema y el proceso
que lo ha producido. Este apartado intenta situar el resultado en su contexto
económico y social, sin atribuir al trabajo un alcance superior al que
razonablemente le corresponde. Miralyze es un prototipo funcional desarrollado
en el marco de un trabajo de fin de grado; las consideraciones que siguen
identifican vías plausibles de impacto, no efectos medidos.

### 7.3.1 Reducción de fricción en el análisis de PYMEs ibéricas

Los search funds operan sobre un segmento del tejido empresarial –PYMEs con
EBITDA aproximado entre uno y diez millones de euros, con frecuencia con
necesidad de relevo generacional– al que las herramientas de inversión más
visibles del mercado prestan una atención limitada. Los terminales financieros
profesionales y las plataformas comerciales de M&A se orientan a operaciones
de mayor tamaño, donde el coste de la licencia se amortiza con facilidad.
Para los equipos pequeños que operan en el segmento PYME ibérico, la
construcción del universo de candidatas suele recaer sobre exportaciones SABI
procesadas manualmente.

Una herramienta que automatiza la parte mecánica de ese proceso reduce de
forma directa el coste por candidata analizada. El efecto agregado, si la
herramienta llega a adoptarse fuera del marco académico inicial, sería un
incremento del número de empresas que cada equipo es capaz de evaluar en un
ciclo dado. Dado que el volumen de operaciones cerradas por search funds en
España y Portugal es todavía reducido en comparación con mercados maduros,
cualquier mejora en la eficiencia del sourcing se traduce con relativa
proporcionalidad en un mayor flujo de operaciones potenciales.

### 7.3.2 Accesibilidad tecnológica del análisis financiero

El stack sobre el que se ha construido Miralyze –Python, Streamlit, PostgreSQL
gestionado por Supabase, Plotly– es un stack gratuito y ampliamente adoptado.
La operación del sistema no exige licencias de software comercial ni
infraestructura de despliegue dedicada; el coste recurrente para un equipo
que lo adopte se limita, en la práctica, al de la suscripción a la fuente de
datos que ya utiliza con anterioridad al sistema.

Esta característica importa más allá del mero ahorro de coste. Las
herramientas de análisis financiero asociadas a licencias comerciales caras
introducen una barrera de entrada que favorece a los equipos consolidados
frente a los de nueva creación. El hecho de que un analista con acceso
universitario a SABI y conocimientos básicos de Python pueda desplegar y
operar el sistema sin intermediación de una consultora externa baja esa
barrera y, en términos generales, contribuye a que el análisis financiero
sistemático deje de ser un atributo exclusivo de los equipos con mayor
capacidad de gasto.

### 7.3.3 Aportación al ecosistema empresarial subyacente

El destinatario último de la inversión vehiculada por un search fund es la
empresa adquirida y, por extensión, el tejido económico al que pertenece. Las
PYMEs sobre las que opera este modelo de inversión son, en buena medida,
empresas familiares con plantillas establecidas, vínculos territoriales
estables y dificultades específicas de relevo generacional. La continuidad
operativa que aporta una operación de search fund bien ejecutada preserva
empleo y conserva tejido productivo en regiones donde la alternativa –cierre
o venta a un competidor industrial que reorganiza la actividad– implicaría
pérdidas mayores.

Una herramienta que mejora la calidad del proceso de selección incide, por
esa cadena de efectos, sobre la probabilidad de que las operaciones que
finalmente se cierren tengan resultados sostenibles para la empresa adquirida.
La afirmación es modesta y deliberadamente cualitativa: el sistema no es por
sí mismo un instrumento de política económica, pero su aportación al sourcing
se inscribe en una cadena cuyo extremo final son empresas reales y empleos
reales del tejido productivo ibérico.

### 7.3.4 Cierre

El sistema entregado no resuelve, ni pretende resolver, ninguno de los
problemas de fondo del modelo de search fund como vía de inversión en PYMEs
ibéricas. Su contribución se sitúa en un plano operativo más limitado:
sistematizar y reducir el coste de una etapa del proceso que hoy se aborda
de forma artesanal. La importancia de esa contribución depende, en última
instancia, de la adopción que el sistema obtenga más allá del marco académico
en el que ha nacido. La herramienta existe, está documentada y está disponible
para esa eventualidad.

---

---

# Bibliografía

> **Nota:** las referencias marcadas con [TODO-REF] requieren localizar la URL o
> DOI exacto antes de la entrega final. El formato sigue IEEE (número, autores,
> título entre comillas, fuente en cursiva, año).

[1] I. C. MacMillan, "Search Funds: An Historical Perspective," *Stanford Graduate
School of Business*, Case E-469, 2021. [TODO-REF: verificar edición más reciente
del Stanford Search Fund Primer]

[2] P. Kelly y I. C. MacMillan, *2022 Search Fund Study*, Stanford Graduate School
of Business, 2022. [TODO-REF: https://www.gsb.stanford.edu/faculty-research/centers-initiatives/ces/research/search-funds]

[3] Bureau van Dijk, "SABI — Iberian Balance Sheet Analysis System," Moody's
Analytics, 2024. Disponible en: https://www.bvdinfo.com/en-gb/our-products/data/national/sabi

[4] A. Panko, "What We Know About Spreadsheet Errors," *Journal of End User
Computing*, vol. 10, n.º 2, pp. 15-21, 1998.

[5] Bloomberg L.P., "Bloomberg Professional Service pricing," 2024.
[TODO-REF: referencia alternativa: artículo periodístico que cite el coste del
terminal Bloomberg, ~$27.000/año en 2024]

[6] Microsoft Corporation, "Power BI documentation," 2024.
Disponible en: https://learn.microsoft.com/en-us/power-bi/

[7] Streamlit Inc., "Streamlit — The fastest way to build data apps," 2024.
Disponible en: https://streamlit.io

[8] Supabase Inc., "Supabase — The open source Firebase alternative," 2024.
Disponible en: https://supabase.com

[9] Plotly Technologies Inc., "Plotly Python Graphing Library," 2024.
Disponible en: https://plotly.com/python/

[10] pandas Development Team, "pandas: powerful Python data analysis toolkit,"
v2.2.3, 2024. Disponible en: https://pandas.pydata.org

[11] L. Wes McKinney, "Data Structures for Statistical Computing in Python," en
*Proc. 9th Python in Science Conf.*, 2010, pp. 56-61.

[12] Instituto Nacional de Estadística, "Clasificación Nacional de Actividades
Económicas CNAE-2009," INE, 2009.
Disponible en: https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177033&menu=ultiDatos&idp=1254735976614

[13] European Search Fund Accelerator (ESFA), *2023 European Search Fund Study*,
IE Business School, 2023. [TODO-REF: verificar URL en https://esfa.eu]

[14] I. Sommerville, *Software Engineering*, 10.ª ed. Pearson, 2016.

[15] E. J. Chikofsky y J. H. Cross, "Reverse engineering and design recovery: a
taxonomy," *IEEE Software*, vol. 7, n.º 1, pp. 13-17, 1990.

[16] Psycopg Team, "Psycopg 3 — PostgreSQL adapter for Python," v3.2.3, 2024.
Disponible en: https://www.psycopg.org/psycopg3/

[17] PostgreSQL Global Development Group, "PostgreSQL 16 Documentation," 2024.
Disponible en: https://www.postgresql.org/docs/16/

[18] Python Software Foundation, "Python 3.11 Documentation," 2024.
Disponible en: https://docs.python.org/3.11/

[19] Registro Mercantil Central, "Publicidad registral mercantil," 2024.
Disponible en: https://www.rmc.es

[20] OpenStreetMap Foundation, "GeoJSON de España por provincias," 2024.
[TODO-REF: indicar la fuente exacta del GeoJSON usado en el mapa geográfico]

---

---

# Anexo A. Esquema SQL de la base de datos

## A.1 Propósito y ejecución

Este anexo recoge el script DDL completo que define el esquema relacional de
Miralyze sobre PostgreSQL. El script reside en el repositorio en el fichero
`database/schema.sql` y se ejecuta una sola vez desde el editor SQL del panel
de Supabase para inicializar la base de datos. Todas las sentencias se han
escrito de forma idempotente (`create table if not exists`,
`create index if not exists`, `create or replace function`,
`drop trigger if exists` antes de `create trigger`), de modo que su ejecución
repetida no produce errores y permite reproducir el entorno desde cero o
sincronizar el esquema entre instancias.

El esquema se compone de cinco tablas, todas ellas con clave primaria
sintética `bigserial` y marcas temporales `created_at` y `updated_at`. Las
tres tablas que mantienen estado de dominio (`companies`, `financials`,
`metrics`) disponen de un *trigger* que mantiene actualizada la marca
`updated_at` en cada modificación. Las dos tablas auxiliares de trazabilidad
de importación (`import_log`, `import_errors`) no requieren actualizaciones
posteriores a la inserción y carecen de *trigger*.

## A.2 Tabla `companies`

Almacena la información identificativa y de clasificación sectorial de cada
empresa del universo. La unicidad efectiva se garantiza mediante un índice
único condicional sobre `bvd_id` (identificador de Bureau van Dijk),
aplicable únicamente cuando el campo está presente y no vacío. Se mantienen
índices secundarios sobre los campos por los que el Screener filtra con
mayor frecuencia.

```sql
create table if not exists companies (
    id bigserial primary key,
    company_name text not null,
    cif text,
    bvd_id text,
    date_of_establishment date,
    website text,
    country text,
    province text,
    guo_name text,
    cnae_code text not null,
    native_trade_description text,
    english_trade_description text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create unique index if not exists idx_companies_bvd_id
    on companies (bvd_id) where bvd_id is not null and bvd_id <> '';
create index if not exists idx_companies_name on companies (company_name);
create index if not exists idx_companies_cif on companies (cif);
create index if not exists idx_companies_cnae on companies (cnae_code);
create index if not exists idx_companies_country on companies (country);
create index if not exists idx_companies_province on companies (province);
```

## A.3 Tabla `financials`

Almacena las magnitudes financieras y operativas brutas de cada empresa para
cada ejercicio fiscal. La integridad referencial con `companies` se garantiza
con `on delete cascade`, de modo que la eliminación de una empresa arrastra
sus datos financieros. La restricción `unique (company_id, year)` materializa
la regla de dominio según la cual una empresa no puede tener más de un
registro financiero por ejercicio.

```sql
create table if not exists financials (
    id bigserial primary key,
    company_id bigint not null references companies(id) on delete cascade,
    year integer not null,
    cash_and_equivalents numeric,
    total_assets numeric,
    working_capital numeric,
    employees integer,
    revenue numeric,
    cost_of_goods_sold numeric,
    ebitda numeric,
    long_term_debts numeric,
    short_term_debts numeric,
    equity numeric,
    net_income numeric,
    cash_flow numeric,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    unique (company_id, year)
);

create index if not exists idx_financials_company on financials(company_id);
create index if not exists idx_financials_year on financials(year);
```

## A.4 Tabla `metrics`

Almacena los quince indicadores derivados que el módulo
`metrics/calculator.py` calcula a partir de los datos financieros. La
estructura replica la de `financials` en cuanto a clave compuesta
empresa-año, restricción de unicidad e índices, lo que permite que las
consultas que cruzan ambas tablas se beneficien del mismo plan de acceso.

```sql
create table if not exists metrics (
    id bigserial primary key,
    company_id bigint not null references companies(id) on delete cascade,
    year integer not null,
    gross_debt numeric,
    net_debt numeric,
    ebitda_margin numeric,
    net_income_margin numeric,
    cash_flow_margin numeric,
    revenue_growth_yoy numeric,
    ebitda_growth_yoy numeric,
    revenue_cagr_3y numeric,
    revenue_cagr_5y numeric,
    net_debt_ebitda numeric,
    revenue_per_employee numeric,
    ebitda_per_employee numeric,
    cash_flow_per_employee numeric,
    cash_conversion numeric,
    equity_ratio numeric,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    unique (company_id, year)
);

create index if not exists idx_metrics_company on metrics(company_id);
create index if not exists idx_metrics_year on metrics(year);
```

## A.5 Tabla `import_log`

Registra cada operación de importación realizada sobre el sistema, con su
sello temporal, el nombre y tipo del fichero, el modo de carga (`append` o
`replace`), los conteos agregados de filas leídas, aceptadas y rechazadas, y
un campo libre de notas. Esta tabla es la base de la trazabilidad operativa
descrita en el Capítulo 4 y consultada desde la vista de gestión de
importaciones de la aplicación.

```sql
create table if not exists import_log (
    id bigserial primary key,
    import_timestamp timestamptz default now(),
    file_name text,
    file_type text,
    load_mode text,
    rows_read integer,
    rows_accepted integer,
    rows_rejected integer,
    notes text
);
```

## A.6 Tabla `import_errors`

Almacena el detalle de cada fila rechazada por el validador, asociada a la
importación en la que se produjo el rechazo. La relación con `import_log`
con `on delete cascade` asegura que la eliminación de una importación
arrastra los errores asociados, de modo que la limpieza del historial es
consistente. El campo `error_description` recoge el motivo en lenguaje
natural emitido por `etl/validator.py`, lo que permite depurar la causa sin
necesidad de inspeccionar la fila original.

```sql
create table if not exists import_errors (
    id bigserial primary key,
    import_id bigint not null references import_log(id) on delete cascade,
    row_number integer,
    error_type text,
    error_description text
);
```

## A.7 Función y *triggers* de mantenimiento de `updated_at`

Para evitar la repetición de la lógica de actualización de marcas temporales
en el código de la aplicación, el esquema declara una función PL/pgSQL
genérica y la asocia mediante *triggers* a las tres tablas que mantienen
estado de dominio. Cada vez que se actualiza una fila de `companies`,
`financials` o `metrics`, el campo `updated_at` se sobrescribe con el
instante actual de forma transparente para la capa de aplicación.

```sql
create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_companies_updated_at on companies;
create trigger trg_companies_updated_at
before update on companies
for each row execute function set_updated_at();

drop trigger if exists trg_financials_updated_at on financials;
create trigger trg_financials_updated_at
before update on financials
for each row execute function set_updated_at();

drop trigger if exists trg_metrics_updated_at on metrics;
create trigger trg_metrics_updated_at
before update on metrics
for each row execute function set_updated_at();
```

## A.8 Convenciones generales del esquema

El conjunto del esquema sigue tres convenciones uniformes que conviene
documentar como referencia para futuras extensiones:

- **Tipo `numeric` sin precisión.** Las magnitudes monetarias y los ratios
  derivados se declaran como `numeric` sin precisión explícita. Esta
  decisión preserva la exactitud aritmética de PostgreSQL en el lado de la
  base de datos y delega en el módulo `database/db_manager.py` la
  conversión a `float` de Python en el punto en el que los valores cruzan
  la frontera hacia el motor de cálculo.
- **Sello temporal `timestamptz`.** Todas las marcas temporales se
  almacenan con zona horaria, lo que garantiza la coherencia entre el
  servidor de Supabase y los clientes que se conecten desde otras zonas.
- **Identificadores `bigserial`.** Las claves primarias se generan con
  `bigserial` (entero de 64 bits autoincremental) en previsión de
  crecimientos futuros del universo de empresas más allá del límite de
  `integer`.

---

# Anexo B. Mapeo de columnas SABI al modelo relacional

## B.1 Propósito del anexo

Este anexo documenta la correspondencia exacta entre las columnas de las
exportaciones nativas de SABI y los campos del modelo relacional descrito en
el Anexo A. La correspondencia se materializa en el módulo `etl/loader.py`
mediante dos diccionarios de mapeo (`SABI_HEADER_MAP` y `SABI_FINANCIAL_MAP`)
y un esquema de offsets temporales (`PERIOD_OFFSETS`). El anexo recoge esos
elementos junto con las reglas de normalización de cabeceras, las reglas de
tratamiento de valores ausentes y el algoritmo de reconstrucción de los
ejercicios fiscales a partir del año de referencia. Constituye, por tanto,
la referencia documental que permite tanto reproducir el comportamiento del
loader como adaptarlo a futuras variaciones del formato de origen.

## B.2 Estructura del fichero SABI de origen

Las exportaciones SABI utilizadas durante el desarrollo se distribuyen en un
único fichero Excel (`.xlsx`) con una sola hoja. Cada fila representa una
empresa y cada columna representa, según el caso, un atributo identificativo
de la empresa o una magnitud financiera asociada a un ejercicio fiscal
relativo. Las cabeceras de las columnas financieras siguen una estructura
multilínea formada por tres componentes separados por saltos de línea
(`\n`):

```text
<Magnitud>\n<Unidad>\n<Periodo relativo>
```

A modo de ejemplo, una columna que contiene la cifra de negocio del último
ejercicio disponible llega con la cabecera `Operating revenue / turnover\nth
EUR\nLast avail. yr`. El loader normaliza este texto, descarta la línea
intermedia de unidad y conserva la primera línea como nombre de la magnitud
y la última línea como periodo relativo.

El año fiscal absoluto al que corresponde el sufijo `Last avail. yr` no
aparece en la cabecera; se extrae de la columna `Last available year`, que
contiene la fecha de cierre del último ejercicio reportado por la empresa.
Los ejercicios anteriores se reconstruyen restando el offset asociado a cada
sufijo (`Year - 1`, `Year - 2`, hasta `Year - 6`).

## B.3 Normalización de cabeceras

Antes de aplicar los mapeos, el loader normaliza cada cabecera con la
función `_normalize_header`, que (a) convierte el texto a minúsculas, (b)
sustituye secuencias consecutivas de espacios o tabuladores por un único
espacio y (c) elimina los espacios iniciales y finales. Esta normalización
hace robusto el reconocimiento ante diferencias menores entre exportaciones
–distintas mayúsculas, espacios duplicados, sangrados accidentales– sin
necesidad de ampliar los diccionarios de mapeo.

```python
def _normalize_header(column) -> str:
    if column is None:
        return ""
    return re.sub(r"[ \t]+", " ", str(column).strip().lower())
```

## B.4 Mapeo de columnas identificativas

La tabla siguiente recoge la correspondencia entre las columnas
identificativas de la exportación SABI (en su forma normalizada) y los
campos de la tabla `companies`, junto con el tipo SQL correspondiente y las
observaciones aplicables.

| Columna SABI (normalizada) | Campo en `companies` | Tipo SQL | Observaciones |
|----------------------------|----------------------|----------|---------------|
| `company name` | `company_name` | `text not null` | Razón social de la empresa |
| `nif code` | `cif` | `text` | Código de identificación fiscal |
| `bvd id` | `bvd_id` | `text` | Identificador interno de Bureau van Dijk; índice único condicional |
| `date of establishment` | `date_of_establishment` | `date` | Acepta fechas anteriores a 1900 con tratamiento defensivo (véase B.7) |
| `web site` | `website` | `text` | URL corporativa, sin validación de formato |
| `country` | `country` | `text` | "Spain" o "Portugal" en el universo cargado |
| `province` | `province` | `text` | Provincia española o distrito portugués; usado por el Mapa geográfico |
| `guo - name` | `guo_name` | `text` | *Global Ultimate Owner* declarado por SABI |
| `cae rev.3 primary code` | `cnae_code` | `text not null` | Código CNAE-2009 a cuatro dígitos |
| `last available year` | (auxiliar, no persistido) | — | Se utiliza para resolver los offsets de los ejercicios financieros |
| `native trade description` | `native_trade_description` | `text` | Descripción de actividad en idioma local |
| `english trade description` | `english_trade_description` | `text` | Descripción de actividad en inglés |

La columna `last available year` no se persiste como tal: su valor se
consume durante la transformación para calcular el año fiscal absoluto
asociado a cada bloque de columnas financieras.

Diccionario equivalente en código:

```python
SABI_HEADER_MAP = {
    "company name": "company_name",
    "nif code": "cif",
    "bvd id": "bvd_id",
    "date of establishment": "date_of_establishment",
    "web site": "website",
    "country": "country",
    "province": "province",
    "guo - name": "guo_name",
    "cae rev.3 primary code": "cnae_code",
    "last available year": "last_available_year",
    "native trade description": "native_trade_description",
    "english trade description": "english_trade_description",
}
```

## B.5 Mapeo de magnitudes financieras

Las doce magnitudes financieras se identifican por la primera línea de la
cabecera multilínea, una vez normalizada. La tabla recoge la correspondencia
entre cada magnitud SABI y el campo correspondiente de la tabla
`financials`.

| Magnitud SABI (primera línea normalizada) | Campo en `financials` | Tipo SQL | Observaciones |
|-------------------------------------------|-----------------------|----------|---------------|
| `cash & cash equivalent` | `cash_and_equivalents` | `numeric` | Tesorería disponible |
| `total assets` | `total_assets` | `numeric` | Activo total |
| `working capital` | `working_capital` | `numeric` | Capital circulante; admite negativos |
| `number of employees` | `employees` | `integer` | Plantilla media; entero |
| `operating revenue / turnover` | `revenue` | `numeric` | Cifra de negocio; rechazada si negativa |
| `cost of goods sold` | `cost_of_goods_sold` | `numeric` | Coste de las ventas |
| `ebitda` | `ebitda` | `numeric` | Resultado bruto de explotación |
| `long term debts` | `long_term_debts` | `numeric` | Deuda a largo plazo |
| `short term debts` | `short_term_debts` | `numeric` | Deuda a corto plazo |
| `shareholders' equity` | `equity` | `numeric` | Patrimonio neto |
| `p/l for period` | `net_income` | `numeric` | Resultado del ejercicio; admite negativos |
| `cash flow` | `cash_flow` | `numeric` | Flujo de caja; admite negativos |

Diccionario equivalente en código:

```python
SABI_FINANCIAL_MAP = {
    "cash & cash equivalent": "cash_and_equivalents",
    "total assets": "total_assets",
    "working capital": "working_capital",
    "number of employees": "employees",
    "operating revenue / turnover": "revenue",
    "cost of goods sold": "cost_of_goods_sold",
    "ebitda": "ebitda",
    "long term debts": "long_term_debts",
    "short term debts": "short_term_debts",
    "shareholders' equity": "equity",
    "p/l for period": "net_income",
    "cash flow": "cash_flow",
}
```

Las magnitudes que tradicionalmente se asocian al análisis financiero pero
que SABI no expone de forma directa en sus exportaciones estándar –como el
EBIT o los gastos financieros– no figuran en este mapeo y, por
consiguiente, tampoco en la tabla `financials`. Su incorporación, en el
caso de que SABI las facilitara en formatos extendidos, supondría únicamente
añadir las entradas correspondientes a `SABI_FINANCIAL_MAP` y las columnas
correspondientes al esquema descrito en el Anexo A.

## B.6 Resolución del periodo fiscal y reconstrucción de ejercicios

Los siete sufijos relativos que SABI emplea para anclar cada magnitud a un
ejercicio se traducen a un offset entero respecto del año de referencia
mediante el diccionario `PERIOD_OFFSETS`:

| Sufijo SABI (normalizado) | Offset respecto a `last_available_year` |
|---------------------------|------------------------------------------|
| `last avail. yr` | 0 |
| `year - 1` | 1 |
| `year - 2` | 2 |
| `year - 3` | 3 |
| `year - 4` | 4 |
| `year - 5` | 5 |
| `year - 6` | 6 |

Equivalente en código:

```python
PERIOD_OFFSETS = {
    "last avail. yr": 0,
    "year - 1": 1,
    "year - 2": 2,
    "year - 3": 3,
    "year - 4": 4,
    "year - 5": 5,
    "year - 6": 6,
}
```

El año fiscal absoluto de cada bloque se obtiene restando el offset al año
extraído de la columna `last available year`. Un ejemplo numérico ilustra el
procedimiento: si la columna `last available year` contiene `2024-12-31`, la
columna `Operating revenue / turnover\nth EUR\nLast avail. yr` se resuelve
como `revenue` del año 2024, y la columna `Operating revenue / turnover\nth
EUR\nYear - 3` se resuelve como `revenue` del año 2021.

El loader genera una fila por cada par empresa-año que tenga al menos una
magnitud financiera no nula. Si un ejercicio queda completamente vacío
–situación habitual cuando SABI no dispone de cuentas depositadas para ese
año– no se emite la fila correspondiente, lo que evita introducir filas
huérfanas en la tabla `financials`.

## B.7 Tratamiento de valores ausentes y casos límite

El loader incorpora reglas explícitas para neutralizar las idiosincrasias
del formato SABI antes de que los datos lleguen al validador.

- **Valores literales de "no disponible".** El conjunto
  `MISSING_VALUES = {"", "n.a.", "na", "n/a", "nan", "none", "-"}` recoge
  las representaciones textuales que SABI utiliza –o que se observan en
  exportaciones depuradas manualmente– para indicar la ausencia de un dato.
  La función `_clean_value` convierte cualquier coincidencia en `None`, lo
  que se traduce en `NULL` al persistir en PostgreSQL.
- **Fechas extremas.** La columna `Date of Establishment` puede contener
  fechas anteriores a 1900 (se observó durante el desarrollo el caso real
  de una empresa con fecha de constitución `21/10/1870`). El parseo se
  realiza de forma defensiva sobre los tipos `datetime`/`date` que pandas
  devuelve, sin imponer límites artificiales que excluirían empresas
  válidas.
- **Año de referencia ilegible.** Si el valor de `last available year` no
  puede convertirse a entero, la empresa se omite por completo, ya que no
  es posible asignar año fiscal a sus magnitudes. La función
  `_extract_year` aplica una conversión tolerante que acepta tanto fechas
  como cadenas que comienzan por cuatro dígitos numéricos.
- **Columnas completamente vacías.** Antes de aplicar cualquier mapeo, el
  loader elimina las columnas que están vacías en la totalidad del fichero
  (`df.dropna(axis=1, how="all")`). Esta operación reduce el coste del
  reconocimiento posterior y evita falsos negativos en la detección del
  formato SABI.

## B.8 Algoritmo de transformación wide-to-long

El procedimiento completo de transformación, una vez aplicadas las reglas
anteriores, se resume en los siguientes pasos. El código fuente
correspondiente reside en las funciones `_load_sabi_wide`,
`_build_sabi_column_map` y `_parse_financial_header` del módulo
`etl/loader.py`.

1. Lectura del fichero Excel con `pd.read_excel`, conservando los tipos
   originales (`dtype=object`) para preservar las representaciones
   textuales de los valores ausentes.
2. Normalización de cada cabecera mediante `_normalize_header`.
3. Detección del formato SABI por la presencia de la cabecera normalizada
   `last available year`. Si no se encuentra, el fichero se interpreta como
   formato interno largo y se pasa por una ruta alternativa.
4. Construcción del mapa de columnas `column_map`, que asocia cada campo
   identificativo y cada par `(campo financiero, offset)` a su índice de
   columna en el fichero original.
5. Para cada fila del fichero, extracción del año de referencia y, a
   continuación, generación de hasta siete bloques empresa-año (uno por
   offset). Los bloques completamente vacíos se descartan.
6. Construcción del `DataFrame` resultante con el orden canónico de
   columnas `HEADER_FIELDS + ["year"] + FINANCIAL_FIELDS`, listo para ser
   consumido por el módulo de validación.

El resultado del loader es un `DataFrame` en formato largo con una
estructura idéntica a la que esperarían las pruebas TC01 y TC03 del Anexo
C, lo que cierra el circuito entre el formato de origen, las reglas
documentadas en este anexo y la suite automatizada que las protege frente a
regresiones.

---

# Anexo C. Catálogo de pruebas de validación

## C.1 Alcance del catálogo

Este anexo recoge la totalidad de las pruebas ejecutadas sobre Miralyze como
evidencia del estado funcional descrito en el Capítulo 6. La validación se
estructura en dos bloques de naturaleza complementaria. El bloque de **pruebas
funcionales y de datos**, identificadas con los códigos P01 a P14, verifica
sobre la aplicación instanciada con la base de datos real que cada componente
del sistema –arranque, conexión, persistencia, importación, cálculo, interfaz
y despliegue– se comporta de la forma esperada por el usuario final. El bloque
de **pruebas automatizadas con pytest**, identificadas con los códigos TC01 a
TC06, verifica sobre los módulos críticos de la pipeline ETL y del motor de
métricas que las reglas de transformación, validación y cálculo se mantienen
estables ante cambios futuros en el código.

Cada ficha de prueba documenta el objetivo, la entrada, el resultado esperado,
el resultado observado y el estado final. Cuando la prueba dispone de evidencia
gráfica, se referencia la figura correspondiente con el código `C.N` definido
en C.4. Las pruebas con estado *Pendiente* corresponden a verificaciones cuya
ejecución requiere la incorporación de capturas o la activación del despliegue
público y se identifican explícitamente en la tabla resumen.

## C.2 Pruebas funcionales y de datos (P01–P14)

Las pruebas P01 a P14 se organizan en tres niveles de validación:

1. **Validación técnica** (P01–P02): arranque local de la aplicación y conexión
   con la base de datos en la nube.
2. **Validación de datos** (P03–P08): persistencia, cálculo de métricas,
   importación de Excel SABI, rechazo de CSV, tratamiento de valores `n.a.` y
   tratamiento de fechas extremas.
3. **Validación funcional** (P09–P14): navegación entre vistas, filtros del
   Screener, ficha de empresa, análisis sectorial, mapa geográfico y despliegue
   en Streamlit Community Cloud.

### C.2.1 Tabla resumen P01–P14

| ID | Prueba | Resultado esperado | Resultado observado | Estado |
|----|--------|--------------------|---------------------|--------|
| P01 | Arranque local | La aplicación abre en `localhost` sin errores | Dashboard cargado correctamente | OK |
| P02 | Conexión con Supabase | La aplicación lee datos desde la base cloud | 9.132 empresas detectadas (Fig. C.3) | OK |
| P03 | Persistencia de datos financieros | Existen registros empresa-año en `financials` | 60.112 registros (Fig. C.3) | OK |
| P04 | Cálculo de métricas | Existe una fila por empresa-año en `metrics` | 60.112 métricas (Fig. C.3) | OK |
| P05 | Importación de Excel SABI | El fichero se valida e importa correctamente | Importación correcta sobre exportación real (Fig. C.1) | OK |
| P06 | Rechazo de CSV | La interfaz solo acepta `.xlsx` y `.xls` | CSV bloqueado en el selector de fichero | OK |
| P07 | Tratamiento de valores `n.a.` | Los valores `n.a.` se almacenan como `NULL` | Conversión correcta verificada en BD (Fig. C.2) | OK |
| P08 | Tratamiento de fechas antiguas | Fechas anteriores a 1900 no rompen PostgreSQL | Parseo seguro implementado en `loader.py` | OK |
| P09 | Filtros del Screener | El ranking responde correctamente a los filtros | Filtros operativos sobre el universo (Fig. C.4) | OK |
| P10 | Navegación Screener → Ficha | El click sobre una empresa abre su ficha | Navegación correcta vía `st.session_state` (Fig. C.5) | OK |
| P11 | Ficha de empresa | Se muestran histórico, métricas y gráficos | Vista renderizada con serie temporal completa | OK |
| P12 | Análisis sectorial | KPIs y gráficos comparan CNAE vs mercado | Gráficos sectoriales operativos | OK |
| P13 | Mapa geográfico | El mapa pinta la distribución provincial | 52 provincias renderizadas (Fig. C.6) | OK |
| P14 | Despliegue en Streamlit Community Cloud | La aplicación es accesible desde URL pública | Pendiente de activación operativa (Fig. C.7) | Pendiente |

### C.2.2 Fichas detalladas P01–P14

**P01 — Arranque local de la aplicación.**
- *Objetivo:* verificar que la aplicación instalada localmente arranca sin
  errores de importación, dependencias ni configuración inicial.
- *Entrada:* ejecución del comando `streamlit run app.py` desde el directorio
  raíz del proyecto, con el entorno virtual activo y las dependencias del
  fichero `requirements.txt` instaladas.
- *Resultado esperado:* el servidor Streamlit arranca en `localhost:8501` y la
  vista del dashboard se carga sin trazas de error en consola.
- *Resultado observado:* arranque correcto. La consola muestra el mensaje de
  inicio de Streamlit y el dashboard se renderiza con los contadores agregados
  de empresas, registros y métricas.
- *Estado:* OK.

**P02 — Conexión con Supabase.**
- *Objetivo:* verificar que la aplicación recupera datos de la base PostgreSQL
  alojada en Supabase y no de un fichero local.
- *Entrada:* consulta de conteo `SELECT COUNT(*) FROM companies` desde el
  módulo `database/queries.py` durante la carga del dashboard.
- *Resultado esperado:* el contador devuelve un valor distinto de cero, lo que
  confirma que la conexión cloud está activa y lee la base correcta.
- *Resultado observado:* la consulta devuelve 9.132 empresas (véase Fig. C.3).
- *Estado:* OK.

**P03 — Persistencia de datos financieros.**
- *Objetivo:* verificar que el pipeline ETL ha persistido en la tabla
  `financials` los registros empresa-año correspondientes a los ficheros
  importados.
- *Entrada:* consulta `SELECT COUNT(*) FROM financials` ejecutada sobre la base
  de datos en la nube.
- *Resultado esperado:* el conteo devuelve un valor coherente con el volumen
  de empresas y la profundidad histórica de seis años por empresa.
- *Resultado observado:* la consulta devuelve 60.112 registros financieros
  (véase Fig. C.3).
- *Estado:* OK.

**P04 — Cálculo de métricas.**
- *Objetivo:* verificar que el motor de cálculo `metrics/calculator.py` ha
  generado una fila de métricas para cada registro financiero.
- *Entrada:* consulta `SELECT COUNT(*) FROM metrics`.
- *Resultado esperado:* el número de filas en `metrics` coincide con el número
  de filas en `financials`, lo que demuestra cobertura completa del cálculo.
- *Resultado observado:* la consulta devuelve 60.112 métricas, idéntico al
  número de registros financieros (véase Fig. C.3).
- *Estado:* OK.

**P05 — Importación de un Excel SABI real.**
- *Objetivo:* verificar el flujo completo de importación desde la interfaz, con
  un fichero Excel SABI auténtico de tamaño representativo.
- *Entrada:* exportación SABI en formato `.xlsx` con varias decenas de empresas
  cargada desde la vista de carga de datos en modo `append`.
- *Resultado esperado:* la pipeline procesa el fichero, las tres tablas
  principales (`companies`, `financials`, `metrics`) reciben filas nuevas y la
  importación queda registrada en `import_log` con estado de éxito.
- *Resultado observado:* importación correcta. La interfaz muestra el resumen
  de inserciones y rechazos, y los contadores del dashboard reflejan el
  incremento (véase Fig. C.1).
- *Estado:* OK.

**P06 — Rechazo de ficheros CSV.**
- *Objetivo:* verificar que la interfaz solo permite formatos compatibles con
  la pipeline (`.xlsx`, `.xls`).
- *Entrada:* intento de carga de un fichero `.csv` desde el selector de la
  vista de carga de datos.
- *Resultado esperado:* el componente `st.file_uploader` no acepta el fichero
  o, si se fuerza por nombre, la pipeline devuelve un error controlado con el
  mensaje "Formato de archivo no soportado".
- *Resultado observado:* el selector está restringido a extensiones Excel y
  rechaza el CSV en la propia interfaz, sin llegar a invocar la pipeline.
- *Estado:* OK.

**P07 — Tratamiento de valores no disponibles (`n.a.`).**
- *Objetivo:* verificar que los valores textuales `n.a.` que SABI emplea para
  ejercicios sin datos no se almacenan como cadena de texto en la base, sino
  que se convierten en `NULL`.
- *Entrada:* fichero Excel SABI con celdas `n.a.` en magnitudes financieras.
- *Resultado esperado:* las celdas correspondientes en `financials` quedan a
  `NULL` y los cálculos de métricas dependientes devuelven `NULL` sin generar
  excepción.
- *Resultado observado:* conversión correcta. La consulta directa sobre la
  base de datos confirma la presencia de `NULL` y la ausencia de cadenas
  literales `n.a.` (véase Fig. C.2).
- *Estado:* OK.

**P08 — Tratamiento de fechas anteriores a 1900.**
- *Objetivo:* verificar que fechas de constitución muy antiguas (como
  `21/10/1870` observada en una empresa real durante el desarrollo) no
  provocan errores de tipo en PostgreSQL ni en la interfaz.
- *Entrada:* fichero Excel SABI con una fecha anterior a 1900 en el campo
  `Date of Establishment`.
- *Resultado esperado:* la fecha se parsea correctamente o se trata de forma
  segura como cadena; en ningún caso aborta la importación.
- *Resultado observado:* parseo correcto. El módulo `loader.py` incorpora
  manejo explícito de fechas extremas, documentado en el código.
- *Estado:* OK.

**P09 — Aplicación de filtros del Screener.**
- *Objetivo:* verificar que los filtros financieros y sectoriales del Screener
  reducen el universo correctamente y que el ranking WSM se recalcula sobre el
  subconjunto resultante.
- *Entrada:* combinación de filtros sobre revenue, deuda, código CNAE y
  ejercicio fiscal.
- *Resultado esperado:* la tabla de resultados se actualiza en tiempo real, el
  ranking se reordena según la puntuación compuesta y el conteo agregado de
  candidatas refleja el efecto de los filtros.
- *Resultado observado:* filtros operativos. La interfaz responde sin
  bloqueos perceptibles sobre el universo de 9.132 empresas (véase Fig. C.4).
- *Estado:* OK.

**P10 — Navegación desde el Screener a la ficha de empresa.**
- *Objetivo:* verificar que la selección de una fila del Screener navega
  correctamente a la ficha individual de la empresa correspondiente.
- *Entrada:* click sobre una empresa cualquiera del ranking del Screener.
- *Resultado esperado:* la aplicación cambia a la vista de Ficha de empresa
  con la empresa seleccionada precargada y su histórico visible.
- *Resultado observado:* navegación correcta vía `st.session_state` (véase
  Fig. C.5).
- *Estado:* OK.

**P11 — Ficha de empresa.**
- *Objetivo:* verificar que la ficha individual presenta el histórico
  financiero, las métricas calculadas y los gráficos de evolución temporal.
- *Entrada:* selección de una empresa con histórico completo de seis años.
- *Resultado esperado:* la vista renderiza la serie temporal de magnitudes
  financieras, los ratios derivados y los gráficos de evolución sin errores
  visuales.
- *Resultado observado:* vista renderizada correctamente con todos los
  componentes operativos.
- *Estado:* OK.

**P12 — Análisis sectorial.**
- *Objetivo:* verificar la comparación entre las empresas de un código CNAE
  concreto y los agregados del mercado.
- *Entrada:* selección de un código CNAE en la vista de análisis sectorial.
- *Resultado esperado:* los KPIs sectoriales y los gráficos comparativos se
  actualizan al CNAE elegido y muestran información coherente.
- *Resultado observado:* gráficos sectoriales operativos tras la corrección
  documentada en la sección 15 de la documentación técnica.
- *Estado:* OK.

**P13 — Mapa geográfico.**
- *Objetivo:* verificar la distribución provincial de empresas y la respuesta
  del mapa a filtros sectoriales.
- *Entrada:* visualización del mapa en modo agregado (todos los sectores) y
  con un filtro CNAE concreto.
- *Resultado esperado:* el mapa pinta correctamente las 52 provincias
  españolas, el ranking regional acompaña al mapa y el filtro CNAE actualiza
  ambas representaciones.
- *Resultado observado:* las 52 provincias se renderizan correctamente con la
  implementación basada en `go.Scatter` con `fill="toself"`, tras la
  incidencia documentada con `go.Choropleth` (véase Fig. C.6).
- *Estado:* OK.

**P14 — Despliegue en Streamlit Community Cloud.**
- *Objetivo:* verificar que la aplicación es accesible desde una URL pública
  cuando se despliega en la infraestructura gestionada de Streamlit.
- *Entrada:* repositorio GitHub vinculado a Streamlit Community Cloud con los
  *secrets* de Supabase configurados.
- *Resultado esperado:* la aplicación arranca en la URL pública asignada y
  reproduce el comportamiento observado en local.
- *Resultado observado:* pendiente de activación operativa programada antes
  de la defensa (véase Fig. C.7 cuando se documente).
- *Estado:* Pendiente.

## C.3 Pruebas automatizadas con pytest (TC01–TC06)

Las pruebas funcionales descritas en C.2 garantizan el comportamiento del
sistema sobre la base de datos real, pero no detectan automáticamente
regresiones futuras introducidas por modificaciones en el código. Para
mitigar parcialmente esa exposición se ha incorporado una suite de pruebas
unitarias e integración ligera ejecutables con `pytest`. Las pruebas se
concentran en los tres módulos donde un cambio silencioso tendría mayor
impacto: el cargador de exportaciones SABI, el validador de filas y el motor
de cálculo de métricas. La suite no requiere conexión con Streamlit ni con
Supabase, lo que permite ejecutarla en cualquier entorno local o de
integración continua.

La dependencia `pytest==8.3.4` se ha añadido al fichero `requirements.txt`. La
ejecución de la suite se realiza con el comando `python -m pytest tests -q`
desde el directorio raíz del proyecto. La verificación de compilación previa
se realiza con `python -m compileall app.py database etl metrics utils views
tests`.

### C.3.1 Tabla resumen TC01–TC06

| ID | Módulo | Prueba | Resultado esperado | Resultado observado | Estado |
|----|--------|--------|--------------------|---------------------|--------|
| TC01 | `etl/loader.py` | Conversión wide-to-long de Excel SABI | Filas empresa-año correctas, tipos coherentes | Conversión correcta verificada por aserciones | OK |
| TC02 | `etl/loader.py` | Rechazo de ficheros CSV | Excepción `ValueError` con mensaje "Formato de archivo no soportado" | Excepción lanzada como se espera | OK |
| TC03 | `etl/validator.py` | Aceptación de negativos en campos válidos | `working_capital`, `net_income` y `cash_flow` negativos no se rechazan | Validación correcta, ningún rechazo | OK |
| TC04 | `etl/validator.py` | Rechazo de duplicados y `revenue` negativo | Las filas problemáticas se mueven a la tabla de rechazos con motivo explícito | Dos filas rechazadas con motivos correctos | OK |
| TC05 | `metrics/calculator.py` | Cálculo de deuda, márgenes, crecimiento y productividad | Los doce indicadores derivados coinciden con el cálculo manual | Todos los valores coinciden con los esperados | OK |
| TC06 | `metrics/calculator.py` | Reglas de deuda parcial y caja ausente | Aplicación correcta de reglas de imputación cuando faltan campos | Tres escenarios verificados con éxito | OK |

Resultado agregado de la ejecución:

```text
6 passed in 7.54 s
```

### C.3.2 Fichas detalladas TC01–TC06

**TC01 — `loader.py`: conversión wide-to-long.**
- *Objetivo:* verificar que una exportación SABI en formato wide se transforma
  correctamente al esquema interno de filas empresa-año, preservando la
  identidad de la empresa y la asignación temporal de cada magnitud.
- *Entrada:* `DataFrame` sintético con una empresa y columnas representativas
  de SABI (`Company Name`, `NIF Code`, `Last available year`, columnas
  multilínea con sufijos `Last avail. yr` y `Year - 1` para `Operating
  revenue`, `EBITDA` y `Cash flow`), serializado a Excel en memoria.
- *Resultado esperado:* dos filas (años 2024 y 2023) con `company_name`,
  `cif`, `cnae_code`, `revenue` y `ebitda` correctamente asignados; el valor
  `n.a.` de `cash_flow` debe convertirse en `None`.
- *Resultado observado:* todas las aserciones se cumplen.
- *Estado:* OK.

**TC02 — `loader.py`: rechazo de CSV.**
- *Objetivo:* garantizar que la pipeline rechaza explícitamente formatos no
  soportados, en lugar de fallar de forma opaca durante el procesamiento.
- *Entrada:* `BytesIO` con contenido CSV mínimo y nombre de fichero
  `sample.csv`.
- *Resultado esperado:* `load_file` lanza `ValueError` cuyo mensaje contiene
  la cadena "Formato de archivo no soportado".
- *Resultado observado:* la excepción se lanza con el mensaje esperado.
- *Estado:* OK.

**TC03 — `validator.py`: aceptación de negativos válidos.**
- *Objetivo:* verificar que el validador no penaliza valores negativos en
  magnitudes donde un signo negativo es financieramente válido (capital
  circulante, resultado neto, flujo de caja).
- *Entrada:* fila con `working_capital = -50`, `net_income = -20` y
  `cash_flow = -10`, junto con el resto de campos obligatorios cumplidos.
- *Resultado esperado:* la fila figura en el conjunto válido y el conjunto
  de rechazos queda vacío.
- *Resultado observado:* validación correcta, ningún rechazo emitido.
- *Estado:* OK.

**TC04 — `validator.py`: rechazo de duplicados y `revenue` negativo.**
- *Objetivo:* verificar las dos reglas de rechazo que protegen la integridad
  de la base: unicidad por `(company, year)` y signo no negativo en `revenue`.
- *Entrada:* tres filas, dos de las cuales comparten clave empresa-año y una
  tercera con `revenue = -1`.
- *Resultado esperado:* una fila válida y dos rechazadas con motivos
  conteniendo las cadenas "Duplicado" y "revenue no puede ser negativo"
  respectivamente.
- *Resultado observado:* el resultado coincide exactamente con el esperado.
- *Estado:* OK.

**TC05 — `calculator.py`: métricas financieras y de productividad.**
- *Objetivo:* verificar el cálculo de los doce indicadores derivados sobre
  una empresa con datos completos y dos ejercicios consecutivos.
- *Entrada:* dos filas financieras sintéticas para los años 2023 y 2024,
  con valores diseñados para que cada métrica produzca un resultado
  conocido.
- *Resultado esperado:* `gross_debt = 60`, `net_debt = 55`, `ebitda_margin =
  0,25`, `net_income_margin = 0,10`, `cash_flow_margin = 0,125`,
  `revenue_growth_yoy = 0,20`, `ebitda_growth_yoy = 0,50`, `net_debt_ebitda
  ≈ 1,833`, `revenue_per_employee = 12`, `ebitda_per_employee = 3`,
  `cash_flow_per_employee = 1,5`, `cash_conversion = 0,5`, `equity_ratio =
  0,4`.
- *Resultado observado:* todas las aserciones se cumplen con la tolerancia
  numérica de `pytest.approx`.
- *Estado:* OK.

**TC06 — `calculator.py`: reglas de deuda parcial y caja ausente.**
- *Objetivo:* verificar que la lógica del cálculo de deuda bruta y deuda neta
  responde correctamente a las tres situaciones límite definidas en el
  diseño: deuda parcial, deuda totalmente ausente y caja ausente.
- *Entrada:* tres filas financieras con configuraciones distintas:
  (a) sin deuda a largo plazo pero con deuda a corto y caja disponible;
  (b) sin deuda de ningún tipo y con caja disponible;
  (c) con deuda a largo plazo, sin deuda a corto y sin caja.
- *Resultado esperado:*
  (a) `gross_debt = 25`, `net_debt = 20`;
  (b) `gross_debt = None`, `net_debt = None`;
  (c) `gross_debt = 10`, `net_debt = None`.
- *Resultado observado:* las tres situaciones producen los valores
  esperados, lo que confirma que las reglas de imputación se aplican como
  se documentaron en el Capítulo 4.
- *Estado:* OK.

## C.4 Evidencia gráfica recomendada

Las capturas de pantalla referenciadas a lo largo de este anexo deben
incorporarse en la versión final del documento en el orden y posición que se
indica a continuación. La numeración `C.N` se utiliza de forma cruzada en las
fichas de C.2.

| Figura | Contenido | Cómo obtenerla | Inserción en el anexo |
|--------|-----------|----------------|-----------------------|
| C.1 | Resultado de una importación correcta | Ejecutar P05 desde la interfaz con un Excel SABI real; capturar la pantalla de resumen tras la importación, mostrando el contador de filas insertadas y el mensaje de éxito | Ficha P05 |
| C.2 | Verificación del tratamiento de `n.a.` | Tras P07, ejecutar `SELECT cash_flow FROM financials WHERE cash_flow IS NULL LIMIT 5` desde el editor SQL de Supabase y capturar el resultado | Ficha P07 |
| C.3 | Conteo agregado de la base de datos | Capturar el dashboard inicial de Miralyze con los contadores agregados de empresas (9.132), registros financieros (60.112) y métricas (60.112) | Fichas P02, P03 y P04 |
| C.4 | Aplicación de filtros en el Screener | Aplicar una combinación de filtros (por ejemplo, `revenue > 5 M€` y CNAE concreto) en la vista del Screener y capturar la pantalla con la tabla de resultados visible | Ficha P09 |
| C.5 | Navegación desde el Screener a la ficha de empresa | Capturar dos pantallas consecutivas: el Screener con una empresa seleccionada y la ficha de esa misma empresa abierta a continuación | Ficha P10 |
| C.6 | Mapa geográfico filtrado por CNAE | Capturar la vista del Mapa geográfico con un código CNAE seleccionado, mostrando el mapa coloreado y el ranking provincial al margen | Ficha P13 |
| C.7 | Aplicación desplegada en Streamlit Community Cloud | Una vez activado el despliegue público, capturar la URL pública y la aplicación en funcionamiento desde un navegador externo | Ficha P14 |

Las pruebas automatizadas TC01 a TC06 no requieren capturas de pantalla. Su
evidencia es la salida textual de la ejecución de `pytest`, ya recogida en
C.3.1, y el código fuente de los tests, depositado en el directorio
`tests/` del repositorio.

---
