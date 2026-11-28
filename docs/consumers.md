# Odbiorcy i integracja

| Repozytorium | Kontrakt | Stan |
| --- | --- | --- |
| [robo-vision](https://github.com/MatPomGit/robo-vision) | Odczyt grafu i diagnostyka telemetrii String | INTEGRATION_PENDING |
| [alf-vis](https://github.com/MatPomGit/alf-vis) | Odczyt transformacji TF2 dla SLAM | INTEGRATION_PENDING |
| Klienci Android i web | ROS bridge / WebSocket | OUT_OF_SCOPE dla pakietu Python |

Integracje pilotażowe nie zastępują istniejącego sterowania, wątków, executorów ani cyklu życia aplikacji. Każdy konsument musi przypiąć SHA biblioteki i wykonać własny test; testy mock nie stanowią dowodu pracy na urządzeniu. Wydanie 1.0.0 wymaga potwierdzonych testów i decyzji licencyjnej.
