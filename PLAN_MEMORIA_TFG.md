# Plan de estructura y revision de la memoria del TFG

Documento creado para ordenar la futura memoria del TFG de Miralyze a partir
del estado actual del proyecto, la documentacion tecnica existente y las normas
habituales de un Trabajo Fin de Grado de Ingenieria Informatica.

Este documento no sustituye a `DOCUMENTACION.md`. Su funcion es convertir esa
bitacora tecnica en un plan de redaccion de memoria academica.

---

## 1. Fuentes consultadas

Fuentes usadas como referencia para orientar la estructura:

- Pagina de Proyecto Fin de Grado de la ETSIINF-UPM:
  https://www.etsiinf.upm.es/?pagina=1383
- Pagina de Normas TFG de la ETSIINF-UPM:
  https://etsiinf.upm.es/index.php?pagina=2113
- Plantilla LaTeX para TFGs ETSIINF-UPM publicada en Overleaf:
  https://www.overleaf.com/latex/templates/plantilla-tfgs-etsiinf-upm/mrjbxqqzjtxh
- Pagina comercial de SABI/Informa:
  https://wwwbeta.informa.es/riesgo-empresarial/sabi

Nota importante: antes de entregar la memoria final conviene revisar la
normativa vigente en Moodle/Secretaria/Coordinacion de TFG, porque los
procedimientos administrativos pueden cambiar y la fuente definitiva debe ser
siempre la documentacion oficial de la escuela.

---

## 2. Revision del documento actual

Documento revisado:

```text
DOCUMENTACION.md
```

Estado general:

- El documento es muy util como registro de desarrollo.
- Contiene decisiones de producto, arquitectura, modelo de datos, migracion a
  Supabase, importacion SABI, calculo de metricas, visualizaciones, pruebas y
  problemas encontrados.
- La Fase 1 funciona como borrador conceptual de memoria.
- La Fase 2 funciona como bitacora tecnica cronologica de implementacion.
- No debe entregarse tal cual como memoria final, porque mezcla estilos:
  explicacion academica, notas de implementacion, changelog y registro de
  errores.

Aspectos positivos:

- Hay trazabilidad clara de decisiones: Streamlit, Supabase, PostgreSQL,
  modelo wide-to-long, metricas financieras y mapa geografico.
- La aplicacion queda justificada desde un caso de uso real: busqueda y
  analisis de empresas objetivo para search funds.
- Hay material suficiente para redactar capitulos de objetivos, diseno,
  implementacion, pruebas y conclusiones.
- Las limitaciones tecnicas y de datos estan documentadas, algo muy valioso
  para una memoria seria.

Aspectos que conviene corregir o reescribir para la memoria:

- Separar memoria academica de diario de desarrollo.
- Homogeneizar idioma, tono y terminologia.
- Revisar codificacion de caracteres: actualmente aparecen secuencias
  extranas, lo que indica un problema de encoding al leer/escribir algunos
  textos.
- Convertir listas de cambios en explicaciones: problema, decision, solucion,
  impacto y validacion.
- Evitar afirmaciones juridicas fuertes sin fuente, por ejemplo "monopolio".
  Es mejor hablar de dependencia de proveedor, concentracion de mercado o
  necesidad de licencia/acuerdo comercial.
- Mover detalles demasiado operativos a anexos: SQL completo, estructura de
  tablas, mapeos SABI, normalizacion geografica y pruebas tecnicas.

Conclusion de revision:

`DOCUMENTACION.md` esta bien como base documental y no hay que tirarlo. La
memoria final debe reescribirse a partir de el, no copiarlo directamente.

---

## 3. Estructura propuesta de la memoria final

La memoria deberia tener una estructura de ingenieria: problema, objetivos,
analisis, diseno, implementacion, validacion y conclusiones.

### 3.1 Portada y preliminares

Contenido:

