# Changelog

## v0.6.0 (07.10.2026)

V2 „Slatki trenuci“ je sada jedini sajt:
- V2 je prebačen u koren projekta (`index.html`, `style.css`) i otvara se na glavnoj adresi.
- Uklonjen je meni „Verzije“ iz zaglavlja.
- Sajt je preuzeo SEO zaglavlje stare glavne verzije: naslov, opis, canonical, Open Graph i JSON-LD (Bakery sa cenama i oblastima dostave). Dodat je preload naslovne fotografije.
- Stara glavna verzija, V1 i V3 su premeštene u `arhiva/` i i dalje rade. Njihov meni „Verzije“ sada vodi kroz arhivu i nazad na sajt. Sve imaju `noindex`.
- Stranica 404 koristi fontove i stil V2.
- `tools/torta.py` i `tools/presek.py` sada pišu samo u `index.html`. Arhiva zadržava svoje crteže.
- `DESIGN.md` stare glavne verzije je premešten u `arhiva/glavna/`.

## v0.5.4 (07.10.2026)

V2 „Slatki trenuci“, mapa dostave:
- Niš i Vranje sada imaju kružić na kraju linije, kao i ostali gradovi, sa istim talasom i iskakanjem na hover. Strelice su uklonjene.
- Natpis „Lebane“ je pomeren ispod kružića, pa linija više ne prelazi preko teksta.
- Natpisi „Leskovac“ i „Besplatno“ su pomereni desno gore od poklona, pa ih linije više ne seku. Imaju tanku podlogu u boji kartice, da ostanu čitki i kad su blizu reke.

## v0.5.3 (07.10.2026)

V2 „Slatki trenuci“, sekcija „Dostava torti u Leskovcu i okolini“:
- Kada miš napusti mapu, linije dostave se uvlače nazad ka Leskovcu istim putem kojim su nacrtane. Ranije su samo nestajale.

## v0.5.2 (07.10.2026)

V2 „Slatki trenuci“, sekcija „Pogledajte šta je unutra“:
- Na hover ništa više ne gubi boju. Ostali slojevi ne posive, a ostali opisi ne blede. Izabrani sloj se ističe roze sjajem, a njegov opis dobija bordo boju i krem podlogu.

## v0.5.1 (07.10.2026)

V2 „Slatki trenuci“, sekcija „Pogledajte šta je unutra“:
- Slojevi parčeta su sada naslagani jedan na drugi, bez razmaka. Ukrasi stoje na ganašu, a parče je malo veće.
- Na hover se slojevi više ne pomeraju. Izabrani sloj ostaje u boji i blago pulsira roze sjajem, a ostali posive.
- Animacija slaganja kreće tek kada se vidi veći deo sekcije (oko 70%, ili 70% ekrana kada je sekcija viša od njega). To radi novi atribut `data-late` u `main.js`, koji ostale sekcije ne koriste.

## v0.5.0 (07.10.2026)

V2 „Slatki trenuci“, sekcija „Pogledajte šta je unutra“:
- Novo parče torte po uzoru na akvarel sa malinom: trouglasto parče sa vrhom udesno, rez okrenut ka posetiocu i kora koja se savija levo.
- Slojevi stoje razmaknuti, kao na rastavljenom crtežu: čokoladni biskvit, kuvani vanila fil sa trakom džema od maline, čokoladna kora, krem sa prepolovljenim malinama, vanila kora i ganaš od belgijske čokolade sa curenjem i šarama od bele čokolade. Iznad lebde maline, ruže od šlaga, list nane, uvijutak bele čokolade i zlatne listiće.
- Na ulazu slojevi padaju odozgo jedan po jedan, od dna ka vrhu, a ukrasi stižu poslednji.
- Opisi su sada levo i desno od torte, spojeni ravnom linijom sa svojim slojem. Hover veza između sloja i opisa ostaje ista.

## v0.4.2 (07.10.2026)

V2 „Slatki trenuci“:
- Kontakt meni: u čokoladnom luku redosled je sada „pošaljite sliku, mi ostalo“, „Javite se“, pa ikonica torte.
- Broj telefona na naslovnoj slici: iznad broja piše „pozovite nas“, a slušalica je u čokoladnom krugu. Na hover se čokolada razlije preko cele pilule, krug postane roze, slušalica zazvoni i oko nje se šire talasi.

## v0.4.1 (07.10.2026)

