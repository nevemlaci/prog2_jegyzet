# Operator overloading - Osztályok nélkül

## Mik az operátorok valójában?

Az operátorok valójában csak speciális függvények. Ez azt jelenti, hogy ugyanúgy bánhatunk velük, habár van némi megkötés, azonban legtöbbször ezek nem fognak az utunkban állni. 

Az operátorokra függvényként hivatkozhatunk, túltöltésük "szintaxisa" is ezen alapszik. pl. `+` operátor: `operator+`.

## Egyszerű operátor példa

Hozzunk létre egy komplex számot modellező struktúrát:
```cpp
struct Komplex{
    double re, im;
};
```

Két komplex számot szeretnénk a `+` operátorral felülírni. Ehhez az `operator+` függvényt kell túlterhelni úgy, hogy az egy komplex számot adjon vissza és két komplex számot kapjon paraméterként, pl. `Komplex operator+(const Komplex&, const Komplex&)` :

[ Futtasd! ](<https://godbolt.org/z/dexTfaWG3>){ .md-button target="_blank"}
```cpp
Komplex operator+(const Komplex& k1, const Komplex& k2){
    Komplex result;
    result.re = k1.re + k2.re;
    result.im = k1.im + k2.im;
}

int main(){
    Komplex k1;
    k1.re = 4;
    k1.im = 2;
    k2.re = 1;
    k2.im = 0;

    Komplex eredmeny = k1 + k2;
    std::cout << eredmeny.re << " + " << eredmeny.im << "i";
}
```

A háttérben az operátor hívás így néz ki:

```cpp
Komplex eredmeny = operator+(k1, k2);
```