- Titulo del TFG.
- Autor.
- Tutor.
- Grado.
- Escuela y universidad.
- Fecha.
- Resumen en castellano.
- Abstract en ingles.
- Palabras clave.
- Indice general.
- Indice de figuras.
- Indice de tablas.

Titulo provisional:

```text
Miralyze: plataforma web para el analisis financiero y geografico de empresas
privadas orientada a procesos de busqueda de adquisiciones
```

Palabras clave posibles:

```text
analisis financiero, search fund, Streamlit, Supabase, PostgreSQL, SABI,
business intelligence, screening de empresas, visualizacion de datos
```

### 3.2 Capitulo 1 - Introduccion

Objetivo del capitulo:

Explicar el contexto del problema y por que tiene sentido construir Miralyze.

Contenido:

- Contexto de la busqueda de empresas privadas.
- Modelo de search fund y necesidad de analizar muchas empresas.
- Problema operativo: datos dispersos, Excel, calculos manuales y dificultad
  para comparar empresas.
- Propuesta: una aplicacion web que centraliza datos financieros, calcula KPIs
  y permite filtrar, comparar y visualizar empresas.

Material de `DOCUMENTACION.md` aprovechable:

- A1. Contexto del proyecto: el modelo de search fund.
- A2. Motivacion y origen de Miralyze.
- 1. Resumen del proyecto.

### 3.3 Capitulo 2 - Objetivos y alcance

Objetivo del capitulo:

Definir que se queria construir y que queda fuera.

Objetivo general:

```text
Disenar e implementar una aplicacion web de analisis financiero que permita
importar datos empresariales procedentes de SABI, persistirlos en una base de
datos cloud y explorarlos mediante dashboards, filtros, fichas de empresa,
analisis sectorial y visualizacion geografica.
```

Objetivos especificos:

- Importar datos financieros desde Excel SABI.
- Normalizar una estructura wide a un modelo relacional empresa-anio.
- Persistir datos en Supabase/PostgreSQL.
- Calcular metricas financieras comparables.
- Mantener una interfaz Streamlit clara y navegable.
- Construir una ficha historica de empresa.
- Construir un screener de companias.
- Construir analisis sectorial.
- Construir un mapa geografico por provincia y CNAE.
- Documentar pruebas, limitaciones y futuras mejoras.

Alcance:

- Primera version privada.
- Sin sistema de usuarios.
- Sin automatizacion directa contra la API de SABI.
- Sin explotacion comercial del dato sin acuerdo con el proveedor.

Material aprovechable:

- A6. Requisitos funcionales y no funcionales.
- 2. Decisiones principales tomadas.
- 16. Estado actual de la aplicacion.

### 3.4 Capitulo 3 - Estado del arte y contexto tecnologico

Objetivo del capitulo:

Situar Miralyze frente a herramientas existentes, fuentes de datos y tecnologias
relacionadas.

Bloques recomendados:

1. Analisis financiero de empresas privadas.
2. Herramientas habituales: Excel, bases de datos financieras, CRMs, BI.
3. Fuentes de datos empresariales: SABI/Informa como fuente comercial.
4. Aplicaciones de business intelligence y dashboards.
5. Tecnologias para prototipado de datos: Streamlit, Dash, Power BI, Tableau.
6. Bases de datos cloud: Supabase/PostgreSQL frente a SQLite local.
7. Visualizacion geografica: mapas coropleticos, GeoJSON y mapas offline.

Punto importante sobre SABI/Sabinforma:

Debe aparecer aqui y tambien en limitaciones.

Redaccion sugerida:

```text
El sistema no genera datos financieros primarios, sino que trabaja sobre
exportaciones procedentes de SABI/Informa. Esto aporta una fuente estructurada y
homogenea, pero introduce una dependencia relevante respecto a un proveedor
externo de informacion empresarial. La actualizacion periodica de la aplicacion
requiere nuevas exportaciones autorizadas desde dicha fuente, y cualquier uso
comercial del producto deberia analizar las condiciones de licencia y, en su
caso, formalizar un acuerdo comercial con el proveedor de datos.
```