V2 „Slatki trenuci“:
- „Lidija i Milan“ ima ponovo raniji izgled (velika fotografija sa značkom „20 godina“ i tekst). Presek torte je ispod, u svojoj roze kartici „Pogledajte šta je unutra“.
- Svaki sloj preseka je sada 3D komad sa svojim vrhom, bokom i prednjom stranom, pa torta ne izgleda prazno dok se slaže.
- Slojevi i opisi su povezani: pređite preko opisa ili sloja i taj sloj izađe iz torte, opis se istakne, a ostali slojevi se priguše. Na telefonu isto rade dugmići sa opisima ispod torte.
- Kontakt meni: čokoladni luk sa natpisom „Javite se“ je sada na dnu.
- Linkovi u meniju: na hover se iza reči pojavi krem polje, a ispod nje mala bordo tačka.

## v0.4.0 (07.10.2026)

V2 „Slatki trenuci“:
- Sekcija „Dostava torti u Leskovcu i okolini“ preneta je sa glavne stranice, sa istim tekstom i mapom, u bojama V2: tačkasta roza kartica, serif natpisi, čokoladna kutija sa roze mašnom za Leskovac. Nova hover animacija: putevi se redom iscrtavaju iz Leskovca, a kad stignu, gradovi zasvetle i rašire talas, i poklopac kutije poskoči. Na telefonu se putevi iscrtaju kad se mapa pojavi na ekranu. Kartica „Daleko ste?“ je sada u punoj širini ispod mape.
- „Lidija i Milan“: detaljan presek torte sa opisima umesto velike fotografije. Kora sa mrvicama i rupicama, krem, domaći džem od malina sa semenkama, čokoladna kora, mus, keks podloga, glazura od belgijske čokolade koja se sliva niz bok, ruže od krema, maline, borovnice, list čokolade, nana i zlatni listići, na tanjiru sa zlatnim rubom i viljuškom. Slojevi padaju jedan na drugi kad se sekcija pojavi. Fotografija je u malom luku pored torte. Crtež pravi `tools/presek.py`.
- Kontakt meni u zaglavlju ima oblik luka sa čokoladnim vrhom i natpisom „Javite se“. Redovi ulaze jedan za drugim, a na hover dobijaju strelicu.
- Uklonjeno lila cveće iz naslovne pozadine.

## v0.3.2 (07.10.2026)

V2 „Slatki trenuci“:
- Sklonjeno lila cveće iza fotografije u sekciji „Svaka torta je napravljena za vas“.
- Tri kartice ispod („Belgijska čokolada“, „Domaće voće“, „Ukras rađen rukom“) su sada lukovi kao naslovna fotografija, u čokoladnoj, bež i rozoj boji iz palete stranice, sa tankim unutrašnjim okvirom, ikonicom u krem krugu i rednim brojem.

## v0.3.1 (07.10.2026)

- Nova fotografija za „Rođendanske torte“ u V1, V2 i V3: roze torta sa siluetom princeze, leptirima i natpisom Happy Birthday, po izboru radionice. Glavna stranica ima zajedničku karticu „Rođendanske i dečje“ i ona ostaje sa fotografijom dečje torte.

## v0.3.0 (07.10.2026)

Prave fotografije radionice, nova Instagram sekcija i nova torta u kalkulatoru, na sve četiri stranice.

- Fotografije: sve zamenske slike zamenjene su fotografijama koje je poslala radionica. Slike sa imenom sekcije stoje u toj sekciji (Svadbene torte, Dečje torte, Krštenje i rođenje bebe, Slavski kolači, Kolači u čaši i praline, Lidija i Milan, Svaka torta je napravljena za vas, Cene bez iznenađenja, naslovna). Ostala mesta dobila su fotografije iz istog foldera.
- Naslovna fotografija ima kvadratnu i široku verziju sa produženom bordo pozadinom, da se cela torta vidi u svakom okviru.
- Instagram: umesto niza objava sa profila, sekcija sada reklamira profil @lidijatorte sa jednom izabranom fotografijom, brojem pratilaca i objava i dugmetom „Zapratite nas“. Svaka verzija ima svoj izgled: polaroid sa nalepnicom (glavna), fotografija u tankom okviru (V1), luk na rozom panelu (V2), okrugla fotografija na pocepanom papiru (V3, sekcija je nova).
- Kalkulator „Koliko torte za vaše goste“: nova ilustracija po uzoru na sliku radionice. Roze spratovi sa uvijenim kremom, belim girlandama i plavim cvetićima, tufnama, jagodama na vrhu i zastavicama „ŽIVELI“, na lila postolju. Jagode i zastavice uvek stoje na najvišem spratu. Crtež pravi `tools/torta.py`.
- Stare zamenske slike sklonjene su iz projekta. Izvori fotografija su u `assets/img/SOURCES.md`.

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
