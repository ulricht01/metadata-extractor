# 🧾 Metadata Extractor

Tento repozitář obsahuje jednoduchý nástroj pro extrakci metadat z datových souborů, napsaný v jazyce Python. Slouží pro analýzu struktury a obsahu souborů a generování přehledu metadat ve standardizované podobě.

## 🔧 Funkce

- Automatická detekce základních vlastností datového souboru
- Výstup ve formátu XML
- Modulární návrh – snadné rozšíření o nové formáty
- Dashboard zobrazující přehled o proběhlém zpracování

## 💻 Požadavky
- Závislosti jsou uvedeny v souboru `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

## 👨‍💻 Autor
- Tento nástroj byl vytvořen jako součást bakalářské práce na Přírodovědecké fakultě UJEP.

## 🧪 Testování
- Testování lze provést ručně pomocí testovacích souborů ve složce test-files/. Automatizované testy nejsou zatím zavedeny.

## Struktura
metadata-extractor/

├── app/                     # Hlavní aplikační logika
│   └── app.py
├── dashboard/               # Export adresář pro dashboard
│   └── dashboard.py
├── exports/                 # Složka pro výstupní metadata v podobě XML
├── nested_exports/          # Složka pro export sloučených XML výstupů
├── plugins/                 # Pluginy pro extrakci z různých typů souborů
│   ├── audio.py             # Extrakce metadat z audio souborů
│   ├── base_extractor.py    # Základní třída pro tvorbu pluginů
│   ├── docs.py              # Plugin pro dokumenty
│   ├── foto.py              # Plugin pro fotografie
│   ├── health.py            # Plugin pro zdravotnické formáty
├── test-files/              # Ukázkové soubory pro testování extrakce
├── tools/                   # Pomocné nástroje
│   └── exiftool/            # Integrace nástroje ExifTool
├── README.md                # Tento popis projektu
├── requirements.txt         # Seznam Python závislostí
└── todo                     # Textový soubor s poznámkami nebo úkoly k implementaci
