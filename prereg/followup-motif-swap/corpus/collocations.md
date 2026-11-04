# Collocations — motif-swap follow-up, Track A

Measure: Dunning log-likelihood (G²) of co-occurrence inside a ±5-token window around any token matching the family seed regex, versus the token's overall frequency in the same text. Sign flipped to negative when the word is *less* frequent near seeds than overall (none of those appear in a top-25). Tokens: lower-cased regex words (`[^\W\d_]+` with internal apostrophes/hyphens), no lemmatisation, language-specific stop lists, min window count 2, min length 3. Columns: collocate | window co-occurrences (raw) | total frequency in text | G². Seed terms are prefix regexes in the text's own language (so `spiegel` also matches *Spiegelbild*, `blick` matches *blickte*). spaCy was not available; see README for what this does and does not buy.

Family → theory: **double** = Rank; **return** = Rank; **separation** = Rank; **exclusion** = Foucault; **silence** = Foucault; **passage** = Foucault; **gaze** = Foucault; **apollonian_dionysian** = Nietzsche (GT §1–8 form vocabulary).

## Text sizes (tokens after header/footer stripping)

| text | lang | tokens | types |
|---|---|---:|---:|
| rank_doppelgaenger_1925 | de | 36684 | 8623 |
| rank_trauma_1924 | de | 63675 | 12557 |
| hoffmann_elixiere | de | 107131 | 13808 |
| chamisso_schlemihl | de | 21563 | 4869 |
| maupassant_horla | fr | 41210 | 7122 |
| stevenson_jekyll_hyde | en | 25704 | 3998 |
| wilde_dorian_gray | en | 79179 | 7117 |
| poe_william_wilson | en | 8022 | 2304 |
| dostoevsky_double_garnett_1917 | en | 63774 | 6757 |
| nietzsche_GT_1-8 | de | 11492 | 3178 |
| nietzsche_JGB | de | 55983 | 9874 |
| nietzsche_Za-IV | de | 23997 | 4407 |
| nietzsche_FW | de | 69809 | 10576 |
| nietzsche_DD | de | 3571 | 1436 |
| nietzsche_BVN-1889 | de | 1717 | 741 |

## A. Theory texts (Rank, Nietzsche)

Foucault's own texts were not obtained (in copyright), so the Foucault families (exclusion / silence / passage / gaze) have no Foucault-text collocates; their seed vocabulary is run on the Nietzsche texts here and on the norming corpus in section B.

### rank_doppelgaenger_1925 — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 700; window tokens: 6874

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | seele | 41 | 69 | 55.9 |
| 2 | selbständig | 8 | 5 | 26.8 |
| 3 | negelein | 9 | 10 | 24.1 |
| 4 | porträt | 7 | 4 | 23.5 |
| 5 | sehen | 18 | 32 | 22.3 |
| 6 | wirft | 10 | 13 | 20.7 |
| 7 | verkörpert | 6 | 5 | 20.1 |
| 8 | ursprünglichste | 6 | 5 | 20.1 |
| 9 | werfen | 5 | 4 | 16.7 |
| 10 | stellen | 4 | 2 | 13.4 |
| 11 | bewunderung | 4 | 3 | 13.4 |
| 12 | gezogen | 4 | 3 | 13.4 |
| 13 | stellungen | 4 | 2 | 13.4 |
| 14 | volksglauben | 4 | 4 | 13.4 |
| 15 | verfolgenden | 4 | 2 | 13.4 |
| 16 | nungen | 4 | 2 | 13.4 |
| 17 | tritt | 10 | 18 | 12.1 |
| 18 | verlust | 6 | 8 | 11.9 |
| 19 | narzißtische | 6 | 8 | 11.9 |
| 20 | körpers | 5 | 6 | 11.8 |
| 21 | ähnliche | 5 | 6 | 11.8 |
| 22 | verhängen | 3 | 3 | 10.0 |
| 23 | unterscheiden | 3 | 2 | 10.0 |
| 24 | eigentlichen | 3 | 2 | 10.0 |
| 25 | unbewußten | 3 | 3 | 10.0 |

### rank_doppelgaenger_1925 — family **separation** (Rank)

Seed regex (`^(...)`): `trennung|geburtsakt|nabelschnur|ablösung|abnabel|hebamme|schwelle|loslösung|geburtstrauma|urangst|angst` — seed hits: 21; window tokens: 210

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | wahnsinn | 2 | 7 | 12.4 |
| 2 | pathologische | 2 | 7 | 12.4 |
| 3 | dichter | 2 | 44 | 4.9 |
| 4 | eigenen | 2 | 51 | 4.4 |

### rank_doppelgaenger_1925 — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 85; window tokens: 844

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | hinein | 5 | 8 | 27.3 |
| 2 | entzückt | 3 | 2 | 22.6 |
| 3 | gealtert | 2 | 1 | 15.1 |
| 4 | entstellt | 2 | 1 | 15.1 |
| 5 | nächt’ger | 2 | 1 | 15.1 |
| 6 | erbleichend | 2 | 1 | 15.1 |
| 7 | tränenden | 2 | 1 | 15.1 |
| 8 | see | 3 | 7 | 13.3 |
| 9 | fällt | 3 | 9 | 11.5 |
| 10 | porträts | 2 | 3 | 11.3 |
| 11 | sah | 4 | 19 | 11.3 |
| 12 | klinke | 2 | 3 | 11.3 |
| 13 | zukünftigen | 2 | 4 | 9.6 |
| 14 | jenen | 2 | 4 | 9.6 |
| 15 | boden | 2 | 5 | 8.5 |
| 16 | konnte | 2 | 5 | 8.5 |
| 17 | bösen | 2 | 6 | 7.6 |
| 18 | zeit | 3 | 18 | 7.1 |
| 19 | nächsten | 2 | 7 | 6.9 |
| 20 | haupt | 2 | 7 | 6.9 |
| 21 | natur | 2 | 7 | 6.9 |
| 22 | selben | 2 | 8 | 6.4 |
| 23 | zurück | 2 | 8 | 6.4 |
| 24 | einige | 2 | 9 | 5.9 |
| 25 | spiegel | 6 | 87 | 5.4 |

### rank_doppelgaenger_1925 — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 6; window tokens: 60

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | the | 2 | 32 | 10.9 |

### rank_trauma_1924 — family **return** (Rank)

Seed regex (`^(...)`): `mutterleib|uterus|rückkehr|wiedergeburt|urzustand|höhle|wasser|meer|schlaf|wiederherstell|zurück|intrauterin|embryo` — seed hits: 486; window tokens: 4750

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | urlust | 5 | 4 | 26.0 |
| 2 | partielle | 5 | 4 | 26.0 |
| 3 | nachgebildet | 5 | 5 | 26.0 |
| 4 | ursituation | 13 | 38 | 22.6 |
| 5 | lustsituation | 4 | 3 | 20.8 |
| 6 | glückshaube | 4 | 3 | 20.8 |
| 7 | angleichung | 5 | 6 | 20.7 |
| 8 | situation | 15 | 54 | 20.1 |
| 9 | mutter | 35 | 208 | 20.1 |
| 10 | phantasie | 7 | 14 | 18.0 |
| 11 | physiologischen | 5 | 7 | 17.9 |
| 12 | wunsch | 8 | 19 | 17.4 |
| 13 | zeitweisen | 3 | 1 | 15.6 |
| 14 | auffassen | 3 | 3 | 15.6 |
| 15 | libidinöse | 3 | 2 | 15.6 |
| 16 | urtendenz | 3 | 3 | 15.6 |
| 17 | reales | 4 | 6 | 13.4 |
| 18 | teilweise | 4 | 6 | 13.4 |
| 19 | lustvollen | 5 | 10 | 12.9 |
| 20 | schützenden | 5 | 10 | 12.9 |
| 21 | tendiert | 3 | 4 | 11.2 |
| 22 | ernährung | 3 | 4 | 11.2 |
| 23 | anagogischen | 2 | 2 | 10.4 |
| 24 | typisches | 2 | 2 | 10.4 |
| 25 | erd | 2 | 2 | 10.4 |

### rank_trauma_1924 — family **separation** (Rank)

Seed regex (`^(...)`): `trennung|geburtsakt|nabelschnur|ablösung|abnabel|hebamme|schwelle|loslösung|geburtstrauma|urangst|angst` — seed hits: 370; window tokens: 3658

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | überwindung | 12 | 22 | 39.5 |
| 2 | stammende | 6 | 3 | 34.3 |
| 3 | infantile | 11 | 25 | 30.2 |
| 4 | unmittelbar | 7 | 15 | 20.2 |
| 5 | genitale | 10 | 33 | 19.4 |
| 6 | schweres | 4 | 5 | 18.0 |
| 7 | neuerlichen | 3 | 3 | 17.1 |
| 8 | auslösung | 3 | 3 | 17.1 |
| 9 | stammenden | 3 | 3 | 17.1 |
| 10 | wiederholung | 7 | 20 | 15.6 |
| 11 | infolge | 4 | 6 | 15.5 |
| 12 | neurotische | 8 | 29 | 14.0 |
| 13 | anscheinend | 4 | 7 | 13.7 |
| 14 | schuldgefühl | 5 | 12 | 13.1 |
| 15 | peinlichen | 3 | 4 | 12.8 |
| 16 | schmerzlichen | 3 | 4 | 12.8 |
| 17 | mutter | 25 | 208 | 11.7 |
| 18 | universelle | 2 | 2 | 11.4 |
| 19 | geburtsvorgang | 2 | 2 | 11.4 |
| 20 | unbestreitbare | 2 | 1 | 11.4 |
| 21 | allgemeinheit | 2 | 1 | 11.4 |
| 22 | allgemein-mensch | 2 | 1 | 11.4 |
| 23 | negierung | 2 | 2 | 11.4 |
| 24 | wiederfindens | 2 | 1 | 11.4 |
| 25 | freiwilliges | 2 | 2 | 11.4 |

### rank_trauma_1924 — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 54; window tokens: 536

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | schriften | 4 | 8 | 27.2 |
| 2 | angewandten | 3 | 4 | 24.2 |
| 3 | religiöse | 4 | 18 | 19.4 |
| 4 | wahrhaftigkeit | 2 | 2 | 19.1 |
| 5 | regungen | 2 | 2 | 19.1 |
| 6 | hineinblicken | 2 | 2 | 19.1 |
| 7 | mythendeutung | 2 | 2 | 19.1 |
| 8 | leipzig | 4 | 22 | 17.7 |
| 9 | wien | 5 | 45 | 17.1 |
| 10 | georg | 2 | 3 | 15.3 |
| 11 | klarheit | 2 | 4 | 13.6 |
| 12 | sublimierte | 2 | 4 | 13.6 |
| 13 | hospitalstrasse | 2 | 4 | 13.6 |
| 14 | roman | 2 | 5 | 12.4 |
| 15 | begriff | 2 | 6 | 11.5 |
| 16 | glaube | 2 | 7 | 10.8 |
| 17 | andreasgasse | 2 | 7 | 10.8 |
| 18 | primitive | 2 | 8 | 10.2 |
| 19 | realen | 2 | 9 | 9.7 |
| 20 | psychologischen | 2 | 10 | 9.2 |
| 21 | entwickelt | 2 | 11 | 8.8 |
| 22 | psychoanalytischer | 2 | 11 | 8.8 |
| 23 | lehre | 2 | 14 | 7.8 |
| 24 | deutung | 2 | 16 | 7.3 |
| 25 | philosophische | 2 | 18 | 6.8 |

### nietzsche_GT_1-8 — family **apollonian_dionysian** (Nietzsche (GT §1–8 form vocabulary))

