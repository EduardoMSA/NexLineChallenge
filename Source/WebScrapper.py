import requests
import lxml.html
from lxml import etree

html = requests.get('https://blog.nextline.mx/')
doc = lxml.html.fromstring(html.content)

posts = doc.xpath('//div[@class="posts"]')[0] #se espesifica la posicion 0 para que no regrese como lista, aunque sea un solo elemento siempte
post = posts.xpath('//div[@class="grid-element col-xs-12 col-sm-12 col-md-6"]')

def getPost(post):

    postTree = etree.Element("Post") #XML donde se guardará el post

    a = post[0] # Parte del post que contiene el articulo

    aTumbnail = a[0] #Parte del articulo que contiene la imagen y el número de Comentarios
    aText = a[2] #Parte del articulo donde esta el nombre, las categorias, la fecha y la direccion

    hComnts = aTumbnail[1][0][3][0][0].text != "0 Comentarios" #Bool para saber si hay comentarios en el post

    #Se crean los Elementos donde se guardaran los datos obtenidos del post

    categories = etree.Element("categories")
    date = etree.Element("date")
    title = etree.Element("title")
    href = etree.Element("href")



    for c in aText[0]:
        categories.append(etree.Element("v", category=c.attrib['title']))   #Se obtienen los nombre de todas las categorias

    date.append(etree.Element("v", date=aText[2].text)) #se obtiene la feha del post
    title.append(etree.Element("v", title=aText[1][0].text)) #se obtiene el nombre del post
    href.append(etree.Element("v", href=aText[1][0].attrib['href'])) #se obtiene el enlace del post

    #Se añaden los elementos al post
    postTree.append(title)
    postTree.append(date)
    postTree.append(href)
    postTree.append(categories)

    print(etree.tostring(postTree, pretty_print=True))

    return postTree



    #postTree = etree.Element("Post", category = catego, date = date, title = title, href = href)
for p in post:
    getPost(p)
    print()
