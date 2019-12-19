import requests
import lxml.html
import copy
from lxml import etree

class NextLineScrapper:

    def __init__(self):

        self.html = 'https://blog.nextline.mx/' #Dirección del bol de NextLine
        self.postsTree = etree.Element("Posts") #Se inicializa el árbol donde se guardará el XML
        self.numPages = self.getNumPages() #Se obtiene el número de páginas del blog

    def getPost(self,post):
        tree = etree.Element("Post") #XML donde se guardará el post

        a = post[0] # Parte del post que contiene el articulo

        aTumbnail = a[0] #Parte del articulo que contiene la imagen y el número de Comentarios
        aText = a[2] #Parte del articulo donde esta el nombre, las categorias, la fecha y la direccion

        hComnts = aTumbnail[1][0][3][0][0].text != "0 Comentarios" #Bool para saber si hay comentarios en el post

        #Se crean los Elementos donde se guardaran los datos obtenidos del post

        categories = etree.Element("categories")
        date = etree.Element("date")
        title = etree.Element("title")
        href = etree.Element("href")
        comments = etree.Element("comments")

        for c in aText[0]:
            categories.append(etree.Element("v", category=c.attrib['title']))   #Se obtienen los nombre de todas las categorias

        date.append(etree.Element("v", date=aText[2].text)) #se obtiene la feha del post
        title.append(etree.Element("v", title=aText[1][0].text)) #se obtiene el nombre del post
        href.append(etree.Element("v", href=aText[1][0].attrib['href'])) #se obtiene el enlace del post
        if(hComnts): #Revisa si existen comentarios, si los hay, se entra a la página del post a buscarlos, si no, omite la pagina
            coment = self.getComments(str(aText[1][0].attrib['href']))
            comments.append(etree.Element("v", Number = coment[0], Last = coment[1]))
        else:
            comments.append(etree.Element("v", Number = "0", Last = ""))

        #Se añaden los elementos al post
        tree.append(title)
        tree.append(date)
        tree.append(href)
        tree.append(categories)
        tree.append(comments)

        #Regresa el árbol del post
        return tree

    def checkCategories(self,category):
        #Revisa si existe la categoria especificada en el árbol
        for c in self.postsTree:
            if c.attrib['category'] == category: #Si existe, se sale de la funcion
                return
        self.addCategory(category) #Si no existe, añade la categoria

    def addCategory(self,category):
        #Añade la categoría especificada al árbol
        self.postsTree.append(etree.Element("c", category=category))

    def addPost(self,post,category):
        #Añade el post dado a la categoria especificada
        for i in self.postsTree:
            if category == i.attrib['category']: #Busca la categoría
                i.append(copy.deepcopy(post)) #Se añade una copia al árbol, esto para que los elementos con más de una categoría puedan estar en ambas
                print(post[0][0].attrib['title'] + " -> " + category) #Se imprime el nombre del post y la categoria a la que corresponde en la consola

    def scanPage(self,html):
        doc = lxml.html.fromstring(html.content)
        posts = doc.xpath('//div[@class="posts"]')[0] #se especifica la posicion 0 para que no regrese como lista, aunque sea un solo elemento siempte
        postList = posts.xpath('//div[@class="grid-element col-xs-12 col-sm-12 col-md-6"]') #se obtienen una lista de todos los posts

        for i in postList: #Se obtiene cada elemento de la lista de posts
            p = self.getPost(i)
            for j in p[3]: #Se obtiene cada categoria del post
                c = j.attrib['category']
                self.checkCategories(c)
                self.addPost(p,c)

    def getComments(self,html):

        doc = lxml.html.fromstring(requests.get(html).content)
        commentList = doc.xpath('//ol[@class="commentlist"]')[0][0] #Se obtiene la sección de comentarios
        commentLen = 0 #No se puede poner simplemente len porque detecta elementos que no son comentarios
        for i in commentList:
            if(i.tag == "article" or i.tag == "ul"): #Si el tag del elemento es article (comentario) o ul (respuesta) se añade uno a nuestro conteo de comentarios
                commentLen=commentLen+1
        lastComment = commentList[0][2][0].text #Se obtiene el texto del último comentario
        return (str(commentLen),lastComment) #Se regresa el numero de comentarios y el texto del ultimo comentario


    def scanSite(self):
        #Se obtendrán los posts de todas las páginas del sitio
        for i in range(1,self.numPages+1):
            #La paginación del sitio solo cambia un numero en la url: https://blog.nextline.mx/page/1/, https://blog.nextline.mx/page/2/,..., https://blog.nextline.mx/page/N/
            html = self.html + 'page/' + str(i) + '/' #Se añade el numero de pagina a la url
            print("\n" + html + "\n") #Se impime en consola la pagina que se trabajará
            self.scanPage(requests.get(html)) #Se escanea la pagina

    def getNumPages(self):
        #Se obtendrá el número de la última página
        doc = lxml.html.fromstring(requests.get(self.html).content)
        pages = doc.xpath('//div[@class="numbered-pages-navi col-xs-12 col-sm-12 col-md-offset-7 col-md-4"]')[0] #Se obtiene el sitio donde se encuentran los botones de cambio de página
        numPages = pages[len(pages)-1].attrib['href'] #Se obtiene la url de la ultima página
        numPages = numPages.split('/')
        numPages = int(numPages[len(numPages)-2]) #Se obtiene el numero de la ultima página
        return numPages

    def generateXML(self):
        data = open('../Data/data.xml','w') #Se crea un archivo XML en la carpeta de Data dentro del proyecto
        print(etree.tostring(self.postsTree, pretty_print=True, encoding='unicode'),file = data) #Se guarda el árbol generado hasta el momento
        data.close()#Se cierra el archivo



ws = NextLineScrapper()
ws.scanSite()
ws.generateXML()
#ws.getComments('https://blog.nextline.mx/nuevo-ano-nuevas-metas/')

#print(etree.tostring(postsTree, pretty_print=True,encoding='unicode'))
