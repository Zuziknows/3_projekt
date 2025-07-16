#"""
#main.py: třetí projekt do Engeto Online Python Akademie

#author: Zuzana Fabiánová
#email: zuzanka72@seznam.cz
#"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def vystup_argumentu():
    if len(sys.argv) != 3:
        print("Ahoj a vítej v programu pro scraper výsledků voleb z roku 2017, který vytáhne data přímo z webu.")
        print("Více o tom, co tento program dělá a jak ho rozeběhnout, se dočteš v souboru README, který jsem pro Tebe připravila.")
        print("-" * 50)
        print("Pokud vidíš tento text, udělal jsi něco špatně. Pro správné spuštění zadej 2 argumenty v tomto pořadí:")
        print("1) Odkaz na územní celek, který chceš scrapovat z této URL --> https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
        print("2) Název výstupního CSV souboru (např. Hodoninsko_vysledky.csv)")
        print("-" * 50)
        print("Příklad použití: python main.py <URL_okresu> <vysledky_voleb.csv>")
        print("Příklad použití: python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205 Hodoninsko_vysledky.csv")
        sys.exit(1)

    url = sys.argv[1]
    vysledky_voleb = sys.argv[2]

    if not url.startswith("http") or "volby.cz" not in url:
        print("Vyskytla se chyba --> první argument není platná URL adresa.")
        sys.exit(1)

    if not vysledky_voleb.endswith(".csv"):
        print("Vyskytla se chyba --> druhý argument musí být název CSV souboru končící .csv")
        sys.exit(1)

    if "ps32" not in url:
        print("Vyskytla se chyba --> URL nevede na stránku okresních výsledků obcí. Použij URL ze sloupce 'Výběr obce'.")
        sys.exit(1)

    return url, vysledky_voleb

def ziskej_odkazy_na_obce(url):
    odpoved = requests.get(url)
    soup = BeautifulSoup(odpoved.text, "html.parser")
    obecni_zaznamy = []

    for tabulka in soup.find_all("table"):
        for row in tabulka.find_all("tr")[2:]:
            td = row.find_all("td")
            if len(td) > 1:
                link = td[0].find("a")
                if link:
                    kod = td[0].text.strip()
                    nazev = td[1].text.strip()
                    href = link["href"]
                    url_obce = "https://www.volby.cz/pls/ps2017nss/" + href
                    obecni_zaznamy.append((kod, nazev, url_obce))

    if not obecni_zaznamy:
        print("Vyskytla se chyba --> nebyly nalezeny žádné odkazy na obce.")
        sys.exit(1)

    return obecni_zaznamy

def ziskej_nazvy_stran(url_obce):
    odpoved = requests.get(url_obce)
    soup = BeautifulSoup(odpoved.text, "html.parser")
    nazvy_stran = []

    for tabulka in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in tabulka.find_all("th")]
        if any("strana" in h for h in headers):
            for row in tabulka.find_all("tr")[1:]:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    nazev_strany = cells[1].get_text(strip=True)
                    if nazev_strany not in nazvy_stran:
                        nazvy_stran.append(nazev_strany)

    if not nazvy_stran:
        print("Vyskytla se chyba --> nenalezena žádná strana v tabulkách.")
        sys.exit(1)

    return nazvy_stran

def zpracuj_obec(kod_obce, nazev_obce, url_obce, nazvy_stran):
    odpoved = requests.get(url_obce)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    try:
        volici = soup.find("td", {"headers": "sa2"}).text.replace("\xa0", "")
        obalky = soup.find("td", {"headers": "sa3"}).text.replace("\xa0", "")
        hlasy = soup.find("td", {"headers": "sa6"}).text.replace("\xa0", "")
    except AttributeError:
        volici = obalky = hlasy = ""

    radek = [kod_obce, nazev_obce, volici, obalky, hlasy]

    hlasy_dict = {}

    for tabulka in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in tabulka.find_all("th")]
        if any("strana" in h for h in headers):
            for row in tabulka.find_all("tr")[2:]:
                cells = row.find_all("td")
                if len(cells) >= 3:
                    nazev_strany = cells[1].get_text(strip=True)
                    pocet_hlasu = cells[2].get_text(strip=True).replace("\xa0", "")
                    if nazev_strany in hlasy_dict:
                        
                        hlasy_dict[nazev_strany] = str(int(hlasy_dict[nazev_strany]) + int(pocet_hlasu))
                    else:
                        hlasy_dict[nazev_strany] = pocet_hlasu

    for strana in nazvy_stran:
        radek.append(hlasy_dict.get(strana, "0"))

    return radek

def uloz_vysledky(soubor, zahlavi, zaznamy):
    with open(soubor, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(zahlavi)
        writer.writerows(zaznamy)

def main():
    url, vysledky_voleb = vystup_argumentu()
    obecni_zaznamy = ziskej_odkazy_na_obce(url)

    prvni_obec_url = obecni_zaznamy[0][2]
    nazvy_stran = ziskej_nazvy_stran(prvni_obec_url)

    zahlavi = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + nazvy_stran
    vsechny_radky = []

    for i, (kod, nazev, url_obce) in enumerate(obecni_zaznamy):
        radek = zpracuj_obec(kod, nazev, url_obce, nazvy_stran)
        vsechny_radky.append(radek)
        print(f"Zpracováno: {nazev} ({i+1}/{len(obecni_zaznamy)})")

    uloz_vysledky(vysledky_voleb, zahlavi, vsechny_radky)
    print(f"\nHotovo! Data byla úspěšně uložena do: {vysledky_voleb}")

if __name__ == "__main__":
    main()
