# BERICHT: DIGITALE BAUSTOFFSTROEME / TRACKING & TRACING

## ReUse-Materialfluss-System Kammgarnhof Bad Voeslau

> **Stand:** 2026-10-08  
> **Autor:** Ing. Julian Zotter / AI-AWEC  
> **Projektbezug:** Kammgarnhof Bad Voeslau (KGH2) / Falkstrasse 6  
> **Version:** 1.0 — Kapitelstruktur mit Beschreibung (Resultate folgen)

---

## Inhaltsverzeichnis

1. [Einleitung und Zielsetzung](#1-einleitung-und-zielsetzung)
2. [Methodik und Quellenlage](#2-methodik-und-quellenlage)
3. [Projekt Kammgarnhof — ReUse FT-Traeger](#3-projekt-kammgarnhof--reuse-ft-traeger)
4. [Digitale Baustoffstroeme — Tracking & Tracing](#4-digitale-baustoffstroeme--tracking--tracing)
5. [RLO / AI-AWEC Systemarchitektur](#5-rlo--ai-awec-systemarchitektur)
6. [Workflow-Phasen im Detail](#6-workflow-phasen-im-detail)
7. [Materialpass und Digital Product Passport (DPP)](#7-materialpass-und-digital-product-passport-dpp)
8. [LCA / GWP-Bilanzierung und Circularity Score](#8-lca--gwp-bilanzierung-und-circularity-score)
9. [Normative Grundlagen und Regelwerke](#9-normative-grundlagen-und-regelwerke)
10. [Handlungsfelder und offene Punkte](#10-handlungsfelder-und-offene-punkte)
11. [Zusammenfassung und Ausblick](#11-zusammenfassung-und-ausblick)
12. [Anhang — Quellenverzeichnis](#12-anhang--quellenverzeichnis)

---

## 1. Einleitung und Zielsetzung

### 1.1 Gegenstand

Dieser Bericht dokumentiert den Aufbau eines digital rueckverfolgbaren ReUse- und Materialfluss-Systems fuer das Projekt Kammgarnhof Bad Voeslau (KGH2). Im Zentrum steht die Wiederverwendung von 222 Stahlbeton-Fertigteiltraegern (STB-T-Gurt-FT-Traeger Typ 1-4, L = 11.17 m, C30/37) aus dem Rueckbau der IG Immo Halle in Guntramsdorf durch die Firma Oberndorfer. Diese Traeger sollen als tragende Balkon- und Laubengangkonstruktion im Kammgarnhof-Projekt wiedereingebaut werden.

### 1.2 Zielsetzung

- Lueckenlose digitale Rueckverfolgbarkeit aller ReUse-Bauteile von der Erfassung bis zum Wiedereinbau
- Erstellung eines Materialpasses fuer jedes wiederverwendete Bauteil
- Nachweis der CO2-Einsparung gegenueber Primaerproduktion (LCA/GWP-Bilanzierung)
- Rezertifizierung der Bauteile durch "Zulassung im Einzelfall"
- Integration in das RLO-System (Resource Loop Optimizer) und die AI-AWEC-Plattform

### 1.3 Scope

Das System umfasst zwei parallele Materialstroeme am Kammgarnhof:

1. **Stahlbetonfertigteiltraeger** (Oberndorfer/Guntramsdorf) — 222 FT-Traeger fuer Balkon-/Laubengangkonstruktion
2. **Historische Eisenbauteile** (Bestand KGH2) — Gusseisensaeulen (Lamellengraphit) und genietete Walz-/Schweissttraeger

---

## 2. Methodik und Quellenlage

### 2.1 Datenbasis

Die Erstellung des MASTER-INDEX erfolgte durch systematische Durchsuchung aller verfuegbaren digitalen Quellen:

| Quelle | Suchverfahren | Treffer |
|--------|---------------|---------|
| Gmail | Thread-basierte Suche mit Keyword-Varianten | 16 Threads |
| Google Drive | Dateisuche ueber API mit Volltextindex | 35+ Dateien |
| Outlook (MS365) | Mail- und Kalendersuche | 8 Eintraege |
| 04-BASIC-KNOWLEDGE | Lokaler Dateiindex (UTF-16LE) | 9 Eintraege |

### 2.2 Suchstrategie

Die Suche wurde mit folgenden Keyword-Kombinationen durchgefuehrt:
- FT-Traeger, Fertigteiltraeger, T-Traeger, T-Gurt
- Oberndorfer, Guntramsdorf, IG Immo
- Kammgarnhof, Bad Voeslau, Falkstrasse, KGH2
- ReUse, Wiederverwendung, Materialpass
- Tracking, Tracing, EPCIS, BIM, IoT
- Digitale Baustoffstroeme, DPP, Materialfluss
- Circularity, GWP, LCA, CO2

### 2.3 Bewertungssystem

Jeder Treffer wurde nach folgendem Schema bewertet:

| Relevanz | Bedeutung |
|----------|-----------|
| A++ | Kerndokument, direkt handlungsrelevant |
| A+ | Hohe Relevanz, ergaenzt Kerndokumentation |
| A | Relevant, Teil des Gesamtbildes |
| B | Kontextinformation, mittelbarer Bezug |

### 2.4 Ergebnis

**64 Eintraege** wurden identifiziert, kategorisiert und dem 8-Phasen-Workflow zugeordnet: 12 x A++, 15 x A+, 19 x A, 18 x B.

---

## 3. Projekt Kammgarnhof — ReUse FT-Traeger

### 3.1 Projektueberblick

Das Kammgarnhof-Projekt (KGH2) in der Falkstrasse 6, Bad Voeslau, sieht die Wiederverwendung tragender Stahlbetonbauteile vor. Die FT-Traeger stammen aus dem Hallenrueckbau der IG Immo Guntramsdorf und werden durch die Firma Oberndorfer demontiert, gelagert und fuer den Wiedereinbau vorbereitet.

### 3.2 Bauteilcharakteristik

- **Typ:** STB-T-Gurt-FT-Traeger Typ 1-4
- **Stueckzahl:** 222 Traeger
- **Laenge:** 11.17 m
- **Betonfestigkeit:** C30/37
- **Teilsicherheitsbeiwert:** gamma_red = 1.35
- **Herkunft:** Halle IG Immo Guntramsdorf (Oberndorfer)
- **Zielprojekt:** Balkon- und Laubengangkonstruktion Kammgarnhof

### 3.3 Projektpartner

- **Oberndorfer** — Rueckbau, Demontage und Bereitstellung der FT-Traeger
- **Materialnomaden GmbH** (Markus Kneidinger) — ReUse-Catalogisierung, Rezertifizierung, Verwendbarkeitsnachweis
- **einszueins architektur** (Dragschitz) — Entwurfsplanung Kammgarnhof
- **EGW** (Jordan) — Auftraggeber Kammgarnhof
- **Zotter** — Tragwerksplanung, statische Bearbeitung
- **Beiglboeck** — Ansprechpartner Oberndorfer

### 3.4 Dokumentenlage

26 Kerndokumente erfasst (Google Drive + Gmail), davon:
- 5 Angebotsdokumente zur Zertifizierung und Verwendbarkeit
- 1 Projektdokumentation (ReUse-Bauteilbegutachtung)
- 1 Herkunftsnachweis (Hallenstatik Guntramsdorf)
- 1 Bauteilkatalog Oberndorfer
- 1 Planliste mit Bauteil-IDs und Geometrien
- 8 Gmail-Threads mit Projektkorrespondenz (Angebote, Abstimmungen, Statikunterlagen)
- 4 Outlook-Eintraege (Eisteiche FT-Traeger-Matrix, Hybriddecke)

### 3.5 Paralleler Materialstrom: Historische Eisenbauteile

Zusaetzlich zu den FT-Traegern umfasst das Kammgarnhof-Projekt die Wiederverwendung historischer Eisenbauteile aus dem Bestand:
- Gusseisensaeulen (Lamellengraphit)
- Genietete Walz- und Schweissttraeger
- Eigener Pruef- und Rezertifizierungspfad (MA39 Materialprüfung)

> **Resultate:** Detaillierte Eintraege siehe MASTER-INDEX Abschnitte A.1 bis A.4

---

## 4. Digitale Baustoffstroeme — Tracking & Tracing

### 4.1 Forschungskontext

Die digitale Rueckverfolgbarkeit von Bauprodukten ist trotz existierender Technologien (BIM, IoT, EPCIS) in der Bauwirtschaft noch nicht durchgaengig implementiert. Zentrale Forschungsfrage: Wie laesst sich mit BIM, IoT und EPCIS eine durchgaengige digitale Rueckverfolgbarkeit von Bauprodukten umsetzen?

### 4.2 Technologie-Stack

| Technologie | Funktion | Bezug zum Projekt |
|-------------|----------|-------------------|
| BIM (Building Information Modeling) | Geometrisch-semantisches Bauteilmodell | Traeger-Geometrie, IFC-Attribute |
| IoT (Internet of Things) | Sensorik und Zustandsueberwachung | Bauteil-Monitoring, Lagerung |
| EPCIS (Electronic Product Code Information Services) | Ereignisbasierte Rueckverfolgbarkeit | Herkunft, Transport, Einbau |
| DPP (Digital Product Passport) | EU-konformer Produktpass | Materialzusammensetzung, LCA-Daten |
| GS1 Standards | Identifikation und Serialisierung | Bauteil-GUID, QR-Code |

### 4.3 KI-basierte Ansaetze

Das Forschungsprojekt "KI for BauChain" zeigt den Einsatz von:
- KI-basierter Materialart-Erfassung
- Echtzeitnaher Prozesssteuerung in der Baustofflogistik
- Kostenguenstiger Sensorik als Alternative zu Spezialloesungen
- Computer Vision und Point Cloud-Analyse fuer Bauteilidentifikation

### 4.4 Material Recovery Right (MRR)

Das MRR-Konzept stellt einen marktbasierten Anreizmechanismus fuer zirkulaeres Bauen dar:
- Restwert gebrauchter Materialien wird als handelbares Zertifikat monetarisiert
- CO2-Vermeidung durch ReUse wird oekonomisch bewertbar
- Integration in ESG-Berichterstattung und Nachhaltigkeitszertifizierung

> **Resultate:** Detaillierte Eintraege siehe MASTER-INDEX Abschnitte B.1 bis B.4

---

## 5. RLO / AI-AWEC Systemarchitektur

### 5.1 Resource Loop Optimizer (RLO)

Der RLO ist das zentrale Werkzeug zur Bewertung und Steuerung von Materialkreislaeufen. Kernprozess:

```
Ressourcen erkennen → pruefen → bilanzieren → rezertifizieren → kreislaufaehig wiedereinsetzen
```

### 5.2 AI-AWEC Plattform

Die AI-AWEC-Plattform (Artificial Intelligence - Architecture, Woodwork, Engineering, Construction) bildet den uebergeordneten Rahmen fuer:
- Knowledge Processing Pipeline (PDF-Parser, Fontprofilierung, Klassifikation)
- Deterministischer Index-/Registry-Generator (aec_wms_index.py, 438 Zeilen, stdlib-only)
- 5-Layer-Modell (L0-L4 + HMI)
- MASTER_INDEX.md als Single Source of Truth (333 indizierte Dateien, 10 aktive Register)

### 5.3 Datenarchitektur

```
00_SYSTEM   → Inventar, Index, Registry, Schemas
10_PARSED   → Extrahierte und normalisierte Dokumente
20_OBJECTS  → Strukturierte Datenobjekte (JSONL)
30_GRAPH    → Wissens- und Beziehungsgraphen
40_REPORTS  → Berichte und Auswertungen
80_EXPORT   → Exportformate (IFC, CSV, JSON)
90_AUDIT    → Pruefsummen, Manifests, Audit-Logs
```

### 5.4 Integrationskonzept

Die FT-Traeger-Dokumentation soll in den bestehenden MASTER_INDEX.md (333 Dateien) integriert werden. Pipeline: metadata → checksum → text_extract → OCR → normalize → chunk → JSONL → validate → audit.

> **Resultate:** Detaillierte Eintraege siehe MASTER-INDEX Abschnitte B.2 und D

---

## 6. Workflow-Phasen im Detail

### 6.1 Phase 1: FIND — Bauteile identifizieren

**Beschreibung:** Identifikation wiederverwendbarer Bauteile und Baustoffstroeme. Systematische Erfassung potenzieller ReUse-Quellen.

**Anwendung Kammgarnhof:** Initialanfrage Oberndorfer/Beiglboeck (September 2025), Greenity Gate als Herkunftsprojekt identifiziert, Hallenstatik Guntramsdorf gesichert.

### 6.2 Phase 2: INVENTORY — Bauteilkatalog erstellen

**Beschreibung:** Erstellung eines vollstaendigen Bauteilkatalogs mit geometrischen, mechanischen und zustandsbezogenen Daten.

**Anwendung Kammgarnhof:** Planliste FT-Traeger+Stuetzen (Bauteil-IDs, Typen, Mengen, Geometrie), Bauteilkatalog Oberndorfer, Fotodokumentation.

### 6.3 Phase 3: TRACE — Rueckverfolgbarkeit herstellen

**Beschreibung:** Digitale Rueckverfolgbarkeit mittels BIM + IoT + EPCIS. Herkunftsnachweis und Transportdokumentation.

**Anwendung Kammgarnhof:** Herkunftsnachweis ueber Hallenstatik Guntramsdorf, GS1/EPCIS-Ereignislog fuer Transport und Lagerung, Weblinkliste als Technologierefrenz.

### 6.4 Phase 4: TEST — Qualitaet pruefen

**Beschreibung:** Pruefung der Wiederverwendbarkeit: Druckfestigkeit, Bewehrungszustand, Carbonatisierung, Chlorideintrag, Betondeckung.

**Anwendung Kammgarnhof:** FT-TRAEGER+STUETZEN-Pruefung, Versuchsplanung im Angebot Materialnomaden, re:concrete Abstimmung (Expositionsklassen XC4/XD3/XF4, Brandschutz).

### 6.5 Phase 5: LCA/GWP — CO2-Bilanzierung

**Beschreibung:** Oekobilanzierung nach EN 15804/EN 15978. Vergleich ReUse vs. Primaerproduktion. Quantifizierung der CO2-Einsparung.

**Anwendung Kammgarnhof:** Aktualisierte Massen- und ReUse-Bilanz (BGF, NF, CO2e), Materialpass+Massen+LCA-Routine, GWP-Kennzahlen von Materialnomaden.

### 6.6 Phase 6: SCORE — Circularity Score

**Beschreibung:** Bewertung des Wiedereinsatzpotenzials. Zirkularitaetsbewertung und Einstufung der Bauteile.

**Anwendung Kammgarnhof:** CirQA (Circularity Quick Assessment), Befundung+Zirkularitaetsbewertung, Wiedereinsatz-Potential-Checker.

### 6.7 Phase 7: RECERTIFY — Rezertifizierung

**Beschreibung:** Verwendbarkeitsnachweis, Zulassung im Einzelfall, Leitdetailplanung, Pruefprogramm.

**Anwendung Kammgarnhof:** Angebot Materialnomaden (29.06.2026) fuer Zulassung im Einzelfall, Leitdetailplanung, Versuchsplanung + Drittdienstleistungen. Aktuellstes Angebotsdokument + Langtext liegen vor.

### 6.8 Phase 8: REUSE — Wiedereinbau

**Beschreibung:** Wiedereinbau der rezertifizierten Bauteile mit vollstaendigem Materialpass und dokumentierter Rueckverfolgbarkeit.

**Anwendung Kammgarnhof:** Angebot V3.0 zur statischen Bearbeitung der Balkon-/Laubengangkonstruktion, Integration beider Tragstrukturen (Oberndorfer-FT-Traeger + historischer Stahl-/Gusseisenbau).

> **Resultate:** Zuordnung aller 64 Index-Eintraege zu Workflow-Phasen siehe MASTER-INDEX

---

## 7. Materialpass und Digital Product Passport (DPP)

### 7.1 Bauteil-Materialpass

Jeder wiederverwendete FT-Traeger erhaelt einen digitalen Materialpass mit:

| Datenfeld | Inhalt |
|-----------|--------|
| Bauteil-GUID | Eindeutige Identifikation (GS1/QR-Code) |
| Geometrie | L, B, H, Querschnittsflaeche, Profil |
| Werkstoff | Betonfestigkeit, Bewehrungsgehalt, Stahlguete |
| Herkunft | Bauwerk, Standort, Rueckbaudatum |
| Zustand | Pruefprotokoll, Carbonatisierung, Chlorid |
| LCA/GWP | CO2-Aequivalent, Energieaufwand |
| Zertifizierung | Zulassung im Einzelfall, Pruefinstitut |
| Ereignislog | EPCIS-Events (Demontage, Transport, Lagerung, Einbau) |

### 7.2 EU Digital Product Passport (DPP)

Der DPP nach EU-Bauprodukte-Verordnung (CPR Revision) stellt sicher, dass:
- Materialzusammensetzung transparent dokumentiert ist
- Umweltwirkung ueber den Lebenszyklus nachvollziehbar bleibt
- Wiederverwendbarkeit als Eigenschaft erfasst wird
- Regulatorische Anforderungen der neuen CPR erfuellt werden

> **Resultate:** Konkrete DPP-Felder und Materialpass-Struktur werden nach Beauftragung definiert

---

## 8. LCA / GWP-Bilanzierung und Circularity Score

### 8.1 CO2-Bilanz ReUse vs. Primaerproduktion

Die Wiederverwendung der FT-Traeger vermeidet:
- Primaere Betonproduktion (Zementherstellung als CO2-Haupttreiber)
- Primaeren Bewehrungsstahl (Hochofenroute)
- Transport und Einbau neuer Bauteile
- Deponiekosten und Entsorgungslogistik

Konkrete GWP-Kennzahlen liegen von Materialnomaden vor (Thread co2 aequivalent, 22.06.2026) und umfassen BGF, NF, BSH, optimierten Beton und Urban-Mining-Vermeidung.

### 8.2 MRR — Material Recovery Right

Das MRR monetarisiert den oekologischen Vorteil der Wiederverwendung als handelbares Zertifikat und schafft einen Marktmechanismus fuer zirkulaeres Bauen.

### 8.3 Circularity Score

Bewertungskriterien:
- Anteil wiederverwendeter Bauteile an der Gesamtkonstruktion
- Verlaengerung der Nutzungsdauer gegenueber Neuproduktion
- CO2-Einsparung gegenueber Referenzszenario
- Rueckbaubarkeit der neuen Konstruktion (Design for Disassembly)

> **Resultate:** Detailberechnung folgt nach Abschluss der Pruefphase

---

## 9. Normative Grundlagen und Regelwerke

### 9.1 Tragwerksplanung

- **OENORM EN 1990-1994** (Eurocodes) — Einwirkungen, Betonbau, Stahlbau
- **Zulassung im Einzelfall** — Verwendbarkeitsnachweis fuer gebrauchte tragende Bauteile
- **OENORM B 3151:2022** — Rueckbau von Bauwerken

### 9.2 Nachhaltigkeit und Kreislaufwirtschaft

- **EN 15804** — Umweltproduktdeklarationen (EPD), Berechnungsregeln
- **EN 15978** — Nachhaltigkeit von Bauwerken, Bewertung der umweltbezogenen Qualitaet
- **DIN SPEC 91525** — Selektiver Rueckbau
- **EU-Bauprodukte-Verordnung (CPR)** — Revision mit DPP-Anforderung

### 9.3 Digitale Standards

- **GS1/EPCIS** — Identifikation und Ereignisbasierte Rueckverfolgbarkeit
- **IFC (Industry Foundation Classes)** — BIM-Datenaustausch
- **Madaster / Circularise** — Materialpass-Plattformen

> **Resultate:** Normenverweise werden in den Materialpass integriert

---

## 10. Handlungsfelder und offene Punkte

### 10.1 Unmittelbar handlungsrelevant (Prioritaet A++)

| Nr. | Handlungsfeld | Status | Naechster Schritt |
|-----|---------------|--------|-------------------|
| 1 | FT-Traeger Zertifizierung Kammgarnhof | Angebot Materialnomaden liegt vor (29.06.2026) | Beauftragung/Freigabe erteilen |
| 2 | Gusseisen/Walzeisen Kammgarnhof | Vorabzug Angebot liegt vor | Freigabe erteilen |
| 3 | Statikunterlagen Integration | Vorstatik + TWP liegen vor | Integration in Nachweiskonzept |

### 10.2 Systemaufbau (Prioritaet A+)

| Nr. | Handlungsfeld | Status | Naechster Schritt |
|-----|---------------|--------|-------------------|
| 4 | Materialpass-Aufbau | Konzept definiert | Bauteil-IDs, GUID/QR-Code, Ereignislog definieren |
| 5 | LCA/GWP-Berechnung | GWP-Kennzahlen vorhanden | CO2-Bilanz ReUse vs. Primaerproduktion konkretisieren |
| 6 | AI-OS Integration | MASTER_INDEX mit 333 Dateien besteht | FT-Traeger-Dokumentation integrieren |

### 10.3 Parallelprojekte und Kontext (Prioritaet A/B)

| Nr. | Handlungsfeld | Status | Naechster Schritt |
|-----|---------------|--------|-------------------|
| 7 | Eisteiche FT-Traeger | Teams-Meetings dokumentiert | FT-Traeger-Matrix-Abstimmung verfolgen |
| 8 | Hybriddecke Oberndorfer | Termin war 05/2025 | Ergebnisse in Gesamtkonzept einarbeiten |
| 9 | Knowledgebase 04-BASIC-KNOWLEDGE | 9 Eintraege erfasst | Weitere Normenquellen integrieren |

---

## 11. Zusammenfassung und Ausblick

### 11.1 Zusammenfassung

Die systematische Durchsuchung aller verfuegbaren digitalen Quellen (Gmail, Google Drive, Outlook, 04-BASIC-KNOWLEDGE) hat **64 relevante Eintraege** identifiziert, die den Aufbau eines digital rueckverfolgbaren ReUse-Materialfluss-Systems fuer das Kammgarnhof-Projekt dokumentieren. Die Eintraege decken alle 8 Phasen des Workflow ab (FIND → INVENTORY → TRACE → TEST → LCA/GWP → SCORE → RECERTIFY → REUSE).

### 11.2 Quellenstatistik

| Kategorie | Anzahl | A++ | A+ | A | B |
|-----------|--------|-----|----|----|---|
| Google Drive (Kammgarnhof) | 15 | 5 | 5 | 5 | 0 |
| Google Drive (Gusseisen/Walzeisen) | 3 | 0 | 2 | 1 | 0 |
| Google Drive (RLO/AI-AWEC) | 8 | 3 | 3 | 2 | 0 |
| Google Drive (Complementary) | 6 | 0 | 0 | 3 | 3 |
| Google Drive (AI-OS Index) | 3 | 1 | 2 | 0 | 0 |
| Gmail (Kammgarnhof) | 8 | 3 | 2 | 1 | 2 |
| Gmail (Tracking/Tracing) | 8 | 0 | 1 | 1 | 6 |
| Outlook | 4 | 0 | 0 | 1 | 3 |
| 04-BASIC-KNOWLEDGE | 9 | 0 | 0 | 5 | 4 |
| **GESAMT** | **64** | **12** | **15** | **19** | **18** |

### 11.3 Ausblick

1. **Resultate-Integration** — Die detaillierten Ergebnisdaten werden in den nachfolgenden Abschnitten dieses Berichts ergaenzt
2. **Materialpass-Pilotierung** — Erstellung des ersten vollstaendigen Materialpasses fuer einen FT-Traeger als Template
3. **CO2-Bilanz** — Quantifizierte Gegenuberstellung ReUse vs. Primaerproduktion
4. **AI-OS Pipeline** — Automatisierte Verarbeitung der 64+ Quelldokumente durch die KB-Processing-Pipeline
5. **CAD-Modellierung** — Parametrisches 3D-Modell der FT-Traeger (CadQuery/Build123d) fuer BIM-Integration

---

## 12. Anhang — Quellenverzeichnis

### A. Referenzdokumente

Alle 64 Quelleneintraege mit vollstaendiger Metadatenerfassung sind im begleitenden MASTER-INDEX dokumentiert:

→ `MASTER-INDEX_DIGITALE-BAUSTOFFSTROEME_TRACKING-TRACING.md`

### B. Projektordner

| Ordner | Inhalt |
|--------|--------|
| Google Drive: P331_REUSE_FT_OBERNDORFER_BadVoeslau | Zentraler Projektordner FT-Traeger |
| Google Drive: REUSE_LABORATORY-EXPERIMENT | Laborexperimente ReUse-Materialpruefung |
| 04-BASIC-KNOWLEDGE / URBAN MINING and REUSE | Fachliteratur Urban Mining |
| 04-BASIC-KNOWLEDGE / BETONBAU | Fachliteratur Betonfertigteile |
| 04-BASIC-KNOWLEDGE / REGENERATIVE BAUSTOFFE | Nachhaltige Baustoffe |

### C. Beteiligte Personen und Organisationen

| Person/Organisation | Rolle |
|---------------------|-------|
| Ing. Julian Zotter | Tragwerksplanung, AI-AWEC, Projektkoordination |
| Markus Kneidinger / Materialnomaden GmbH | ReUse-Katalogisierung, Rezertifizierung |
| Beiglboeck / Oberndorfer | Rueckbau, Demontage, Bauteilbereitstellung |
| Dragschitz / einszueins architektur | Entwurfsplanung Kammgarnhof |
| Jordan / EGW | Auftraggeber Kammgarnhof |
| Gisela Gary / Zement+Beton | Greenity Gate (Herkunftsprojekt) |

---

*Generiert: 2026-10-08 | Bericht v1.0 — Kapitelstruktur mit Beschreibung*  
*Resultate werden in nachfolgender Bearbeitung ergaenzt*  
*Basis: MASTER-INDEX mit 64 Eintraegen aus Gmail, Google Drive, Outlook, 04-BASIC-KNOWLEDGE*
