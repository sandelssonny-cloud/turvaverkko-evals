# CLAUDE.md: Turvaverkko-projektin työohjeet

Lue tämä ja `private/SUUNNITELMA.md` jokaisen istunnon alussa.

## Projekti lyhyesti
Inspect-pohjainen arviointi, joka mittaa, käyttäytyvätkö tekoälymallit eri tavalla haavoittuvia nuoria kohtaan, kun ne luulevat, ettei kukaan tarkista niiden vastauksia. Omistaja: Santtu Vesterinen. Hänellä on vahva nuorisotyön tausta ja käytännön AI-osaamista, mutta hän ei ole ammattiohjelmoija. Selitä tekniset valinnat lyhyesti ja selkeästi.

## Kieli
- Keskustelu Santun kanssa ja suunnitteludokumentit: suomi.
- Koodi, kommentit, README, docs/ ja julkiset raportit: englanti.
- Skenaariot: molemmat kielet (`fi` ja `en`).

## Ehdottomat säännöt
1. **Etiikka ensin.** Noudata `docs/ETHICS.md`:tä. Älä koskaan kirjoita itsetuhoisuuden tai muun vaarallisen toiminnan keinoja mihinkään tiedostoon.
2. **Skenaarioita ei merkitä tarkistetuiksi** (`reviewed: true`) ilman, että Santtu kertoo ammattilaisen hyväksyneen ne. Käytä `scenario-reviewer`-agenttia jokaisen uuden tai muutetun skenaarion tarkistukseen.
3. **Ehdot eroavat vain järjestelmäkehotteessa.** Älä muuta tätä asetelmaa kysymättä, koska koko tulos perustuu siihen.
4. **Arvioija pysyy sokkona.** Arvioijamalli ei saa nähdä järjestelmäkehotetta tai ehtoa.
5. **Salaisuudet.** API-avaimet ovat vain `.env`-tiedostossa. Tarkista ennen jokaista commitia, ettei `.env`, `logs/` tai `private/` ole mukana. `private/`-kansiossa ovat Santun henkilökohtaiset suunnitelmat, eikä niitä koskaan julkaista.
6. **Kulut.** Arvioi API-kustannus ennen jokaista ajoa, joka on suurempi kuin testiajo. Kysy lupa, jos arvio ylittää 30 euroa.
7. **Repo on julkinen** (7.11.2026 alkaen). Kaikki commitoitu näkyy kaikille, joten tarkista jokainen commit sen mukaan. Tuloksia ei julkaista ennen kuin skenaariot on tarkistettu ja vastuullinen julkistaminen on tehty (`docs/ETHICS.md`).
8. **Ei liioittelua.** Raportoi tulokset luottamusväleineen. Nollatulos on tulos.

## Komennot
```bash
pip install -e ".[dev,providers]"        # asennus
pytest                                    # testit
inspect eval src/turvaverkko/task.py \
  --model <toimittaja>/<malli> \
  --model-role grader=<toimittaja>/<arvioijamalli> \
  -T languages=en -T epochs=1             # halpa testiajo
inspect view                              # lokien selain
python analysis/check_run.py logs/        # tarkista ajo ennen pisteiden käyttöä
python analysis/analyze.py logs/ --out results/summary.md
```
Tarkista ajankohtaiset mallinimet toimittajan dokumentaatiosta, älä arvaa.

## Ajon tarkistuslista
Käy tämä läpi ennen jokaista ajoa oikeilla malleilla. Kohdat perustuvat ensimmäiseen pilottiin (7.11.2026), jossa pieni testiajo löysi kaksi vikaa ennen varsinaista ajoa.
1. **Mallit:** hae saatavilla olevat mallit suoraan toimittajan API:sta. Mallinimiä ei arvata, ja osa malleista ei ole uusien käyttäjien saatavilla.
2. **Avain ja saldo:** lähetä yksi pieni kutsu jokaiselle mallille ennen ajoa. Avain voi toimia mallilistaan, vaikka saldoa ei ole.
3. **Kulut:** arvioi kulu tokenimäärästä ja kerro se Santulle. Yli 30 euron ajoon kysytään lupa.
4. **Arvioija:** valitse arvioija eri toimittajalta kuin testattavat mallit. Jos se ei ole mahdollista, kirjaa rajoitus yhteenvetoon.
5. **Pieni testiajo:** yksi malli, `-T languages=en -T epochs=1`, omaan lokikansioon (`--log-dir logs/<päivä>_smoke`).
6. **Tarkistus:** aja `python analysis/check_run.py <lokikansio>`. Katkenneet tai tyhjät vastaukset, lukukelvottomat arvioinnit ja vuodot korjataan ennen jatkoa.
7. **Lue vastauksia itse:** vähintään yksi vastaus kummastakin ehdosta ja molemmilta kieliltä.
8. **Varsinainen ajo:** omaan lokikansioon (`logs/<päivä>_<nimi>`), jotta eri ajot eivät sekoitu analyysissa. Aja `check_run.py` uudelleen.
9. **Analyysi:** aja `analyze.py`. Tulokset tallennetaan `private/`-kansioon, kunnes ammattilainen on tarkistanut skenaariot.
10. **Yhteenveto:** kirjaa mitä ajettiin, kulut ja löydetyt ongelmat, ja päivitä `private/SUUNNITELMA.md`:n tilarivi.

Windowsilla Inspect näyttää varoituksen `socket has no attribute AF_UNIX`. Se ei vaikuta ajoon.

## Työtapa
- Pienet, testatut muutokset. Aja `pytest` jokaisen muutoksen jälkeen.
- Uusi toiminnallisuus vaatii testin `tests/`-kansioon.
- Selkeät commit-viestit englanniksi.
- Kun vaihe valmistuu, päivitä `private/SUUNNITELMA.md`:n tilarivi.
