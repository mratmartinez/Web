---
Title:   Algunas notas sobre el desarrollo de mi blog (Parte 2)
Summary: Este si es posta.
Author:  Juan Martínez
Date:    2019-10-05
---

El post anterior no dice nada sobre la web, pero este sí. No tomó mucho tiempo hacerla (en total, re colgué algunos días).

Para hacerla, reciclé una que tenía en el 2016. El HTML fue "embellecido" (y ni tanto) y pasado a unos templates de Django. Para el estilo, a parte del pequeño CSS que tenía de antes, lo que hice fue buscar un framework en el sector "lightweight" de [esta lista](https://github.com/troxler/awesome-css-frameworks#very-lightweight) porque [Bootrstrap](https://getbootstrap.com/) tiene muchísimas más cosas de las que necesito.  
En un principio elegí [Pure](http://purecss.io), pero al final me decidí por otro llamado [Wing](https://kbrsh.github.io/wing/).

### Sobre Wing y otros frameworks

Como soy un asco con todo lo que involucre diseñar cosas bonitas tuve un mambo confuso para elegir entre cuando usar Flex y cuando usar el Grid de Wing.  
Usé [esta guía](https://medium.com/youstart-labs/beginners-guide-to-choose-between-css-grid-and-flexbox-783005dd2412) para saber qué decisión tomar.  
En caso de que no tengas ganas de leer (en inglés), la hago corta:  
    *Flex: Para cuando tenés que poner una sola cosa en un solo lugar. Se achica o agranda según sea necesario.  
    *Grid: Si tenés que poner bocha de cosas en fila. Las mueve sin que quede todo un desastre.

Este es un excelente momento para aclarar que se pueden usar grillas sin usar Wing, Bootstrap, Pure o cualquier otra chota [(fuera de joda hay un framework de CSS que se llama así)](https://jenil.github.io/chota/), utilizando las grillas nativas de CSS. De hecho, todos estos frameworks están hechos encima de ese sistema pero solo adaptado a clases para que sea más sencillo usarlos y no tengas que entender los conceptos necesarios para usar las que vienen por defecto. Es decir, si te interesa aprender más de frontend o tu proyecto no es lo suficientemente grande como para usar Bootstrap, se recomienda usar las que vienen por defecto. Como mi proyecto no es gran cosa y por ahora no quiero saber más de frontend, voy a seguir usando Wing. Pero algún día, si me despierto inspirado, aprenderé a usar las grillas de CSS y dejaré linda mi web.

### El Markdown

Para el que no sabe lo que es el Makrdown, lo explico rápido y sencillo:  
Makrdown es un lenguaje de marcado (como HTML) pero que en lugar de usar etiquetas como "<h1>Un header</h1>", usa alternativas que son más legibles para el ojo humano. Por ejemplo, para separar un parrafo de otro, se deja una línea en blanco. O para marcar un salto luego de una línea, se la finaliza con "  " (sí, dos espacios).  
Me encanta la sintaxis para insertar links:

~~~
[Esto es un link a mi nuevo dominio](https://juanci.to)
~~~

Como verán, es una alternativa muy buena a escribir directamente en HTML, donde este ejemplo se traduciría como:

~~~
<a href="https://juanci.to">Este es un link a mi nuevo dominio</a>
~~~

#### ¿Por qué Markdown y no BBCode?

Me encanta BBCode y pensé en usarlo, pero no sé si por gusto o solo porque crecí escribiendo en foros donde eso era lo que único que se usaba. Pero siendo realista, escribir BBCode a mano es embolante al lado de Markdown. A parte, usar esta tecnología no fue mi decisión, yo simplemente quería un blog lo más sencillo posible y me creé uno en Jekyll.

Jekyll es un generador de blogs estáticos. Está hecho en Ruby y lo único que tenés que hacer para que funcione es darle un archivo con un nombre como este: ´2018-05-14-instalando-el-vps-para-el-blog.md´ que incluya todo el texto de tu post en Markdown.

Mi idea era "transplantar" estos posts de Jekyll sin hacerme mucho drama con el formato, entonces lo que hice fue usar [django-markdown-editor](https://github.com/agusmakmun/django-markdown-editor), un plugin para Django que no solo permite tener un editor para markdown desde el admin, sino que también trae un template tag para renderizarlo a HTML sin ningún truco raro.  
Para ser honesto, estuve sorprendido de que haya funcionado a la primera.

### La revelación

Un día me desperté más vivo que de costumbre y me pintó rehacer lo poco que tenía mi web en Flask. La razón era que estaba viendo bocha de ofertas laborales en Flask y me viene bárbaro. De hecho, elegí Django porque era lo que encontraba que se pedía mucho hace unos años.  
Decisión razonable o no, fue genial.

Primero que nada, Flask es una huevada. Creo que cualquiera que sepa Python básico puede usarlo y no cuesta nada.  
Flask no trae nada y eso es algo que para mí es muy divertido.

Por ejemplo, para el temita del Markdown que mencioné recién probé 2 módulos que ya estaban hechos para Flask. Uno es [Flask-Misaka](https://flask-misaka.readthedocs.io/en/latest/) que la verdad que ya no recuerdo que problema tuve con ese, y el otro es [Flask-Markdown](https://pythonhosted.org/Flask-Markdown/) que se negaba a cargar la extensión ´fenced-code´ que para mí es importante.

#### ¿Qué tiene de bueno si no te anduvo nada?

Eso es lo genial. No me costó nada implementar lo que necesito por mi cuenta y a mi medida.  
Mi blog anterior (el de Django) tenía un admin donde podía escribir en Markdown, tenía soporte para varios usuarios, y cada post se guardaba en un SQLite.  
¿Necesitaba yo todo esto? Nah, ni ahí.  
Mi idea era seguir escribiendo como escribía en Jekyll, que es de la misma manera en la que escribo todo: desde NeoVim y subiendo a un repositorio Git. Eso era algo que me desmotivaba de tener un admin y una base de datos. Se perdía ese espíritu de web estática y minimalista que yo tanto quería seguir manteniendo.  
¿Por qué querría tener soporte para varios usuarios si arriba dice "Juancito"? ¿Por qué habría otro autor acá a parte de Juancito? ¿Por qué hablo de Juancito en tercera persona? Estas son preguntas sin respuesta.

Django está muy bueno. Es un CMS completo, pulido y seguro, y eso sin mencionar la comunidad tremenda que tiene. Pero si no vas a usar todo o la mayoría de las cosas que ofrece, puede que sea una solución incómoda. Y si querés algo muy sencillo, esa estructura que te ofrece puede ser contraproductiva. Al menos así lo fue en mi experiencia.

Django requiere que sepas que es lo que el framework hace y como lo hace, y requiere que te adaptes a él. Flask, en cambio, requiere que sepas que el framework no hace casi nada, pero que se adapta.

### ¿Y ahora?

Probablemente te estés preguntando, ¿cuál es el punto de este post?  
Nada. La verdad que hice esta web porque no puede ser programador y no tener una, así que me da un poco de seguridad a la hora de ponerme a mandar CVs.

Tengo 3 planes con este blog para el futuro:  
1) Comenzar una serie de posts sobre como aprender (aunque sea una base) de programación. Tengo muchas amistades a las que me gustaría apuntar en eso.  
2) Escribir sobre Mapuche. Es una gilada pero me entretiene.  
3) Ponerlo en mi CV y buscar laburo. Si estás viendo esto y me podés ofrecer un puesto:
![](/static/help.jpg)