Seed regex (`^(...)`): `apollin|apollo|dionys|traum|rausch|maass|mass|schein|schleier|bild|chor|individuation|principium|form|grenze|musik|plastisch|tanz|lyrik|satyr` — seed hits: 462; window tokens: 4372

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | erlösung | 9 | 6 | 17.4 |
| 2 | wiederum | 6 | 6 | 11.6 |
| 3 | andrerseits | 6 | 2 | 11.6 |
| 4 | kräfte | 5 | 5 | 9.7 |
| 5 | grausen | 5 | 4 | 9.7 |
| 6 | entweder | 5 | 2 | 9.7 |
| 7 | verhält | 5 | 5 | 9.7 |
| 8 | zustände | 5 | 4 | 9.7 |
| 9 | braucht | 5 | 3 | 9.7 |
| 10 | tragödie | 19 | 29 | 9.0 |
| 11 | sah | 4 | 4 | 7.7 |
| 12 | deutet | 4 | 3 | 7.7 |
| 13 | schrecken | 4 | 3 | 7.7 |
| 14 | darf | 4 | 4 | 7.7 |
| 15 | principii | 4 | 4 | 7.7 |
| 16 | einzelnen | 4 | 4 | 7.7 |
| 17 | erregte | 4 | 3 | 7.7 |
| 18 | dithyrambische | 4 | 3 | 7.7 |
| 19 | einzelne | 4 | 4 | 7.7 |
| 20 | wirkung | 4 | 4 | 7.7 |
| 21 | aufgehoben | 4 | 3 | 7.7 |
| 22 | sichtbar | 4 | 3 | 7.7 |
| 23 | ursprünglich | 4 | 4 | 7.7 |
| 24 | zustandes | 4 | 3 | 7.7 |
| 25 | sinne | 8 | 10 | 7.4 |

### nietzsche_GT_1-8 — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 58; window tokens: 574

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | schmerzlosem | 2 | 1 | 12.0 |
| 2 | weiten | 2 | 1 | 12.0 |
| 3 | strahlenden | 2 | 1 | 12.0 |
| 4 | unseren | 2 | 2 | 12.0 |
| 5 | versunken | 2 | 2 | 12.0 |
| 6 | majestät | 2 | 2 | 12.0 |
| 7 | drehn | 2 | 1 | 12.0 |
| 8 | selber | 2 | 1 | 12.0 |
| 9 | visionswelt | 2 | 2 | 12.0 |
| 10 | reine | 3 | 5 | 11.5 |
| 11 | machen | 2 | 3 | 8.3 |
| 12 | eignen | 2 | 4 | 6.7 |
| 13 | zuschauer | 3 | 12 | 5.4 |
| 14 | einzige | 2 | 6 | 4.8 |
| 15 | viel | 2 | 6 | 4.8 |
| 16 | lust | 2 | 7 | 4.1 |
| 17 | begriff | 2 | 7 | 4.1 |
| 18 | zugleich | 3 | 16 | 3.9 |
| 19 | derselben | 2 | 8 | 3.6 |
| 20 | weisheit | 2 | 10 | 2.8 |
| 21 | satyr | 2 | 10 | 2.8 |
| 22 | sieht | 2 | 11 | 2.5 |
| 23 | können | 2 | 13 | 2.0 |
| 24 | dichter | 2 | 13 | 2.0 |
| 25 | apollinische | 2 | 14 | 1.7 |

### nietzsche_JGB — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 184; window tokens: 1824

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | priori | 5 | 5 | 34.3 |
| 2 | abgrund | 4 | 3 | 27.4 |
| 3 | falsche | 3 | 3 | 20.5 |
| 4 | synthetische | 3 | 3 | 20.5 |
| 5 | fasst | 3 | 2 | 20.5 |
| 6 | blauen | 3 | 2 | 20.5 |
| 7 | synthetischen | 3 | 4 | 16.1 |
| 8 | verzichtleisten | 2 | 2 | 13.7 |
| 9 | meers | 2 | 2 | 13.7 |
| 10 | anzüchtet | 2 | 1 | 13.7 |
| 11 | zugrundegehens | 2 | 1 | 13.7 |
| 12 | treuen | 2 | 1 | 13.7 |
| 13 | leeren | 2 | 1 | 13.7 |
| 14 | selten | 5 | 22 | 11.8 |
| 15 | einwand | 2 | 3 | 9.9 |
| 16 | glaubwürdigkeit | 2 | 3 | 9.9 |
| 17 | erträglich | 2 | 3 | 9.9 |
| 18 | weite | 2 | 3 | 9.9 |
| 19 | bewundert | 2 | 3 | 9.9 |
| 20 | vertheidigen | 2 | 3 | 9.9 |
| 21 | grau | 2 | 3 | 9.9 |
| 22 | in’s | 5 | 32 | 8.3 |
| 23 | aufgemacht | 2 | 4 | 8.3 |
| 24 | verstummen | 2 | 4 | 8.3 |
| 25 | stärke | 3 | 11 | 8.2 |

### nietzsche_JGB — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 29; window tokens: 290

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | üppigkeit | 2 | 3 | 17.3 |
| 2 | vieler | 2 | 4 | 15.5 |
| 3 | himmel | 2 | 6 | 13.5 |
| 4 | volk | 2 | 25 | 7.4 |
| 5 | fast | 2 | 29 | 6.8 |
| 6 | tiefe | 2 | 35 | 6.1 |
| 7 | alten | 2 | 41 | 5.5 |
| 8 | irgend | 2 | 60 | 4.1 |

### nietzsche_JGB — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 23; window tokens: 230

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | auges | 2 | 2 | 22.0 |
| 2 | zögern | 2 | 4 | 16.5 |
| 3 | reden | 3 | 27 | 14.4 |
| 4 | heraus | 2 | 20 | 9.1 |
| 5 | stolz | 2 | 21 | 8.9 |
| 6 | geben | 2 | 27 | 7.9 |
| 7 | kraft | 2 | 34 | 7.0 |
| 8 | gut | 2 | 57 | 5.1 |
| 9 | giebt | 2 | 121 | 2.6 |

### nietzsche_JGB — family **passage** (Foucault)

Seed regex (`^(...)`): `übergang|durchgang|pforte|thür|tür|thor|brücke|schiff|wander|weg|reise|fahrt|schwelle` — seed hits: 69; window tokens: 686

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | zustandes | 2 | 2 | 17.6 |
| 2 | bestraft | 2 | 2 | 17.6 |
| 3 | entscheidungen | 2 | 2 | 17.6 |
| 4 | geheimnissvollen | 2 | 3 | 13.8 |
| 5 | neuen | 4 | 31 | 12.1 |
| 6 | dorthin | 2 | 4 | 12.1 |
| 7 | zarten | 2 | 4 | 12.1 |
| 8 | proben | 2 | 5 | 11.0 |
| 9 | hintergrunde | 2 | 5 | 11.0 |
| 10 | gehn | 3 | 17 | 10.9 |
| 11 | mal | 3 | 17 | 10.9 |
| 12 | psychologie | 2 | 6 | 10.1 |
| 13 | gefühl | 3 | 21 | 9.6 |
| 14 | worten | 2 | 8 | 8.8 |
| 15 | erscheint | 2 | 9 | 8.3 |
| 16 | sehe | 2 | 11 | 7.4 |
| 17 | besser | 2 | 12 | 7.0 |
| 18 | steht | 3 | 36 | 6.6 |
| 19 | beinahe | 3 | 37 | 6.4 |
| 20 | jenem | 2 | 14 | 6.4 |
| 21 | dingen | 2 | 15 | 6.2 |
| 22 | lernen | 2 | 15 | 6.2 |
| 23 | stelle | 2 | 15 | 6.2 |
| 24 | zwei | 2 | 15 | 6.2 |
| 25 | europa’s | 2 | 17 | 5.7 |

### nietzsche_Za-IV — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 38; window tokens: 378

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | wanderer | 5 | 8 | 31.1 |
| 2 | brauche | 2 | 2 | 16.6 |
| 3 | freiwillige | 3 | 11 | 12.3 |
| 4 | andern | 2 | 4 | 11.1 |
| 5 | fast | 2 | 7 | 8.4 |
| 6 | vergieb | 2 | 9 | 7.3 |
| 7 | gewissenhafte | 2 | 9 | 7.3 |
| 8 | dein | 3 | 26 | 7.1 |
| 9 | liegt | 3 | 27 | 6.8 |
| 10 | antwortete | 3 | 29 | 6.5 |
| 11 | hast | 2 | 14 | 5.5 |
| 12 | bettler | 2 | 15 | 5.2 |
| 13 | eure | 2 | 19 | 4.4 |
| 14 | ach | 2 | 24 | 3.5 |
| 15 | zarathustra’s | 2 | 30 | 2.8 |
| 16 | lange | 2 | 50 | 1.3 |
| 17 | zarathustra | 5 | 233 | 0.4 |
| 18 | sprach | 2 | 101 | 0.1 |

### nietzsche_Za-IV — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 49; window tokens: 482

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | welch | 4 | 4 | 31.3 |
| 2 | tiefe | 5 | 17 | 19.0 |
| 3 | rosenrothe | 2 | 1 | 15.6 |
| 4 | entwölktes | 2 | 1 | 15.6 |
| 5 | bucht | 2 | 2 | 15.6 |
| 6 | singe | 2 | 2 | 15.6 |
| 7 | manches | 2 | 1 | 15.6 |
| 8 | ward | 4 | 16 | 13.8 |
| 9 | schiff | 2 | 3 | 11.9 |
| 10 | standen | 2 | 3 | 11.9 |
| 11 | lang | 2 | 5 | 9.0 |
| 12 | lacht | 2 | 6 | 8.2 |
| 13 | alte | 4 | 36 | 7.5 |
| 14 | plötzlich | 2 | 7 | 7.5 |
| 15 | hört | 2 | 8 | 6.9 |
| 16 | welt | 4 | 40 | 6.7 |
| 17 | blieb | 2 | 9 | 6.4 |
| 18 | hart | 2 | 9 | 6.4 |
| 19 | nothschrei | 2 | 10 | 6.0 |
| 20 | glück | 3 | 27 | 5.6 |
| 21 | geschah | 2 | 11 | 5.6 |
| 22 | herzen | 3 | 29 | 5.2 |
| 23 | besten | 2 | 12 | 5.2 |
| 24 | mitternacht | 2 | 14 | 4.6 |
| 25 | seele | 2 | 22 | 3.0 |

### nietzsche_Za-IV — family **passage** (Foucault)

Seed regex (`^(...)`): `übergang|durchgang|pforte|thür|tür|thor|brücke|schiff|wander|weg|reise|fahrt|schwelle` — seed hits: 83; window tokens: 820

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | führt | 6 | 6 | 40.6 |
| 2 | höhle | 12 | 44 | 31.8 |
| 3 | dorthin | 3 | 3 | 20.3 |
| 4 | gieng | 5 | 17 | 14.0 |
| 5 | heiligen | 3 | 5 | 13.7 |
| 6 | athmen | 2 | 2 | 13.5 |
| 7 | eifersüchtiger | 2 | 1 | 13.5 |
| 8 | worauf | 2 | 1 | 13.5 |
| 9 | eifersüchtig | 2 | 1 | 13.5 |
| 10 | leiter | 2 | 1 | 13.5 |
| 11 | trete | 2 | 1 | 13.5 |
| 12 | bucht | 2 | 2 | 13.5 |
| 13 | schriebe | 2 | 1 | 13.5 |
| 14 | unbedingten | 2 | 2 | 13.5 |
| 15 | schatten | 5 | 25 | 10.2 |
| 16 | schlecht | 3 | 8 | 10.0 |
| 17 | hinauf | 4 | 16 | 9.9 |
| 18 | zarathustra’s | 5 | 30 | 8.5 |
| 19 | geht | 4 | 19 | 8.5 |
| 20 | kleine | 3 | 10 | 8.5 |
| 21 | wozu | 2 | 4 | 8.1 |
| 22 | eilig | 2 | 4 | 8.1 |
| 23 | mögen | 2 | 4 | 8.1 |
| 24 | hörst | 2 | 5 | 7.0 |
| 25 | willst | 4 | 24 | 6.8 |

### nietzsche_Za-IV — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 115; window tokens: 1132

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | schloss | 3 | 3 | 18.3 |
| 2 | manne | 3 | 3 | 18.3 |
| 3 | hellen | 3 | 1 | 18.3 |
| 4 | mund | 5 | 11 | 16.0 |
| 5 | lehrt | 4 | 7 | 15.2 |
| 6 | abgründe | 3 | 4 | 13.9 |
| 7 | dunklem | 2 | 1 | 12.2 |
| 8 | hauch | 2 | 2 | 12.2 |
| 9 | greis | 2 | 1 | 12.2 |
| 10 | scharfen | 2 | 2 | 12.2 |
| 11 | fahren | 2 | 2 | 12.2 |
| 12 | angesehn | 2 | 2 | 12.2 |
| 13 | suchten | 2 | 2 | 12.2 |
| 14 | husch | 3 | 5 | 11.8 |
| 15 | wandte | 3 | 6 | 10.3 |
| 16 | falschmünzer | 2 | 3 | 8.5 |
| 17 | gästen | 2 | 3 | 8.5 |
| 18 | blieb | 3 | 9 | 7.5 |
| 19 | schwarzen | 2 | 4 | 6.9 |
| 20 | erschrak | 2 | 4 | 6.9 |
| 21 | gelüstet | 2 | 4 | 6.9 |
| 22 | thränen | 2 | 4 | 6.9 |
| 23 | euer | 3 | 10 | 6.8 |
| 24 | jeder | 3 | 10 | 6.8 |
| 25 | diess | 6 | 38 | 6.6 |

