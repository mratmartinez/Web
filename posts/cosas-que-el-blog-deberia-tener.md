---
Title:          Cosas que el blog debería tener.
Summary:        Un post sobre la clase de huevadas que quiero hostear. English TL;DR at the end of the post.
Author:         Juan Martínez
Category:       Computers
Tags:           Web
                Software Development
		CSS
		HTML
		Python
		Flask
Language:       ES
Date:           2020-01-10
---

Quiero arrancar un lindo año, por eso me voy a poner un toque las pilas con la presentación del blog. No quiero que sea más lindo, quiero que sea lo necesario.  
La verdad que nunca aclaré mucho lo que iba a escribir acá. Yo solo tengo esta página para que parezca que soy un toque profesional y para hacer un poco de bulto en el currículum. Si alguien realmente se pusiera a leer esto probablemente desistiría de la idea de contratarme.

Así que este post se trata de darle un poco de explicación a por qué hago las cosas como las hago. También para que no se note que me da alta paja escribir y que por eso hay solo 2 entradas en toda la web.

#### Lo que tiene (y podría ser mejor)

En este momento si tengo que definir tecnicamente esta web diría que es solamente una app de Flask que renderiza Markdowns y los muestra estaticamente. Es sencillo, pero hay cosas que ya estoy haciendo y que podría hacer mejor:  

* Estoy guardando los Markdowns en el sistema de archivos a mi manera cuando podría aprovechar algo como Flask-Caching que incluso tiene una solución de cache en sistema de archivos (muy parecido a lo que hago actualmente).  
* Que los posts puedan ser modificados en la web directamente (y/o tener una API para subir desde curl, eso es más canchero).  
* Que se muestre la última vez que un post fue editado.  
* El CSS está medio baqueteado con cosas que hice al voleo en 2016.  
* No quiero usar ningún framework de CSS.

#### Lo que le falta (además de contenido)

* Me gustaría un área donde la gente con cuenta pueda entrar. Esto es más que nada para pasarle anotaciones y borradores a conocidos.  
* Que se pueda elegir el idioma, así puedo postear en inglés algunas cosas más interesantes y que no se mezcle con giladas como esta.  
* Un lugar donde pueda poner links que me gustaron.  
* Ayer, en un grupo de Whatsapp un pibe preguntó como revisar la validez de una string para que al usar slugify no quede vacía. No es complicado, pero me hizo darme cuenta de que no lo hice acá. Así que ese es el primer bug fix del año.

### ¿Cuál es el razonamiento para estos cambios?

Obvio que la mayoría son caprichitos que quiero en mi código. Pero también quiero mantener cosas a manera de filosofía.  
Este blog **no va a tener**:  

* Anuncios. Porque no quiero.  
* Scripts de Google (excepto algún que otro video de Youtube embebido). Ni va a aparecer en el buscador, porque eso no importa.  
* La menor cantidad de Javascript que pueda. Probablemente ponga algo de analytics sencillo pero no mucho más.  
* Pocas dependencias. No quiero que esta web se muera de la nada porque una actualización me rompió todo. Tampoco es una muy buena práctica el hacer todo desde cero como hago yo, pero por lo menos es divertido y de eso se trata la vida (la mía al menos).

### Reflexiones

