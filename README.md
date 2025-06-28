
# Elections Scraper

## Popis projektu

Tento projekt slouží k extrahování výsledků parlamentních voleb z roku 2017. Scraper stáhne data vždy pro zvolenou oblast. Výsledky jsou extrahovány z tohoto [webu](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102).


## Instalace knihoven

Knihovny, které jsou použity v kódu najdeš v souboru requirments.txt. Pro instalaci knihoven doporučuji použít nové virtuální prostředí, aby knihovny z tohoto projektu neovlivnily tvé jiné projekty. Knihovnu můžeš do svého virtuálního prostředí nahrát prostřednictvím terminálu a následujícíhopříkazu:

$ pip install -r requirements.txt

## Verze Pythonu

K funkčnosti je třeba mít nainstalovánp verzi Pythonu 3.8+

## Spuštění projektu 

Spuštění projektu main.py a získání dat v rámci příkazového řádku požaduje 2 povinné argumenty:
1) Odkaz na územní celek, který chceš scrapovat z výše uvedené URL. Tento odkaz zkopíruj ze sloupce 'Výběr obce', který se nachází pod znakem X.
2) Název výstupního CSV souboru s koncovkou .csv.

Příklad použití:

$ python main.py <URL_okresu> <vysledky_voleb.csv>

Reálný příklad pro obec Hodonín:

$ python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205 <Hodoninsko_volby.csv

#### Dej pozor! Příkazový řáadek nemusí zadaný argument URL přečíst správně v případě, že obsahuje znak "&". Pokud URL tento znak obsahuje je potřeba URL dát do uvozovek. 

Spuštění programu:

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205" Hodoninsko_vysledky.csv

Průběh stahování:  
Zpracováno: Archlebov (1/82)  
Zpracováno: Blatnice pod Svatým Antonínkem (2/82)  
Zpracováno: Blatnička (3/82)  
Zpracováno: Bukovany (4/82)  
Zpracováno: Bzenec (5/82)  
Zpracováno: Čejč (6/82)  
Zpracováno: Čejkovice (7/82)  
*  
*  
*  
Zpracováno: Vracov (75/82)  
Zpracováno: Vřesovice (76/82)  
Zpracováno: Žádovice (77/82)  
Zpracováno: Žarošice (78/82)  
Zpracováno: Ždánice (79/82)  
Zpracováno: Želetice (80/82)  
Zpracováno: Žeravice (81/82)  
Zpracováno: Žeraviny (82/82)

Hotovo! Data byla úspěšně uložena do: Hodoninsko_vysledky.csv


## Výsledek
Výsledný CSV soubor obsahuje pro každou obec ve zvolené oblasti:  
kód obce  
název obce  
voliči v seznamu  
vydané obálky  
platné hlasy  
kandidující strany (co sloupec, to počet hlasů pro stranu pro všechny strany).

Ukázka výstupu CSV souboru [ZDE](https://github.com/Zuziknows/3_projekt/blob/main/hodoninsko_vysledky.jpg)