### nietzsche_FW — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 273; window tokens: 2706

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | offenen | 4 | 5 | 21.1 |
| 2 | wobei | 3 | 3 | 19.5 |
| 3 | streng | 3 | 4 | 15.1 |
| 4 | gebärde | 4 | 9 | 14.0 |
| 5 | phantasiren | 2 | 2 | 13.0 |
| 6 | weites | 2 | 1 | 13.0 |
| 7 | weissliches | 2 | 1 | 13.0 |
| 8 | allzuoft | 2 | 2 | 13.0 |
| 9 | ertrug | 2 | 2 | 13.0 |
| 10 | leo’s | 2 | 1 | 13.0 |
| 11 | entläuft | 2 | 1 | 13.0 |
| 12 | gegenüber | 2 | 2 | 13.0 |
| 13 | gnädiger | 2 | 1 | 13.0 |
| 14 | scharfen | 2 | 2 | 13.0 |
| 15 | hässlichen | 2 | 2 | 13.0 |
| 16 | festigkeit | 2 | 2 | 13.0 |
| 17 | schändlicher | 2 | 2 | 13.0 |
| 18 | litterat | 2 | 2 | 13.0 |
| 19 | wesentlich | 4 | 10 | 13.0 |
| 20 | ästhetischen | 3 | 5 | 12.9 |
| 21 | darüber | 4 | 11 | 12.1 |
| 22 | wenigen | 3 | 6 | 11.4 |
| 23 | moralischen | 5 | 23 | 9.8 |
| 24 | sehkraft | 2 | 3 | 9.3 |
| 25 | ruhigem | 2 | 3 | 9.3 |

### nietzsche_FW — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 42; window tokens: 420

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | unterirdische | 2 | 2 | 20.5 |
| 2 | vorher | 2 | 4 | 14.9 |
| 3 | einsamkeit | 2 | 9 | 11.0 |
| 4 | meer | 2 | 15 | 8.8 |
| 5 | hinter | 2 | 16 | 8.6 |
| 6 | ruhe | 2 | 19 | 7.9 |
| 7 | finden | 2 | 22 | 7.3 |
| 8 | dagegen | 2 | 24 | 7.0 |
| 9 | oft | 2 | 39 | 5.1 |
| 10 | glück | 2 | 40 | 5.0 |
| 11 | lebens | 2 | 42 | 4.9 |
| 12 | wenig | 2 | 44 | 4.7 |
| 13 | wesen | 2 | 44 | 4.7 |
| 14 | leidenschaft | 2 | 45 | 4.6 |
| 15 | ebenso | 2 | 55 | 3.9 |
| 16 | art | 2 | 122 | 1.5 |
| 17 | leben | 2 | 153 | 1.0 |
| 18 | selber | 2 | 165 | 0.8 |
| 19 | menschen | 2 | 235 | 0.2 |

### nietzsche_FW — family **passage** (Foucault)

Seed regex (`^(...)`): `übergang|durchgang|pforte|thür|tür|thor|brücke|schiff|wander|weg|reise|fahrt|schwelle` — seed hits: 100; window tokens: 996

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | dächer | 2 | 1 | 17.0 |
| 2 | ruhebett | 2 | 2 | 17.0 |
| 3 | hinter | 4 | 16 | 16.4 |
| 4 | land | 3 | 7 | 16.1 |
| 5 | weit | 3 | 11 | 12.8 |
| 6 | gegangen | 3 | 11 | 12.8 |
| 7 | warf | 2 | 4 | 11.5 |
| 8 | phantasterei | 2 | 5 | 10.4 |
| 9 | hinauf | 2 | 5 | 10.4 |
| 10 | höhen | 2 | 5 | 10.4 |
| 11 | fragte | 2 | 5 | 10.4 |
| 12 | meere | 2 | 5 | 10.4 |
| 13 | zieht | 2 | 6 | 9.5 |
| 14 | sonne | 3 | 22 | 8.5 |
| 15 | stadt | 2 | 8 | 8.2 |
| 16 | giebt | 6 | 111 | 7.4 |
| 17 | glücke | 2 | 10 | 7.2 |
| 18 | verlieren | 2 | 10 | 7.2 |
| 19 | nächsten | 2 | 11 | 6.8 |
| 20 | jedes | 3 | 33 | 6.3 |
| 21 | schatten | 2 | 13 | 6.2 |
| 22 | tages | 2 | 14 | 5.9 |
| 23 | unsrer | 2 | 17 | 5.1 |
| 24 | ehre | 2 | 22 | 4.2 |
| 25 | trieb | 2 | 23 | 4.0 |

### nietzsche_FW — family **exclusion** (Foucault)

Seed regex (`^(...)`): `ausschl|ausgestoss|ausgestoß|verbann|verstoss|verstoß|einsperr|gefangen|wahnsinn|irr|aussätz|bann` — seed hits: 66; window tokens: 652

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | ausbricht | 2 | 2 | 18.7 |
| 2 | bekanntere | 2 | 1 | 18.7 |
| 3 | schwerlich | 2 | 2 | 18.7 |
| 4 | unten | 2 | 3 | 14.9 |
| 5 | bekannte | 2 | 3 | 14.9 |
| 6 | köpfen | 2 | 3 | 14.9 |
| 7 | vier | 2 | 4 | 13.2 |
| 8 | erwägt | 2 | 6 | 11.1 |
| 9 | deine | 3 | 25 | 10.1 |
| 10 | glücke | 2 | 10 | 8.8 |
| 11 | empfunden | 2 | 10 | 8.8 |
| 12 | drei | 2 | 14 | 7.4 |
| 13 | solcher | 2 | 19 | 6.2 |
| 14 | namentlich | 2 | 22 | 5.7 |
| 15 | wahrheit | 3 | 55 | 5.7 |
| 16 | worden | 2 | 29 | 4.6 |
| 17 | welt | 3 | 87 | 3.5 |
| 18 | lebens | 2 | 42 | 3.4 |
| 19 | moral | 2 | 45 | 3.1 |
| 20 | lassen | 2 | 47 | 3.0 |
| 21 | müssen | 2 | 48 | 2.9 |
| 22 | unsere | 2 | 62 | 2.2 |
| 23 | mensch | 2 | 109 | 0.7 |
| 24 | vielleicht | 2 | 130 | 0.4 |
| 25 | menschen | 3 | 235 | 0.3 |

### nietzsche_DD — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 6; window tokens: 60

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | wanderer | 2 | 2 | 16.4 |
| 2 | zarathustras | 2 | 2 | 16.4 |
| 3 | nannte | 2 | 2 | 16.4 |
| 4 | selber | 2 | 17 | 4.6 |

### nietzsche_DD — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 13; window tokens: 130

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | wahrheit | 5 | 12 | 17.5 |
| 2 | sehe | 3 | 4 | 15.5 |
| 3 | aufwärts | 2 | 2 | 13.3 |
| 4 | gross | 2 | 2 | 13.3 |
| 5 | einsam | 2 | 4 | 7.9 |
| 6 | komm | 2 | 5 | 6.8 |

### nietzsche_DD — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 24; window tokens: 230

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | abgründe | 3 | 2 | 16.5 |
| 2 | sammtenen | 3 | 1 | 16.5 |
| 3 | trifft | 3 | 2 | 16.5 |
| 4 | lange | 4 | 8 | 11.4 |
| 5 | fels | 2 | 2 | 11.0 |
| 6 | zögert | 2 | 1 | 11.0 |
| 7 | holt | 2 | 2 | 11.0 |
| 8 | dunklem | 2 | 1 | 11.0 |
| 9 | zögernden | 2 | 1 | 11.0 |
| 10 | lieblich | 2 | 1 | 11.0 |
| 11 | tiefe | 2 | 3 | 7.3 |
| 12 | glüht | 2 | 3 | 7.3 |
| 13 | dein | 3 | 9 | 5.8 |
| 14 | wahrheit | 2 | 12 | 1.5 |
| 15 | gleich | 2 | 14 | 1.1 |

### nietzsche_DD — family **return** (Rank)

Seed regex (`^(...)`): `mutterleib|uterus|rückkehr|wiedergeburt|urzustand|höhle|wasser|meer|schlaf|wiederherstell|zurück|intrauterin|embryo` — seed hits: 10; window tokens: 100

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | seele | 2 | 4 | 8.9 |
| 2 | deiner | 2 | 5 | 7.8 |
| 3 | komm | 2 | 5 | 7.8 |
| 4 | unbekannter | 2 | 6 | 6.9 |

### nietzsche_BVN-1889 — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 1; window tokens: 10

_No collocate reached the minimum window count of 2._

### nietzsche_BVN-1889 — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 2; window tokens: 20

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | welt | 2 | 8 | 9.1 |

## B. Doppelgänger norming corpus (all seven families per text)

### hoffmann_elixiere — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 33; window tokens: 330

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | gräßlichen | 4 | 13 | 30.3 |
| 2 | finstre | 2 | 9 | 13.7 |
| 3 | meines | 2 | 59 | 6.0 |
| 4 | kloster | 2 | 95 | 4.3 |
| 5 | stand | 2 | 126 | 3.4 |

### hoffmann_elixiere — family **return** (Rank)

Seed regex (`^(...)`): `mutterleib|uterus|rückkehr|wiedergeburt|urzustand|höhle|wasser|meer|schlaf|wiederherstell|zurück|intrauterin|embryo` — seed hits: 153; window tokens: 1524

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | tiefem | 5 | 13 | 25.4 |
| 2 | kehre | 2 | 2 | 17.0 |
| 3 | unreine | 2 | 2 | 17.0 |
| 4 | kloster | 8 | 95 | 15.7 |
| 5 | vermochte | 5 | 34 | 15.0 |
| 6 | erlag | 2 | 3 | 13.2 |
| 7 | entsetzt | 2 | 3 | 13.2 |
| 8 | angiola | 3 | 12 | 12.3 |
| 9 | hauch | 2 | 4 | 11.5 |
| 10 | gefoltert | 2 | 5 | 10.4 |
| 11 | sonnenzeit | 2 | 5 | 10.4 |
| 12 | standhaft | 2 | 5 | 10.4 |
| 13 | kalt | 2 | 6 | 9.5 |
| 14 | ermüdet | 2 | 6 | 9.5 |
| 15 | floß | 2 | 6 | 9.5 |
| 16 | flucht | 3 | 20 | 9.1 |
| 17 | leonardus | 5 | 66 | 8.9 |
| 18 | kehrte | 2 | 7 | 8.8 |
| 19 | kapuziners | 2 | 7 | 8.8 |
| 20 | abschnitt | 2 | 7 | 8.8 |
| 21 | tiefen | 3 | 22 | 8.5 |
| 22 | nacht | 4 | 49 | 7.6 |
| 23 | all | 3 | 26 | 7.6 |
| 24 | fand | 4 | 50 | 7.5 |
| 25 | graf | 4 | 52 | 7.2 |

### hoffmann_elixiere — family **separation** (Rank)

Seed regex (`^(...)`): `trennung|geburtsakt|nabelschnur|ablösung|abnabel|hebamme|schwelle|loslösung|geburtstrauma|urangst|angst` — seed hits: 34; window tokens: 340

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | scheuer | 2 | 4 | 17.5 |
| 2 | standen | 2 | 12 | 12.3 |
| 3 | seufzer | 2 | 13 | 11.9 |
| 4 | zweifel | 2 | 15 | 11.3 |
| 5 | tiefen | 2 | 22 | 9.7 |
| 6 | herz | 2 | 24 | 9.4 |
| 7 | entsetzen | 2 | 35 | 7.9 |
| 8 | voll | 2 | 36 | 7.8 |
| 9 | fühlte | 2 | 62 | 5.7 |
| 10 | vielleicht | 2 | 75 | 5.0 |
| 11 | endlich | 2 | 97 | 4.1 |

