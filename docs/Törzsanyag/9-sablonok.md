# Sablonok (template)

!!! warning
    A sablon téma a jegyzetben átdolgozás alatt áll!

## Sablon alapok
A C++ egyik legnagyobb előnye a C-vel szemben a generikus programozási lehetőségekben rejlik. A jegyzetben már szerepelt az alábbi függvény:

<https://godbolt.org/z/86ae5adTr>
```cpp
//swap C++ -ban
void cpp_swap(int& x, int& y){
    int tmp = x;
    x = y;
    y = tmp;
}
```

Ezt a függvényt szeretnénk megírni, hogy működjön mindenféle típusra. Természetesen ez C tudással lehetetlen küldetésnek tűnhet, 
azonban a C++ templatek fő felhasználási módja éppen ez.


<https://godbolt.org/z/rrzMjYvK7>
```cpp
template <typename T> //sablondeklaráció, sablonparaméterek(itt T) felsorolása
void cpp_swap(T& x, T&y){ //cpp_swap<T> függvénysablon
    T tmp = x;
    x = y;
    y = tmp;
}
```

!!! danger "Figyelem!"
    
    A template definíciókat (explicit specializációkat kivéve) header fileokban kell megírni!
    Ez vonatkozik a függvénysablonokra és osztálysablonokra is.

    A miértjéről az alábbi (egyébként szintén általam írt) rövid article-ben olvashattok:
    [TCCPP Article](https://github.com/TCCPP/wiki/blob/60d51923ed1100c2ed76e68ece7f2a33db68bc46/articles/template-header.md)


A fent látható `cpp_swap` -ot *függvénysablon*nak hívjuk. Önmagában nem függvény, ahhoz "példányosítani" kell. Ez a gyakorlatban annyit jelent, hogy használjuk.

pl.
```cpp
int main(){
    int x = 6;
    int y = 2;

    // cpp_swap<T> függvénysablon példányosítása T=int sablonparaméterekkel
    cpp_swap<int>(x, y); //<int> <- sablonparaméter megadása

    std::cout << x << ' ' << y << '\n';

    float a = 7.3;
    float b = 1.2;
    cpp_swap<float>(a, b);
    std::cout << a << ' ' << b;
}
```

Amikor egy sablont példányosítunk adott sablonparaméterekkel, olyankor valójában fordításidőben kód generálódik az adott sablonparaméterek behelyettesítésével.
Pl.
```cpp
cpp_swap<int>(x, y); //cpp_swap<T> függvénysablon példányosítása T=int sablonparaméterekkel
```
esetén a
```cpp
void cpp_swap_int(int& x, int& y){ 
    int tmp = x;
    x = y;
    y = tmp;
}
```
kód generálódik. A `T` helyére mindenhol `int` kerül. Ezt a generált kódot nekük természetesen nem kell látnunk, vagy foglalkoznunk vele.

!!! warning

    A függvény neve nem garantáltan `cpp_swap_int` lesz, ennek a névnek eldöntése a fordító dolgam nekünk ezzel nem kell foglalkozni,
    csak példaként van itt.

A sablonparamétereket a fordító néha le tudja vezetni a kapott függvényparaméterekből (template parameter deduction).

Például:
```cpp
double a = 5.2;
double b = 1.2;
cpp_swap(a, b); //nem kell megadni, hogy double típus, mivel a és b double típusúak

cpp_swap<double>(a, x); //meg kell adni, hogy double típus, mivel a és x különböző típusúak, így a fordító nem tud dönteni
```

## Duck typing

A sablonokkal felmerül egy újabb kérdés: milyen típusokat fogadunk el? A válasz erre egyszerű: mindent, amivel a függvény kódja lefordul.

Ezt "duck typing" -nak hívjuk: *"If it walks like a duck and it quacks like a duck, then it must be a duck"*

Például nézzünk meg egy függvényt, ami megmondja két *valamiről*, hogy az első *valami* nagyobb-e, mint a második *valami*.

```cpp
template<typename T>
bool nagyobbe(T elso, T masodik){
    return elso > masodik;
}
```

Milyen típusokra működik ez a függvény?
Hát azokra, amelyek ezeket a feltételeket teljesítik:
* lemásolhatók (hiszen másolatként vesszük át őket)
* összehasonlíthatók a `>` operátorral

*Vegyük észre*: ezek pontosan azok a feltételek, amelyek ahhoz kellenek, hogy a kódban az adott típust T helyére beillesztve a kód leforduljon.

!!! note

    Természetesen ezeken a feltételeken lazíthatnánk, ha érték helyett konstans referenciaként vennénk át a paramétereket.

A sablonok korlátozására léteznek további technikák (SFINAE, concept), azonban ezek messze túlmutatnak a tárgy anyagán.

## Részleges specializáció

Tegyük fel, hogy szeretnénk ha egy adott sablon egy speciális módon működjön, ha egy adott típust kap. 
Például ha a swap függvényünk int-et kap, akkor írja ki, hogy "int", különben működjön normális módon.

<https://godbolt.org/z/zj1bfe5s9>
```cpp
template <typename T> 
void cpp_swap(T& x, T&y){ 
    T tmp = x;
    x = y;
    y = tmp;
}

template <> 
void cpp_swap<int>(int& x, int&y){ //specializáció a T=int esetre
    std::cout << "int ";
    int tmp = x;
    x = y;
    y = tmp;
}
```

## Osztálysablonok
Mint ahogyan a függvényekhez, az osztályokhoz is lehet sablonokat készítnei. 
pl.
```cpp
template <typename T>
class Foo{
public:
    T x;
};
```
Nagyon hasonlóan működik a függvényparaméterekhez, szimpla kódgenerálásról van szó. 
Ugynúgy működik velük a specializáció, valamint létezik a függvényeknél ismert sablonparaméter levezetés is,
ezt **C**lass **T**emplate **A**rgument **D**eduction (CTAD) -nek nevezik. 

!!! note

    A CTAD kicsit máshogy működik, mint az általános, függvényekre vonatkozó TAD. 
    Akit érdekel, annak ajánlom [Nina Ranns cppcon előadását a témával kapcsolatban](https://www.youtube.com/watch?v=pcroTezEbX8).


### Dinamikus tömb átírása template-re

!!! note

    Mivel az egész tömb egy osztálysablon lesz, így ez az egész header fileba fog kerülni.

Igazából ez nem egy bonyolult folyamat. Mindenhol, ahol az `int` mint tárolt típus szerepel, ott lecseréltük `T` -re.

!!! note
    Az új verzióban `const T&` -t veszünk át beillesztésnél.
    Egész számot olcsó volt másolni, de itt már nem ismerjük a típust.

```cpp
#include <cstddef> // std::size_t
#include <stdexcept> // std::out_of_range
#include <iostream> // std::cout


template<typename T>
class DinTomb{
    T* tomb; //pointer a dinamikus tömbre
    std::size_t meret; //a dinamikus tömb mérete

public:
    /**
     * @brief Default konstruktor, mindent 0-ra inicializál
     */
    DinTomb() : tomb(nullptr), meret(0) {}

    /**
     * @brief hozzáad egy új elemet a tömb végéhez. Nagyon hasonlít a C-ben megismert algoritmushoz, csak malloc-free helyett new-delete[] van
     * @param elem az elem amit hozzáadunk(lemásolható kell, hogy legyen)
     */
    void push_back(const T& elem) {
        T* uj_tomb = new T[meret + 1];
        for(std::size_t i = 0; i < meret; ++i){
            uj_tomb[i] = tomb[i];
        }
        uj_tomb[meret] = elem;
        delete[] tomb; // delete[], mert tömböt szabadítunk fel.
        tomb = uj_tomb;
        ++meret;
    }

    std::size_t size() const { return meret; }

    /**
     * @brief indexelő függvény
     * @param idx
     * @return referencia az adott indexen lévő elemre
     * @throw std::out_of_range, ha túlindexelés történik
     */
    T& at(std::size_t idx) {
        if(idx >= meret) {
            throw std::out_of_range("Tomb tulindexelve!");
        }
        return tomb[idx];
    }

    //ua. mint az előbb, csak konstans verzió
    const T& at(std::size_t idx) const { 
        if(idx >= meret) {
            throw std::out_of_range("Tomb tulindexelve!");
        }
        return tomb[idx];
    }

    ~DinTomb() {
        delete[] tomb; //destruktor felszabadítja a lefoglalt memóriát
    }
};

int main(){
    DinTomb<double> tomb; // így már megy double-ra is :D

    tomb.push_back(4.2);
    tomb.push_back(3.5);
    tomb.at(0) = 5.1; 
    std::cout << tomb.at(1);
    return 0; 
}
```

## Nem-típus sablonparaméterek

Sablonparaméterként átadható nem csak típus, hanem gyakorlatilag bármilyen más objektum is. Pl. a standard library egy típusa az `std::array`, amely első függvényparamétere a tömbben tárolt típus, második függvényparamétere egy pozitív egész szám, a tömb mérete.

```cpp
std::array<int, 5> tomb; //5 méretű int-eket tároló tömb
```

Ezt kódban a következőként "replikálhatjuk":
```cpp
template<typename T, std::size_t siz>
struct array{ // array<T, siz> "osztálysablon"(osztályok később)
    T belso_tomb[siz];
    //array implementáció...
};

template <int N>
void print_template_int(){
    std::cout << N << '\n';
}
```
Fontos azt megjegyezni, hogy a sablonok fordításidőben példanyosodnak, szóval minden sablonparaméternek fordításidőben konstansnak kell lennie.
pl.
```cpp
print_template_int<5>(); //ok
int x = 5;
print_template_int<x>(); //hiba, x nem fordításidejű konstans(const int x sem oldaná meg)
```