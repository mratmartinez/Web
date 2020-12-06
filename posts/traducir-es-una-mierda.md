---
Title:       Traducir es un garrón.
Summary:     Un pequeño rant sobre traducir fechas.
Author:      Juan Martínez
Category:    Computers
Tags:        Web
             Software Development
             Python
             C
             General Computing
Language:    ES
Date:        2020-04-05
---

Sé que dije que iba a escribir 2 posts mensuales en este blog. Pero he concluído en que no soy bueno administrando mi tiempo. Se están tomando medidas al respecto.  
Escribo esto porque me acordé que tenía muchas actualizaciones del código del blog y tenía que ponerlas en el server, pero me colgué.  

#### Febrero

Primero que nada dejando una variable en los posts especificando los idiomas disponibles. Y, segundo, agregando la fecha de publicación (cosa que debería de haber estado desde un principio).

El asunto es que como el locale del server está en inglés, cuando quería convertir un timestamp como "2020-01-04" en "Sábado 04 de Enero de 2020", esto resultaba en "Saturday 04 de January de 2020". Una tremenda mierda. Entonces lo que hice fue cambiar de locale usando una sola línea: `locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")`.


#### Abril

Resulta que en marzo leí uno de los mejores commits de la historia de Git. Es uno de un tipo que se queja de [la idea de los locales en libc](https://github.com/mpv-player/mpv/commit/1e70e82baa9193f6f027338b0fab0f5078971fbe) generando problemas inoportunos porque afecta en partes donde no debería. Ojalá nunca tenga que estar tan indignado como para hacer un rant en un commit de Git.  
Uno de sus argumentos dice que es un garrón tener que definir un locale global que afecta al resto del código, dejandote con una suerte de estado que puede ser muy "confuso" si tenés otras dependencias que revisan eso, lo cual puede contribuir a errores inesperados.

Él lo dice así:  
~~~
This is shitfucked on its own, because it's GLOBAL STATE to configure that GLOBAL STATE should not be GLOBAL STATE, i.e. completely broken garbage, because it requires agreement over all modules/libraries what behavior should be used. I mean, sure, makign setlocale() affect only the current thread would have been the reasonable behavior. Making this behavior configurable isn't, because you can't rely on what behavior is active.)
~~~

Entonces, para cuando revisé el código y encontré que había usado locales, me sentí indignado conmigo mismo. Tranquilos, me hubiese indignado por alguna otra razón de todos modos. Pero luego de ver eso encontré una solución más llevadera: Babel.  
Babel, como supondrán por el nombre, es una librería que sirve para facilitar esos tejes raros de traducción.

Afortunadamente, tiene algo como [lo que estoy buscando](http://babel.pocoo.org/en/latest/dates.html): Un método de formateo de fechas al cuál le pasás el idioma que buscás entre los argumentos y te devuelve lo que necesitás.

Y nada, lo cambié y fue una gilada. Eso es todo. Venía a decir que es una boludez usar Babel y que, si tienen que hacer algo parecido, fíjense eso.
La verdad que ahora no sé como cerrar el thread, así que permítame preguntarle: ¿Qué carajo hace leyendo este blog? Vaya a hacer algo útil.

Cariñitos,  
Juan <3

PD: Renové el dominio de la web por 5 años más.  
Me gusta creer que a algún otro hispano llamado Juan le van a dar ganas de que su web sea "juanci.to" y va a revisar para encontrarse con que otro Juan le ganó. 33 de mano.