### hoffmann_elixiere — family **exclusion** (Foucault)

Seed regex (`^(...)`): `ausschl|ausgestoss|ausgestoß|verbann|verstoss|verstoß|einsperr|gefangen|wahnsinn|irr|aussätz|bann` — seed hits: 152; window tokens: 1516

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | mönch | 14 | 136 | 32.6 |
| 2 | rettet | 3 | 5 | 18.9 |
| 3 | hermogen | 8 | 82 | 17.8 |
| 4 | verzweiflung | 5 | 28 | 17.0 |
| 5 | melancholie | 2 | 2 | 17.0 |
| 6 | gotteslästerlichen | 2 | 2 | 17.0 |
| 7 | hunger | 2 | 2 | 17.0 |
| 8 | brudermörder | 2 | 2 | 17.0 |
| 9 | versammlungen | 2 | 1 | 17.0 |
| 10 | hebe | 3 | 7 | 16.1 |
| 11 | kriminalgericht | 3 | 7 | 16.1 |
| 12 | gebracht | 4 | 22 | 13.7 |
| 13 | aufs | 5 | 39 | 13.7 |
| 14 | schützt | 2 | 3 | 13.2 |
| 15 | spuren | 2 | 3 | 13.2 |
| 16 | fluch | 2 | 4 | 11.5 |
| 17 | frisch | 2 | 4 | 11.5 |
| 18 | bringt | 2 | 5 | 10.4 |
| 19 | stürzte | 3 | 18 | 9.8 |
| 20 | zenobio | 2 | 6 | 9.5 |
| 21 | wilden | 3 | 19 | 9.4 |
| 22 | försters | 2 | 7 | 8.8 |
| 23 | laßt | 2 | 7 | 8.8 |
| 24 | walde | 3 | 22 | 8.6 |
| 25 | stille | 2 | 8 | 8.2 |

### hoffmann_elixiere — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 71; window tokens: 706

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | unterbricht | 2 | 2 | 20.1 |
| 2 | blieb | 5 | 64 | 15.9 |
| 3 | laß | 3 | 15 | 15.3 |
| 4 | gekehrt | 2 | 8 | 11.2 |
| 5 | amtmann | 2 | 9 | 10.7 |
| 6 | frommen | 3 | 35 | 10.1 |
| 7 | einigen | 2 | 12 | 9.4 |
| 8 | ende | 2 | 14 | 8.8 |
| 9 | tisch | 2 | 23 | 6.8 |
| 10 | ruhig | 2 | 24 | 6.6 |
| 11 | gesellschaft | 2 | 24 | 6.6 |
| 12 | fuhr | 3 | 66 | 6.6 |
| 13 | stand | 4 | 126 | 6.3 |
| 14 | fort | 4 | 129 | 6.2 |
| 15 | trug | 2 | 30 | 5.8 |
| 16 | nahm | 2 | 39 | 4.8 |
| 17 | endlich | 3 | 97 | 4.6 |
| 18 | sprach | 4 | 181 | 4.1 |
| 19 | geworden | 2 | 47 | 4.1 |
| 20 | nacht | 2 | 49 | 4.0 |
| 21 | aurelie | 3 | 119 | 3.7 |
| 22 | heilige | 2 | 58 | 3.4 |
| 23 | frug | 2 | 60 | 3.3 |
| 24 | seele | 2 | 69 | 2.9 |
| 25 | bild | 2 | 70 | 2.8 |

### hoffmann_elixiere — family **passage** (Foucault)

Seed regex (`^(...)`): `übergang|durchgang|pforte|thür|tür|thor|brücke|schiff|wander|weg|reise|fahrt|schwelle` — seed hits: 197; window tokens: 1962

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | hebe | 10 | 7 | 80.1 |
| 2 | öffnete | 8 | 24 | 34.1 |
| 3 | mordes | 4 | 7 | 22.6 |
| 4 | weiten | 4 | 9 | 19.8 |
| 5 | hinaus | 5 | 18 | 19.2 |
| 6 | räumen | 2 | 2 | 16.0 |
| 7 | angelehnt | 2 | 2 | 16.0 |
| 8 | kabinetts | 2 | 2 | 16.0 |
| 9 | schwüle | 2 | 2 | 16.0 |
| 10 | geschäftig | 2 | 2 | 16.0 |
| 11 | bahnte | 2 | 1 | 16.0 |
| 12 | gesprengt | 2 | 2 | 16.0 |
| 13 | bewachte | 2 | 2 | 16.0 |
| 14 | übermannte | 2 | 2 | 16.0 |
| 15 | morgen | 6 | 40 | 15.5 |
| 16 | brautgemachs | 2 | 3 | 12.2 |
| 17 | klopfte | 3 | 11 | 11.4 |
| 18 | führte | 4 | 25 | 10.8 |
| 19 | hierher | 3 | 12 | 10.8 |
| 20 | preußen | 2 | 4 | 10.5 |
| 21 | spielzeug | 2 | 4 | 10.5 |
| 22 | nebenzimmer | 2 | 4 | 10.5 |
| 23 | behalten | 2 | 4 | 10.5 |
| 24 | königsberg | 2 | 4 | 10.5 |
| 25 | angeln | 2 | 4 | 10.5 |

### hoffmann_elixiere — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 654; window tokens: 6426

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | scharf | 13 | 12 | 73.2 |
| 2 | tränen | 17 | 31 | 54.8 |
| 3 | funkelnden | 9 | 6 | 50.7 |
| 4 | hohlen | 8 | 7 | 45.0 |
| 5 | schwarzen | 9 | 11 | 40.5 |
| 6 | stieren | 7 | 6 | 39.4 |
| 7 | gerichtet | 8 | 10 | 35.3 |
| 8 | stand | 24 | 126 | 25.0 |
| 9 | dunkelblauen | 4 | 2 | 22.5 |
| 10 | strahlenden | 4 | 3 | 22.5 |
| 11 | gräßlichen | 7 | 13 | 22.2 |
| 12 | sah | 21 | 112 | 21.4 |
| 13 | demselben | 8 | 21 | 18.7 |
| 14 | gefalteten | 3 | 3 | 16.9 |
| 15 | niedergeschlagenen | 3 | 3 | 16.9 |
| 16 | niederschlug | 3 | 2 | 16.9 |
| 17 | beleben | 3 | 1 | 16.9 |
| 18 | klaren | 5 | 9 | 16.3 |
| 19 | frug | 13 | 60 | 16.3 |
| 20 | schwieg | 5 | 9 | 16.3 |
| 21 | gerichteten | 4 | 7 | 13.3 |
| 22 | ernst | 6 | 17 | 13.1 |
| 23 | jäher | 3 | 4 | 12.5 |
| 24 | haupte | 3 | 4 | 12.5 |
| 25 | ernstem | 3 | 4 | 12.5 |

### chamisso_schlemihl — family **double** (Rank)

Seed regex (`^(...)`): `doppelg|spiegel|ebenbild|zwilling|schatten|abbild|dämon|seelen` — seed hits: 126; window tokens: 1250

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | wesen | 3 | 2 | 17.1 |
| 2 | gekommen | 4 | 7 | 13.6 |
| 3 | obgleich | 3 | 4 | 12.7 |
| 4 | kurz | 3 | 4 | 12.7 |
| 5 | angeboren | 2 | 1 | 11.4 |
| 6 | verliehen | 2 | 1 | 11.4 |
| 7 | sehn | 2 | 1 | 11.4 |
| 8 | breiten | 2 | 2 | 11.4 |
| 9 | schönes | 2 | 2 | 11.4 |
| 10 | sichtbarlich | 2 | 2 | 11.4 |
| 11 | falschen | 2 | 2 | 11.4 |
| 12 | zeigen | 2 | 2 | 11.4 |
| 13 | leider | 2 | 2 | 11.4 |
| 14 | nägel | 2 | 2 | 11.4 |
| 15 | fest | 5 | 17 | 9.3 |
| 16 | eignen | 3 | 7 | 8.0 |
| 17 | gelassen | 2 | 3 | 7.7 |
| 18 | hätten | 2 | 3 | 7.7 |
| 19 | notwendig | 2 | 3 | 7.7 |
| 20 | beiden | 2 | 3 | 7.7 |
| 21 | geld | 2 | 3 | 7.7 |
| 22 | gleich | 4 | 15 | 6.7 |
| 23 | schwieg | 2 | 4 | 6.1 |
| 24 | dienen | 2 | 4 | 6.1 |
| 25 | unsichtbar | 2 | 4 | 6.1 |

### chamisso_schlemihl — family **return** (Rank)

Seed regex (`^(...)`): `mutterleib|uterus|rückkehr|wiedergeburt|urzustand|höhle|wasser|meer|schlaf|wiederherstell|zurück|intrauterin|embryo` — seed hits: 59; window tokens: 588

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | hafen | 3 | 5 | 15.0 |
| 2 | ungestört | 2 | 2 | 14.4 |
| 3 | gesunden | 2 | 1 | 14.4 |
| 4 | august | 2 | 1 | 14.4 |
| 5 | julius | 2 | 2 | 14.4 |
| 6 | winde | 2 | 2 | 14.4 |
| 7 | bewußtsein | 2 | 2 | 14.4 |
| 8 | öden | 2 | 3 | 10.7 |
| 9 | wirtshause | 2 | 3 | 10.7 |
| 10 | morgen | 3 | 10 | 9.8 |
| 11 | dennoch | 2 | 4 | 9.0 |
| 12 | andern | 4 | 25 | 8.0 |
| 13 | berlin | 2 | 5 | 7.8 |
| 14 | mädchen | 2 | 5 | 7.8 |
| 15 | floh | 2 | 5 | 7.8 |
| 16 | zwei | 3 | 14 | 7.7 |
| 17 | schritte | 3 | 14 | 7.7 |
| 18 | einst | 2 | 8 | 5.7 |
| 19 | stadt | 2 | 10 | 4.8 |
| 20 | hinter | 2 | 10 | 4.8 |
| 21 | hause | 2 | 11 | 4.5 |
| 22 | trat | 3 | 28 | 3.9 |
| 23 | nacht | 2 | 14 | 3.6 |
| 24 | menschen | 2 | 14 | 3.6 |
| 25 | mußte | 3 | 33 | 3.2 |

### chamisso_schlemihl — family **separation** (Rank)

Seed regex (`^(...)`): `trennung|geburtsakt|nabelschnur|ablösung|abnabel|hebamme|schwelle|loslösung|geburtstrauma|urangst|angst` — seed hits: 8; window tokens: 80

_No collocate reached the minimum window count of 2._

### chamisso_schlemihl — family **exclusion** (Foucault)

Seed regex (`^(...)`): `ausschl|ausgestoss|ausgestoß|verbann|verstoss|verstoß|einsperr|gefangen|wahnsinn|irr|aussätz|bann` — seed hits: 7; window tokens: 70

_No collocate reached the minimum window count of 2._

### chamisso_schlemihl — family **silence** (Foucault)

Seed regex (`^(...)`): `schweig|stumm|still|verstumm|lautlos|sprachlos` — seed hits: 30; window tokens: 300

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | erfolgte | 3 | 2 | 25.7 |
| 2 | langes | 3 | 2 | 25.7 |
| 3 | sitz | 2 | 2 | 17.1 |
| 4 | geschehen | 3 | 8 | 15.2 |
| 5 | gesucht | 2 | 3 | 13.3 |
| 6 | blickte | 2 | 6 | 9.6 |
| 7 | lag | 2 | 8 | 8.3 |
| 8 | mutter | 2 | 9 | 7.8 |
| 9 | ließ | 3 | 30 | 6.9 |
| 10 | wollen | 2 | 14 | 6.0 |
| 11 | weg | 2 | 19 | 4.8 |
| 12 | wort | 2 | 23 | 4.1 |
| 13 | nahm | 2 | 26 | 3.7 |
| 14 | stand | 2 | 30 | 3.2 |
| 15 | sah | 2 | 49 | 1.7 |

### chamisso_schlemihl — family **passage** (Foucault)

