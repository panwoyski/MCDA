Projekt zaliczeniowy z przedmiotu Optymalizacja Wielokryterialna
Autor: Tomasz Jonak

W projekcie zaimplementowane zostaly dwie metody wielokryterialne
    Topsis
    Electre IS

Informacje wstepne

Wymagane do rozruchu
Python 3.5 + paczki
    numpy
    itertools
    csv

Sposob uruchomienia
python3 mcda.py -m electre_is

Uruchamia metode Electre IS z parametrami z katalogu input_files/electre_test_input
Celem uruchomiena metody topsis nalezy podac odpowiednie sciezki do katalogu input_files/topsis_test_input

Sposob podania sciezek mozna wyswietlic za pomoca
python3 mcda.py -h

Kod zostal zaimplementowany uzywajac systemu Ubuntu 16.04 LTS, nie byl testowany pod zadnym innym systemem operacyjnym

Przykladowy rozruch programu mozna alternatywnie wykonac
TOPSIS
    cd topsis
    python3 topsis.py
ELECTRE IS
    cd electre_is
    python3 electre_is.py

gdzie katalogiem startowym jest katalog bazowy projektu
