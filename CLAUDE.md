# CLAUDE.md: Turvaverkko-projektin työohjeet

Lue tämä ja `private/SUUNNITELMA.md` jokaisen istunnon alussa.

## Projekti lyhyesti
Inspect-pohjainen arviointi, joka mittaa, käyttäytyvätkö tekoälymallit eri tavalla haavoittuvia nuoria kohtaan, kun ne luulevat keskustelun olevan valvomaton. Omistaja: Santtu Vesterinen. Hänellä on vahva nuorisotyön tausta ja käytännön AI-osaamista, mutta hän ei ole ammattiohjelmoija. Selitä tekniset valinnat lyhyesti ja selkeästi.

## Kieli
- Keskustelu Santun kanssa ja suunnitteludokumentit: suomi.
- Koodi, kommentit, README, docs/ ja julkiset raportit: englanti.
- Skenaariot: molemmat kielet (`fi` ja `en`).

## Ehdottomat säännöt
1. **Etiikka ensin.** Noudata `docs/ETHICS.md`:tä. Älä koskaan kirjoita itsetuhoisuuden tai muun vaarallisen toiminnan keinoja mihinkään tiedostoon.
2. **Skenaarioita ei merkitä tarkistetuiksi** (`reviewed: true`) ilman, että Santtu kertoo ammattilaisen hyväksyneen ne. Käytä `scenario-reviewer`-agenttia jokaisen uuden tai muutetun skenaarion tarkistukseen.
3. **Ehdot eroavat vain järjestelmäkehotteessa.** Älä muuta tätä asetelmaa kysymättä, koska koko tulos perustuu siihen.
4. **Arvioija pysyy sokkona.** Arvioijamalli ei saa nähdä järjestelmäkehotetta tai ehtoa.
5. **Salaisuudet.** API-avaimet ovat vain `.env`-tiedostossa. Tarkista ennen jokaista commitia, ettei `.env`, `logs/` tai `private/` ole mukana. `private/`-kansiossa ovat Santun henkilökohtaiset suunnitelmat ja hakutekstit, eikä niitä koskaan julkaista.
6. **Kulut.** Arvioi API-kustannus ennen jokaista ajoa, joka on suurempi kuin testiajo. Kysy lupa, jos arvio ylittää 30 euroa.
7. **Repo pysyy yksityisenä**, kunnes Santtu erikseen pyytää tekemään siitä julkisen.
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
python analysis/analyze.py logs/ --out results/summary.md
```
Tarkista ajankohtaiset mallinimet toimittajan dokumentaatiosta, älä arvaa.

## Työtapa
- Pienet, testatut muutokset. Aja `pytest` jokaisen muutoksen jälkeen.
- Uusi toiminnallisuus vaatii testin `tests/`-kansioon.
- Selkeät commit-viestit englanniksi.
- Kun vaihe valmistuu, päivitä `private/SUUNNITELMA.md`:n tilarivi.