Seed regex (`^(...)`): `übergang|durchgang|pforte|thür|tür|thor|brücke|schiff|wander|weg|reise|fahrt|schwelle` — seed hits: 68; window tokens: 678

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | erst | 5 | 11 | 19.9 |
| 2 | teil | 3 | 5 | 14.2 |
| 3 | golddurchwirkten | 2 | 2 | 13.8 |
| 4 | preußen | 2 | 2 | 13.8 |
| 5 | verbot | 2 | 2 | 13.8 |
| 6 | wißbegieriger | 2 | 1 | 13.8 |
| 7 | tagebuch | 2 | 1 | 13.8 |
| 8 | setzte | 4 | 15 | 11.0 |
| 9 | macht | 3 | 8 | 10.5 |
| 10 | galt | 2 | 3 | 10.1 |
| 11 | begegnete | 2 | 3 | 10.1 |
| 12 | menge | 2 | 3 | 10.1 |
| 13 | keines | 2 | 3 | 10.1 |
| 14 | welt | 5 | 28 | 9.8 |
| 15 | fort | 4 | 18 | 9.5 |
| 16 | stillschweigend | 2 | 4 | 8.4 |
| 17 | teppich | 2 | 5 | 7.3 |
| 18 | suchte | 2 | 5 | 7.3 |
| 19 | band | 2 | 7 | 5.8 |
| 20 | leicht | 2 | 8 | 5.2 |
| 21 | weit | 2 | 8 | 5.2 |
| 22 | namen | 2 | 9 | 4.8 |
| 23 | sprang | 2 | 9 | 4.8 |
| 24 | viele | 2 | 10 | 4.3 |
| 25 | sprach | 2 | 12 | 3.7 |

### chamisso_schlemihl — family **gaze** (Foucault)

Seed regex (`^(...)`): `blick|auge|anschau|anblick|beobacht|prüf|richter|urtheil|urteil|schau|starr` — seed hits: 75; window tokens: 740

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | warf | 6 | 17 | 19.2 |
| 2 | maß | 2 | 2 | 13.5 |
| 3 | genießen | 2 | 2 | 13.5 |
| 4 | abwenden | 2 | 1 | 13.5 |
| 5 | fragte | 2 | 1 | 13.5 |
| 6 | verhaßter | 2 | 2 | 13.5 |
| 7 | ritt | 2 | 2 | 13.5 |
| 8 | gierigen | 2 | 1 | 13.5 |
| 9 | klopfenden | 2 | 1 | 13.5 |
| 10 | erhub | 2 | 1 | 13.5 |
| 11 | finster | 2 | 2 | 13.5 |
| 12 | erschrak | 3 | 8 | 10.0 |
| 13 | schnellen | 2 | 3 | 9.7 |
| 14 | getreu | 2 | 3 | 9.7 |
| 15 | herzens | 2 | 3 | 9.7 |
| 16 | still | 3 | 9 | 9.2 |
| 17 | tief | 2 | 4 | 8.1 |
| 18 | öffnete | 2 | 4 | 8.1 |
| 19 | hut | 2 | 5 | 7.0 |
| 20 | erscheinung | 2 | 6 | 6.1 |
| 21 | nie | 2 | 6 | 6.1 |
| 22 | eignen | 2 | 7 | 5.5 |
| 23 | machte | 2 | 8 | 4.9 |
| 24 | bald | 3 | 23 | 3.8 |
| 25 | wirklich | 2 | 11 | 3.7 |

### maupassant_horla — family **double** (Rank)

Seed regex (`^(...)`): `double|miroir|reflet|ombre|image|sosie` — seed hits: 16; window tokens: 160

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | brume | 2 | 2 | 22.2 |
| 2 | tour | 3 | 20 | 16.6 |
| 3 | seconde | 2 | 7 | 13.9 |
| 4 | dedans | 2 | 10 | 12.3 |
| 5 | porte | 3 | 60 | 10.0 |
| 6 | pensée | 2 | 17 | 10.0 |
| 7 | l'homme | 2 | 27 | 8.2 |
| 8 | avait | 2 | 117 | 2.9 |

### maupassant_horla — family **return** (Rank)

Seed regex (`^(...)`): `retour|eau|mer|sommeil|mère|maison` — seed hits: 143; window tokens: 1424

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | l'après-midi | 4 | 4 | 26.9 |
| 2 | bontemps | 5 | 7 | 25.4 |
| 3 | clochette | 5 | 10 | 20.2 |
| 4 | approchant | 3 | 4 | 15.8 |
| 5 | paumelle | 3 | 4 | 15.8 |
| 6 | sable | 2 | 2 | 13.5 |
| 7 | déracine | 2 | 2 | 13.5 |
| 8 | soulève | 2 | 2 | 13.5 |
| 9 | détruit | 2 | 2 | 13.5 |
| 10 | banale | 2 | 1 | 13.5 |
| 11 | s'asseoir | 2 | 2 | 13.5 |
| 12 | cesse | 3 | 8 | 10.0 |
| 13 | étendu | 2 | 3 | 9.7 |
| 14 | tombé | 2 | 3 | 9.7 |
| 15 | pigeons | 2 | 3 | 9.7 |
| 16 | aperçurent | 2 | 3 | 9.7 |
| 17 | n'avaient | 2 | 4 | 8.1 |
| 18 | accablé | 2 | 4 | 8.1 |
| 19 | fossé | 2 | 4 | 8.1 |
| 20 | enfin | 4 | 21 | 7.7 |
| 21 | arbres | 3 | 12 | 7.3 |
| 22 | jure | 2 | 5 | 6.9 |
| 23 | murmura | 3 | 13 | 6.9 |
| 24 | garder | 2 | 5 | 6.9 |
| 25 | demi-heure | 2 | 5 | 6.9 |

### maupassant_horla — family **separation** (Rank)

Seed regex (`^(...)`): `séparat|seuil|porte|naissance|seul` — seed hits: 141; window tokens: 1394

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | sou | 4 | 4 | 27.1 |
| 2 | ouvrit | 4 | 5 | 22.2 |
| 3 | fermé | 3 | 3 | 20.3 |
| 4 | s'ouvrit | 4 | 6 | 19.6 |
| 5 | double | 3 | 5 | 13.7 |
| 6 | soin | 2 | 2 | 13.5 |
| 7 | l'enfermai | 2 | 1 | 13.5 |
| 8 | d'entrée | 2 | 2 | 13.5 |
| 9 | éteint | 2 | 2 | 13.5 |
| 10 | confidences | 2 | 2 | 13.5 |
| 11 | implorait | 2 | 1 | 13.5 |
| 12 | coups | 4 | 13 | 11.7 |
| 13 | savait | 3 | 7 | 11.0 |
| 14 | poussa | 3 | 8 | 10.1 |
| 15 | n'osait | 2 | 3 | 9.8 |
| 16 | ouvrir | 2 | 3 | 9.8 |
| 17 | soulever | 2 | 4 | 8.1 |
| 18 | demoiselles | 2 | 4 | 8.1 |
| 19 | ouvertes | 2 | 4 | 8.1 |
| 20 | laissant | 2 | 4 | 8.1 |
| 21 | chef | 2 | 4 | 8.1 |
| 22 | désir | 2 | 4 | 8.1 |
| 23 | l'après-midi | 2 | 4 | 8.1 |
| 24 | atteignirent | 2 | 4 | 8.1 |
| 25 | désert | 2 | 4 | 8.1 |

### maupassant_horla — family **exclusion** (Foucault)

Seed regex (`^(...)`): `exclu|enferm|prison|fou|folie|asile|aliéné|renferm|cellule|banni` — seed hits: 49; window tokens: 482

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | rendit | 3 | 3 | 26.7 |
| 2 | croirais | 2 | 2 | 17.8 |
| 3 | n'étais | 2 | 2 | 17.8 |
| 4 | épidémie | 2 | 1 | 17.8 |
| 5 | comparable | 2 | 1 | 17.8 |
| 6 | deviens | 2 | 3 | 14.0 |
| 7 | ordonna | 2 | 3 | 14.0 |
| 8 | rage | 2 | 4 | 12.3 |
| 9 | s'y | 2 | 5 | 11.1 |
| 10 | juillet | 3 | 18 | 10.8 |
| 11 | absolument | 2 | 6 | 10.3 |
| 12 | êtes | 2 | 7 | 9.5 |
| 13 | j'ai | 6 | 117 | 8.7 |
| 14 | deux | 6 | 126 | 8.0 |
| 15 | maître | 2 | 10 | 8.0 |
| 16 | mort | 3 | 29 | 8.0 |
| 17 | randel | 2 | 13 | 6.9 |
| 18 | neige | 2 | 18 | 5.6 |
| 19 | semblait | 2 | 20 | 5.2 |
| 20 | suis | 3 | 55 | 4.6 |
| 21 | nouveau | 2 | 25 | 4.4 |
| 22 | fit | 2 | 25 | 4.4 |
| 23 | femmes | 2 | 40 | 2.8 |
| 24 | l'air | 2 | 44 | 2.5 |
| 25 | c'est | 2 | 126 | 0.2 |

### maupassant_horla — family **silence** (Foucault)

Seed regex (`^(...)`): `silenc|muet|taire|tais|tus|tut` — seed hits: 24; window tokens: 240

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | demeura | 2 | 4 | 15.1 |
| 2 | laisse | 2 | 6 | 13.0 |
| 3 | profond | 2 | 7 | 12.3 |
| 4 | peu | 3 | 53 | 8.4 |
| 5 | mort | 2 | 29 | 6.4 |

### maupassant_horla — family **passage** (Foucault)

Seed regex (`^(...)`): `passag|porte|pont|navire|voyage|chemin|route|traverse|seuil` — seed hits: 147; window tokens: 1458

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | ouvrit | 4 | 5 | 21.8 |
| 2 | fermé | 3 | 3 | 20.1 |
| 3 | s'ouvrit | 4 | 6 | 19.2 |
| 4 | jette | 3 | 4 | 15.6 |
| 5 | double | 3 | 5 | 13.5 |
| 6 | traînés | 2 | 2 | 13.4 |
| 7 | brisants | 2 | 2 | 13.4 |
| 8 | fermée | 2 | 1 | 13.4 |
| 9 | d'entrée | 2 | 2 | 13.4 |
| 10 | sédentaires | 2 | 2 | 13.4 |
| 11 | continuer | 2 | 2 | 13.4 |
| 12 | conduisaient | 2 | 2 | 13.4 |
| 13 | pousse | 2 | 2 | 13.4 |
| 14 | suivent | 2 | 1 | 13.4 |
| 15 | fêter | 2 | 2 | 13.4 |
| 16 | implorait | 2 | 1 | 13.4 |
| 17 | grands | 4 | 11 | 12.8 |
| 18 | tour | 5 | 20 | 12.0 |
| 19 | coups | 4 | 13 | 11.3 |
| 20 | tue | 3 | 7 | 10.8 |
| 21 | poussa | 3 | 8 | 9.8 |
| 22 | grande | 5 | 27 | 9.1 |
| 23 | passant | 3 | 9 | 9.0 |
| 24 | ouvertes | 2 | 4 | 8.0 |
| 25 | bouteilles | 2 | 4 | 8.0 |

### maupassant_horla — family **gaze** (Foucault)

Seed regex (`^(...)`): `regard|oeil|yeux|œil|observ|examin|fix|juge|surveill` — seed hits: 151; window tokens: 1488

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | baissés | 3 | 3 | 19.9 |
| 2 | levée | 3 | 2 | 19.9 |
| 3 | vache | 4 | 6 | 19.1 |
| 4 | commença | 3 | 5 | 13.4 |
| 5 | attendit | 3 | 5 | 13.4 |
| 6 | rouvris | 2 | 2 | 13.3 |
| 7 | contemplais | 2 | 1 | 13.3 |
| 8 | deviner | 2 | 1 | 13.3 |
| 9 | fascinant | 2 | 1 | 13.3 |
| 10 | affolés | 2 | 1 | 13.3 |
| 11 | hardis | 2 | 1 | 13.3 |
| 12 | souris | 2 | 1 | 13.3 |
| 13 | néanmoins | 2 | 2 | 13.3 |
| 14 | luisantes | 2 | 1 | 13.3 |
| 15 | défi | 2 | 1 | 13.3 |
| 16 | l'agent | 2 | 2 | 13.3 |
| 17 | laisses | 2 | 2 | 13.3 |
| 18 | suffit | 2 | 2 | 13.3 |
| 19 | officier | 2 | 1 | 13.3 |
| 20 | l'appeler | 2 | 1 | 13.3 |
| 21 | leva | 4 | 12 | 11.9 |
| 22 | bouche | 4 | 12 | 11.9 |
| 23 | j'écoute | 2 | 3 | 9.5 |
| 24 | l'abîme | 2 | 3 | 9.5 |
| 25 | brillants | 2 | 3 | 9.5 |

