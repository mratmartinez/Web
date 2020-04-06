---
Title:          Traducir es un garrón.
Summary:        Un pequeño rant sobre traducir fechas.
Author:         Juan Martínez
Category:       Computers
Tags:           Web
                Software Development
		Python
        C
        General Computing
Language:       ES
Date:           2020-04-05
---

Sé que dije que iba a escribir 2 posts mensuales en este blog. Pero bueno, no suelo cumplir promesas asociadas al tiempo.  
Escribo esto porque me acordé que tenía muchas actualizaciones del código del blog y tenía que ponerlas en el server pero me colgué. Cuando agarré ese código me encontré con lo mismo que encuentro siempre que abro un código mío de más de 2 semanas de antigüedad: decisiones de diseño horribles.  
No sé si aprendo muy rápido o sí es que me odio mucho siendo consciente de que *soy una vergüenza para la sociedad*. Probablemente sean ambas.

#### Febrero

En febrero estaba en mi laburo anterior, tenía un cargo de **DevOps Engineer**. ¿Alguna vez escucharon el rumor de que los sysadmins se rascan las pelotas? Bueno, es posta.  
Cuestión que era un miércoles como cualquier otro en el que estaba en la oficina muy ansioso. ¿Por qué? Porque estaba al pedo y tenía que estar ahí 10 horas. Entonces me daba alto cagazo ver a los demás que sí tenían responsabilidades y yo ahí que no quería parecer (o demostrar ser) tan innecesario en la mayor parte del día.  
Entonces lo que hacía para parecer que estaba muy ocupado era programar mi web. Los demás pasaban y miraban mi pantalla con una terminal del WSL2 (me obligaban a usar Windows en esa empresa) con Vim abierto y puro código. Ese era el lado productivo de ir a un lugar público: Cuando estoy así libre en mi casa veo algún animé, en la oficina no era tan descarado como para hacerlo.

Cuestión que programé mucho código para este blog. Detallitos lindos, planes para el futuro lejano, novedades que me parecen piolas. Creo que en la posterioridad (cuando me pinte darle bola a esto) la plataforma resultante va a quedar bastante cheta.  
Cosas que hice / empecé / planeé:

* Categorías.  
* Como (creo que) mencioné anteriormente, cambié el caching y ahora el código es bastante más corto.  
* La traducción de posts.

Lo de la traducción no lo hice, porque para ello tendría que haberme tomado la molestia de traducir un post y la verdad que es una tremenda paja.  
Pero había dejado todo preparado para cuando me dieran ganas. ¿Cómo?  
Primero que nada dejando una variable en los posts especificando los idiomas disponibles. Y, segundo, agregando la fecha de publicación (cosa que debería de haber estado desde un principio).

El asunto es que como el locale del server está en inglés, cuando quería convertir un timestamp como "2020-01-04" en "Sábado 04 de Enero de 2020", esto resultaba en "Saturday 04 de January de 2020". Una tremenda mierda. Entonces lo que hice fue cambiar de locale usando una sola línea en Python: `locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")`.


#### Abril

Resulta que en marzo leí uno de los mejores commits de la historia de Git. Es uno de un tipo que se queja de [la idea de los locales en libc](https://github.com/mpv-player/mpv/commit/1e70e82baa9193f6f027338b0fab0f5078971fbe). Ojalá nunca tenga que estar tan indignado como para hacer un rant en un commit de Git.  
Uno de los argumentos suyos es que es un garrón tener que definir un locale global que afecta al resto del código, dejandote con una suerte de estado que puede ser muy confuso y que puede contribuir a errores inesperados.

Él lo dice así:  
(Nota: la expresión "shitfucked" está en todos lados ahí)  
~~~
This is shitfucked on its own, because it's GLOBAL STATE to configure that GLOBAL STATE should not be GLOBAL STATE, i.e. completely broken garbage, because it requires agreement over all modules/libraries what behavior should be used. I mean, sure, makign setlocale() affect only the current thread would have been the reasonable behavior. Making this behavior configurable isn't, because you can't rely on what behavior is active.)
~~~

Entonces, para cuando revisé el código y encontré que había usado locales, me sentí indignado conmigo mismo. Tranquilos, me hubiese enfurecido conmigo mismo por alguna otra razón de todos modos.  
Pero por lo menos encontré una solución más llevadera, que no depende de decisiones de diseño lamentables con las cuales cargamos desde C: Babel.  
Babel, como supondrán por el nombre, es una librería que sirve para facilitar esas cosas de traducción.

Afortunadamente, tiene algo como [lo que estoy buscando](http://babel.pocoo.org/en/latest/dates.html): Un método de formateo de fechas al cuál le pasás el idioma que buscás entre los argumentos y te devuelve lo que necesitás.

Y bueno, eso es todo.  
De la misma manera en hacer un buen remate para un chiste es dificil, me es complicado saber cerrar estos threads.  
Así que si no les gusta vayanse a la mierda, giles. ¿Qué pija hacen leyendo este blog del orto?  

Cariñitos,  
Juan <3

PD: Renové el dominio de la web por 5 años más.  
Me gusta creer que a algún otro hispano llamado Juan le van a dar ganas de que su web sea "juanci.to" y va a revisar para encontrarse con que hay otro Juan más capo que lo hizo antes. Ponele.
