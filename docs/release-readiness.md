# Gotowość do 1.0.0

Wersja 0.2.0 jest kandydatem do stabilizacji. Bez automatycznego podbicia do 1.0.0 przed odbiorem.

| Bramka | Dowód wymagany |
| --- | --- |
| API i instalacja | CI finalnego SHA, wheel, clean venv, public_api, hash |
| ROS 2 | Natywny test Jazzy, digest obrazu, syntetyczny DDS |
| Odbiorcy | Dwa osobne repozytoria, przypięty SHA i wynik ich testów |
| Licencja | Wybór właściciela, zgodne metadane, przegląd zależności |
| Dystrybucja | Artefakt, SHA256, niezależna recenzja i zgoda na publikację |

Nie oznaczać release-gate jako PASS bez dowodów. Testy sprzętowe i zdalne transporty nie są deklarowane jako wspierane. Brak automatycznej publikacji. Po spełnieniu bramek zaktualizować spójnie pyproject, CITATION, kontrakt i metadane do 1.0.0; ponowić testy finalnego SHA. 