### stevenson_jekyll_hyde — family **double** (Rank)

Seed regex (`^(...)`): `double|mirror|shadow|reflection|twin|likeness|portrait|rival|counterpart|namesake` — seed hits: 21; window tokens: 210

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | occasion | 2 | 3 | 15.4 |

### stevenson_jekyll_hyde — family **return** (Rank)

Seed regex (`^(...)`): `return|womb|water|sea|cave|sleep|enclos|cradle|mother|home` — seed hits: 92; window tokens: 912

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | square | 4 | 10 | 13.7 |
| 2 | likewise | 2 | 1 | 13.4 |
| 3 | enfield | 5 | 18 | 13.1 |
| 4 | richard | 2 | 3 | 9.6 |
| 5 | wild | 2 | 4 | 8.0 |
| 6 | fall | 2 | 4 | 8.0 |
| 7 | another | 4 | 20 | 7.9 |
| 8 | well | 6 | 49 | 6.8 |
| 9 | coming | 2 | 5 | 6.8 |
| 10 | evening | 2 | 5 | 6.8 |
| 11 | doctor | 4 | 25 | 6.3 |
| 12 | lawyer | 7 | 67 | 6.2 |
| 13 | marked | 2 | 6 | 6.0 |
| 14 | several | 2 | 7 | 5.3 |
| 15 | asked | 3 | 19 | 4.6 |
| 16 | now | 6 | 64 | 4.4 |
| 17 | guest | 2 | 9 | 4.3 |
| 18 | within | 2 | 9 | 4.3 |
| 19 | jekyll | 7 | 85 | 4.0 |
| 20 | poole | 5 | 61 | 2.9 |
| 21 | rather | 2 | 15 | 2.5 |
| 22 | place | 2 | 16 | 2.3 |
| 23 | utterson | 8 | 128 | 2.3 |
| 24 | quite | 2 | 17 | 2.1 |
| 25 | yes | 2 | 18 | 2.0 |

### stevenson_jekyll_hyde — family **separation** (Rank)

Seed regex (`^(...)`): `separat|threshold|door|birth|cord|sever|part|orphan|exile|alone` — seed hits: 127; window tokens: 1268

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | baize | 3 | 3 | 18.1 |
| 2 | dream | 3 | 3 | 18.1 |
| 3 | laboratory | 5 | 10 | 16.8 |
| 4 | opened | 4 | 8 | 13.4 |
| 5 | small | 5 | 14 | 12.8 |
| 6 | wicked-looking | 2 | 1 | 12.0 |
| 7 | press | 2 | 2 | 12.0 |
| 8 | total | 2 | 2 | 12.0 |
| 9 | agonies | 2 | 2 | 12.0 |
| 10 | locked | 3 | 5 | 11.5 |
| 11 | red | 3 | 6 | 10.0 |
| 12 | existence | 2 | 3 | 8.3 |
| 13 | by-street | 3 | 9 | 7.2 |
| 14 | cabinet | 5 | 26 | 6.8 |
| 15 | dining-room | 2 | 4 | 6.7 |
| 16 | behind | 2 | 4 | 6.7 |
| 17 | entered | 2 | 4 | 6.7 |
| 18 | closed | 2 | 4 | 6.7 |
| 19 | lock | 2 | 4 | 6.7 |
| 20 | work | 2 | 4 | 6.7 |
| 21 | better | 3 | 10 | 6.6 |
| 22 | open | 4 | 18 | 6.4 |
| 23 | theatre | 3 | 11 | 6.0 |
| 24 | inquired | 2 | 5 | 5.6 |
| 25 | went | 3 | 13 | 5.0 |

### stevenson_jekyll_hyde — family **exclusion** (Foucault)

Seed regex (`^(...)`): `exclu|outcast|banish|shut|confin|prison|cell|madhouse|asylum|lunatic|mad|insan|leper|cast` — seed hits: 57; window tokens: 562

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | attempt | 2 | 1 | 15.3 |
| 2 | he’s | 2 | 3 | 11.5 |
| 3 | haste | 2 | 3 | 11.5 |
| 4 | disposition | 2 | 3 | 11.5 |
| 5 | nodded | 2 | 4 | 9.8 |
| 6 | colleague | 2 | 5 | 8.7 |
| 7 | away | 3 | 18 | 7.4 |
| 8 | enough | 3 | 19 | 7.1 |
| 9 | days | 2 | 9 | 6.1 |
| 10 | himself | 3 | 26 | 5.4 |
| 11 | sure | 2 | 13 | 4.6 |
| 12 | door | 4 | 53 | 4.4 |
| 13 | perhaps | 2 | 14 | 4.3 |
| 14 | like | 4 | 56 | 4.1 |
| 15 | now | 4 | 64 | 3.3 |
| 16 | off | 2 | 19 | 3.3 |
| 17 | part | 2 | 19 | 3.3 |
| 18 | saw | 2 | 24 | 2.5 |
| 19 | doctor | 2 | 25 | 2.4 |
| 20 | cabinet | 2 | 26 | 2.3 |
| 21 | old | 2 | 28 | 2.0 |
| 22 | jekyll | 4 | 85 | 1.9 |
| 23 | long | 2 | 29 | 1.9 |
| 24 | thought | 2 | 39 | 1.2 |
| 25 | house | 2 | 38 | 1.2 |

### stevenson_jekyll_hyde — family **silence** (Foucault)

Seed regex (`^(...)`): `silen|mute|dumb|speechless|hush|quiet|wordless` — seed hits: 23; window tokens: 230

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | walked | 2 | 7 | 10.6 |
| 2 | london | 2 | 11 | 8.6 |
| 3 | read | 2 | 11 | 8.6 |
| 4 | small | 2 | 14 | 7.6 |
| 5 | night | 2 | 28 | 4.9 |
| 6 | utterson | 2 | 128 | 0.5 |

### stevenson_jekyll_hyde — family **passage** (Foucault)

Seed regex (`^(...)`): `passag|gate|bridge|ship|voyage|journey|wander|path|road|cross|threshold|door` — seed hits: 77; window tokens: 762

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | laboratory | 5 | 10 | 21.7 |
| 2 | stairs | 3 | 3 | 21.1 |
| 3 | baize | 3 | 3 | 21.1 |
| 4 | theatre | 5 | 11 | 20.4 |
| 5 | opened | 4 | 8 | 17.3 |
| 6 | save | 3 | 5 | 14.5 |
| 7 | red | 3 | 6 | 13.0 |
| 8 | cabinet | 5 | 26 | 11.0 |
| 9 | straight | 2 | 3 | 10.3 |
| 10 | dreadful | 2 | 3 | 10.3 |
| 11 | by-street | 3 | 9 | 10.0 |
| 12 | open | 4 | 18 | 9.9 |
| 13 | behind | 2 | 4 | 8.7 |
| 14 | entered | 2 | 4 | 8.7 |
| 15 | closed | 2 | 4 | 8.7 |
| 16 | lock | 2 | 4 | 8.7 |
| 17 | went | 3 | 13 | 7.7 |
| 18 | locked | 2 | 5 | 7.5 |
| 19 | place | 3 | 16 | 6.5 |
| 20 | story | 2 | 7 | 6.0 |
| 21 | shut | 2 | 7 | 6.0 |
| 22 | give | 2 | 8 | 5.4 |
| 23 | often | 2 | 9 | 5.0 |
| 24 | room | 3 | 22 | 4.7 |
| 25 | against | 2 | 10 | 4.6 |

### stevenson_jekyll_hyde — family **gaze** (Foucault)

Seed regex (`^(...)`): `gaze|eye|look|stare|watch|examin|observ|scrutin|judge|inspect|witness` — seed hits: 129; window tokens: 1280

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | ugly | 3 | 4 | 13.6 |
| 2 | windowless | 2 | 1 | 12.0 |
| 3 | structure | 2 | 1 | 12.0 |
| 4 | quality | 2 | 2 | 12.0 |
| 5 | forgive | 2 | 2 | 12.0 |
| 6 | giving | 2 | 1 | 12.0 |
| 7 | proceeded | 2 | 2 | 12.0 |
| 8 | metamorphoses | 2 | 1 | 12.0 |
| 9 | keen | 2 | 1 | 12.0 |
| 10 | mouth | 2 | 2 | 12.0 |
| 11 | lawyer’s | 3 | 5 | 11.5 |
| 12 | use | 3 | 5 | 11.5 |
| 13 | court | 4 | 11 | 10.3 |
| 14 | pleased | 2 | 3 | 8.3 |
| 15 | thoroughly | 2 | 3 | 8.3 |
| 16 | round | 3 | 8 | 7.9 |
| 17 | pale | 3 | 8 | 7.9 |
| 18 | changed | 3 | 8 | 7.9 |
| 19 | sight | 3 | 9 | 7.2 |
| 20 | lawyer | 9 | 67 | 7.1 |
| 21 | secrets | 2 | 4 | 6.7 |
| 22 | seem | 2 | 4 | 6.7 |
| 23 | bradshaw | 2 | 4 | 6.7 |
| 24 | vain | 2 | 4 | 6.7 |
| 25 | contents | 3 | 11 | 5.9 |

### wilde_dorian_gray — family **double** (Rank)

Seed regex (`^(...)`): `double|mirror|shadow|reflection|twin|likeness|portrait|rival|counterpart|namesake` — seed hits: 108; window tokens: 1076

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | painted | 9 | 32 | 40.0 |
| 2 | fantastic | 6 | 16 | 30.7 |
| 3 | fatal | 3 | 10 | 13.8 |
| 4 | front | 4 | 23 | 13.7 |
| 5 | art | 6 | 75 | 11.7 |
| 6 | corners | 2 | 4 | 11.7 |
| 7 | haggard | 2 | 4 | 11.7 |
| 8 | cap | 2 | 5 | 10.5 |
| 9 | shapes | 2 | 5 | 10.5 |
| 10 | wonderful | 5 | 58 | 10.4 |
| 11 | unjust | 2 | 6 | 9.7 |
| 12 | feeling | 3 | 20 | 9.4 |
| 13 | bear | 3 | 20 | 9.4 |
| 14 | grotesque | 2 | 7 | 9.0 |
| 15 | strong | 2 | 8 | 8.4 |
| 16 | creeping | 2 | 8 | 8.4 |
| 17 | misshapen | 2 | 8 | 8.4 |
| 18 | burden | 2 | 9 | 7.9 |
| 19 | showed | 2 | 9 | 7.9 |
| 20 | wall | 2 | 9 | 7.9 |
| 21 | hallward | 5 | 81 | 7.5 |
| 22 | gazing | 2 | 11 | 7.0 |
| 23 | sunlight | 2 | 12 | 6.7 |
| 24 | revealed | 2 | 12 | 6.7 |
| 25 | determined | 2 | 12 | 6.7 |

### wilde_dorian_gray — family **return** (Rank)

Seed regex (`^(...)`): `return|womb|water|sea|cave|sleep|enclos|cradle|mother|home` — seed hits: 156; window tokens: 1546

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | happy | 6 | 26 | 20.0 |
| 2 | farm | 3 | 4 | 19.2 |
| 3 | veil | 3 | 5 | 17.0 |
| 4 | wordy | 2 | 1 | 15.7 |
| 5 | refreshed | 2 | 1 | 15.7 |
| 6 | expressed | 2 | 2 | 15.7 |
| 7 | needs | 2 | 2 | 15.7 |
| 8 | proud | 3 | 7 | 14.2 |
| 9 | happiness | 3 | 7 | 14.2 |
| 10 | watch | 4 | 17 | 13.5 |
| 11 | forth | 2 | 3 | 12.0 |
| 12 | corpse | 2 | 3 | 12.0 |
| 13 | floating | 2 | 3 | 12.0 |
| 14 | margaret | 2 | 4 | 10.3 |
| 15 | sensual | 2 | 4 | 10.3 |
| 16 | lines | 3 | 15 | 9.1 |
| 17 | devereux | 2 | 5 | 9.1 |
| 18 | sympathy | 2 | 5 | 9.1 |
| 19 | pink | 2 | 5 | 9.1 |
| 20 | pearl | 2 | 5 | 9.1 |
| 21 | o’clock | 3 | 16 | 8.7 |
| 22 | twelve | 2 | 6 | 8.3 |
| 23 | victor | 2 | 6 | 8.3 |
| 24 | sensations | 2 | 7 | 7.6 |
| 25 | leaving | 2 | 7 | 7.6 |

