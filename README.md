
# Elections Scraper

## Popis projektu

Tento projekt slouží k extrahování výsledků parlamentních voleb z roku 2017. Scraper stáhne data vždy pro zvolenou oblast. Výsledky jsou extrahovány z tohoto [webu](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7102).


## Instalace knihoven

Knihovny, které jsou použity v kódu najdeš v souboru requirments.txt. Pro instalaci knihoven doporučuji použít nové virtuální prostředí, aby knihovny z tohoto projektu neovlivnily tvé jiné projekty. Knihovnu můžeš do svého virtuálního prostředí nahrát prostřednictvím terminálu a následujícího příkazu:

$ pip install -r requirements.txt

## Verze Pythonu

K funkčnosti je třeba mít nainstalovanou verzi Pythonu 3.8+

## Spuštění projektu 

Spuštění projektu main.py a získání dat v rámci příkazového řádku požaduje 2 povinné argumenty:
1) Odkaz na územní celek, který chceš scrapovat z výše uvedené URL. Tento odkaz zkopíruj ze sloupce 'Výběr obce', který se nachází pod znakem X.
2) Název výstupního CSV souboru s koncovkou .csv.

Příklad použití:

$ python main.py <URL_okresu> <vysledky_voleb.csv>

Reálný příklad pro územní celek Hodonín:

$ python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205 Hodoninsko_vysledky.csv

#### Dej pozor! Příkazový řáadek nemusí zadaný argument URL přečíst správně v případě, že obsahuje znak "&". Pokud URL tento znak obsahuje je potřeba URL dát do uvozovek. 

Spuštění programu:

$  python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205" Hodoninsko_vysledky.csv

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
Výsledný CSV soubor obsahuje pro každou obec pro zvolený územní celek:  
kód obce  
název obce  
voliči v seznamu  
vydané obálky  
platné hlasy  
kandidující strany (co sloupec, to počet hlasů pro stranu pro všechny strany).

### Ukázka výsledku
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana
586030,Archlebov,752,416,415,25,0,0,47,1,12,49,9,2,3,1,1,39
586048,Blatnice pod Svatým Antonínkem,1733,1066,1055,101,1,1,70,4,50,61,7,9,42,0,2,74
586056,Blatnička,356,239,238,16,0,0,14,0,10,17,3,0,1,0,0,23
586072,Bukovany,618,380,372,35,0,0,43,0,5,42,4,5,3,0,0,52
586081,Bzenec,3501,2016,2004,235,4,1,153,2,72,181,17,15,23,0,0,135
586099,Čejč,1019,643,630,70,0,0,42,0,35,61,10,5,6,0,1,78
586102,Čejkovice,2107,1258,1256,164,3,2,80,0,51,107,15,15,21,1,0,112
586111,Čeložnice,337,217,216,11,0,0,12,1,13,21,1,5,5,0,0,16
586129,Dambořice,1079,634,624,19,0,1,65,2,19,47,5,7,6,0,1,38
586137,Dolní Bojanovice,2349,1566,1530,73,5,0,61,0,102,54,15,4,35,1,5,91

Ukázka výstupu CSV souboru [ZDE](https://github.com/Zuziknows/3_projekt/blob/main/hodoninsko_vysledky.jpg).