Evitar escribir sin prueba:

```text
SABI es un monopolio.
```

Mejor:

```text
SABI/Informa actua como proveedor central de los datos usados por el sistema, lo
que genera dependencia funcional y comercial respecto a una fuente externa.
```

Material aprovechable:

- A3.1 Stack tecnologico.
- A3.2 Streamlit frente a Dash y Flask.
- 2.1 Plataforma de despliegue.
- 2.2 Persistencia de datos.
- 7. Importacion SABI.
- 13. Despliegue en Streamlit Community Cloud.

### 3.5 Capitulo 4 - Analisis de requisitos

Objetivo del capitulo:

Traducir el problema en requisitos verificables.

Requisitos funcionales:

- RF1: importar ficheros Excel SABI.
- RF2: validar campos obligatorios y tipos de datos.
- RF3: transformar datos wide a registros anuales.
- RF4: persistir empresas, financieros y metricas.
- RF5: calcular deuda bruta, deuda neta, margenes, crecimiento y ratios.
- RF6: consultar dashboard general.
- RF7: consultar listado de empresas.
- RF8: abrir ficha historica de empresa.
- RF9: filtrar empresas desde Screener.
- RF10: analizar sectores CNAE.
- RF11: visualizar distribucion geografica.

Requisitos no funcionales:

- RNF1: persistencia cloud.
- RNF2: despliegue sencillo en Streamlit Community Cloud.
- RNF3: uso privado mediante secrets.
- RNF4: importacion robusta frente a datos incompletos.
- RNF5: interfaz coherente con identidad visual Miralyze.
- RNF6: no depender de internet para el GeoJSON en produccion.
- RNF7: trazabilidad de importaciones y errores.

Material aprovechable:

- A6. Requisitos funcionales y no funcionales.
- 8. Validacion de datos.
- 14. Pruebas realizadas.

### 3.6 Capitulo 5 - Diseno del sistema

Objetivo del capitulo:

Explicar la arquitectura antes de bajar al codigo.

Secciones recomendadas:

- Arquitectura general.
- Flujo de datos.
- Modelo de dominio.
- Modelo relacional.
- Gestion de importaciones.
- Calculo de metricas.
- Diseno de interfaz.
- Diseno de visualizaciones.

Diagrama recomendado:

```text
Excel SABI -> Loader -> Validator -> Transformer -> Supabase/PostgreSQL
                                             |
                                             v
                                      Metrics calculator
                                             |
                                             v
                                       Streamlit views
```

Tablas principales:

- `companies`: una fila por empresa.
- `financials`: una fila por empresa y anio.
- `metrics`: una fila por empresa y anio con KPIs calculados.
- `import_log`: historial de importaciones.
- `import_errors`: errores de carga.

Material aprovechable:

- A3.3 Arquitectura del sistema.
- A3.4 Modelo de datos conceptual.
- 4. Arquitectura actual.
- 5. Base de datos Supabase/PostgreSQL.
- 6. Capa de conexion a Supabase.

### 3.7 Capitulo 6 - Implementacion

Objetivo del capitulo:

Explicar como se construyo la solucion.

Secciones recomendadas:

- Estructura del repositorio.
- Capa de base de datos.
- Importador Excel SABI.
- Validacion y limpieza de datos.
- Transformacion wide-to-long.
- Upserts en PostgreSQL.
- Calculo de metricas financieras.
- Interfaz Streamlit.
- Dashboard.
- Carga de datos.
- Listado de empresas.
- Ficha de empresa.
- Screener.
- Analisis sectorial.
- Mapa geografico.

Material aprovechable:

- 7. Importacion SABI.
- 8. Validacion de datos.
- 9. Transformacion y upsert.
- 10. Calculo de metricas.
- 11. Interfaz Streamlit.
- 19. Mejora de graficos en analisis sectorial.
- 20. Correcciones en Screener y graficos sectoriales.