### wilde_dorian_gray — family **separation** (Rank)

Seed regex (`^(...)`): `separat|threshold|door|birth|cord|sever|part|orphan|exile|alone` — seed hits: 158; window tokens: 1578

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | opened | 13 | 29 | 62.7 |
| 2 | knock | 6 | 8 | 38.1 |
| 3 | behind | 10 | 36 | 36.9 |
| 4 | locked | 5 | 9 | 27.0 |
| 5 | shutting | 4 | 5 | 26.4 |
| 6 | open | 6 | 17 | 25.4 |
| 7 | closed | 4 | 8 | 20.4 |
| 8 | times | 6 | 25 | 20.2 |
| 9 | wider | 2 | 2 | 15.7 |
| 10 | valet | 4 | 13 | 15.6 |
| 11 | quietly | 3 | 6 | 15.3 |
| 12 | entered | 5 | 26 | 14.6 |
| 13 | key | 4 | 15 | 14.4 |
| 14 | went | 7 | 63 | 13.1 |
| 15 | inevitable | 2 | 3 | 11.9 |
| 16 | came | 8 | 99 | 10.7 |
| 17 | entitled | 2 | 4 | 10.2 |
| 18 | unlocked | 2 | 4 | 10.2 |
| 19 | necessary | 2 | 5 | 9.1 |
| 20 | danced | 2 | 6 | 8.2 |
| 21 | singing | 2 | 6 | 8.2 |
| 22 | force | 2 | 6 | 8.2 |
| 23 | shut | 2 | 7 | 7.5 |
| 24 | position | 2 | 8 | 6.9 |
| 25 | bored | 2 | 8 | 6.9 |

### wilde_dorian_gray — family **exclusion** (Foucault)

Seed regex (`^(...)`): `exclu|outcast|banish|shut|confin|prison|cell|madhouse|asylum|lunatic|mad|insan|leper|cast` — seed hits: 193; window tokens: 1918

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | monstrous | 8 | 25 | 29.0 |
| 2 | answer | 8 | 32 | 24.7 |
| 3 | observation | 2 | 2 | 14.9 |
| 4 | melodramatic | 2 | 2 | 14.9 |
| 5 | weariness | 2 | 1 | 14.9 |
| 6 | filippo | 2 | 1 | 14.9 |
| 7 | warned | 2 | 1 | 14.9 |
| 8 | inlaid | 2 | 2 | 14.9 |
| 9 | confession | 3 | 8 | 12.0 |
| 10 | ivory | 3 | 9 | 11.2 |
| 11 | cabinet | 2 | 3 | 11.1 |
| 12 | ferrol | 2 | 4 | 9.4 |
| 13 | temper | 2 | 4 | 9.4 |
| 14 | brain | 4 | 24 | 9.1 |
| 15 | page | 2 | 5 | 8.3 |
| 16 | door | 6 | 64 | 7.7 |
| 17 | imagination | 3 | 16 | 7.5 |
| 18 | dreamed | 2 | 6 | 7.4 |
| 19 | love | 8 | 109 | 7.3 |
| 20 | studio | 3 | 18 | 6.8 |
| 21 | vivid | 2 | 7 | 6.8 |
| 22 | duke | 2 | 7 | 6.8 |
| 23 | prince | 3 | 19 | 6.5 |
| 24 | perfect | 3 | 22 | 5.7 |
| 25 | changed | 3 | 22 | 5.7 |

### wilde_dorian_gray — family **silence** (Foucault)

Seed regex (`^(...)`): `silen|mute|dumb|speechless|hush|quiet|wordless` — seed hits: 45; window tokens: 450

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | crept | 3 | 17 | 15.4 |
| 2 | corners | 2 | 4 | 15.2 |
| 3 | infamous | 2 | 4 | 15.2 |
| 4 | leaned | 2 | 5 | 14.0 |
| 5 | unconscious | 2 | 8 | 11.8 |
| 6 | round | 4 | 80 | 10.5 |
| 7 | house | 3 | 49 | 9.0 |
| 8 | keep | 2 | 19 | 8.1 |
| 9 | door | 3 | 64 | 7.5 |
| 10 | became | 2 | 30 | 6.3 |
| 11 | answer | 2 | 32 | 6.1 |
| 12 | behind | 2 | 36 | 5.6 |
| 13 | absolutely | 2 | 39 | 5.3 |
| 14 | mother | 2 | 42 | 5.1 |
| 15 | across | 2 | 61 | 3.8 |
| 16 | went | 2 | 63 | 3.6 |
| 17 | moment | 2 | 67 | 3.4 |
| 18 | before | 2 | 73 | 3.2 |
| 19 | after | 2 | 103 | 2.1 |
| 20 | time | 2 | 106 | 2.0 |
| 21 | made | 2 | 109 | 1.9 |
| 22 | thing | 2 | 120 | 1.7 |
| 23 | basil | 2 | 153 | 1.1 |
| 24 | man | 2 | 171 | 0.8 |
| 25 | dorian | 2 | 410 | -0.0 |

### wilde_dorian_gray — family **passage** (Foucault)

Seed regex (`^(...)`): `passag|gate|bridge|ship|voyage|journey|wander|path|road|cross|threshold|door` — seed hits: 111; window tokens: 1110

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | opened | 13 | 29 | 71.7 |
| 2 | behind | 10 | 36 | 43.6 |
| 3 | knock | 6 | 8 | 42.3 |
| 4 | locked | 5 | 9 | 30.4 |
| 5 | open | 6 | 17 | 29.5 |
| 6 | shutting | 4 | 5 | 29.2 |
| 7 | euston | 3 | 3 | 25.6 |
| 8 | closed | 4 | 8 | 23.2 |
| 9 | elements | 3 | 4 | 21.1 |
| 10 | entered | 5 | 26 | 17.8 |
| 11 | through | 8 | 84 | 17.6 |
| 12 | went | 7 | 63 | 17.4 |
| 13 | quietly | 3 | 6 | 17.4 |
| 14 | key | 4 | 15 | 17.1 |
| 15 | wider | 2 | 2 | 17.1 |
| 16 | chain | 2 | 2 | 17.1 |
| 17 | unhooked | 2 | 1 | 17.1 |
| 18 | mare | 2 | 2 | 17.1 |
| 19 | swerved | 2 | 2 | 17.1 |
| 20 | stumbled | 2 | 3 | 13.3 |
| 21 | came | 7 | 99 | 11.8 |
| 22 | unlocked | 2 | 4 | 11.6 |
| 23 | silent | 3 | 14 | 11.4 |
| 24 | heard | 4 | 37 | 9.7 |
| 25 | danced | 2 | 6 | 9.5 |

### wilde_dorian_gray — family **gaze** (Foucault)

Seed regex (`^(...)`): `gaze|eye|look|stare|watch|examin|observ|scrutin|judge|inspect|witness` — seed hits: 468; window tokens: 4626

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | fixed | 5 | 5 | 28.4 |
| 2 | startled | 5 | 4 | 28.4 |
| 3 | came | 21 | 99 | 26.4 |
| 4 | henry | 34 | 223 | 25.6 |
| 5 | round | 18 | 80 | 24.4 |
| 6 | puzzled | 4 | 4 | 22.7 |
| 7 | tear-dimmed | 4 | 2 | 22.7 |
| 8 | half-closed | 4 | 3 | 22.7 |
| 9 | lord | 34 | 248 | 20.7 |
| 10 | tears | 7 | 15 | 20.0 |
| 11 | listless | 3 | 3 | 17.0 |
| 12 | picturesque | 3 | 3 | 17.0 |
| 13 | elevating | 3 | 3 | 17.0 |
| 14 | drooped | 3 | 3 | 17.0 |
| 15 | steadfastly | 3 | 2 | 17.0 |
| 16 | face | 18 | 107 | 16.0 |
| 17 | turned | 12 | 54 | 16.0 |
| 18 | dorian | 45 | 410 | 15.9 |
| 19 | pale | 6 | 14 | 15.9 |
| 20 | hallward | 15 | 81 | 15.5 |
| 21 | amazement | 4 | 6 | 15.3 |
| 22 | back | 16 | 100 | 13.1 |
| 23 | james | 6 | 18 | 12.6 |
| 24 | gray | 24 | 189 | 12.4 |
| 25 | met | 9 | 40 | 12.2 |

### poe_william_wilson — family **double** (Rank)

Seed regex (`^(...)`): `double|mirror|shadow|reflection|twin|likeness|portrait|rival|counterpart|namesake` — seed hits: 22; window tokens: 216

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | companion | 2 | 1 | 14.5 |
| 2 | hated | 2 | 2 | 14.5 |
| 3 | dreaded | 2 | 1 | 14.5 |
| 4 | bransby’s | 2 | 4 | 9.0 |
| 5 | myself | 2 | 23 | 2.0 |

### poe_william_wilson — family **return** (Rank)

Seed regex (`^(...)`): `return|womb|water|sea|cave|sleep|enclos|cradle|mother|home` — seed hits: 12; window tokens: 120

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | immediately | 2 | 4 | 11.4 |
| 2 | took | 2 | 5 | 10.2 |

### poe_william_wilson — family **separation** (Rank)

Seed regex (`^(...)`): `separat|threshold|door|birth|cord|sever|part|orphan|exile|alone` — seed hits: 29; window tokens: 288

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | apartment | 3 | 5 | 13.4 |
| 2 | unclosing | 2 | 1 | 13.3 |
| 3 | folding | 2 | 2 | 13.3 |
| 4 | small | 2 | 5 | 6.8 |
| 5 | although | 2 | 10 | 3.9 |
| 6 | even | 2 | 19 | 1.8 |
| 7 | myself | 2 | 23 | 1.3 |

### poe_william_wilson — family **exclusion** (Foucault)

Seed regex (`^(...)`): `exclu|outcast|banish|shut|confin|prison|cell|madhouse|asylum|lunatic|mad|insan|leper|cast` — seed hits: 13; window tokens: 128

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | infamy | 2 | 1 | 16.6 |
| 2 | abandoned | 2 | 5 | 9.9 |

### poe_william_wilson — family **silence** (Foucault)

Seed regex (`^(...)`): `silen|mute|dumb|speechless|hush|quiet|wordless` — seed hits: 6; window tokens: 60

_No collocate reached the minimum window count of 2._

### poe_william_wilson — family **passage** (Foucault)

Seed regex (`^(...)`): `passag|gate|bridge|ship|voyage|journey|wander|path|road|cross|threshold|door` — seed hits: 15; window tokens: 146

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | apartment | 3 | 5 | 17.4 |
| 2 | folding | 2 | 2 | 16.1 |
| 3 | wall | 2 | 3 | 12.3 |
| 4 | late | 2 | 4 | 10.6 |

### poe_william_wilson — family **gaze** (Foucault)

Seed regex (`^(...)`): `gaze|eye|look|stare|watch|examin|observ|scrutin|judge|inspect|witness` — seed hits: 13; window tokens: 128

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | schoolfellows | 2 | 1 | 16.6 |
| 2 | minute | 2 | 2 | 16.6 |
| 3 | moment | 2 | 7 | 8.4 |

### dostoevsky_double_garnett_1917 — family **double** (Rank)

