# Nagyházi tervezés, avagy így írjunk nagyházit.

A tantárgy egyik nagy követelménye egy nagyházi feladat elkészítése. Ez az oldal ennek a tervezéséhez nyújt segítséget, hiszen egy rosszul tervezett/elkezdett házi feladatot sokszor nehéz javítani.

## Dinamikus tároló tervezése

Minden házihoz szükséges lesz egy dinamikus tároló megtervezése. A legtöbb nyilvántartásos feladatban elég egy dinamikus tömb, esetleg láncolt lista (bár ezzel nehezebb dolgozni).

Mivel a legtöbb háziban nem megengedett az STL tárolók használata, ezért ezeket a tárolókat nekünk kell implementálni.

A házit érdemes a tárolóval kezdeni, ezzel utána lehet dolgozni. 

A tárolókat érdemes az alábbiak alapján elkezdeni:

* Tudjon minden típust tárolni (template)
* Lehessen bele elemeket beszúrni (ha a feladathoz kell, akkor megadott indexre)
* Lehessen belőle elemeket törölni
* Kezeljen minden memóriát, ne kelljen kívülről memóriát kezelni
* Ha lista, vagy egyéb "Node" alapú tároló, akkor ezeket ne kelljen kívülről piszkálni
* Ha dinamikus tömb, akkor mindenképp lehessen indexelni (ez listánál lassú, inkább iterátorokkal legyen megoldva)
* Lehessen iterátorokkal is lépkedni rajta, listánál főleg fontos

Ha heterogén tároló kell, akkor implementáljunk egyet, ami az előző pontok alapján implementált dinamikus tárolót használja.

A tároló implementálása nagyon fontos, hiszen ezután minden "hmm ebből több is kéne" problémát megoldottunk.

## Alapvető osztályok megtervezése