### 3.8 Capitulo 7 - Validacion y pruebas

Objetivo del capitulo:

Demostrar que el sistema funciona con datos reales y casos relevantes.

Pruebas recomendadas:

- Importacion de Excel con 1.000 empresas.
- Importacion de Excel con mas empresas.
- Comprobacion de fechas antiguas.
- Comprobacion de valores `n.a.` convertidos a `NULL`.
- Comprobacion de unidades en miles de euros.
- Validacion manual de deuda bruta y deuda neta.
- Validacion de ficha de empresa.
- Validacion de Screener.
- Validacion de analisis sectorial.
- Validacion del mapa geografico.
- Prueba de despliegue en Streamlit Community Cloud.

Incluir tabla:

```text
Prueba | Entrada | Resultado esperado | Resultado obtenido | Estado
```

Material aprovechable:

- 14. Pruebas realizadas.
- 15. Problemas detectados y soluciones.

### 3.9 Capitulo 8 - Despliegue y operacion

Objetivo del capitulo:

Explicar como se ejecuta y mantiene la aplicacion.

Contenido:

- Despliegue en Streamlit Community Cloud.
- Secrets necesarios.
- Conexion a Supabase.
- Preparacion inicial de la base de datos.
- Flujo de actualizacion de datos.
- Restricciones de rendimiento.
- Consideraciones de seguridad.

Material aprovechable:

- 13. Despliegue en Streamlit Community Cloud.
- 2.3 Seguridad.
- 12. Dependencias.

### 3.10 Capitulo 9 - Limitaciones, riesgos y aspectos comerciales

Objetivo del capitulo:

Mostrar madurez tecnica: que funciona, que depende de terceros y que habria que
resolver para convertirlo en producto.

Limitaciones tecnicas:

- Streamlit es adecuado para prototipo avanzado y uso interno, pero no ofrece
  el mismo control de producto que una aplicacion web desarrollada desde cero.
- La importacion depende de que el Excel mantenga una estructura compatible.
- El rendimiento depende del volumen de datos y de la configuracion de
  Supabase/Streamlit.
- No hay autenticacion de usuarios en la primera version.

Limitaciones de datos:

- Los datos financieros proceden de SABI/Informa.
- La aplicacion no actualiza informacion financiera automaticamente.
- Cada nuevo ejercicio requiere una nueva exportacion y carga de datos.
- La calidad del analisis depende de la calidad y cobertura de los datos de
  origen.
- Los campos descriptivos y geograficos pueden requerir normalizacion.

Aspecto comercial clave:

```text
Para comercializar Miralyze con datos procedentes de SABI/Informa seria
necesario revisar las condiciones de licencia de la fuente de datos y,
previsiblemente, establecer un acuerdo comercial que autorice dicho uso.
```

Este punto puede aparecer en:

- Estado del arte: dependencia de fuentes privadas de informacion financiera.
- Limitaciones: dependencia funcional y comercial del proveedor.
- Trabajo futuro: integraciones/licencias/acuerdos de datos.
- Viabilidad comercial: costes y restricciones del dato.

### 3.11 Capitulo 10 - Gestion del proyecto

Objetivo del capitulo:

Explicar la evolucion temporal del trabajo.

Contenido:

- Plan inicial.
- Iteracion 1: version local con SQLite.
- Iteracion 2: migracion a Supabase.
- Iteracion 3: importador SABI robusto.
- Iteracion 4: visualizaciones y mapa.
- Iteracion 5: mejoras de interfaz y analisis sectorial.
- Herramientas de apoyo: control de versiones, asistentes de IA, pruebas
  manuales, Streamlit, Supabase.

Material aprovechable:

- A9. Cambios respecto al Plan de Trabajo de la primera entrega.
- A11. Herramientas de generacion de documentos del TFG.
- Fase 2 completa como cronologia tecnica.

