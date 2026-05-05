# Miralyze - Documentacion tecnica y registro de desarrollo

Este documento recoge en orden cronologico todas las decisiones de diseno,
cambios de implementacion y contexto necesarios para redactar la memoria final
del TFG con la maxima calidad. Se divide en dos fases:

- **Fase 1** (secciones A): diseno conceptual, implementacion inicial SQLite y
  documentacion del TFG. Registrado durante el desarrollo asistido con Claude
  (abril-mayo 2026).
- **Fase 2** (secciones numericas): migracion a Supabase/PostgreSQL, despliegue
  en Streamlit Community Cloud y nuevas funcionalidades. Registrado durante el
  desarrollo asistido con Codex.

No se incluyen contrasenas, tokens, claves de Supabase ni credenciales reales.

---

# FASE 1 — Diseno conceptual, implementacion inicial y documentacion del TFG

*(Registrado durante el desarrollo asistido con Claude — abril/mayo 2026)*

---

## A1. Contexto del proyecto: el modelo de search fund

Un **search fund** es un vehiculo de inversion en el que uno o dos emprendedores
(los *searchers*) recaudan capital de un grupo reducido de inversores para
financiar una busqueda estructurada de una unica empresa privada susceptible de
ser adquirida y gestionada directamente por ellos. El modelo fue introducido en
la decada de 1980 en la Universidad de Stanford y ha experimentado un
crecimiento significativo en Europa e Iberia en la ultima decada.

El proceso de un search fund se articula en tres fases:

1. **Busqueda (sourcing):** 18-24 meses de identificacion y preselecion de
   empresas objetivo. El searcher evalua sistematicamente decenas o centenares
   de companyias usando criterios de sector, tamanyo, rentabilidad, crecimiento
   y perfil de deuda.
2. **Adquisicion:** due diligence, valoracion y cierre de la operacion.
3. **Gestion:** operacion y creacion de valor durante 4-8 anyos.

La fase de busqueda es intensiva en analisis financiero y consume una parte
desproporcionada del tiempo del searcher en tareas operativas de bajo valor:
recopilar datos de distintas fuentes, unificar formatos, calcular KPIs
comparables, y generar listados filtrados segun criterios de inversion.

**Fuentes de datos tipicas del search fund iberico:**

