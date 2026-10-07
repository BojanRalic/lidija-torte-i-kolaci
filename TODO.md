# TODO · Lidija Torte i Kolači

## Od klijenta (pre objave)

- [ ] Posle zamene bilo koje fotografije pokrenuti `sh tools/slike.sh` (pravi manje verzije od 400 i 800 px za telefone).
- [x] Prave fotografije radionice ubačene na sve četiri stranice (07.10.2026, `assets/img/SOURCES.md`).
- [ ] Klijent bira fotografiju za Instagram sekciju (sada `radionica-lidija.webp`, torta u radionici sa natpisom LIDIJA).
- [ ] Potvrditi broj pratilaca i objava u Instagram sekciji (sada 3.515 pratilaca i 1.634 objave).
- [ ] Natpis na zastavicama torte u kalkulatoru je „ŽIVELI“; menja se u `WORD` u `tools/torta.py`, pa `python3 tools/torta.py`.
- [ ] Potvrditi pravilo porcija: kalkulator računa oko 8 parčadi po kilogramu, minimum 2 kg.
- [ ] Potvrditi radno vreme: upitnik kaže porudžbine od 10 do 19h, Google Maps kaže da otvaraju u 9h.
- [ ] Potvrditi godinu: „registrovana 2020“ u odgovorima, a naziv firme je „TORTE KOLAČI LIDIJA 2022“.
- [ ] Nejasni ukusi iz upitnika: „grkinja“, „moska“, „kidi“. Na sajtu su izostavljeni dok se ne potvrde.
- [ ] Da li drugi broj (064 453 7545) ima Viber i WhatsApp? Sada je na sajtu samo za poziv.
- [ ] Link ka Facebook stranici („Lidija Lidija“) i YouTube prilogu.
- [ ] Odobriti tekst „O nama“ i slogan „Torte koje se prvo pojedu očima.“
- [ ] Poruke zahvalnosti mušterija (sa imenom i mestom) za sekciju utisaka.
- [x] Izabrane varijante: „Kako se poručuje“ P1 (satenska traka), „Lidija i Milan“ L4 (presek torte) na kariranom stolnjaku. Preneto u `index.html`.

## Izabran dizajn: V2 „Slatki trenuci“ (07.10.2026)

V2 je sada jedini sajt: `index.html` i `style.css` u korenu. Meni „Verzije“ je uklonjen sa sajta.
Ostale tri verzije su u `arhiva/` (`glavna/`, `v1-slatka-radnja/`, `v3-rukom-pravljeno/`), sa `noindex`, van sitemap-a. Rade i dalje i imaju svoj meni „Verzije“ koji vodi kroz arhivu i nazad na sajt.
- `arhiva/glavna/DESIGN.md` opisuje staru glavnu verziju. Za V2 još ne postoji DESIGN.md.
- Pregled: https://bojanralic.github.io/lidija-torte-i-kolaci/ (sajt) i https://bojanralic.github.io/lidija-torte-i-kolaci/arhiva/glavna/ (arhiva).
- [ ] Pre objave: navesti autore fotografija iz `assets/deco/SOURCES.md` (CC BY-SA traži atribuciju), npr. jedan red „Izvori fotografija“ u futeru.
- [ ] Pri objavi na domenu: ne objavljivati `arhiva/` ni `assets/verzije.css`; deo „Version switcher“ u `main.js` koristi samo arhiva.
- [ ] Pri objavi na domenu: u `index.html` vratiti `robots` na `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` (sada je `noindex` zbog pregleda na github.io).

## Google recenzije uživo

Sekcija „Slatke reči sa Google mape“ je gotova (`index.html#recenzije`, `functions/api/recenzije.js`). Dok se ne podesi, prikazuje statičnu ocenu 5,0 i 69 recenzija sa linkom na Google mapu. Izgled sa primerima: `index.html?primer`.

- [ ] Pitati klijenta za pristup Google Business Profile-u (dodaju nas kao menadžera). To daje sve recenzije i odgovore, a ne samo 5, i omogućava odgovaranje na recenzije.
- [ ] Do tada: Google Cloud projekat, uključiti Places API (New), napraviti API ključ ograničen samo na Places API, i naći Place ID radionice (Place ID Finder).
- [ ] U Cloudflare Pages podesiti promenljive `GOOGLE_PLACES_KEY` i `GOOGLE_PLACE_ID`. Odgovor se kešira 12h, pa je potrošnja mala; proveriti trenutni besplatni limit za Place Details sa recenzijama pre uključivanja.
- [ ] Pre objave proveriti Google uslove za prikaz Places sadržaja (atribucija „Google Maps“, ime autora, bez menjanja teksta). Sada: tekst se ne menja i ne filtrira, prikazuje se ime autora i atribucija.
- [ ] Kad stigne pristup Business Profile-u: prebaciti funkciju na Business Profile API i prikazati odgovore radionice ispod recenzija.

