# Changelog

## v0.2.1 (07.10.2026)

Ništa više ne viri iz svog okvira i telefon ima više prostora, na sve četiri stranice.

- Isečeni elementi: washi traka na kartici „Šta nam pošaljete“ više nije odsečena maskom, kanap kartice u futeru i nalepnica „Za svaki praznik“ ostaju na ekranu, lila cveće u V2, gipsofila u V1, grančica i pečat u V3 ostaju unutar svojih okvira.
- Telefon: zaglavlje staje u jedan red, mašna na kutiji ima prostor ispod zaglavlja, presek torte popunjava širinu, natpisi na mapi se ne preklapaju, kanap više ne visi bez kartice, gipsofila u V1 ne prekriva naslov u futeru, brojevi telefona se ne lome u dva reda.
- Svi linkovi i dugmad na telefonu imaju bar 44 px za prst.

## v0.2.0 (07.10.2026)

Nacrtane CSS dekoracije zamenjene su pravim materijalima na sve četiri stranice.

- Glavna stranica: sjajni prelivi od čokolade i glazure sa odsjajem i senkom, prava satenska mašna (fotografija) na kutiji i na traci u koracima poručivanja, satenske trake, washi trake od papira sa vlaknima i pocepanim krajevima, tkani karirani stolnjak, papirni podmetač sa reljefom, jutani kanap i zrno papira na svim karticama.
- V1 „Slatka radnja“: prave grančice gipsofile i borovnice sa senkama umesto nacrtanih grančica i tačkica.
- V2 „Slatki trenuci“: pravo lila cveće iza fotografija, kao na referenci.
- V3 „Rukom pravljeno“: pocepan papir sa belim vlaknastim rubom, zrno papira i botanička gravura iz 1831. u zlatnom tonu.
- Sve nove slike su WebP u `assets/deco/`, sa izvorima i licencama u `assets/deco/SOURCES.md`. Generator u `tools/deco.py` pravi teksture koje nisu fotografije.

## v0.1.0 (07.10.2026)

Prvi pregled za klijenta, objavljen na GitHub Pages.

- Home stranica „Kutija sa mašnom“ (`index.html`): ponuda, cenovnik, ukusi, kalkulator količine, poručivanje preko Vibera, WhatsApp-a i poziva, Lidija i Milan, Google recenzije, dostava sa animiranom mapom, dijaspora, česta pitanja.
- Tri alternativne verzije dizajna u `verzije/`: „Slatka radnja“, „Slatki trenuci“ i „Rukom pravljeno“.
- Meni „Verzije“ u zaglavlju svih stranica, za poređenje pravaca.
- SEO temelj: naslovi, opisi, JSON-LD (WebSite i Bakery), OG slika, sitemap, robots.txt, 404 stranica.
- Sve fotografije su WebP sa verzijama od 400 i 800 px; logo i ukrasi su SVG.
- Pregled ima `noindex`, jer sajt još nema domen.
