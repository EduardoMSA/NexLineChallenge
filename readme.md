# NextLine Data Scientist Challenge

**Autor: Eduardo Méndez**

## Descripción
El objetivo del desafío es la obtención de datos dentro del [blog de NextLine](https://blog.nextline.mx) y exportarlos a dos archivos CSV preestablecidos

## Instrucciones del desafío
Dentro de la carpeta [*Instrucciones*](https://github.com/EduardoMSA/NexLineChallenge/tree/master/Instrucciones) se pueden encontrar los requerimientos del desafío, así como una muestra de los resultados esperados.

## Herramientas utilizadas
Para realizar el desafío se utilizó [Python 3](https://www.python.org/) acompañado por las siguientes librerías:
* [Requests](https://2.python-requests.org/en/master/)
* [lxml](https://lxml.de/)

## Estructura
La solución está compuesta por tres clases, todas ellas contenidas dentro de la carpeta [*Source*](https://github.com/EduardoMSA/NexLineChallenge/tree/master/Source):
* [Scrapper](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Source/WebScrapper.py): Se encuentran todos los métodos necesarios para obtener los datos del [blog](https://blog.nextline.mx) y convertirlos a un [archivo XML](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Data/data.xml)
* [Writer](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Source/CsvWritter.py): Se encuentra lo necesario para tomar los datos del [archivo XML](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Data/data.xml) y representarlos en CSV de la manera en que se especifica ([Categorization](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Data/example-categorization.csv) y [List](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Data/example-list.csv))
* [Main](https://github.com/EduardoMSA/NexLineChallenge/blob/master/Source/main.py): Se ejecuta el programa

## Para iniciar
* python3 main.py

Los datos son guardados dentro de la carpeta [*Data*](https://github.com/EduardoMSA/NexLineChallenge/tree/master/Data)
