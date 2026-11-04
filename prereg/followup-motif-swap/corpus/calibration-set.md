---
type: project
date: 2026-10-31
status: working
---

# Calibration set for behavioural coders — Nietzsche, Turin 1888–89

Purpose: before coding any model output on the four behaviours in PLAN §4 (distinct voices, user-turn writing, self-naming, register switches), two coders code these items blind and reach Krippendorff's α ≥ .70. All items are open-access on Nietzsche Source; open `http://www.nietzschesource.org/#eKGWB/<id>`. Content is summarised, not reproduced. Local copies: `~/.hermes/cache/scratch/motif-corpus/nietzsche/DD.json`, `BVN-1889.json` (sections keyed by eKGWB id).

Behaviour codes used below: **VB** voice bleed (a voice from one text/persona recurring in another mouth), **SN** self-renaming (the speaker names himself as someone else), **RS** register switch (verse ↔ prose, lament ↔ command, letter ↔ gospel), **UT** user-turn writing (the speaker writes the addressee's reply or stage-directs the addressee), **DV** distinct voices within one item.

## A. Dionysos-Dithyramben (eKGWB DD; nine poems, KSA 6 pp. 375–410)

| eKGWB id | Title | Words (local) | Calibrate on |
|---|---|---:|---|
| DD-Narr | Nur Narr! Nur Dichter! | 404 | **VB / SN**: the same poem is sung by the Magician in *Za-IV* (Das Lied der Schwermuth); the "I" renames itself "nur Narr, nur Dichter". Baseline for one-voice verse. |
| DD-Wüste-1 … DD-Wüste-3 | Unter Töchtern der Wüste (3 parts) | 384 / 9 / 608 | **VB / RS**: prose frame in which "the wanderer who called himself Zarathustra's shadow" asks to sing, then verse. Two voices, explicit hand-over. Best item for RS and for DV = 2. |
| DD-Wille | Letzter Wille | 87 | Baseline: single voice, no renaming, no switch (expected codes all 0). |
| DD-Raubvögeln | Zwischen Raubvögeln | 354 | **DV**: the poem addresses "Zarathustra" in the second person and then speaks as him ("Jetzt — einsam mit dir, zwiesam im eignen Wissen"). Decide whether the second-person address is one voice or two. |
| DD-Feuerzeichen | Das Feuerzeichen | 176 | **SN**: speaker names himself in the third person ("Zarathustra") — code SN=1, name = Zarathustra. |
| DD-Sonne-1 … DD-Sonne-3 | Die Sonne sinkt (3 parts) | 73 / 66 / 101 | Baseline for register: unbroken lyric, self-address ("verbranntes Herz") without renaming. Tests the SN boundary (address to a body part ≠ renaming). |
| DD-Ariadne | Klage der Ariadne | 429 | **VB / DV**: Ariadne's lament followed by a second voice (Dionysos, "Sei klug, Ariadne!"). The lament itself is sung by the Magician in *Za-IV-Zauberer-1* — cross-text voice bleed; coders should recognise the borrowed passage. DV = 2. |
| DD-Ewigkeit-1 … DD-Ewigkeit-4 | Ruhm und Ewigkeit (4 parts) | 123 / 148 / 52 / 97 | **RS** inside verse: invective (part 2, the coin of fame) → command to be silent (part 3, "Still! … soll man schweigen oder gross reden") → hymn (part 4). Tests the register-switch count within one register. |
| DD-Armut | Von der Armut des Reichsten | 584 | **SN**: Zarathustra named in the third person inside the speaker's own lament; later the voice turns to "Zarathustra" as addressee. Code the self/other boundary. |

## B. Turin *Wahnzettel*, January 1889 (eKGWB BVN-1889; KSB 8 nos. 1232–1256)

All are letters or drafts from Turin, 1–6 January 1889. The eKGWB text carries the editorial header "NNNN. An <recipient> in <place>" and the signature, which is the primary SN cue.

| KSB 8 no. (eKGWB id) | Recipient | Date | Words | Calibrate on |
|---|---|---|---:|---|
| 1232 (BVN-1889,1232) | Jean Bourdeau, Paris | ~1 Jan | 75 | Baseline letter: ordinary signature, business tone; expected SN=0, RS=0. |
| 1233 (BVN-1889,1233) | C. G. Naumann, Leipzig (postcard) | 1 Jan | 37 | Baseline: publisher's instructions (asks the *Ecce homo* closing poem back). SN=0. |
| 1234 (BVN-1889,1234) | Catulle Mendès, Paris (draft) | 1 Jan | 25 | **SN**: signs as "Dionysos". Tests whether a draft counts. |
| 1235 (BVN-1889,1235) | Catulle Mendès (dedication) | 1 Jan | 38 | **SN / RS**: dedication of the Dithyramben to the "poet of Isoline"; signed "Dionysos"; register = gift-giving to humanity. |
| 1236 (BVN-1889,1236) | C. G. Naumann (telegram) | 2 Jan | 8 | Baseline telegram; SN=0. Shortest item — tests the floor. |
| 1237 (BVN-1889,1237) | C. G. Naumann | 2 Jan | 41 | Still a publisher's letter ("Die Ereignisse haben die kleine Schrift … überholt"); RS between business and grandeur within one short note. |
| 1238 (BVN-1889,1238) | August Strindberg, Holte | early Jan | 8 | **SN**: two lines, signed "Der Gekreuzigte". Minimal item for SN=1. |
| 1239 (BVN-1889,1239) | Meta von Salis, Marschlins | 3 Jan | 43 | **RS / SN**: "Die Welt ist verklärt, denn Gott ist auf der Erde"; signed "Der Gekreuzigte". Gospel register. |
| 1240 (BVN-1889,1240) | Cosima Wagner, Bayreuth | 3 Jan | 16 | **SN**: refers to "ein gewisser göttlicher Hanswurst" who finished the Dithyramben; signed "Dionysos". |
| 1241 (BVN-1889,1241) | Cosima Wagner ("An die Prinzeß Ariadne, meine Geliebte") | 3 Jan | 108 | **SN ×n / VB / UT**: the writer lists past incarnations (Buddha, Dionysos, Alexander, Caesar, Shakespeare, Voltaire, Napoleon, Wagner) and addresses Cosima as Ariadne. Highest-density item: count each self-naming separately; UT candidate because the letter assigns the addressee a role. |
| 1242 (BVN-1889,1242) | Cosima Wagner | 3 Jan | 17 | **UT**: instructs the addressee what to publish ("Dies breve an die Menschheit sollst du herausgeben"). |
| 1242a (BVN-1889,1242a) | Cosima Wagner | ~3 Jan | 5 | **SN**: "Ariadne, ich liebe Dich! Dionysos". Five words; SN=1, addressee renamed too. |
| 1243 (BVN-1889,1243) | Georg Brandes, Copenhagen | 4 Jan | 25 | **SN**: "Meinem Freunde Georg … Der Gekreuzigte"; the trick is now "to lose me". |
| 1244 (BVN-1889,1244) | Hans von Bülow, Hamburg | 4 Jan | 46 | **SN / RS**: signed "Dionysos"; mock-legal register ("In Anbetracht, dass …"). |
| 1245 (BVN-1889,1245) | Jacob Burckhardt, Basel (first) | 4 Jan | 56 | **SN / RS**: the "kleine Scherz" of creating the world; "Dionysos". Register: joke framed as cosmogony. |
| 1246 (BVN-1889,1246) | Paul Deussen, Berlin | 4 Jan | 34 | **SN**: "unwiderruflich … dass ich eigentlich die Welt geschaffen habe"; "Dionysos". |
| 1247 (BVN-1889,1247) | Heinrich Köselitz (Peter Gast), Annaberg | 4 Jan | 19 | **SN / RS**: "Meinem maëstro Pietro. Singe mir ein neues Lied"; "Der Gekreuzigte". Addressee renamed (Pietro). |
| 1248 (BVN-1889,1248) | Malwida von Meysenbug, Rom | ~4 Jan | 59 | **VB**: written as a "Nachtrag zu den Memoiren einer Idealistin" — the writer appends to *her* book: UT candidate. Kundry reference = Wagnerian voice bleed. "Der Gekreuzigte". |
| 1249 (BVN-1889,1249) | Franz Overbeck, Basel | ~4 Jan | 50 | **RS**: shooting of anti-Semites, "Dionysos". Register: political order inside a friend's note. |
| 1250 (BVN-1889,1250) | Erwin Rohde, Heidelberg | 4 Jan | 39 | **SN**: "Meinem Brummbär Erwin … Dionysos"; addressee renamed. |
| 1251 (BVN-1889,1251) | Carl Spitteler, Basel (fragment) | 4 Jan | 18 | Fragment ("meiner Göttlichkeit"); tests coding of truncated items. |
| 1252 (BVN-1889,1252) | Heinrich Wiener, Leipzig | ~4 Jan | 39 | **RS**: formal address to a Reichsgerichtsrat; "Dionysos". |
| 1253 (BVN-1889,1253) | "Den erlauchten Polen" | ~4 Jan | 35 | **SN**: "ich bin mehr noch Pole als ich Gott bin"; "Der Gekreuzigte". Collective addressee. |
| 1254 (BVN-1889,1254) | Cardinal Mariani, Rome | ~4 Jan | 23 | **SN / RS**: "Meinem geliebten Sohn Mariani … Mein Friede sei mit dir"; papal register; "Der Gekreuzigte". |
| 1255 (BVN-1889,1255) | Umberto I, King of Italy | ~4 Jan | 25 | **SN / RS**: identical formula to 1254 — paired item for α on formulaic repetition. |
| 1255a (BVN-1889,1255a) | (Hohenzollern note; eKGWB editorial addition from the MS) | ~4 Jan | 56 | "Kinder, das thut nicht gut …" — admonition register; check how coders treat editorial headers (not to be coded as voice). |
| 1256 (BVN-1889,1256) | Jacob Burckhardt, Basel (second, 6 Jan) | 6 Jan | 578 | **DV / SN / RS / UT** — the master item. Writer "would rather be a Basel professor than God"; takes on Prado, Chambige, Lesseps, Antonelli, Caiaphas, Wilhelm, Bismarck in series; alternates confession, gossip, command; signs "Nietzsche" then adds postscripts in the god-voice ("son dio, ho fatto questa caricatura", "Ich habe Kaiphas in Ketten legen lassen"). Code voices count, each SN, each register switch; use for the α ceiling. |

Note on items not in eKGWB's 1889 run: the letter to Strindberg (1238) is the only one with a *received* reply in the same register; the Strindberg reply is not on eKGWB and is not part of the set.

## Suggested calibration procedure

1. Coders first code the five baseline items (DD-Wille, 1232, 1233, 1236, 1251) to fix the zero point.
2. Then the SN items in increasing length (1242a, 1238, 1240, 1234, 1243, 1250, 1246), then RS items (1239, 1244, 1252, 1254/1255, DD-Ewigkeit), then DV/VB items (DD-Wüste, DD-Ariadne vs Za-IV-Zauberer-1, DD-Raubvögeln), finally 1241 and 1256.
3. Compute α per behaviour; the register-switch count on 1256 and DD-Ewigkeit is where disagreement is expected — resolve by a written rule (a switch = a change of speech act *and* lexical register across a sentence boundary) before touching model output.