- Exportaciones de SABI (Sistema de Analisis de Balances Ibericos, Bureau van
  Dijk / Moody's Analytics): cuentas anuales del Registro Mercantil espanyol y
  portugues. Formato Excel con columnas en ingles, valores en miles EUR, datos
  en formato wide (una fila por empresa, columnas por anyo).
- Informa D&B: alternativa a SABI, misma fuente (Registro Mercantil), distinta
  nomenclatura de columnas.
- Ficheros Excel ad-hoc recibidos directamente de propietarios de empresas.
- Notas internas de conversaciones con asesores y propietarios.

**Problema central:** ninguna herramienta disponible permite integrar en un unico
flujo la ingesta de datos de estas fuentes heterogeneas, calcular KPIs
comparables de forma automatica y filtrar/puntuar las empresas segun criterios
configurables. Las herramientas comerciales (Bloomberg, Capital IQ) estan
orientadas a empresas cotizadas y tienen un coste prohibitivo para un fondo en
fase de busqueda (>20.000 USD/usuario/anyo). Las hojas de calculo no escalan
bien a universos de mas de 50-70 empresas con series historicas multianyales.

---

## A2. Motivacion y origen de Miralyze

Miralyze surge de la experiencia directa trabajando dentro de un search fund en
Iberia. La herramienta se crea para reducir el tiempo dedicado a tareas
operativas de bajo valor durante la fase de sourcing y liberar capacidad para el
analisis cualitativo y la toma de decisiones.

**Nombre:** Miralyze (portmanteau de "mirar" + "analyze").

**Titulo del TFG:**
- Titulo inicial en el Plan de Trabajo (primera entrega, 28/02/2026): "Sistema
  de gestion y visualizacion de datos financieros empresariales para apoyo a
  decisiones de inversion".
- Titulo definitivo: "Herramienta de Deal Screener con Dashboard y Scoring".
- Subtitulo: "Herramienta de Screening Financiero para Search Funds".

**Cambio de titulo justificado por:** el titulo definitivo refleja con mayor
precision el foco en el proceso de deal screening aplicado al contexto especifico
de los search funds, diferenciandolo de un sistema de gestion generico.

**Datos de la propuesta:**
- Alumno: Alejandro Conde Uceda
- Tutor: Alberto Tejero
- Centro: ETSIINF — Universidad Politecnica de Madrid
- Grado: Ingenieria Informatica
- Fecha plan de trabajo: 28/02/2026

---

## A3. Decisiones de diseno conceptual

### A3.1 Stack tecnologico — justificacion

| Componente | Tecnologia elegida | Alternativas descartadas | Razon |
|---|---|---|---|
| Lenguaje | Python 3.11 | — | Estandar de facto en analisis de datos |
| Interfaz web | Streamlit 1.41.1 | Dash, Flask + React | Streamlit permite construir apps de datos interactivas directamente desde scripts Python sin backend separado ni HTML/JS. Su modelo reactivo (cada cambio en widget redibuja la vista) es ideal para screeners con filtros en tiempo real. Prototipado 3-5x mas rapido que Dash. |
| Base de datos inicial | SQLite (stdlib sqlite3) | PostgreSQL local, MongoDB | Cero dependencias de servidor, un unico fichero .db portatil, SQL estandar para agregaciones. Apropiado para uso local monousuario. |
| Base de datos final | Supabase / PostgreSQL | Firebase, PlanetScale | Ver seccion Fase 2 (decision de Codex). |
| Visualizacion | Plotly 5.24.1 | Matplotlib, Altair, Bokeh | Graficos HTML interactivos (zoom, hover, filtrado) con integracion nativa en Streamlit. Soporte para graficos financieros (lineas, barras, scatter, radar, scatter geo). |
| Manipulacion de datos | pandas 2.2.3 + NumPy | polars | Estandar de facto; amplia documentacion y ecosistema. |
| Lectura de Excel | openpyxl 3.1.5 | xlrd | Soporte .xlsx nativo; xlrd solo soporta .xls antiguo. |
| Clasificacion sectorial | CNAE-2009 | SIC, NACE | CNAE-2009 es el sistema de referencia en los registros mercantiles espanyoles y equivale a NACE Rev. 2 europea. Es el codigo que proporciona SABI. |

### A3.2 Justificacion de Streamlit frente a Dash y Flask

Streamlit fue seleccionado frente a Dash (mas verboso, requiere callbacks
explicitos) y Flask (requiere desarrollo frontend separado) por:

1. Velocidad de prototipado: cada widget se declara en una linea.
2. Modelo reactivo: el script se reejcuta de arriba a abajo con cada interaccion,
   sin necesidad de gestionar estado de callbacks.
3. Idoneidad para datos: disenyado especificamente para aplicaciones de analisis.
4. Comunidad activa: >30.000 estrellas en GitHub a 2024.

### A3.3 Arquitectura del sistema — tres capas

```
Capa de presentacion:  Streamlit + Plotly (vistas, navegacion, CSS)
        |
        v
Capa de logica:        ETL (loader, validator, transformer)
                       Motor de scoring (calculator, WSM)
        |
        v
Capa de datos:         SQLite (fase 1) -> Supabase/PostgreSQL (fase 2)
```

La interaccion es unidireccional. La capa de presentacion solo consulta la logica
de negocio; nunca accede directamente a la BD.

### A3.4 Modelo de datos conceptual — cuatro entidades

| Entidad | Descripcion |
|---|---|
| Empresa | Datos maestros: NIF/CIF, nombre, CNAE, provincia, fecha de constitucion, estado |
| CuentasAnuales | Cifras anuales por empresa: revenue, EBITDA, EBIT, resultado neto, activo total, DFN, fondos propios |
| KPI | Metricas calculadas derivadas por empresa-anyo |
| Score | Puntuacion WSM calculada por ejecucion, con los pesos utilizados y posicion en ranking |

En la implementacion con PostgreSQL estas entidades corresponden a las tablas
`companies`, `financials`, `metrics` e `import_log` (ver seccion Fase 2).

---

## A4. Modelo de scoring financiero

### A4.1 Metodologia: Weighted Sum Model (WSM)

El scoring utiliza el **Weighted Sum Model (WSM)**, el metodo mas extendido en
la practica de screening financiero por su interpretabilidad. Es un metodo de
toma de decisiones multicriterio (MCDM).

Formula:

```
Score = SUM(w_i * score_kpi_i) * 100
```

Donde:
- `w_i` = peso asignado a cada KPI (suma total = 1.0)
- `score_kpi_i` = KPI normalizado al intervalo [0, 1]
- El resultado final esta en la escala [0, 100]

Referencia: C. L. Hwang y K. Yoon, *Multiple Attribute Decision Making:
Methods and Applications*, Springer-Verlag, 1981.

### A4.2 Normalizacion min-max

Antes de aplicar el WSM, cada KPI se normaliza al intervalo [0, 1]:

```
score_kpi = (x - x_min) / (x_max - x_min)
```

Para KPIs donde un valor mayor implica peor situacion (p. ej., ratio ND/EBITDA):

```
score_kpi = 1 - (x - x_min) / (x_max - x_min)
```

Los valores atipicos superiores al percentil 99 se recortan antes de normalizar
para evitar que distorsionen el ranking.

La normalizacion es **relativa al universo de empresas analizado**, no a
benchmarks sectoriales externos. Esto significa que una puntuacion de 80 indica
que la empresa esta en el percentil 80 del universo actual.

### A4.3 Once KPIs definidos

| # | KPI | Formula | Dimension | Sentido |
|---|---|---|---|---|
| 1 | Margen EBITDA | EBITDA / Revenue | Rentabilidad | Mayor = mejor |
| 2 | Margen neto | Net income / Revenue | Rentabilidad | Mayor = mejor |
| 3 | ROE | Net income / Equity | Rentabilidad | Mayor = mejor |
| 4 | ROA | Net income / Total assets | Rentabilidad | Mayor = mejor |
| 5 | CAGR revenue 3y | Tasa de crecimiento anual compuesto a 3 anyos | Crecimiento | Mayor = mejor |
| 6 | CAGR revenue 5y | Tasa de crecimiento anual compuesto a 5 anyos | Crecimiento | Mayor = mejor |
| 7 | Ratio ND/EBITDA | Net debt / EBITDA | Apalancamiento | Menor = mejor |
| 8 | Ratio cobertura intereses | EBIT / Gastos financieros | Apalancamiento | Mayor = mejor |
| 9 | Revenue (ultimo ejercicio) | Revenue del ultimo anyo disponible | Tamanyo | Mayor = mejor |
| 10 | Anyos con datos | Numero de anyos con registros financieros | Estabilidad | Mayor = mejor |
| 11 | Variabilidad margen EBITDA | Desviacion tipica del margen EBITDA | Estabilidad | Menor = mejor |

### A4.4 Cuatro dimensiones y pesos por defecto

| Dimension | KPIs incluidos | Peso por defecto |
|---|---|---|
| Rentabilidad | KPIs 1-4 | 40% |
| Crecimiento | KPIs 5-6 | 30% |
| Apalancamiento | KPIs 7-8 | 20% |
| Tamanyo y estabilidad | KPIs 9-11 | 10% |

Los pesos son **configurables por el usuario** desde la interfaz del screener
antes de recalcular el ranking, sin necesidad de modificar el codigo. Los pesos
por defecto reflejan las prioridades tipicas de un search fund centrado en
empresas rentables con bajo apalancamiento.

---

## A5. Clasificacion sectorial CNAE-2009

La herramienta usa el codigo **CNAE-2009** (Clasificacion Nacional de
Actividades Economicas, equivalente a NACE Rev. 2 europea) como sistema de
referencia para la clasificacion sectorial.

- CNAE de 4 digitos: nivel de analisis sectorial en la vista sectorial y filtros.
- CNAE de 2 digitos (division): agrupacion para comparativas sectoriales.
- CNAE de 1 letra (seccion): agrupacion de alto nivel (A-U).

SABI proporciona el campo `CAE Rev.3 Primary Code`, que equivale al CNAE-2009.

Fuente oficial: Instituto Nacional de Estadistica (INE), *Clasificacion Nacional
de Actividades Economicas 2009 (CNAE-2009)*, INE, Madrid, 2009.

---

## A6. Requisitos funcionales y no funcionales (version inicial)

### Requisitos funcionales

| ID | Requisito |
|---|---|
| RF-01 | Importacion de ficheros SABI en formato Excel (.xlsx, .xls) |
| RF-02 | Validacion automatica de campos obligatorios y deteccion de valores anomalos |
| RF-03 | Almacenamiento persistente de empresas y series financieras historicas |
| RF-04 | Calculo automatico de 11 KPIs financieros por empresa y anyo |
| RF-05 | Scoring comparativo WSM con pesos configurables por el usuario |
| RF-06 | Filtrado dinamico por sector CNAE, tamanyo, provincia y rango de KPIs |
| RF-07 | Dashboard con seis vistas diferenciadas |
| RF-08 | Exportacion de resultados a CSV |

### Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | Usabilidad: la interfaz debe permitir a un usuario sin conocimientos tecnicos realizar un screening completo sin formacion especifica |
| RNF-02 | Rendimiento: el dashboard debe responder a cambios de filtro en menos de 2 segundos para universos de hasta 500 empresas |
| RNF-03 | Portabilidad: debe ejecutarse en Windows y macOS sin dependencias de servicios externos (version inicial local) |
| RNF-04 | Mantenibilidad: codigo modularizado en componentes independientes (ETL, scoring, presentacion) con responsabilidades claras |
| RNF-05 | Privacidad: todos los datos se almacenan localmente (version inicial); sin envio a servidores externos |

---

## A7. Vistas planificadas y estado en la version inicial SQLite

| Vista | Descripcion | Estado |
|---|---|---|
| Dashboard | Tarjetas resumen (empresas, registros, importaciones, paises), Top-10 CNAE, ultimas importaciones | Completada |
| Cargar datos | Formulario de carga Excel SABI, selector modo append/replace, barra de progreso, tabla de errores | Completada |
| Listado de empresas | Tabla paginada, busqueda por nombre/CIF, filtros por pais y CNAE | Completada |
| Ficha de empresa | Series historicas, graficos temporales, gauge scoring, benchmarks sectoriales | Completada |
| Screener | Filtros avanzados multidimensionales, scoring configurable, tabla exportable, scatter crecimiento vs rentabilidad | Completada |
| Analisis sectorial | KPIs agregados, boxplot, ranking, comparativa multisectorial, mapa de burbujas | Completada |
| Mapa geografico | Distribucion por provincia/distrito, GeoJSON local Iberia, filtro por CNAE | Anadida en Fase 2 |

---

## A8. Identidad visual Miralyze

La aplicacion tiene una identidad visual corporativa consistente:

| Elemento | Valor |
|---|---|
| Modo | Oscuro |
| Fondo principal | #0E1825 (midnight) |
| Fondo tarjetas | #182639 (navy) |
| Color principal | #C8A96E (dorado) — titulos y elementos destacados |
| Color secundario | #1D6FA4 (zafiro) — graficos |
| Texto | Ivory / Frost |
| Acentos positivos | Emerald (#2ECC71) |
| Acentos negativos | Crimson (#E74C3C) |

El CSS personalizado se centraliza en `utils/theme.py`. Se aplica a todos los
componentes nativos de Streamlit y a los graficos Plotly para coherencia visual
total.

El logo Miralyze se guarda en:
- `assets/Disenos de logo de Miralyze (1).png` — fichero original del design sheet.
- `assets/logo_miralyze_sidebar.png` — version recortada para el sidebar (cargada directamente por la app).

---

## A9. Cambios respecto al Plan de Trabajo de la primera entrega

La primera entrega (Plan de Trabajo, 28/02/2026) contemplaba:
- 10 tareas (T1-T10)
- 3 pantallas en la interfaz (T7): carga + log, buscador de empresa, screener
- Gantt de 12 semanas desde marzo de 2026
- Titulo: "Sistema de gestion y visualizacion de datos financieros..."

Modificaciones realizadas y justificacion:

| # | Modificacion | Justificacion |
|---|---|---|
| 1 | Cambio de titulo | Refleja mejor el foco en deal screening para search funds |
| 2 | T7 (3 pantallas) -> T8-T16 (6 vistas) | Se identificaron necesidades no cubiertas: dashboard general, ficha separada del buscador, analisis sectorial |
| 3 | Diseno visual corporativo (T14-T15) | No estaba en el plan; se anyadio para mejorar usabilidad y percepcion del usuario |
| 4 | Vista de analisis sectorial (T16) | Emerge como consecuencia de los requisitos de comparacion sectorial identificados durante el desarrollo |
| 5 | Inicio anticipado (oct 2025 vs mar 2026) | El trabajo comenzo antes de la formalizacion del plan, lo que permitio completar T1-T16 en la segunda entrega |
| 6 | T10 -> T19-T25 (redaccion por capitulo) | Desglose para seguimiento granular y feedback del tutor por secciones |
| 7 | Migracion SQLite -> Supabase (Fase 2) | Ver seccion Fase 2 |

El numero definitivo de tareas en el nuevo plan es T1-T26 (26 tareas).

---

## A10. Estructura de la memoria final del TFG

### A10.1 Indice completo (7 capitulos + Apendices)

El indice propuesto por el tutor en la primera entrega (Introduccion, Estado del
arte, Objetivos, Metodologia, Desarrollo, Resultados, Conclusiones) se ha
adaptado a la plantilla oficial ETSIINF, que incluye un capitulo obligatorio de
Analisis de Impacto:

```
Resumen (espanyol)
Abstract (ingles)
Tabla de contenidos

Capitulo 1. Introduccion
  1.1 Motivacion
  1.2 Objetivos generales
  1.3 Contribucion del trabajo
  1.4 Estructura del documento

Capitulo 2. Estado del arte
  2.1 El modelo de search fund y el proceso de sourcing
  2.2 Herramientas comerciales de datos de empresas privadas
      2.2.1 SABI e Informa D&B
      2.2.2 Plataformas de mercados cotizados (Bloomberg, Capital IQ)
      2.2.3 Hojas de calculo como alternativa habitual
      2.2.4 Plataformas de Business Intelligence
  2.3 Tecnologias utilizadas
  2.4 Metodologias de scoring financiero
  2.5 Clasificacion sectorial CNAE-2009
  2.6 Identificacion de brechas (gap analysis)

Capitulo 3. Analisis y diseno del sistema
  3.1 Descripcion del problema y requisitos
      3.1.1 Requisitos funcionales
      3.1.2 Requisitos no funcionales
  3.2 Actores del sistema
  3.3 Arquitectura del sistema
  3.4 Modelo de datos

Capitulo 4. Desarrollo
  4.1 Pipeline ETL de datos financieros
      4.1.1 Fuentes de datos y formatos de entrada
      4.1.2 Normalizacion y validacion de datos
      4.1.3 Almacenamiento en base de datos
  4.2 Motor de scoring financiero
      4.2.1 Definicion de KPIs
      4.2.2 Normalizacion min-max
      4.2.3 Modelo WSM y configuracion de pesos
  4.3 Dashboard e interfaz de usuario
      4.3.1 Vista de listado y screener con filtros
      4.3.2 Vista de detalle de empresa
      4.3.3 Vista de analisis sectorial por CNAE
      4.3.4 Vista de mapa geografico
      4.3.5 Vista comparativa entre empresas

Capitulo 5. Evaluacion y validacion
  5.1 Estrategia de pruebas
  5.2 Dataset de validacion (datos reales SABI)
  5.3 Validacion del modelo de scoring
  5.4 Pruebas funcionales del dashboard

Capitulo 6. Resultados y conclusiones
  6.1 Resultados obtenidos
  6.2 Conclusiones
  6.3 Trabajo futuro

Capitulo 7. Analisis de Impacto
  7.1 Impacto personal, social y economico
  7.2 Objetivos de Desarrollo Sostenible (ODS 8, 9, 10)

Bibliografia (formato IEEE)

Anexos
  Anexo A: Esquema completo de la base de datos
  Anexo B: Definicion y formulas de los 11 KPIs
  Anexo C: Guia de uso de Miralyze
```

### A10.2 Correspondencia indice — documentacion disponible

| Seccion de la memoria | Fuente principal en esta documentacion |
|---|---|
| Cap. 1 Introduccion | Secciones A1, A2 |
| Cap. 2 Estado del arte | Secciones A3.1, A4.1, A5 + esta seccion |
| Cap. 3 Analisis y diseno | Secciones A3.3, A3.4, A6 |
| Cap. 4.1 Pipeline ETL | Secciones Fase 2: 7, 8, 9 |
| Cap. 4.2 Motor scoring | Secciones A4 |
| Cap. 4.3 Dashboard | Secciones A7, Fase 2: 11 |
| Cap. 5 Evaluacion | Secciones Fase 2: 14, 15 |
| Cap. 6 Resultados | Secciones Fase 2: 16 |
| Cap. 7 Impacto | Pendiente de redaccion |
| Anexo A Esquema BD | Secciones Fase 2: 5 |
| Anexo B KPIs | Seccion A4.3 |

### A10.3 Bibliografia IEEE (referencias principales)

```
[1] R. S. Ruback y R. Yudkoff, HBR Guide to Buying a Small Business.
    Boston: HBR Press, 2017.
[2] IESE Business School, Search Fund Study Europe 2022.
    Barcelona: IESE EIC, 2022.
[3] P. Kelly y H. H. Stevenson, "Search Funds: An Entrepreneurial Path to
    Business Acquisition," HBS Case 9-391-086, 1991.
[4] Bureau van Dijk, SABI - Sistema de Analisis de Balances Ibericos.
    [Online]. Disponible: bvdinfo.com. [Acceso: 2025].
[5] Bloomberg L.P., Bloomberg Terminal. [Online]. Disponible:
    bloomberg.com/professional. [Acceso: 2025].
[6] W. McKinney, "Data Structures for Statistical Computing in Python,"
    Proc. 9th Python in Science Conf., Austin, TX, 2010, pp. 51-56.
[7] C. R. Harris et al., "Array programming with NumPy," Nature, vol. 585,
    pp. 357-362, 2020.
[8] Streamlit Inc., Streamlit — A faster way to build and share data apps.
    [Online]. Disponible: streamlit.io. [Acceso: 2025].
[9] Plotly Technologies Inc., Collaborative data science. [Online].
    Disponible: plot.ly. [Acceso: 2025].
[10] INE, Clasificacion Nacional de Actividades Economicas 2009 (CNAE-2009).
     INE, Madrid, 2009.
[11] C. L. Hwang y K. Yoon, Multiple Attribute Decision Making: Methods
     and Applications. Berlin: Springer, 1981.
[12] Supabase Inc., Supabase — The Open Source Firebase Alternative.
     [Online]. Disponible: supabase.com. [Acceso: 2026].
[13] psycopg contributors, psycopg 3 — PostgreSQL adapter for Python.
     [Online]. Disponible: psycopg.org. [Acceso: 2026].
```

---

## A11. Herramientas de generacion de documentos del TFG

### A11.1 Documento de segunda entrega (gen_tfg.js)

Se genero el documento de la segunda entrega mediante un script Node.js que usa
la libreria `docx` (npm) para generar ficheros .docx programaticamente.

- Script: `C:\Users\acond\AppData\Local\Temp\gen_tfg.js`
- Output: `Segunda_Entrega_TFG_Miralyze_v4.docx`
- Libreria: `docx` (instalacion global npm)
- Ejecucion: `NODE_PATH=...npm/node_modules node gen_tfg.js`

Estructura del documento generado:
- **Portada:** titulo, autor, tutor, centro, fecha.
- **Parte A:** resumen del trabajo realizado, modificaciones al plan,
  revision de objetivos, revision de tareas (tabla T1-T26), diagrama de
  Gantt (oct 2025 - jun 2026).
- **Parte B:** borrador del indice completo (7 capitulos + apendices),
  Capitulo 1 completo (Introduccion), Capitulo 2 completo (Estado del arte),
  bibliografia IEEE (20 referencias).

### A11.2 Plantilla oficial ETSIINF (TFG_Miralyze_ETSIINF_v3.docx)

Se rellenoyla plantilla oficial de la ETSIINF manipulando directamente el XML
del fichero .docx mediante el workflow: descomprimir ZIP -> editar
`word/document.xml` -> recomprimir.

- Fichero resultado: `TFG_Miralyze_ETSIINF_v3.docx`
- Script de edicion: `C:\Users\acond\AppData\Local\Temp\update_tfg_doc.py`
- Script de empaquetado: `pack.py` (de las skills de Claude Code)

Estilos de la plantilla ETSIINF usados:
- `Ttulo1` — encabezados de capitulo (H1)
- `Ttulo2` — secciones (H2)
- `Ttulo3` — subsecciones (H3)
- `Ttulo4` — subsubsecciones (H4)
- `Prrafodelista` — elementos de lista numerada

Margenes: top/bottom 1417 DXA, left/right 1701 DXA.

Contenido insertado en la plantilla:
- Portada: titulo, autor (Alejandro Conde), tutor (Alberto Tejero), grado
  (Ingenieria Informatica), departamento, fecha (abril 2026).
- Resumen en espanyol y abstract en ingles.
- Capitulo 1 (Introduccion) completo.
- Capitulo 2 (Estado del arte) completo con todas las subsecciones.
- Esqueletos con contenido de Capitulos 3, 4 y 5 (analisis, desarrollo,
  evaluacion).
- Subsecciones de Capitulos 6 y 7.
- 16 referencias IEEE en el apartado de Bibliografia.

---

## A12. Estado del proyecto al final de la Fase 1 (antes de Codex)

Al terminar la Fase 1 (asistida por Claude), el estado del proyecto era:

**Completado:**
- T1-T3: Diseno BD y modelo de datos (SQLite, 4 tablas)
- T4-T6: Pipeline ETL completo (loader, validator, transformer)
- T7: Motor de calculo de 11 KPIs
- T8-T12: Cinco vistas funcionales (Dashboard, Carga, Listado, Ficha, Screener)
- T13: Modulo de scoring configurable (WSM + min-max)
- T14-T15: Diseno visual corporativo Miralyze (CSS, paleta, logo)
- T16: Vista de analisis sectorial por CNAE
- T19-T20: Redaccion Capitulos 1 y 2 de la memoria (con citas IEEE)

**Pendiente al inicio de Fase 2:**
- T17-T18: Pruebas con datos reales y evaluacion con el tutor
- T21-T24: Redaccion Capitulos 3-7
- T25-T26: Revision y presentacion
- Migracion SQLite -> BD cloud
- Despliegue en produccion

**Datos de la aplicacion al final de Fase 1:**
- Backend: SQLite local (`database/screener.db`)
- Formato de entrada: CSV y Excel
- Vistas: 6 (sin mapa geografico)
- KPIs: 11
- Dimensiones de scoring: 4

---
---

# FASE 2 — Migracion a Supabase, despliegue y nuevas funcionalidades

*(Registrado durante el desarrollo asistido con Codex)*

---

## 1. Resumen del proyecto

Miralyze es una aplicacion de screening financiero desarrollada en Python con
Streamlit. Su objetivo es permitir la carga, normalizacion, analisis y
visualizacion de empresas procedentes de exportaciones SABI, facilitando la
identificacion de companias interesantes para procesos de analisis financiero o
deal flow.

La aplicacion mantiene una interfaz visual de tipo dashboard, con navegacion
lateral, graficos Plotly, tablas interactivas, ficha de empresa, screener,
analisis sectorial y mapa geografico.

Durante esta fase se ha realizado una migracion importante: se ha pasado de una
base de datos local SQLite a una base de datos persistente en Supabase/PostgreSQL.
La aplicacion continua siendo una app Streamlit, pero ahora los datos se guardan
de forma centralizada y persistente, lo que permite desplegarla en Streamlit
Community Cloud sin depender de un fichero local `screener.db`.

## 2. Decisiones principales tomadas

### 2.1 Plataforma de despliegue

Se analizaron dos alternativas:

- Vercel, que habria requerido transformar la aplicacion a una arquitectura web
  diferente, probablemente Next.js o similar.
- Streamlit Community Cloud, que permite desplegar directamente la aplicacion
  existente manteniendo la interfaz y la logica ya desarrollada.

La decision fue mantener Streamlit porque el proyecto ya estaba construido con
ese framework y porque la prioridad era conservar la experiencia visual actual:
sidebar, dashboard, vistas financieras, graficos Plotly, screener y ficha de
empresa.

### 2.2 Persistencia de datos

La base de datos local SQLite se sustituyo por Supabase/PostgreSQL. La razon es
que SQLite local no es una buena opcion para despliegue en cloud cuando se
necesita persistencia entre sesiones, cargas de datos recurrentes y acceso desde
una aplicacion desplegada.

La conexion a Supabase se implemento con SQL directo usando `psycopg`, no con
`supabase-py`. Esto permite mantener un patron de trabajo similar al que ya
existia con SQLite: consultas SQL explicitas y helpers propios para ejecutar
queries.

### 2.3 Seguridad

La aplicacion se plantea inicialmente como privada. La URL de conexion a la base
de datos se lee desde:

- `st.secrets` en Streamlit Cloud.
- Variable de entorno `SUPABASE_DB_URL`.
- `.streamlit/secrets.toml` en desarrollo local.

El fichero `.streamlit/secrets.toml` no debe subirse al repositorio. Debe estar
incluido en `.gitignore`.

### 2.4 Unidad monetaria

Los importes procedentes de SABI se guardan en miles de euros, tal como llegan en
el Excel. No se multiplican por 1.000 durante la importacion.

En la interfaz se han ajustado textos y etiquetas para reflejar que los importes
estan en `miles EUR` o `th EUR`.

## 3. Decisiones de campos financieros SABI

Durante la revision de campos SABI se tomaron varias decisiones importantes:

### 3.1 Deuda neta

La deuda neta no viene directamente en SABI, por lo que se calcula internamente.
La definicion adoptada es:

```text
gross_debt = long_term_debts + short_term_debts
net_debt = gross_debt - cash_and_equivalents
```

Reglas aplicadas:

- Si `long_term_debts` y `short_term_debts` son ambas `NULL`, entonces
  `gross_debt` tambien es `NULL`.
- Si solo existe una de las dos partidas de deuda, se usa la existente.
- Si caja (`cash_and_equivalents`) es `NULL`, no se calcula `net_debt`.
- La caja se guarda de forma separada y tambien se usa en otros analisis.

### 3.2 Equity

Entre los campos disponibles en SABI se eligio `Shareholders' equity` como campo
principal para representar el patrimonio neto/equity utilizado en los analisis.

Se descartaron para este uso principal otros campos como:

- `Equity-accounted companies`, porque se refiere a participaciones contabilizadas
  por el metodo de puesta en equivalencia.
- `Total equity and liabilities`, porque representa el total del balance por el
  lado de financiacion, no el equity aislado.

### 3.3 Net income

El campo `P/L for period` se interpreto como resultado neto del periodo y se
guarda internamente como `net_income`.

### 3.4 Cash flow

Se anadio `cash_flow` como nuevo campo financiero porque permite enriquecer el
analisis de calidad de beneficios y conversion de EBITDA en caja.

## 4. Arquitectura actual

Estructura principal del proyecto:

```text
tfg_screener/
|-- app.py
|-- requirements.txt
|-- DOCUMENTACION.md
|-- assets/
|   |-- logo_miralyze_sidebar.png
|   |-- Disenos de logo de Miralyze (1).png
|   `-- geo/
|       `-- iberia_regions.geojson
|-- database/
|   |-- db_manager.py
|   `-- schema.sql
|-- etl/
|   |-- loader.py
|   |-- validator.py
|   `-- transformer.py
|-- metrics/
|   `-- calculator.py
|-- utils/
|   |-- geography.py
|   |-- helpers.py
|   `-- theme.py
`-- views/
    |-- home.py
    |-- upload.py
    |-- company_list.py
    |-- company_detail.py
    |-- screener.py
    |-- sector.py
    `-- geo_map.py
```

### 4.1 `app.py`

Es el punto de entrada de la aplicacion Streamlit. Sus responsabilidades son:

- Configurar la pagina (`st.set_page_config`).
- Aplicar el CSS corporativo de Miralyze.
- Cargar el logo del sidebar.
- Definir la navegacion lateral.
- Importar y renderizar la vista seleccionada.

Vistas actuales:

- Dashboard.
- Cargar datos.
- Listado de empresas.
- Ficha de empresa.
- Screener.
- Mapa geografico.
- Analisis sectorial.

### 4.2 `utils/theme.py`

Centraliza la identidad visual de Miralyze:

- Paleta corporativa.
- Colores para graficos Plotly.
- CSS global para Streamlit.
- Helpers de layout para graficos.

Colores principales:

```text
midnight
navy
sapphire
gold
ivory
frost
steel
emerald
crimson
bg_deep
bg_card
bg_input
```

### 4.3 `utils/helpers.py`

Contiene funciones compartidas:

- Formateo de importes.
- Formateo de porcentajes.
- Obtencion de anos disponibles.
- Obtencion de paises disponibles.
- Obtencion de CNAEs disponibles.

### 4.4 `utils/geography.py`

Modulo nuevo creado para el mapa geografico. Sus responsabilidades son:

- Normalizar nombres de pais y provincia.
- Cargar el GeoJSON local de regiones ibericas.
- Construir un catalogo de regiones.
- Consultar la distribucion de empresas por provincia/distrito.
- Cruzar los nombres de SABI con las claves normalizadas del GeoJSON.

## 5. Base de datos Supabase/PostgreSQL

La base de datos se estructura en tablas normalizadas.

### 5.1 Tabla `companies`

Una fila representa una empresa.

Campos principales:

```text
id
company_name
cif
bvd_id
date_of_establishment
website
country
province
guo_name
cnae_code
native_trade_description
english_trade_description
created_at
updated_at
```

Origen SABI:

```text
company_name               <- Company Name
cif                        <- NIF Code
bvd_id                     <- BvD ID
date_of_establishment      <- Date of Establishment
website                    <- Web site
country                    <- Country
province                   <- Province
guo_name                   <- GUO - Name
cnae_code                  <- CAE Rev.3 Primary Code
native_trade_description   <- Native trade description
english_trade_description  <- English trade description
```

### 5.2 Tabla `financials`

Una fila representa los datos financieros de una empresa en un ano concreto.

Campos:

```text
id
company_id
year
cash_and_equivalents
total_assets
working_capital
employees
revenue
cost_of_goods_sold
ebitda
long_term_debts
short_term_debts
equity
net_income
cash_flow
created_at
updated_at
```

Restriccion importante:

```text
UNIQUE(company_id, year)
```

### 5.3 Tabla `metrics`

Una fila representa metricas calculadas para una empresa y un ano.

Campos:

```text
id
company_id
year
gross_debt
net_debt
ebitda_margin
net_income_margin
cash_flow_margin
revenue_growth_yoy
ebitda_growth_yoy
revenue_cagr_3y
revenue_cagr_5y
net_debt_ebitda
revenue_per_employee
ebitda_per_employee
cash_flow_per_employee
cash_conversion
equity_ratio
created_at
updated_at
```

Restriccion importante:

```text
UNIQUE(company_id, year)
```

### 5.4 Tablas de importacion

`import_log` guarda un resumen de cada carga:

- Fecha.
- Nombre de archivo.
- Modo de carga.
- Filas aceptadas.
- Filas rechazadas.

`import_errors` guarda errores de validacion o importacion, permitiendo explicar
por que ciertas filas no se han cargado.

## 6. Capa de conexion a Supabase

El modulo `database/db_manager.py` sustituye la antigua dependencia de SQLite.

Funciones principales:

```python
get_connection()
execute_query()
execute_insert()
execute_update()
execute_many()
init_db()
```

`init_db()` se mantiene por compatibilidad, pero ya no crea tablas. El esquema se
ejecuta una vez desde Supabase SQL Editor mediante `database/schema.sql`.

Diferencias respecto a SQLite:

- Se usa `psycopg`.
- Los placeholders pasan de `?` a `%s`.
- Las filas se devuelven como diccionarios con `dict_row`.
- Los valores `Decimal` devueltos por PostgreSQL se convierten a `float` para no
  romper calculos ni visualizaciones.

## 7. Importacion SABI

### 7.1 Formato de entrada

El Excel SABI definitivo se considero en formato wide:

- Una fila por empresa.
- Columnas para el ultimo ano disponible.
- Columnas para anos anteriores (`Year - 1`, ..., `Year - 6`).

La aplicacion transforma ese formato wide a formato long:

```text
1 empresa con 7 periodos disponibles
-> hasta 7 filas en financials
```

Ejemplo:

```text
Last available year = 2024-12-31
Last avail. yr      -> 2024
Year - 1            -> 2023
Year - 2            -> 2022
...
Year - 6            -> 2018
```

### 7.2 Campos de empresa esperados

```text
Company Name
NIF Code
BvD ID
Date of Establishment
Web site
Country
Province
GUO - Name
CAE Rev.3 Primary Code
Native trade description
English trade description
```

### 7.3 Campos financieros esperados

```text
Cash & cash equivalent
Total assets
Working capital
Number of employees
Operating revenue / turnover
Cost of goods sold
EBITDA
Long term debts
Short term debts
Shareholders' equity
P/L for period
Cash flow
```

### 7.4 Tratamiento de valores no disponibles

Se convierten a `None`/`NULL`:

- Celdas vacias.
- `n.a.`
- Valores equivalentes a no disponible.

### 7.5 Fechas

Se corrigio un problema detectado al importar empresas con fechas antiguas como:

```text
21/10/1870
```

PostgreSQL podia interpretar la fecha con un `datestyle` incompatible y lanzar:

```text
date/time field value out of range
```

La solucion fue parsear las fechas antes de insertarlas, usando interpretacion
dia/mes/ano cuando procede, para enviar a PostgreSQL un valor de fecha seguro.

### 7.6 Excel frente a CSV

Se evaluo permitir importacion CSV, pero se decidio deshabilitarla en la primera
version estable porque:

- Los CSV pueden variar por separador, encoding y configuracion regional.
- Las descripciones de actividad pueden contener comas.
- Aunque un CSV bien escapado seria tecnicamente valido, aumentaba el riesgo de
  errores de carga para el usuario.

Por tanto, la vista de carga acepta solo:

```text
.xlsx
.xls
```

## 8. Validacion de datos

El modulo `etl/validator.py` valida las filas normalizadas antes de insertarlas.

Campos minimos requeridos:

```text
company_name
cif
cnae_code
year
```

Validaciones relevantes:

- El ano debe ser interpretable.
- Los campos numericos deben convertirse correctamente.
- Se permiten valores negativos en:
  - `net_income`
  - `cash_flow`
  - `working_capital`
- No se rechaza una fila por tener deuda parcial `NULL`.

## 9. Transformacion y upsert

El modulo `etl/transformer.py` inserta o actualiza datos en Supabase.

Regla de identificacion de empresa:

1. Preferentemente `bvd_id`.
2. Si no existe, `cif`.
3. Si tampoco existe, nombre normalizado.

Esto evita duplicados cuando se realizan varias cargas sobre empresas ya
existentes.

Los datos anuales se guardan por:

```text
company_id + year
```

Si una combinacion ya existe, se actualiza.

## 10. Calculo de metricas

El modulo `metrics/calculator.py` calcula las metricas derivadas a partir de
`financials`.

### 10.1 Deuda

```text
gross_debt = long_term_debts + short_term_debts
net_debt = gross_debt - cash_and_equivalents
net_debt_ebitda = net_debt / ebitda
```

### 10.2 Margenes

```text
ebitda_margin = ebitda / revenue
net_income_margin = net_income / revenue
cash_flow_margin = cash_flow / revenue
```

### 10.3 Crecimiento

```text
revenue_growth_yoy
ebitda_growth_yoy
revenue_cagr_3y
revenue_cagr_5y
```

### 10.4 Productividad por empleado

```text
revenue_per_employee = revenue / employees
ebitda_per_employee = ebitda / employees
cash_flow_per_employee = cash_flow / employees
```

### 10.5 Caja y conversion

```text
cash_conversion = cash_flow / ebitda
```

### 10.6 Solidez

```text
equity_ratio = equity / total_assets
```

## 11. Interfaz Streamlit

La interfaz mantiene el diseno visual corporativo Miralyze en modo oscuro.

### 11.1 Sidebar

El sidebar incluye:

- Logo Miralyze.
- Navegacion de vistas.
- Caption del TFG.

Se corrigio un problema por el que el logo podia no verse correctamente. La
solucion fue crear una imagen ya recortada:

```text
assets/logo_miralyze_sidebar.png
```

La app ya no depende de recortar dinamicamente el fichero grande del design
sheet.

### 11.2 Dashboard

El dashboard muestra:

- Numero total de empresas.
- Numero de registros financieros.
- Numero de importaciones.
- Numero de paises.
- Top 10 sectores CNAE por numero de empresas.
- Ultimas importaciones.

Se sustituyo un grafico poco legible del Top 10 CNAE por un ranking visual HTML
con barras proporcionales.

Problemas corregidos:

- El primer elemento del ranking se estaba renderizando como codigo HTML en vez
  de como componente visual. Se soluciono usando `streamlit.components.v1.html`.
- El ranking mostraba solo parte de las filas por falta de altura. Se aumento la
  altura del componente para mostrar las 10 filas.

### 11.3 Cargar datos

La vista de carga permite subir archivos Excel SABI.

Mejoras realizadas:

- Se elimino la opcion CSV.
- Se anadio barra de progreso durante la importacion.
- La barra diferencia entre:
  - carga/importacion,
  - recalculo de metricas.

### 11.4 Listado de empresas

Vista de consulta general de empresas importadas. Permite revisar las companias
disponibles en base de datos.

### 11.5 Ficha de empresa

La ficha de empresa mantiene los graficos y analisis historicos y se adapto al
nuevo modelo de datos de Supabase.

Campos enriquecidos disponibles:

```text
Web
Provincia
BvD ID
GUO
Fecha de constitucion
Descripcion corta
Descripcion larga
```

Se incorporaron campos financieros nuevos, especialmente deuda bruta, deuda
neta, cash flow y cash conversion.

### 11.6 Screener

El screener mantiene la logica principal de filtrado y ranking.

Ajustes realizados:

- Adaptacion de consultas a PostgreSQL.
- Uso de la nueva deuda neta calculada.
- Etiquetas monetarias en miles EUR.
- Incorporacion de columnas nuevas donde no sobrecarga la tabla.

El scoring original se mantiene sin introducir cash flow en la primera version,
para no alterar demasiado la logica de negocio inicial.

### 11.7 Analisis sectorial

La vista sectorial mantiene:

- KPIs sectoriales.
- Boxplots.
- Rankings.
- Comparativas.
- Mapa de burbujas financiero.

Se adapto a Supabase/PostgreSQL y a las nuevas columnas financieras.

### 11.8 Mapa geografico

Se creo una vista nueva:

```text
Mapa geografico
```

Objetivo:

Visualizar la distribucion geografica de empresas por provincia o distrito.

Controles:

- Selector de sector:
  - `Todos los sectores`
  - `CNAE XXXX`
- Selector de vista:
  - `Peninsula`
  - `Completo`

Metricas superiores:

- Empresas.
- Regiones.
- Top region.
- Sector.

Tabla inferior:

```text
Region | Pais | Empresas | % del total
```

### 11.9 GeoJSON local

Se genero el fichero:

```text
assets/geo/iberia_regions.geojson
```

Incluye:

- 52 provincias de Espana.
- 18 distritos de Portugal.

Fuentes usadas:

- Espana: `es-atlas`, basado en datos del Instituto Geografico Nacional.
  https://github.com/martgnz/es-atlas
- Portugal: dataset `districts-portugal` de E-REDES.
  https://e-redes.opendatasoft.com/explore/dataset/districts-portugal/map/

El GeoJSON se guarda localmente para que la aplicacion no dependa de internet en
produccion.

### 11.10 Normalizacion geografica

Se normalizan nombres de SABI para cruzarlos con el GeoJSON.

Ejemplos:

```text
a Coruña                       -> A Coruña
Alava                          -> Araba/Alava
Avila                          -> Avila
Guipuzcoa                      -> Gipuzkoa
Vizcaya                        -> Bizkaia
Jaen                           -> Jaen
Baleares                       -> Illes Balears
Las Palmas de Gran Canaria     -> Las Palmas
Santa Cruz de Tenerife         -> Santa Cruz de Tenerife
```

Resultado validado con la base actual:

```text
52 provincias detectadas
52 provincias mapeadas
0 provincias sin ubicar
```

### 11.11 Render del mapa

Inicialmente se intento usar `go.Choropleth` con GeoJSON. Sin embargo, en la app
se observaba que Plotly mostraba la barra de color pero no pintaba correctamente
los poligonos.

Solucion aplicada:

- Renderizar cada poligono del GeoJSON como una traza `go.Scatter`.
- Usar `fill="toself"` para rellenar provincias/distritos.
- Mantener una barra de color continua mediante una traza invisible.

Esto hizo el mapa estable dentro de Streamlit.

### 11.12 Paleta del mapa

La escala final se simplifico a un degradado de dos extremos:

```text
azul oscuro -> dorado
```

El azul oscuro representa menos empresas o ausencia de datos. El dorado
representa mayor concentracion de empresas.

### 11.13 Hover del mapa

Se corrigio un problema por el que, al pasar el raton por una provincia, Plotly
mostraba `trace` en lugar del nombre de la provincia.

Solucion:

- Cada traza recibe `name=region_name`.
- Se genera un `hover_text` propio.
- Se usa `hovertemplate="%{text}<extra></extra>"`.

Ejemplo de hover:

```text
Madrid
Pais: Espana
Empresas: 2.069
Sector: Todos los sectores
```

## 12. Dependencias

Dependencias principales:

```text
streamlit==1.41.1
pandas==2.2.3
plotly==5.24.1
openpyxl==3.1.5
psycopg[binary]==3.2.3
Pillow>=10.0.0
```

`openpyxl` se usa para leer Excel. `psycopg[binary]` se usa para conectar con
Supabase/PostgreSQL.

## 13. Despliegue en Streamlit Community Cloud

Para desplegar en Streamlit Community Cloud:

1. Subir el repositorio con el codigo.
2. Configurar los secrets de Streamlit.
3. Ejecutar previamente el esquema SQL en Supabase.
4. Asegurarse de que `requirements.txt` contiene todas las dependencias.
5. Mantener los assets necesarios en el repositorio:
   - Logo.
   - GeoJSON local.
   - Configuracion visual.

Secret necesario:

```toml
SUPABASE_DB_URL = "postgresql://postgres.[PROJECT_REF]:[PASSWORD]@[POOLER_HOST]:5432/postgres?sslmode=require"
```

La contrasena real debe configurarse solo en Streamlit secrets o entorno local,
nunca en la documentacion ni en el repositorio.

## 14. Pruebas realizadas

### 14.1 Pruebas de importacion

Se importo un Excel de prueba con 2 empresas y 7 anos por empresa:

```text
2 empresas
14 filas en financials
14 filas en metrics
```

Se valido:

- Conversion de formato wide a long.
- Interpretacion de `Last available year`.
- Conversion de `n.a.` a `NULL`.
- Conservacion de importes en miles EUR.

### 14.2 Prueba con datos reales

Estado observado tras cargas reales:

```text
7.949 empresas
52 provincias
503 CNAEs
0 provincias vacias
0 provincias sin ubicar en mapa
```

Top CNAE observado:

```text
4511 -> 366 empresas
4631 -> 240 empresas
6420 -> 181 empresas
5511 -> 140 empresas
4120 -> 138 empresas
```

### 14.3 Pruebas de metricas

Se verificaron reglas de:

- Deuda bruta.
- Deuda neta.
- Net debt / EBITDA.
- Margenes.
- Cash conversion.
- CAGR.

Tambien se corrigio un problema de tipos `Decimal` procedentes de PostgreSQL,
convirtiendo a `float` para evitar errores en calculos financieros.

### 14.4 Pruebas de interfaz

Se comprobo:

- Arranque de Streamlit.
- Dashboard.
- Vista de carga.
- Vista de mapa geografico.
- Render del logo.
- Render del mapa.
- Hover del mapa.
- Ranking Top 10 CNAE.

### 14.5 Pruebas tecnicas

Se ejecuto compilacion de modulos con:

```text
python -m compileall
```

Tambien se realizaron pruebas de conexion HTTP local contra Streamlit en:

```text
http://127.0.0.1:8501
```

## 15. Problemas detectados y soluciones

### 15.1 Fecha fuera de rango en PostgreSQL

Problema:

```text
date/time field value out of range: "21/10/1870"
```

Causa:

PostgreSQL podia interpretar la fecha con un formato distinto al esperado.

Solucion:

Parsear fechas antes de insertarlas y enviar a PostgreSQL un valor seguro.

### 15.2 CSV con descripciones que contienen comas

Problema:

Los campos descriptivos pueden contener comas, lo que aumenta el riesgo de
errores si el CSV no esta correctamente escapado o si Excel cambia el separador.

Solucion:

Deshabilitar CSV y permitir solo Excel.

### 15.3 Ranking HTML renderizado como codigo

Problema:

El primer elemento del ranking CNAE aparecia como HTML visible.

Solucion:

Usar `streamlit.components.v1.html`.

### 15.4 Ranking Top 10 incompleto

Problema:

El dashboard consultaba 10 CNAEs, pero visualmente se veian menos filas.

Solucion:

Aumentar la altura del componente HTML y compactar el espaciado interno.

### 15.5 Logo roto

Problema:

El sidebar mostraba un icono roto o una imagen no cargada.

Solucion:

Crear `assets/logo_miralyze_sidebar.png` ya recortado y cargarlo directamente.

### 15.6 Choropleth no pintaba el mapa

Problema:

Plotly mostraba la colorbar pero no los poligonos.

Solucion:

Renderizar manualmente los poligonos como trazas `go.Scatter`.

### 15.7 Hover del mapa mostraba `trace`

Problema:

Al pasar el raton sobre una provincia, Plotly mostraba `trace`.

Solucion:

Asignar texto y `hovertemplate` propio a cada provincia.

## 16. Estado actual de la aplicacion

La aplicacion actualmente:

- Funciona con Supabase/PostgreSQL.
- Importa Excel SABI en formato wide.
- Normaliza datos anuales a formato long.
- Calcula metricas financieras.
- Permite visualizar empresas, sectores, screener y fichas.
- Incluye mapa geografico por CNAE.
- Usa assets locales para logo y geometria geografica.
- Esta preparada para despliegue en Streamlit Community Cloud.

## 17. Mejoras futuras propuestas

### 17.1 Producto y analisis

- Filtro por provincia en el screener.
- Busqueda por descripcion de actividad.
- Ranking por cash flow margin.
- Ranking por cash conversion.
- Comparativa geografica por revenue o EBITDA, no solo numero de empresas.
- Mapa con selector de metrica:
  - numero de empresas,
  - revenue total,
  - EBITDA medio,
  - cash flow total.

### 17.2 Scoring

- Anadir ponderacion opcional de cash conversion.
- Anadir ponderacion opcional de cash flow margin.
- Mantener estas opciones desactivadas por defecto para preservar la logica
  inicial.

### 17.3 Datos

- Control avanzado de duplicados.
- Informes de importacion descargables.
- Validaciones mas especificas para sectores concretos.
- Procesamiento por lotes si se importan ficheros muy grandes.

### 17.4 Seguridad

- Login de usuarios.
- Roles de usuario.
- Row Level Security en Supabase.
- Separacion entre entorno de desarrollo y produccion.

### 17.5 Despliegue y mantenimiento

- Documentar el proceso exacto de despliegue paso a paso.
- Crear scripts de verificacion.
- Crear tests automatizados para ETL y calculo de metricas.

## 18. Posible estructura para la memoria del TFG

Este documento puede reutilizarse para los siguientes capitulos:

```text
1. Introduccion
2. Objetivos
3. Estado del arte / herramientas utilizadas
4. Analisis de requisitos
5. Diseno del sistema
6. Modelo de datos
7. Implementacion
8. Pruebas y validacion
9. Despliegue
10. Conclusiones y trabajo futuro
```

Correspondencia recomendada:

- Introduccion y objetivos: secciones 1 y 2.
- Diseno del sistema: secciones 4 y 5.
- Modelo de datos: seccion 5.
- Implementacion: secciones 6 a 11.
- Pruebas: seccion 14.
- Problemas y soluciones: seccion 15.
- Trabajo futuro: seccion 17.

## 19. Mejora de graficos en analisis sectorial

Fecha de documentacion: 2026-05-01.

Se revisaron los graficos superiores de la vista `Analisis sectorial` porque las
visualizaciones originales no eran suficientemente interpretables:

- El boxplot de EBITDA por ano generaba mucho ruido visual y no explicaba bien
  la evolucion del sector.
- El grafico de crecimiento comparaba el sector contra una media de mercado
  afectada por outliers extremos, llegando a mostrar porcentajes de crecimiento
  de millones. Esto hacia que el grafico perdiese utilidad.

### 19.1 Sustitucion del boxplot de EBITDA

Se sustituyo el grafico `Distribucion EBITDA por ano` por un grafico de
`Evolucion del sector`.

El nuevo grafico combina:

- Barras de `Revenue total` del sector por ano.
- Linea de `Margen EBITDA mediano` por ano.

Motivo del cambio:

- El revenue total muestra el tamano agregado del sector.
- El margen EBITDA mediano resume la rentabilidad operativa de forma mas robusta
  que una media simple.
- La combinacion permite ver si el sector crece en volumen y si esa evolucion se
  acompana o no de mejora de margen.

Implementacion:

```text
views/sector.py
_render_sector_evolution(df_all, selected_cnae)
```

Agregaciones utilizadas:

```text
companies        = numero de empresas unicas por ano
total_revenue    = suma de revenue por ano
median_ebitda    = mediana de EBITDA por ano
median_margin    = mediana de ebitda_margin por ano
```

### 19.2 Cambio del grafico de crecimiento

Se redisenio el grafico de crecimiento para evitar que los outliers distorsionen
la lectura.

Antes:

```text
AVG(revenue_growth_yoy)
```

Problema:

La media era muy sensible a casos extremos, especialmente cuando una empresa
pasaba de revenue muy bajo a revenue normal, generando crecimientos porcentuales
desproporcionados.

Ahora:

```text
mediana de revenue_growth_yoy
rango intercuartil del sector
mediana del mercado total
```

Ademas, el mercado se filtra a los mismos anos disponibles para el CNAE
seleccionado, evitando comparar el sector con anos que no aparecen en la serie
del sector.

Tambien se filtran crecimientos extremos fuera del rango practico:

```text
-100% <= revenue_growth_yoy <= 300%
```

Objetivo del filtro:

- Mantener el grafico interpretable.
- Evitar escalas absurdas.
- Conservar una lectura robusta de tendencia.

Implementacion:

```text
views/sector.py
_render_growth_trend(df_all, selected_cnae)
_filter_growth_outliers(...)
```

### 19.3 Ajuste de KPIs sectoriales

En la fila de KPIs sectoriales se sustituyeron medias por medianas para mantener
consistencia con los nuevos graficos:

```text
Margen EBITDA medio      -> Margen EBITDA mediano
Crecimiento medio        -> Crecimiento mediano
```

Esto reduce la influencia de empresas atipicas y hace que el resumen superior
sea mas representativo del comportamiento habitual del sector.

### 19.4 Validacion con CNAE 0121

Se probo el cambio con el CNAE `0121`, que era el caso donde el grafico anterior
mostraba un eje de crecimiento completamente desproporcionado.

Resultado observado:

```text
Anos disponibles: 2018-2024
Empresas por ano: 4
Revenue total 2024: 160.612 miles EUR
Margen EBITDA mediano 2024: 23,1%
Crecimiento mediano sector 2024: 12,8%
Crecimiento mediano mercado 2024: 6,2%
```

El nuevo grafico evita escalas de millones y permite comparar la tendencia del
sector frente al mercado de forma visualmente util.

## 20. Correcciones en Screener y graficos sectoriales

Fecha de documentacion: 2026-05-04.

Se revisaron tres problemas visuales y funcionales detectados en la aplicacion:

- El grafico principal del Screener no aportaba informacion suficientemente util.
- La tabla de resultados del Screener no permitia abrir directamente la ficha de
  una empresa haciendo click.
- Algunas leyendas y ejes de los graficos de Analisis sectorial se solapaban en
  determinados CNAEs.
- La comparativa multisector separaba excesivamente los CNAEs cuando sus codigos
  estaban numericamente alejados.

### 20.1 Sustitucion del grafico del Screener

El grafico anterior del Screener era un scatter de crecimiento frente a margen
EBITDA:

```text
x = crecimiento revenue YoY
y = margen EBITDA
tamano = revenue
color = CNAE
```

Problemas detectados:

- Los outliers distorsionaban mucho los ejes.
- La leyenda listaba demasiados CNAEs y ocupaba demasiado espacio.
- No ayudaba de forma directa a priorizar empresas.

Se sustituyo por un ranking horizontal:

```text
Top empresas del screener
x = score
y = empresa
color = intensidad del score
```

El nuevo grafico muestra las 20 empresas con mayor score dentro de los filtros
activos. En el hover se incluyen:

```text
Empresa
CNAE
Score
Revenue
Margen EBITDA
Crecimiento revenue
ND/EBITDA
```

Motivo del cambio:

El Screener tiene como finalidad seleccionar y priorizar companias. Por tanto,
un ranking por score es mas accionable que un mapa de dispersion con muchos
sectores mezclados.

Implementacion:

```text
views/screener.py
_render_priority_chart(df)
```

### 20.2 Navegacion desde Screener a ficha de empresa

Se anadio seleccion directa de fila en la tabla de resultados del Screener.

Comportamiento:

1. El usuario hace click en una empresa de la tabla.
2. Se guarda el `company_id` en `st.session_state["selected_company_id"]`.
3. Se establece `st.session_state["nav_page"] = "Ficha de empresa"`.
4. La aplicacion hace `st.rerun()` y abre la ficha de la empresa seleccionada.

Implementacion:

```text
st.dataframe(..., on_select="rerun", selection_mode="single-row")
```

Esto replica desde el Screener el flujo que ya existia en el listado de
empresas, pero de forma mas directa.

### 20.3 Correccion de solapes en Analisis sectorial

Se ajustaron los graficos superiores de la vista `Analisis sectorial` para evitar
solapes de leyendas, ejes y modebar.

Cambios realizados:

- Se desactivo la modebar de Plotly en los graficos sectoriales.
- Se aumento la altura de los graficos superiores.
- Se amplio el margen inferior.
- Se movieron las leyendas por debajo del area de dibujo.
- Se simplifico la leyenda del grafico de crecimiento, ocultando el rango
  intercuartil como elemento independiente de leyenda.
- Se corrigio el eje secundario del grafico de evolucion para que no heredase
  por error el titulo del eje principal.

Implementacion:

```text
views/sector.py
PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}
```

### 20.4 Correccion de comparativa multisector

Problema:

Cuando se comparaban CNAEs numericamente alejados, Plotly interpretaba el eje X
como eje numerico. Esto hacia que las barras apareciesen muy separadas y el
grafico quedase practicamente vacio.

Solucion:

Se fuerza el eje X a modo categorico:

```text
fig.update_xaxes(type="category")
```

Ademas, se sustituyeron medias por medianas para que la comparativa sea mas
robusta:

```text
Margen EBITDA mediano
Crecimiento revenue mediano
Equity ratio mediano
```

Para el crecimiento revenue se mantiene el filtro practico:

```text
-100% <= revenue_growth_yoy <= 300%
```

Esto evita que valores extremos de crecimiento contaminen la comparativa entre
sectores.