Como no tengo nada más que decir voy a agarrar [este artículo](https://jeffhuang.com/designed_to_last/) de un profesor de *andá a saber qué* en *andá a saber dónde* (ni ganas de stalkearlo) que dice que su web es re piola y sencillita y que por eso va a durarle bocha. Él enumera 7 puntos por los cuales eso va a pasar y que vos también tenés que respetar si querés que tu web viva más que vos. Sus argumentos son más o menos como lo que dije arriba pero un toque (bastante) más rebuscado.

Él dice lo siguiente:  

1. **Vanilla HTML y CSS**: Es la tercera vez que digo que estoy de acuerdo con esto, literalmente una vez por cada post de este blog. Posta que Bootstrap es overkill si lo único que querés es diseño responsivo.  
2. **Que no minimices el HTML**: Parcialmente de acuerdo. Esto no tiene nada que ver con la durabilidad de la web, el profe acá descarriló del tema, pero su argumento simplemente se basa en que esto antes no se hacía y que por lo tanto debe ser bueno, cuando no afecta realmente en nada. Lo unico que cambia es que ya no podés entrar a leer el código HTML de la página como podías hacer en el 2007 y ver giladas. Está bueno que el HTML sea lindo, pero el único que estaría tan al pedo como para leerlo es Richard Stallman, y él no va a entrar acá. Ni siquiera soy yo quien escribe la mayoría del HTML de esto; yo uso Markdown y después mi código hace el resto.  
3. **Tener una sola página en vez de muchas porque es más fácil de mantener**: Depende de cada uno. A mí me chupa un huevo, para eso está [Jinja](https://jinja.palletsprojects.com/en/2.10.x/).  
4. **Terminar con el hotlinking**: Estoy de acuerdo. Hasta me siento un poquito culpable linkeando al server del framework de CSS que uso, pero como dije, lo voy a sacar a la mierda. También estoy seguro de que no les estoy consumiendo mucha red. Por cierto, este punto es el segundo que hace que tiene que ver realmente con la durabilidad de una web.  
5. **Usá las fuentes que vienen por defecto y no te hagas el canchero con las de Google**: Parcialmente en desacuerdo. Usá las fuentes que quieras, pero hostealas vos, si no lo hacés es exactamente lo mismo que dice el punto anterior.  
6. **Comprimí las imágenes**: No podría *no* estar de acuerdo. Acá hay gente que va creer que el autor de ese artículo se está contradiciendo porque no quiere que se reduzca el HTML pero sí las imágenes. Recordemos que el punto del HTML era solo porque el tipo tenía el capricho de leer el código. Yo creo que está bárbaro que la gente quiera comprimir *todo* sin distinciones. La optimización es buena, quiero que un webmaster sea gentil con la gente que no tiene tan buen internet. Odio esas páginas fieras que pesan 100MBs cuando principalmente solo quiero leer el texto.  
7. **Darte cuenta cuando está caída la web**: Obvio. Lamentablemente el autor acá hace una cosa muy estúpida. No solo tiene un servicio que monitorea que su web esté funcionando. Tiene un segundo servicio que le informa en caso de que el primero falle. Todo bien con ser precavido, pero esta web la hice para que figure en mi currículum nomás. Si se cae me chupa un huevo, me enteraré cuando pase. Además, meses sin darle mucha bola y todavía no se cayó. Me relajo.

Bueno, el señor solo escribió 2 cosas que tienen que ver con que una web pueda perdurar en el tiempo y, en resumen, es lo mismo de siempre: minimalismo.  
Evitar el hotlinking, las fuentes de Google o un framework de CSS es lo mismo que decir que te ahorres las dependencias innecesarias que pueden morir cuando un tercero se aburra de mantenerlas por vos. Nunca hay que permitir que te quiten el control de tu propio código (**Stallman intensifies**). Si estás dependiendo mucho de una librería misteriosa que lo único que hace es generarte una URL válida, [implementalo vos mismo y cagate de risa](https://github.com/mratmartinez/Web/commit/fb2837c71b7a5c7febb55b436ae5ce9c07c30f27) aprendiendo en el proceso.

#### La autosuficiencia

Como habrá quedado claro, el minimalismo en las funcionalidades y las dependencias no es solo por una cuestión de mantenimiento y preservación, es algo hasta filosófico (ahre). También está la gloriosa satisfacción de saber que comprendés todo tu proyecto y que si se rompe algo vas a tener todo en un solo lugar donde encontrar el problema.

Eso, sumado a la tranquilidad de saber que no tengo que pagar AWS.

Y termino el post acá nomás porque me importa todo un carajo.  
Procuraré escribir un post nuevo cada 2 meses. Es una banda eso para mí, no me apuren.


### English TL;DR

In case you are reading this and wondering what the hell I'm talking about because it's all written in spanish with a lot of slang:

1. More features for this web! Once I finish all of these things I'll start posting in english too. Stay tuned!  
2. Some directives about how this blog will be developed (without hundreds of dependencies, as little Javascript as possible) and what to expect from it.
3. Cool stuff that I didn't write in the spanish section: I'll be hosting my own Git here so I can ditch Github, and there'll be a post about how to do that.

Here are some posts I expect to write, *both in spanish and english*, in the (not that near) future:

* One about hosting your own e-mail service.
* Docker best practices.
* A post about why PyQt is better than the original Qt and how to port your widgets from the C++ to Python.
* **A lot** of posts about nice stuff on Linux. Arch and Gentoo users, stay tuned you too!