## Tehničko

- [ ] Self-hostovati fontove umesto Google Fonts (brzina, privatnost).
- [ ] Domen (predlozi klijenta: lidijatorteikolaci.rs, torteleskovac.rs) i Cloudflare Pages. Objavljivati iz posebnog foldera (bez `.impeccable/`, `~resources/`, `tools/`, `dev/`, `arhiva/`), a `functions/` ostaje u korenu projekta.
- [ ] Google Analytics 4 i Search Console.
- [ ] Admin za galeriju (Cloudflare Pages Functions + R2) i automatski Instagram feed.
- [ ] Ostale stranice: vidi „SEO plan“ ispod.

## SEO

**Urađeno 07.10.2026.** title i description sa „torte i kolači Leskovac“, H1 sa ključnom rečju, canonical, Open Graph slika 1200x630 (`assets/img/og-lidija.webp`), JSON-LD (`WebSite` + `Bakery` sa cenama po kg, oblastima dostave, oba telefona, mapom), sekcije „Cene torti i kolača“, „Dostava torti u Leskovcu i okolini“ i deset pitanja sa odgovorima, `robots.txt`, `sitemap.xml` (`node tools/sitemap.mjs` pre svakog deploy-a), `404.html`, `_headers` za Cloudflare Pages.

**Pre objave:**
- [ ] Kad se kupi domen: zameniti `https://lidijatorteikolaci.rs/` u `index.html` (canonical, og, JSON-LD), `robots.txt` i `tools/sitemap.mjs`.
- [ ] Jedna adresa: non-www, https, 301 sa www (Cloudflare Redirect Rule, ne 307).
- [ ] Search Console (domain property), poslati sitemap.
- [ ] GA4: upisati Measurement ID u `GA_ID` na vrhu bloka za analitiku u `main.js`, pa u GA4 označiti događaj `contact_click` kao ključni događaj (parametri `method`: telefon/whatsapp/viber i `section`: deo sajta). `outbound_click` beleži klikove na mapu, recenziju i Instagram.
- [ ] Odlučiti o pristanku za kolačiće pre uključivanja GA4 (zakon o zaštiti podataka o ličnosti). Baner ne sme imati „cookie“ u id/class jer ga Brave sakriva.
- [ ] Google Business Profile: link na sajt, isti naziv, adresa i telefon kao na sajtu; kategorije, radno vreme (tek kad se potvrdi 9 ili 10h), fotografije, odgovori na recenzije. Bez ključnih reči u nazivu.
- [ ] Link na sajt u Instagram bio i na Facebook stranici.
- [ ] Radno vreme u JSON-LD (`openingHoursSpecification`) tek posle potvrde.
- [ ] Apple touch ikona traži PNG; sada je samo SVG favicon jer sve slike moraju biti WebP. Odlučiti da li je PNG izuzetak.

**SEO plan, podstranice (svaka sa svojim tekstom, fotografijama i `BreadcrumbList`):**
- [ ] `/svadbene-torte`: torte za venčanje u Leskovcu, proba ukusa, spratovi, dostava i sklapanje u sali.
- [ ] `/rodjendanske-torte` i `/decje-torte`: po uzrastu i temi, figure od fondana, jestiva slika.
- [ ] `/torte-za-krstenje`: krštenje i rođenje bebe.
- [ ] `/slavski-kolaci`: sitni kolači posni i masni, slavska torta, cena po kg.
- [ ] `/galerija`: prave fotografije sa opisnim alt tekstom (posle admina za galeriju).
- [ ] `/dostava`: jedna stranica za Leskovac i okolinu. Bez posebnih stranica po gradovima dok tamo nema stvarnog prisustva (doorway stranice krše smernice).
- [ ] Blog tek kada Search Console pokaže upite za koje nema stranice.

**Šta se ne radi:** `aggregateRating` sa Google ocene (Google ne prikazuje samohvalne ocene za LocalBusiness), `FAQPage` markup (rich result ukinut; pitanja su vidljiva na stranici), `llms.txt`, `meta keywords`, ključne reči u nazivu Business Profile-a.
