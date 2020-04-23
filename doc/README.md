# Documentation

Readme about documentation here

> Work in progress ...

---

## LOG

> ***Viernes 17 de Abril de 2020 - 6:00PM***
Estoy revisando los datos publicados por el INS en su sitio https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx y también estoy revisando los datos publicados por el INS en la pagina de datos abiertos del gobierno https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data ambos datos están actualizados al día de hoy y he detectado varias inconsistencias:
En la página del INS se reportan 3439 casos al día de hoy
En la página de datos abiertos también se reportan 3439 casos al día de hoy
Primera inconsistencia que identifico, en la página del INS ahora sólo están publicando el reporte diario, es decir no se encuentra el reporte historico de casos registrados, pero este reporte diario que actualmente publican incluye casos con fecha de diagnóstico de dias pasados (esto me hace suponer que al día de hoy se han recuperado o fallecido personas)
Segunda inconsistencia que identifico, existen casos registrados al día de hoy con una fecha que no tiene un formato válido, por ejemplo año 1900 mes 00, día 00
Tercera inconsistencia que identifico, tanto en la pagina del INS como en datos abiertos se reporta la misma cantidad de casos, entonces hice una búsqueda de casos registrados por fecha en datos abiertos (17/04/2020) y no se registra ningún caso con esa fecha, lo cual no tiene sentido partiendo de que se tienen la misma cantidad de casos tanto en el INS como en datos abiertos
Cuarta inconsistencia que identifico, tomé un ID de caso de la página del INS (3227) y realicé una búsqueda en los datos de datos abiertos y el caso registrado que se encuentra no corresponde al caso registrado en la pagina del INS, aún mas grave porque entonces cómo se tiene trazabilidad de los casos que actualizan y que se recuperan o han fallecido
Con esta evidencia, no sé a que datos creerle, ni tampoco que datos tomar como verídicos.
Abro este hilo para discusión

---

> ***Sabado 18 de Abril de 2020 - 3:00AM***
He estado revisando el dashboard del INS pude obtener los datos que ellos usan en el dashboard, hasta la hora ya tengo actualizado el dataset del Time Line hasta el día 17 pero existe cierta diferencia con los datos, creo que eso se debe a la forma en que ellos están actualizando los reportes que hasta el momento no me queda claro cómo es que ellos lo están haciendo, es decir, actualizar datos me refiero a que no es claro en la forma en que el INS modifica datos que ya existen ó crean nuevos datos con los cambios ó eliminan y remplazan. Hasta el día de anteayer estaban publicando el historico, pero ahora dividieron la información en 4 casos, un grupo de casos "nuevos" (entre comillas nuevos porque pude evidenciar que también hacen referencia a casos de días pasados), un grupo de casos "Fallecidos", un grupo de casos "Recuperados" y un grupo de casos "Recuperados (Hospital)", esta debe ser la razón por la cual existe cierta diferencia con los datos.
Como dato aparte, en el siguiente dataset estoy guardando los reportes de Google Community Mobility:
https://raw.githubusercontent.com/sebaxtian/colombia_covid_19_pipe/master/output/google_community_mobility_reports.csv

---

> ***Sabado 18 de Abril de 2020 - 6:38PM***
Al día de hoy el INS hace el reporte de casos relacionados al Covid19, las múltiples inconsistencias en los datos persisten a tal punto que a día de hoy en el reporte no existe ningún caso relacionda a la fecha 18/04/2020 pero en el número de casos positivos con coronavirus incrementó, esto me hace suponer que actualmente están actualizando casos registrados como "En estudio" a alguno de los tipos "Relacionado" o "Importado", o tal vez actualizan casos que tenian estado "Recuperado" a "Fallecido", hasta este punto las inconsistencias persisten, varias personas atraves de Twitter estan manifestando los mismos hallasgos y ahora en Chis.pa se ha publicado un post para abrir la discusión frente al manejo de datos abiertos por parte del INS y que se puede extender a varias entidades del gobierno en general, dejo aquí el link al post donde se puede tener un resumen detallado de las inconsistencias identificadas hasta la fecha.
https://chis.pa/covid-19-cali-2020/

---

---

> ***Lunes 20 de Abril de 2020 - 11:19AM***
Hola, el INS actualizó la estructura que hace de los reportes, perece que ahora mejoraron la estructura para cada reporte, aquí dicen la descripción de la actualización que hicieron y como van hacer las actualizaciones futuras que se presenten
https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr
Como tarea pendiente, actualizar el pipeline para procesar la nueva estructura de reportes del INS, hasta la fecha y hora no se han actualizado los datos relacionados a muestras procesadas por semana.

---

---

> ***Martes 21 de Abril de 2020 - 02:07PM***
Realizo una reestructuración del código fuente del pipeline para poder procesar las nuevas fuentes de datos oficiales del INS relacionados a casos reportados por Covid19 y al histórico de muestras procesadas en Colombia.

---

---

> ***Jueves 23 de Abril de 2020 - 12:26AM***
Actualizo el codigo fuente del pipeline, segmento codigo para procesar en pipeline en un notebook y creo otro notebook para procesar el time line. El proceso de automatizacion del pipeline funcionó sin problemas el día Miercoles 22 de Abril de 2020, pendiente la nueva actualización para hoy.

---

> Work in progress ...
