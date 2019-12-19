from WebScrapper import NextLineScrapper
from CsvWritter import Writter

class main:
    def __init__(self):
        #Se inicializa el WebScrapper
        scrapper = NextLineScrapper()

        #Se escanea el sitio https://blog.nextline.mx
        scrapper.scanSite()

        #Se genera un XML con los datos solicitados
        scrapper.generateXML()

        #Se inicializa el CsvWritter
        writter = Writter()

        #Se generan los archivos CSV solicitados
        writter.generateCsv()

#Se inicia la ejecución del programa
main()