### 3.12 Capitulo 11 - Conclusiones y trabajo futuro

Objetivo del capitulo:

Cerrar el TFG mostrando que se han cumplido los objetivos y que queda una ruta
realista de evolucion.

Conclusiones posibles:

- Se ha construido una aplicacion funcional de analisis financiero.
- Se ha migrado de persistencia local a persistencia cloud.
- Se ha adaptado el modelo de datos al formato real de SABI.
- Se han incorporado visualizaciones financieras, sectoriales y geograficas.
- El sistema es util para reducir trabajo manual en procesos de screening.

Trabajo futuro:

- Autenticacion y roles.
- Mejoras de rendimiento para datasets mayores.
- Automatizacion de actualizaciones de datos.
- Integracion con fuentes externas mediante acuerdos.
- Scoring configurable.
- Comparativas temporales mas avanzadas.
- Exportacion de informes.
- Version producto con frontend propio si se decide ir mas alla de Streamlit.

---

## 4. Mapa de `DOCUMENTACION.md` a memoria final

```text
DOCUMENTACION.md                                  -> Memoria final
---------------------------------------------------------------------------
A1, A2                                           -> Introduccion
A3.1, A3.2                                      -> Estado del arte / tecnologia
A3.3, A3.4                                      -> Diseno del sistema
A4                                              -> Modelo de scoring / metricas
A5                                              -> Clasificacion sectorial
A6                                              -> Requisitos
A7                                              -> Diseno funcional inicial
A8                                              -> Diseno visual
A9                                              -> Gestion del proyecto
A10                                             -> Base para indice final
A11                                             -> Herramientas y metodologia
A12                                             -> Estado inicial
1, 2                                            -> Introduccion / decisiones
3                                               -> Datos financieros SABI
4, 5, 6                                         -> Diseno e implementacion
7, 8, 9                                         -> Importacion y ETL
10                                              -> Calculo de metricas
11                                              -> Interfaz
12, 13                                          -> Dependencias y despliegue
14                                              -> Validacion y pruebas
15                                              -> Problemas y soluciones
16                                              -> Estado actual
17                                              -> Trabajo futuro
18                                              -> Referencia para estructura
19, 20                                          -> Implementacion / mejoras UI
```

---

## 5. Figuras y tablas recomendadas

Figuras:

- Arquitectura general del sistema.
- Flujo de importacion SABI.
- Modelo entidad-relacion.
- Captura del dashboard.
- Captura de carga de datos.
- Captura de ficha de empresa.
- Captura del Screener.
- Captura de analisis sectorial.
- Captura del mapa geografico.

Tablas:

- Requisitos funcionales.
- Requisitos no funcionales.
- Campos de `companies`.
- Campos de `financials`.
- Campos de `metrics`.
- Mapeo SABI -> base de datos.
- Metricas calculadas y formulas.
- Pruebas de importacion.
- Pruebas de interfaz.
- Limitaciones y mitigaciones.

---

## 6. Plan de trabajo para reescribir la memoria

### Fase 1 - Inventario

- Revisar todo `DOCUMENTACION.md`.
- Separar contenido academico de contenido tecnico operativo.
- Marcar que secciones pasan a memoria y cuales pasan a anexos.
- Revisar si existe algun `.docx`, `.tex` o plantilla fuera del repositorio.

### Fase 2 - Esqueleto

- Crear documento base de memoria.
- Incluir portada, resumen, indices y capitulos.
- Insertar placeholders de figuras y tablas.
- Definir estilo de citas.

### Fase 3 - Redaccion tecnica

- Redactar introduccion, objetivos y alcance.
- Redactar estado del arte con citas.
- Redactar requisitos.
- Redactar diseno.
- Redactar implementacion.
- Redactar pruebas.

### Fase 4 - Revision de coherencia

