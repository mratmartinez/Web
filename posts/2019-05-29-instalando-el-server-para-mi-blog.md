---
Title:   Algunas notas sobre el desarrollo de mi blog (Parte 1)
Summary: Un artículo en el que amago con escribir cosas sobre este blog pero al final no digo (casi) nada al respecto.
Author:  Juan Martínez
Date:    2019-05-29
---

**Buenas noches**, es de magrugada y estoy empezando este blog (actualmente en Jekyll) porque tengo algo sobre que escribir.

Hoy, después de cenar, mi mamá me regaló un VPS durante un año, el más simple que encontré, que es más que suficiente. Y como lo único que tengo es este feo sitio estático hosteado en Github Pages decidí que era un buen momento para programarme un blog propio, tal vez hecho en Flask o Django.

Primero voy a incluir todo lo del mambo de **sysadmin**, pues eso es lo primero que quiero es asegurarme. Que el server esté lo más seguro que pueda, y obviamente, sea apto para comenzar cómodo con mi workflow.

Actualizando, creando user, y... ¿revisando logs?
---------------------

Comencé por actualizar el sistema aprovechando que estaba en root.  
Creé un user para trabajar de manera segura y dejo el server corriendo sin darle atención. 3 horas después regreso a casa y se me ocurre aprender un poco de systemd (en el Gentoo que tengo en mi PC uso OpenRC).

Casualmente se me ocurrió ver los logs para llevarme la sorpresa de que aún siendo el server nuevo, hay alguien intentando acceder a él por fuerza bruta a travéz del SSH.

Acá les dejo un cachito de mis logs (sacados de **journalctl**):  
~~~
May 14 01:41:38 vps43947294.local sshd[2784]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.92.0.144  user=root
May 14 01:41:40 vps43947294.local sshd[2784]: Failed password for root from 218.92.0.144 port 59597 ssh2
May 14 01:41:43 vps43947294.local sshd[2784]: Failed password for root from 218.92.0.144 port 59597 ssh2
May 14 01:41:45 vps43947294.local sshd[2784]: Failed password for root from 218.92.0.144 port 59597 ssh2
May 14 01:41:48 vps43947294.local sshd[2784]: Failed password for root from 218.92.0.144 port 59597 ssh2
May 14 01:41:50 vps43947294.local sshd[2784]: Failed password for root from 218.92.0.144 port 59597 ssh2
May 14 01:41:53 vps43947294.local sshd[2784]: Failed password for root from 218.92.0.144 port 59597 ssh2
May 14 01:41:53 vps43947294.local sshd[2784]: error: maximum authentication attempts exceeded for root from 218.92.0.144 port 59597 ssh2 [preauth]
May 14 01:41:53 vps43947294.local sshd[2784]: Disconnecting: Too many authentication failures [preauth]
May 14 01:41:53 vps43947294.local sshd[2784]: PAM 5 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.92.0.144  user=root
May 14 01:41:53 vps43947294.local sshd[2784]: PAM service(sshd) ignoring max retries; 6 > 3
~~~

Y así sigue un buen rato. Al rato volvió con otra IP:  
~~~
May 14 04:56:17 vps43947294.local sshd[4310]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.92.0.209  user=root
May 14 04:56:20 vps43947294.local sshd[4310]: Failed password for root from 218.92.0.209 port 17284 ssh2
May 14 04:56:23 vps43947294.local sshd[4310]: Failed password for root from 218.92.0.209 port 17284 ssh2
May 14 04:56:25 vps43947294.local sshd[4310]: Failed password for root from 218.92.0.209 port 17284 ssh2
May 14 04:56:25 vps43947294.local sshd[4310]: Received disconnect from 218.92.0.209 port 17284:11:  [preauth]
May 14 04:56:25 vps43947294.local sshd[4310]: Disconnected from 218.92.0.209 port 17284 [preauth]
May 14 04:56:25 vps43947294.local sshd[4310]: PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=218.92.0.209  user=root
~~~

Bueno, por si no se entiende:  
`vps43947294.local` es el hostname por defecto que tiene el VPS.  
`sshd[2784]` es el proceso que escribe en el log y su respectivo PID.  
`pam_unix(sshd:auth): authentication failure;` dice que hubo un error de autenticación (gracias al cielo, y al equipo de OpenBSD que hizo OpenSSH).  
`rhost=218.92.0.144` es la (aparente) dirección de IP del intento de intruso. Según iplocation.net, esa IP es de China, un país muy habitual entre los proxy servers.  
`user=root` quiere decir que está tratando de acceder (logicamente) a la cuenta de root para obtener permisos administrativos.  
Luego, en un lapso de 13 segundos ingresó contraseñas incorrectas 6 veces hasta que fue desconectado por el servidor. Ahí pasa algo interesante, PAM (voy a asumir que sabés que es) decide ignorar la configuración de sshd y bajar el número de intentos de 6 a 3.  
Pueden fijarse en el ejemplo siguiente que a pesar de haber cambiado la IP luego de 3 horas sigue desconectándolo al tercer intento.

