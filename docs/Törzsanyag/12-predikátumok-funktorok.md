# Predikátumok

Van, hogy egy függvényt szeretnénk paraméterként átvenni.

Pl. írjunk függvényt, amely egy másik, predikátumfüggvény alapján megkeres egy elemet egy tömbben és visszaadja az indexét, vagy a tömb méretét(az első "invalid" elem indexét) ha nincs benne.

A predikátumfüggvény típusát akár ki is írhatnánk, de az csúnyán nézne ki: `bool(*)(const T&)`, vagy valami hasonló szörnyeteg, úgyhogy inkább template paraméterként átvesszük ezt a típust is, a fordító úgyis levezeti a függvényparaméterből.


[ Futtasd! ](<https://godbolt.org/z/h3xfrz7x1>){ .md-button target="_blank"}
```cpp
#include <iostream>
#include <array>

template<typename T, std::size_t N, typename P>
std::size_t find_elem(const std::array<T, N>& a, P predicate){
    for(std::size_t i = 0; i < a.size(); ++i){
        if(predicate(a[i])){
            return i;
        }
    }
    return a.size();
}

//egy példa predikátumfüggvény:

template<typename T>
bool isDivisibleBy2(const T& x){
    return x % 2 == 0;
}

int main(){
    std::array<int, 4> arr = {1, 3, 4, 5};
    std::cout << find_elem(arr, isDivisibleBy2<int>);
}
```

Mint látjuk, a `P` sablonparamétert valóban nem kell kézzel megadni, azt a fordító a kapott predikátumfüggvényből levezeti.

## Nem csak függvények...

A fenti példában a `P` típus helyére minden olyan típus beilleszthető, amely `bool` -t(vagy `bool`-ra implicit konvertálható típust) ad vissza és egy `const T&` -et vesz át paraméterként. Az a kérdés, hogy csak függvények elégíthetik -e ki ezt a követelményt.

Nos a válasz erre az, hogy nem, ugyanis a függvényhívás operátor túltölthető. Azokat az osztályokat amelyeknek van függvényhívó operátora *funktor*nak nevezzük.

A funktorok hasznosak, ha iterálás alatt valamilyen generikus függvénynek kell hívható objektumot átadni, azonban valamilyen állapotot (state) is szeretnénk nyilvántartani.

Pl. itt egy funktor, amelynek habár sok mindent nem csinál, példának jó lesz...

[ Futtasd! ](<https://godbolt.org/z/dGaEG3brT>){ .md-button target="_blank"}
```cpp
#include <string>
#include <iostream>

struct foo{
    foo() : x(0) {}

    void operator()(const std::string& str = "") {
        std::cout << "hello from foo, i've been called: " << x << " times before! You have said:" << str << '\n';
        x++;
    }

    private:
        int x;
};

int main(){
    foo f;
    f("hello!");
    f();
    f("bar");
}
```