- Comprobar que cada objetivo tiene una validacion.
- Comprobar que cada decision tecnica esta justificada.
- Eliminar duplicidades.
- Homogeneizar terminos: empresa, company, compania; revenue, ingresos,
  facturacion; EBITDA; CNAE; deuda neta.

### Fase 5 - Revision academica

- Revisar ortografia y acentos.
- Revisar calidad de figuras.
- Revisar bibliografia.
- Revisar conclusiones.
- Revisar anexos.

### Fase 6 - Entrega

- Exportar a PDF.
- Comprobar numeracion de figuras y tablas.
- Comprobar que enlaces y referencias cruzadas funcionan.
- Preparar presentacion de defensa a partir de la memoria.

---

## 7. Checklist de calidad antes de entregar

- La memoria explica el problema antes de explicar la solucion.
- Los objetivos son verificables.
- La arquitectura se entiende sin leer el codigo.
- El modelo de datos esta justificado.
- Las metricas financieras incluyen formula y unidad.
- Las unidades monetarias se indican como miles de euros.
- La dependencia de SABI/Informa esta explicada como limitacion.
- No aparecen secretos, tokens ni contrasenas.
- Las capturas corresponden a la version final.
- Las pruebas incluyen datos reales.
- Las conclusiones responden a los objetivos iniciales.
- El trabajo futuro no parece una lista de fallos, sino una evolucion natural.

---

## 8. Decision sobre la dependencia de SABI/Informa

Este punto es suficientemente importante para aparecer en la memoria, pero debe
redactarse con precision.

Idea del usuario:

```text
Los datos proceden de Sabinforma/SABI. Para actualizar anualmente el sistema hay
que volver a alimentar la base de datos con nuevas exportaciones. Para
comercializar el producto haria falta un acuerdo comercial con el proveedor.
```

Tratamiento recomendado:

- En "Estado del arte": describir SABI/Informa como fuente de informacion
  empresarial estructurada.
- En "Limitaciones": explicar la dependencia de proveedor y la actualizacion no
  automatica.
- En "Viabilidad comercial": indicar que el uso comercial del producto con esos
  datos requiere revisar licencia y acuerdo.
- En "Trabajo futuro": plantear integraciones, acuerdos de datos o conectores de
  actualizacion.

Redaccion final sugerida:

```text
Miralyze se apoya en exportaciones procedentes de SABI/Informa, por lo que la
aplicacion depende de una fuente externa de datos financieros empresariales. Esta
decision permite trabajar con informacion estructurada y comparable, pero
tambien limita la autonomia del sistema: la actualizacion de nuevos ejercicios
requiere nuevas cargas de datos y cualquier explotacion comercial deberia
ajustarse a las condiciones de licencia del proveedor, pudiendo requerir un
acuerdo comercial especifico.
```

---

## 9. Proximos documentos que conviene crear

1. `MEMORIA_TFG_BORRADOR.md`

   Primer borrador continuo de memoria, ya con tono academico.

2. `ANEXO_TECNICO.md`

   Detalle de SQL, mapeo SABI, formulas, normalizacion geografica y pruebas.

3. `LISTA_FIGURAS_TFG.md`

   Inventario de capturas necesarias y estado de cada una.

4. `PRESENTACION_DEFENSA_TFG.md`

   Guion de la defensa cuando la memoria este avanzada.

---

## 10. Recomendacion final

La mejor estrategia no es escribir la memoria desde cero ni entregar
`DOCUMENTACION.md` directamente. Lo mas solido es usar `DOCUMENTACION.md` como
fuente primaria de verdad tecnica y redactar una memoria nueva, con estructura
academica, apoyada en capturas, tablas, formulas y una seccion clara de
limitaciones.

El proyecto ya tiene suficiente contenido tecnico para una memoria completa. El
trabajo pendiente es convertir ese contenido en relato de ingenieria:
necesidad, diseno, construccion, validacion y aprendizaje.

---

