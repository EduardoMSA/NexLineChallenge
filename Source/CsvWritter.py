from lxml import etree
import csv


class Writter:
    #Clase que se encargará de tomar el XML obtenido del WebScrapper y convertirlo en los archivos CSV requeridos

    def __init__(self):
        #Se obtiene el archivo XML generado con el WebScrapper
        #Se añade el .getroot() para obtener el Element del Element_Tree, lo que nos facilita su manejo
        self.tree = etree.parse('../Data/data.xml').getroot()

        #Se obtienen las listas de filas con los datos solicitados
        rows = self.getRows()
        self.rows1 = rows[0]
        self.rows2 = rows[1]

    def getMaxPostNum(self):
        #Se obtiene el número máximo de posts dentro de una sola categoría
        max = len(self.tree[0])
        for i in range(len(self.tree)):
            if max < len(self.tree[i]):
                max = len(self.tree[i])
        return max

    def getRows(self):
        #Se generan las filas a agregar dentro de cada archivo CSV requerido

        #Para nuestro primer archivo, se sabe que la primera fila serán los encabezados de los datos requeridos
        rows1 = [['Título','Categoría','Fecha','Número de Comentarios','Último Comentario']]

        #Para nuestro segundo archivo, se inicializa una matriz Número máximo de posts dentro de una categoría X Número de categorías
        rows2 = [ [ "" for i in range(len(self.tree)) ] for j in range(self.getMaxPostNum()+1) ]

        #Se recorrerá el arbol XML arbol->categorias->post
        for i in range(len(self.tree)):

            #Se añade al segundo archivo el encabezado en la fila correspondiente
            #El encabezado consta de el nombre de la categoria y el número de elementos dentro de ella
            rows2[0][i] = self.tree[i].attrib['category'] + " (" + str(len(self.tree[i])) + ")"

            for j in range(len(self.tree[i])):

                #Se añaden a un string todas las categorias del post especificado
                categories = ""
                for category in self.tree[i][j][3]:
                    categories = categories + category.attrib['category'] + "  "

                #Se añade a una fila los datos requeridos para el primer archivo
                row = [self.tree[i][j][0][0].attrib['title'],categories,self.tree[i][j][1][0].attrib['date'],self.tree[i][j][4][0].attrib['Number'],self.tree[i][j][4][0].attrib['Last']]

                #Si la fila no se encuentra repetida (Puede suceder en el caso de que el post tenga más de una categoría) se añade al primer archivo
                if row not in rows1:
                    rows1.append(row)

                #Se añade en la posición de categoría correspondiente el titulo del post, para ser añadido posteriormente al segundo archivo
                rows2[j+1][i] = self.tree[i][j][0][0].attrib['title']

        #Se retornan las dos listas de filas para los archivos CSV
        return(rows1,rows2)

    def generateCsv(self):
        #Se abre el primer archivo para escritura y se añaden la listas de filas correspondiente
        with open('../Data/example-list.csv', 'w', newline='') as file1:
            writer = csv.writer(file1)
            writer.writerows(self.rows1)

        #Se abre el segundo archivo para escritura y se añaden la listas de filas correspondiente
        with open('../Data/example-categorization.csv', 'w', newline='') as file2:
            writer = csv.writer(file2)
            writer.writerows(self.rows2)
