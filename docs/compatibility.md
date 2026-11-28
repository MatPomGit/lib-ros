# Macierz zgodności

Wyniki historyczne dotyczą wyłącznie SHA `d4813d48ef60a9649df122d6df3cc056312608b5` (28.11.2026), a nie bieżącego HEAD. Aktualny kandydat wymaga ponownego potwierdzenia po każdej zmianie.

| Środowisko | Cel | Wynik historyczny |
| --- | --- | --- |
| Linux / Python 3.11 | Wheel, clean install, mock, API | [PASS](https://github.com/MatPomGit/lib-ros/actions/runs/46153876157) |
| Linux / ROS 2 Jazzy | Natywny backend, syntetyczny DDS | [PASS](https://github.com/MatPomGit/lib-ros/actions/runs/46153876157) |
| robo-vision / Python 3.11 | Opcjonalny pilotaż mock | [PASS](https://github.com/MatPomGit/robo-vision/actions/runs/46153983979) |
| alf-vis / Python 3.11 | Opcjonalny pilotaż TF2 mock | [PASS](https://github.com/MatPomGit/alf-vis/actions/runs/46153930447) |
| Windows, inne dystrybucje ROS i wersje Python | Zgodność środowiska | NOT_RUN |
| Natywne integracje aplikacji i sprzęt | E2E | NOT_RUN |

Python >=3.11 jest wymaganiem pakietu, a nie deklaracją testów wszystkich wersji. Natywny backend wymaga interpretera ABI zgodnego z instalacją ROS. Pilotaż mock nie potwierdza pełnego CI aplikacji ani pracy na urządzeniu. Szczegóły: [odbiorcy](consumers.md), [testy](testing.md). Wyniki nie stanowią zgody na wydanie.