## 11. Revision posterior de documentos `.docx` encontrados

Tras una segunda revision se localizaron documentos fuera de la carpeta
`tfg_screener`, en el directorio padre del proyecto:

```text
TFG_Miralyze_ETSIINF_v3.docx
Segunda_Entrega_TFG_Miralyze_v4.docx
TFG_Miralyze_ETSIINF.docx
TFG_Miralyze_ETSIINF_v2.docx
```

Documento principal identificado:

```text
TFG_Miralyze_ETSIINF_v3.docx
```

Motivo:

- Tiene formato completo de memoria ETSIINF.
- Incluye portada, resumen, abstract, introduccion, estado del arte, analisis,
  desarrollo, evaluacion, conclusiones, impacto, bibliografia y anexos.
- Es mas extenso que la segunda entrega y parece el borrador formal mas
  avanzado.

Documento secundario:

```text
Segunda_Entrega_TFG_Miralyze_v4.docx
```

Motivo:

- Es una entrega intermedia.
- Contiene material util de planificacion y estado inicial.
- No parece ser la memoria final, sino un documento de seguimiento.

### 11.1 Diagnostico de `TFG_Miralyze_ETSIINF_v3.docx`

La memoria existente tiene una estructura academica buena, pero esta
desactualizada respecto al estado real del proyecto.

Problema principal:

La memoria describe la version anterior de Miralyze:

- Persistencia local con SQLite.
- Importacion mediante CSV.
- Modelo inicial sin Supabase/PostgreSQL.
- Sin despliegue real en Streamlit Community Cloud.
- Sin mapa geografico.
- Sin los nuevos campos SABI definitivos.
- Sin cash flow.
- Sin el redisenyo de analisis sectorial y Screener.

Comprobaciones textuales realizadas:

```text
TFG_Miralyze_ETSIINF_v3.docx
SQLite: 13 apariciones
CSV: 12 apariciones
Supabase: 0 apariciones
PostgreSQL: 0 apariciones
cash flow: 0 apariciones
Streamlit Community Cloud: 0 apariciones
```

Conclusion:

El documento no esta mal, pero ya no representa el sistema actual. Debe
considerarse un borrador de memoria de la Fase 1, no la version final.

### 11.2 Estructura actual del `.docx`

La estructura encontrada en `TFG_Miralyze_ETSIINF_v3.docx` es:

```text
Resumen
Abstract
1. Introduccion
1.1 Objetivos
1.2 Contribucion
1.3 Estructura del documento
2. Estado del arte
2.1 Herramientas comerciales de datos de empresas privadas
2.1.1 SABI e Informa D&B
2.1.2 Plataformas de mercados cotizados
2.1.3 Hojas de calculo
2.1.4 Plataformas de Business Intelligence
2.2 Tecnologias utilizadas
2.3 Gap analysis
3. Analisis y diseno del sistema
3.1 Problema y requisitos
3.2 Actores
3.3 Arquitectura
3.4 Modelo de datos
4. Desarrollo
4.1 Pipeline ETL
4.2 Motor de scoring
4.3 Dashboard e interfaz
5. Evaluacion y validacion
6. Resultados y conclusiones
7. Analisis de impacto
Bibliografia
Anexos
```

Esta estructura es aprovechable. No hace falta cambiarla radicalmente, pero si
hay que actualizar el contenido interno de casi todos los capitulos tecnicos.

### 11.3 Reescritura necesaria por capitulos

#### Resumen y abstract

Actualizar para reflejar:

- Persistencia cloud con Supabase/PostgreSQL.
- Importacion desde Excel SABI.
- Analisis financiero, sectorial y geografico.
- Despliegue en Streamlit Community Cloud.
- Uso de datos en miles de euros.

#### Capitulo 1 - Introduccion

Mantener gran parte del contexto de search funds.

Actualizar:

