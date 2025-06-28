#"""
#main.py: třetí projekt do Engeto Online Python Akademie

#author: Zuzana Fabiánová
#email: zuzanka72@seznam.cz
#"""

#Jdeme na to!!!!

import sys
import requests
from bs4 import BeautifulSoup
import csv

def main():
    if len(sys.argv) != 3:
        print("Ahoj a vítej v programu pro scraper výsledků voleb z roku 2017, který vytáhne data přímo z webu.")
        print("Více o tom, co tento program dělá a jak ho rozeběhnout, se dočteš v souboru README, který jsem pro Tebe připravila.")
        print("-" * 30)
        print("Pokud vidíš tento text, udělal jsi něco špatně. Pro správné spuštění zadej 2 argumenty v tomto pořadí:")
        print("1) Odkaz na územní celek, který chceš scrapovat z této URL --> https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
        print("2) Název výstupního CSV souboru (např. Hodoninsko_volby.csv)")
        print("-" * 30)
        print("Příklad použití: python main.py <URL_okresu> <vysledky_voleb.csv>")
        print("Příklad použití: python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205 <Hodoninsko_volby.csv")
        sys.exit(1)

    url = sys.argv[1]
    vysledky_voleb = sys.argv[2]

    if not url.startswith("http") or "volby.cz" not in url:
        print("První argument není platná URL adresa.")
        sys.exit(1)

    if not vysledky_voleb.endswith(".csv"):
        print("Druhý argument musí být název CSV souboru končící .csv")
        sys.exit(1)

    if "ps32" not in url:
        print("URL nevede na stránku okresních výsledků obcí. Použij URL ze sloupce 'Výběr obce'.")
        sys.exit(1)

    zahlavi = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]

    try:
        okresni_data = requests.get(url)
        okresni_soup = BeautifulSoup(okresni_data.text, "html.parser")

        obecni_zaznamy = []
        for tabulka in okresni_soup.find_all("table"):
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

        prvni_obec_url = obecni_zaznamy[0][2]
        prvni_data = requests.get(prvni_obec_url)
        prvni_soup = BeautifulSoup(prvni_data.text, "html.parser")

        strany_tabulka = None
        for tabulka in prvni_soup.find_all("table"):
            headers = [th.get_text(strip=True).lower() for th in tabulka.find_all("th")]
            if any("strana" in h for h in headers):
                strany_tabulka = tabulka
                break

        if not strany_tabulka:
            print("Vyskytla se chyba --> nenalezena tabulka kandidujících stran.")
            sys.exit(1)

        nazvy_stran = []
        for row in strany_tabulka.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) >= 2:
                nazvy_stran.append(cells[1].get_text(strip=True))
                zahlavi.append(cells[1].get_text(strip=True))

        with open(vysledky_voleb, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(zahlavi)

            for i, (kod_obce, nazev_obce, link_obce) in enumerate(obecni_zaznamy):
                obec_data = requests.get(link_obce)
                obec_soup = BeautifulSoup(obec_data.text, "html.parser")

                try:
                    volici = obec_soup.find("td", {"headers": "sa2"}).text.replace("\xa0", "")
                    obalky = obec_soup.find("td", {"headers": "sa3"}).text.replace("\xa0", "")
                    hlasy = obec_soup.find("td", {"headers": "sa6"}).text.replace("\xa0", "")
                except AttributeError:
                    volici = obalky = hlasy = ""

                row_data = [kod_obce, nazev_obce, volici, obalky, hlasy]

                strany_pol = obec_soup.find_all("table")
                hlasy_dict = {}
                for tabulka in strany_pol:
                    headers = [th.get_text(strip=True).lower() for th in tabulka.find_all("th")]
                    if any("strana" in h for h in headers):
                        for row in tabulka.find_all("tr")[2:]:
                            cells = row.find_all("td")
                            if len(cells) >= 3:
                                hlasy_dict[cells[1].get_text(strip=True)] = cells[2].get_text(strip=True).replace("\xa0", "")
                        break

                for strana in nazvy_stran:
                    row_data.append(hlasy_dict.get(strana, "0"))

                writer.writerow(row_data)
                print(f"Zpracováno: {nazev_obce} ({i+1}/{len(obecni_zaznamy)})")

        print(f"\nHotovo! Data byla úspěšně uložena do: {vysledky_voleb}")

    except Exception as e:
        print(f"Neočekávaná chyba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