Después vemos la configuración del server SSH, el intruso todavía tiene para rato intentando averiguar la pass.

Instalando Ansible (BONUS: Mis problemas con el niceness value)
---------------------

**Aclaración**: Si alguien entra a estos posts esperando un tutorial, se equivoca. Yo solo cuento mi mambo. Espero que le guste.

Culpa de un error mío (algo que me suele pasar con frecuencia, de hecho) casi pierdo todo lo que escribí hasta este punto.  
Mi computadora se tildó (sí, eso puede pasar en Linux por si te han dicho que no como excusa para que te cambies) porque dejé compilando Ansible en Gentoo mientras escribía, sin percatarme de que no subí el niceness. Esto me obligó a reiniciar mi laptop. El archivo lo recuperé gracias al buffer de Neovim (ubicado en `~/.local/share/nvim/swap/`).

"¿Qué es el niceness?", se preguntarán.  
Se traduce del inglés como "amabilidad", y es exactamente eso. Es un valor para definir que tan amable es tu proceso con los otros en lo que respecta la prioridad de cada uno.  
Esto lo decide el scheduler automáticamente en base al valor de niceness que tiene cada proceso. Dicho valor puede ir desde -20 hasta 19, y el valor por defecto de todos los procesos es 0.  

En Debian, por ejemplo, puedo poner `nice -n 12 apt-get upgrade` y va a actualizar el sistema con normalidad, pero el proceso que inicia tiene menor prioridad para el sistema que el resto de los que se ejecutan.  
En Gentoo, el gestor de paquetes mismo incluye una variable para interferir en el niceness de todos los procesos que inicia. En mi caso puse `sudo PORTAGE_NICENESS=14 emerge --resume` para continuar lo que estaba compilando pero pidiéndole a Portage que sea gentil (con 14 de niceness) y que me deje seguir trabajando en otras cosas mientras compila.

Después de esto me topé con otro problema, esta vez en Debian.  
Luego de agaregar el PPA de Ansible, que es el mismo para Ubuntu, necesitaba conseguir la clave para verifiar el firamdo del paquete oficial.  
Ejecutar `apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367` me dio un error muy claro: **no tenía `dirmngr`**.  
Esto se soluciona muy fácil (instándolo, `apt-get install dirmngr`) y tiene una explicación razonable: `gnupg` en Debian no incluye a ese paquete como dependencia, sino como recomendado. La razón la dieron en [este bug report](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=845720) y es que esa dependencia es necesaria unicamente en las funcionalidades de red. Todas las demás capacidades locales del programa funcionan sin problemas sin eso, pero debemos instalarlo para esta clase de cosas. Aunque, ya que tengo la clave, voy a desinstalarlo hasta que sea necesario nuevamente.

«*Six-teen-twelve, that's the code to my heart!*» (Asegurando OpenSSH)
---------------------

Como Ansible depende de SSH, estaría bueno que ande bien desde el principio. Para eso voy a guiarme mayormente de lo que dice el [Manual de Seguridad de Debian](https://www.debian.org/doc/manuals/securing-debian-howto/ch-sec-services.en.html#s5.1) para editar el archivo `/etc/ssh/sshd_config`.

Primero que nada, voy a cambiar el puerto del SSH. Mi puerto alternativo va a ser el 1612, [como la canción de Vulfpeck](https://www.youtube.com/watch?v=TiiWR6436Eg). Escuchenlos porque son tremendos.  
Esto de ninguna manera es una medida de seguridad eficiente. Solo lo uso como filtro para reducir las posibilidades de un tontolo automatizado floodeandome los logs como el de hoy.  

Segundo, hay que desactivar el root desde SSH. La opción para hacerlo es `PermitRootLogin no`.  
La opción `MaxAuthTries` la puse en 3, estando en 6 previamente.  
También deshabilito `X11Forwarding` porque no voy a instalar nada relacionado a X11 en este VPS (y probablemente en ningún otro).  

Luego de editar estas cosas básicas, me creé una clave SSH nueva para el VPS, usando `ssh-keygen -t rsa -C "mratmartinez@anche.no"`.  
Para subir la clave al VPS lo único que hay que hacer es `ssh-copy-id -i ~/.ssh/id_rsa.pub username@server.org` obviamente reemplazando el archivo por su clave pública y el host correspondiente.

Ahora que tengo otro método de login, en `sshd_config` coloco `PasswordAuthentication no`. Explico como funciona esto:  
1) SSH siempre trata de acceder primero usando las claves criptográficas como las que generamos.  
2) Si eso falla (o sea, con casi todo mundo) entonces sí se pide la contraseña de la cuenta a la que queremos acceder.

Con esto deshabilitamos esta segunda parte, porque confiamos en que yo siempre voy a tener la clave (y es la razón por la cual tengo que cuidarla bien).

*[VPS]: Virtual Private Server
*[SSH]: Secure Shell
*[PPA]: Personal Package Archive
*[PID]: Process ID
