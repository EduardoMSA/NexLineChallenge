from WebScrapper import NextLineScrapper
from lxml import etree
import csv
import numpy as np


#ws = NextLineScrapper()
#ws.scanSite()
#ws.generateXML()


#print(etree.tostring(tree, pretty_print=True,encoding='unicode'))

class writter:

    def getMaxPostNum(self):
        max = len(self.tree[0])
        for i in range(len(self.tree)):
            if max < len(self.tree[i]):
                max = len(self.tree[i])
        return max

    def getRows(self):

        rows1 = [['Título','Categoría','Fecha','Número de Comentarios','Último Comentario']]

        rows2 = [ [ "" for i in range(len(self.tree)) ] for j in range(self.getMaxPostNum()+1) ]

        for i in range(len(self.tree)):

            rows2[0][i] = self.tree[i].attrib['category'] + " (" + str(len(self.tree[i])) + ")"

            for j in range(len(self.tree[i])):

                categories = ""
                for category in self.tree[i][j][3]:
                    categories = categories + category.attrib['category'] + "  "

                row = [self.tree[i][j][0][0].attrib['title'],categories,self.tree[i][j][1][0].attrib['date'],self.tree[i][j][4][0].attrib['Number'],self.tree[i][j][4][0].attrib['Last']]

                if row not in rows1:
                    rows1.append(row)

                rows2[j+1][i] = self.tree[i][j][0][0].attrib['title']

        print(rows1)
        print(rows2)

        return(rows1,rows2)

    def generateCsv(self):
        with open('../Data/example-list.csv', 'w', newline='') as file1:
            writer = csv.writer(file1)
            writer.writerows(self.rows1)
        with open('../Data/example-categorization.csv', 'w', newline='') as file2:
            writer = csv.writer(file2)
            writer.writerows(self.rows2)

    def __init__(self):
        self.tree = etree.parse('../Data/data.xml').getroot()
        rows = self.getRows()
        self.rows1 = rows[0]
        self.rows2 = rows[1]


w = writter()
w.generateCsv()