Seed regex (`^(...)`): `double|mirror|shadow|reflection|twin|likeness|portrait|rival|counterpart|namesake` — seed hits: 175; window tokens: 1732

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | eee | 10 | 36 | 31.1 |
| 2 | siamese | 4 | 3 | 28.9 |
| 3 | eae | 4 | 8 | 18.0 |
| 4 | sie | 3 | 5 | 15.0 |
| 5 | ave | 2 | 2 | 14.4 |
| 6 | reer | 2 | 1 | 14.4 |
| 7 | gues | 2 | 1 | 14.4 |
| 8 | tis | 2 | 1 | 14.4 |
| 9 | born | 2 | 1 | 14.4 |
| 10 | handiwork | 2 | 1 | 14.4 |
| 11 | provided | 2 | 2 | 14.4 |
| 12 | thr | 2 | 2 | 14.4 |
| 13 | roe | 2 | 2 | 14.4 |
| 14 | powerful | 2 | 2 | 14.4 |
| 15 | chapter | 4 | 13 | 13.3 |
| 16 | ere | 4 | 13 | 13.3 |
| 17 | yours | 3 | 8 | 11.3 |
| 18 | eas | 2 | 3 | 10.7 |
| 19 | ata | 2 | 3 | 10.7 |
| 20 | striking | 3 | 9 | 10.5 |
| 21 | treacherous | 2 | 4 | 9.0 |
| 22 | wonder | 2 | 4 | 9.0 |
| 23 | golyadkin’s | 8 | 86 | 8.8 |
| 24 | greatcoat | 3 | 13 | 8.1 |
| 25 | divine | 2 | 5 | 7.9 |

### dostoevsky_double_garnett_1917 — family **return** (Rank)

Seed regex (`^(...)`): `return|womb|water|sea|cave|sleep|enclos|cradle|mother|home` — seed hits: 120; window tokens: 1190

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | drive | 4 | 12 | 16.9 |
| 2 | neue | 2 | 1 | 15.9 |
| 3 | canal | 2 | 2 | 15.9 |
| 4 | liberal | 2 | 2 | 15.9 |
| 5 | good-night | 2 | 2 | 15.9 |
| 6 | nature | 3 | 10 | 11.9 |
| 7 | getting | 4 | 23 | 11.3 |
| 8 | petrushka | 8 | 102 | 11.2 |
| 9 | await | 2 | 4 | 10.5 |
| 10 | staying | 2 | 4 | 10.5 |
| 11 | least | 3 | 13 | 10.2 |
| 12 | public | 2 | 5 | 9.3 |
| 13 | slept | 2 | 5 | 9.3 |
| 14 | drops | 2 | 6 | 8.4 |
| 15 | cold | 3 | 18 | 8.2 |
| 16 | told | 3 | 19 | 7.9 |
| 17 | delay | 2 | 7 | 7.7 |
| 18 | better | 4 | 38 | 7.6 |
| 19 | shestilavotchny | 2 | 8 | 7.2 |
| 20 | shouted | 2 | 9 | 6.7 |
| 21 | wish | 2 | 9 | 6.7 |
| 22 | above | 2 | 10 | 6.2 |
| 23 | black | 2 | 10 | 6.2 |
| 24 | actually | 2 | 10 | 6.2 |
| 25 | live | 2 | 12 | 5.5 |

### dostoevsky_double_garnett_1917 — family **separation** (Rank)

Seed regex (`^(...)`): `separat|threshold|door|birth|cord|sever|part|orphan|exile|alone` — seed hits: 168; window tokens: 1674

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | opened | 16 | 24 | 86.5 |
| 2 | creaked | 4 | 4 | 29.1 |
| 3 | room | 13 | 83 | 26.4 |
| 4 | behind | 7 | 35 | 17.4 |
| 5 | slammed | 2 | 2 | 14.6 |
| 6 | admitted | 2 | 2 | 14.6 |
| 7 | locked | 2 | 2 | 14.6 |
| 8 | cooking | 2 | 2 | 14.6 |
| 9 | pulled | 3 | 6 | 13.7 |
| 10 | ball | 3 | 6 | 13.7 |
| 11 | noisily | 3 | 6 | 13.7 |
| 12 | confess | 3 | 8 | 11.5 |
| 13 | towards | 4 | 18 | 10.8 |
| 14 | carriage | 7 | 60 | 10.6 |
| 15 | next | 4 | 19 | 10.4 |
| 16 | stopped | 3 | 11 | 9.4 |
| 17 | persons | 4 | 22 | 9.2 |
| 18 | opening | 2 | 4 | 9.1 |
| 19 | officials | 2 | 4 | 9.1 |
| 20 | knocked | 2 | 4 | 9.1 |
| 21 | native | 2 | 4 | 9.1 |
| 22 | rushed | 4 | 23 | 8.9 |
| 23 | suddenly | 6 | 56 | 8.2 |
| 24 | stood | 5 | 40 | 8.1 |
| 25 | gay | 2 | 5 | 8.0 |

### dostoevsky_double_garnett_1917 — family **exclusion** (Foucault)

Seed regex (`^(...)`): `exclu|outcast|banish|shut|confin|prison|cell|madhouse|asylum|lunatic|mad|insan|leper|cast` — seed hits: 124; window tokens: 1234

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | mind | 23 | 64 | 99.9 |
| 2 | falbalas | 4 | 3 | 31.6 |
| 3 | appearance | 6 | 13 | 29.7 |
| 4 | scrape | 3 | 3 | 23.7 |
| 5 | grimaces | 2 | 2 | 15.8 |
| 6 | émigrée | 2 | 1 | 15.8 |
| 7 | fatal | 2 | 2 | 15.8 |
| 8 | slight | 3 | 7 | 14.3 |
| 9 | example | 3 | 8 | 13.3 |
| 10 | mistake | 3 | 10 | 11.7 |
| 11 | nowadays | 3 | 13 | 10.0 |
| 12 | clear | 2 | 5 | 9.2 |
| 13 | hopes | 2 | 6 | 8.3 |
| 14 | appeal | 2 | 6 | 8.3 |
| 15 | devil | 2 | 6 | 8.3 |
| 16 | they'll | 2 | 6 | 8.3 |
| 17 | french | 2 | 7 | 7.6 |
| 18 | haste | 3 | 21 | 7.2 |
| 19 | doubt | 3 | 21 | 7.2 |
| 20 | movement | 2 | 8 | 7.0 |
| 21 | hero | 10 | 200 | 7.0 |
| 22 | learnt | 2 | 8 | 7.0 |
| 23 | night | 3 | 23 | 6.6 |
| 24 | effort | 2 | 9 | 6.5 |
| 25 | sit | 2 | 13 | 5.1 |

### dostoevsky_double_garnett_1917 — family **silence** (Foucault)

Seed regex (`^(...)`): `silen|mute|dumb|speechless|hush|quiet|wordless` — seed hits: 42; window tokens: 420

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | followed | 4 | 17 | 21.8 |
| 2 | brief | 3 | 7 | 20.7 |
| 3 | subsided | 2 | 2 | 20.1 |
| 4 | remained | 3 | 8 | 19.6 |
| 5 | better | 4 | 38 | 15.1 |
| 6 | eloquent | 2 | 4 | 14.6 |
| 7 | served | 2 | 4 | 14.6 |
| 8 | keep | 3 | 17 | 14.5 |
| 9 | pre | 2 | 5 | 13.4 |
| 10 | significant | 2 | 6 | 12.5 |
| 11 | hero | 7 | 200 | 12.3 |
| 12 | h’m | 2 | 11 | 9.8 |
| 13 | long | 3 | 46 | 8.5 |
| 14 | petrushka | 4 | 102 | 7.8 |
| 15 | making | 2 | 27 | 6.2 |
| 16 | after | 3 | 92 | 4.9 |
| 17 | however | 2 | 43 | 4.5 |
| 18 | olsufy | 2 | 48 | 4.1 |
| 19 | rather | 2 | 49 | 4.0 |
| 20 | still | 2 | 49 | 4.0 |
| 21 | voice | 2 | 49 | 4.0 |
| 22 | everything | 2 | 49 | 4.0 |
| 23 | round | 2 | 54 | 3.7 |
| 24 | nothing | 3 | 123 | 3.5 |
| 25 | ivanovitch | 3 | 131 | 3.2 |

### dostoevsky_double_garnett_1917 — family **passage** (Foucault)

Seed regex (`^(...)`): `passag|gate|bridge|ship|voyage|journey|wander|path|road|cross|threshold|door` — seed hits: 112; window tokens: 1108

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | ismailovsky | 18 | 15 | 146.2 |
| 2 | opened | 16 | 24 | 99.6 |
| 3 | semyonovsky | 5 | 4 | 40.6 |
| 4 | room | 11 | 83 | 26.8 |
| 5 | carriage | 8 | 60 | 19.6 |
| 6 | forgot | 4 | 11 | 18.3 |
| 7 | slammed | 2 | 2 | 16.2 |
| 8 | provoking | 2 | 1 | 16.2 |
| 9 | anitchkov | 2 | 1 | 16.2 |
| 10 | locked | 2 | 2 | 16.2 |
| 11 | pulled | 3 | 6 | 16.1 |
| 12 | fontanka | 3 | 6 | 16.1 |
| 13 | noisily | 3 | 6 | 16.1 |
| 14 | stairs | 5 | 26 | 15.8 |
| 15 | straight | 5 | 27 | 15.4 |
| 16 | towards | 4 | 18 | 13.9 |
| 17 | next | 4 | 19 | 13.4 |
| 18 | run | 3 | 10 | 12.4 |
| 19 | across | 2 | 3 | 12.4 |
| 20 | stood | 5 | 40 | 11.6 |
| 21 | opening | 2 | 4 | 10.7 |
| 22 | refreshment-room | 2 | 4 | 10.7 |
| 23 | knocked | 2 | 4 | 10.7 |
| 24 | creaked | 2 | 4 | 10.7 |
| 25 | empty | 2 | 5 | 9.6 |

### dostoevsky_double_garnett_1917 — family **gaze** (Foucault)

Seed regex (`^(...)`): `gaze|eye|look|stare|watch|examin|observ|scrutin|judge|inspect|witness` — seed hits: 364; window tokens: 3602

| # | collocate | window n | text freq | G² |
|---:|---|---:|---:|---:|
| 1 | round | 20 | 54 | 47.8 |
| 2 | fixed | 10 | 12 | 46.9 |
| 3 | raised | 9 | 12 | 38.6 |
| 4 | master’s | 6 | 5 | 34.5 |
| 5 | raising | 5 | 5 | 28.7 |
| 6 | fastened | 4 | 4 | 23.0 |
| 7 | wider | 4 | 4 | 23.0 |
| 8 | stern | 4 | 3 | 23.0 |
| 9 | saw | 11 | 36 | 21.8 |
| 10 | bad | 7 | 14 | 21.7 |
| 11 | golyadkin | 67 | 689 | 18.1 |
| 12 | during | 3 | 2 | 17.2 |
| 13 | open-eyed | 3 | 3 | 17.2 |
| 14 | screwing | 3 | 2 | 17.2 |
| 15 | uneasily | 3 | 3 | 17.2 |
| 16 | unwell | 3 | 1 | 17.2 |
| 17 | lustreless | 3 | 2 | 17.2 |
| 18 | vitch | 7 | 19 | 16.6 |
| 19 | tears | 7 | 20 | 15.9 |
| 20 | strangely | 4 | 7 | 13.8 |
| 21 | closed | 3 | 4 | 12.9 |
| 22 | intently | 3 | 4 | 12.9 |
| 23 | around | 3 | 4 | 12.9 |
| 24 | doctor | 5 | 13 | 12.4 |
| 25 | before | 13 | 77 | 12.3 |

## C. Reading notes

- Rank *Doppelgänger*: the double-family seeds pull **seele** (41 window hits) — the soul/shadow/mirror-image equation that is the book's ethnographic core (ch. IV–V) — plus *porträt*, *verkörpert*, *wirft* (*wirft keinen Schatten*).
- Rank *Trauma*: return seeds pull **ursituation / urlust / lustsituation / mutter / glückshaube / angleichung** — the intrauterine "primal situation" cluster; separation seeds pull **überwindung / infantile / genitale / neurotische / wiederholung / auslösung**, i.e. separation is framed as the thing that is *overcome* or *repeated*, not depicted.
- Nietzsche GT §1–8: the form vocabulary collocates with **erlösung, kräfte, grausen, zustände, tragödie** — the Apollonian is named as redemption-through-image, the Dionysian as *Grausen*.
- Norming corpus: the "separation/passage" seeds in Wilde, Stevenson and Dostoevsky are dominated by **door** vocabulary (*opened, locked, knock, behind, slammed, creaked*) — the threshold motif is literally a door in the double-novellas; the "gaze" seeds in Hoffmann pull **stieren, funkelnden, hohlen, scharf** (the staring double) and in Dostoevsky **fixed, fastened, stern** (being looked at by superiors).
- OCR noise: *eee/eae/reer* in the Dostoevsky OCR; *negelein* in Rank is a cited author (Negelein) not a motif.
