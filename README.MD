# Introduccion

En este proyecto se hara un proyecto sobre el analisis del indice de mortalidad en el estado de Guanajuato ademas del analisis de las mismas en los municipios correspondientes gracias a datos abiertos del INEGI.

* [Datos INEGI](https://www.inegi.org.mx/app/descarga/)

## Informacion del dataset

| Id        | Nombre   | Descripcion |
|--------------|-----------|------------|
|1002000030| Defunciones generales| Esta información se actualiza anualmente       |
|1002000031|Defunciones generales hombres|La información se presenta por lugar de residencia habitual del fallecido|
|1002000032|Defunciones generales mujeres|La información se presenta por lugar de residencia habitual del fallecido|
|1002000033|Defunciones generales de sexo no especificado|La información se presenta por lugar de residencia habitual del fallecido|
|1002000034|Defunciones de menores de un año|La información se presenta por lugar de residencia habitual del fallecido|
|1002000035|Defunciones de menores de un año hombres|La información se presenta por lugar de residencia habitual del fallecido|
|1002000036|Defunciones de menores de un año mujeres|La información se presenta por lugar de residencia habitual del fallecido|
|1002000037|Defunciones de menores de un año de sexo no especificado|La información se presenta por lugar de residencia habitual del fallecido|
|6200240338|Suicidios registrados|Defunciones registradas por entidad federativa de residencia habitual de la persona fallecida|
|6200240468|Índice de sobremortalidad masculina|Es la relación de las defunciones masculinas por cada cien defunciones femeninas|
|6200240526|Porcentaje de muertes por suicidio con respecto al total de muertes violentas|El cálculo se realizó con base en las defunciones generales de residencia habitual de la persona fallecida|

## Requerimientos

Se esta usando una version 3.10.7 de Python en un ambiente virtual previamente creado, los requerimientos se pueden ver en este archivo de texto:

* [Requerimientos](./requeriments.txt)

## Notebooks

Cada notebook cuenta con un dashboard interactivo **es necesario correr las celdas de codigo**

* [Limpieza y Filtrado de Datos](./limpieza_filtrado.ipynb)

* [Analisis de indice de mortalidad Estatal](./mortalidad_estado.ipynb)

* [Analisis de indice de mortalidad por municipios](./mortalidad_municipios.ipynb)

* [Analisis de indice de mortalidad en lugares no especificados](./mortalidad_no_especificado.ipynb)

## Dashboard Final

* [Codigo (Actualizandose)](./app.py)

* [Dasboard desplegado (Actualizandose)](https://mortalidad-gto.onrender.com/)