- El alcance ya no es solo dashboard y scoring.
- Miralyze ahora es tambien una plataforma persistente cloud.
- Incluir mapa geografico y analisis territorial como valor nuevo.

#### Capitulo 2 - Estado del arte

Mantener:

- Search funds.
- SABI/Informa.
- Hojas de calculo.
- BI.
- Streamlit.

Anadir:

- Supabase/PostgreSQL como alternativa moderna a SQLite local.
- Limitacion de dependencia de SABI/Informa.
- Necesidad de licencia/acuerdo comercial para explotacion del dato.
- Visualizacion geografica con GeoJSON local.

#### Capitulo 3 - Analisis y diseno

Reescribir con el modelo actual:

- `companies`
- `financials`
- `metrics`
- `import_log`
- `import_errors`

Cambiar:

- SQLite por PostgreSQL/Supabase.
- CSV por Excel SABI.
- Formato de una fila por empresa y columnas por anio a transformacion
  wide-to-long.
- Nueva clave anual basada en `Last available year`.

#### Capitulo 4 - Desarrollo

Reescribir gran parte:

- Capa de conexion `psycopg`.
- Secrets de Streamlit.
- Importador Excel.
- Validacion de fechas y valores `n.a.`.
- Calculo de deuda bruta y deuda neta:

```text
gross_debt = long_term_debts + short_term_debts
net_debt = gross_debt - cash_and_equivalents
```

- Nuevas metricas de cash flow.
- Vistas actuales:
  - Dashboard
  - Cargar datos
  - Listado de empresas
  - Ficha de empresa
  - Screener
  - Analisis sectorial
  - Mapa geografico

#### Capitulo 5 - Evaluacion y validacion

Actualizar con pruebas reales actuales:

- Importacion de 1.000 empresas.
- Intento de importacion de 2.000 empresas y correccion de fechas antiguas.
- Decision de quitar CSV y mantener Excel.
- Validacion de Supabase.
- Validacion del mapa geografico.
- Validacion de visualizaciones sectoriales corregidas.

#### Capitulo 6 - Resultados y conclusiones

Actualizar resultados:

- Ya existe persistencia cloud.
- La aplicacion puede funcionar con miles de empresas.
- Se ha mejorado el analisis sectorial.
- Se ha incorporado mapa territorial.
- El producto sigue teniendo limitaciones de datos/licencia.

#### Capitulo 7 - Impacto

Anadir impacto economico y comercial:

- Reduce tiempo de analisis manual.
- Puede mejorar procesos de sourcing.
- Pero depende de una fuente de datos privada.
- Su comercializacion requeriria acuerdo con el proveedor de datos si se usan
  datos SABI/Informa.

#### Anexos

Mover aqui:

- Esquema SQL.
- Mapeo completo de columnas SABI.
- Formulas de metricas.
- Capturas.
- Pruebas.
- Normalizacion geografica.
- GeoJSON.

### 11.4 Decision recomendada

No crear la memoria final desde cero.

Estrategia recomendada:

1. Usar `TFG_Miralyze_ETSIINF_v3.docx` como base formal.
2. Usar `DOCUMENTACION.md` como fuente tecnica actualizada.
3. Usar `PLAN_MEMORIA_TFG.md` como mapa de reescritura.
4. Crear una nueva version:

```text
TFG_Miralyze_ETSIINF_v4_actualizada.docx
```

5. Reescribir los capitulos tecnicos, manteniendo lo aprovechable de contexto,
   motivacion y estado del arte.

### 11.5 Prioridad de cambios

Prioridad alta:

- Resumen y abstract.
- Objetivos.
- Arquitectura.
- Modelo de datos.
- Desarrollo.
- Pruebas.
- Limitaciones de SABI/Informa.

Prioridad media:

- Estado del arte.
- Impacto.
- Trabajo futuro.
- Capturas actualizadas.

Prioridad baja:

- Ajustes menores de estilo.
- Reordenacion de anexos.
- Maquetacion final.
