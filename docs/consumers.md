# Odbiorcy i integracja

Pilotaże są opcjonalne i dotyczą biblioteki 0.2.0 przypiętej do `d4813d48ef60a9649df122d6df3cc056312608b5`.

| Repozytorium | Kontrakt | Dowód dla przypiętego SHA |
| --- | --- | --- |
| [robo-vision #79](https://github.com/MatPomGit/robo-vision/pull/79) | Graf i dekodowanie telemetrii String | [PASS offline](https://github.com/MatPomGit/robo-vision/actions/runs/46153983979), HEAD konsumenta `4265ff53ce27191b50604a8669f6386e1cb56466` |
| [alf-vis #32](https://github.com/MatPomGit/alf-vis/pull/32) | Odczyt transformacji TF2 dla SLAM | [PASS offline](https://github.com/MatPomGit/alf-vis/actions/runs/46153930447), HEAD konsumenta `b548fee62b82343fe07292ea9fe5724e45988676` |
| Klienci Android i web | ROS bridge / WebSocket | OUT_OF_SCOPE dla pakietu Python |

Oba PR pozostają otwarte. W alf-vis [Pylint](https://github.com/MatPomGit/alf-vis/actions/runs/46153930329) zakończył się FAIL, a [główne CI](https://github.com/MatPomGit/alf-vis/actions/runs/46153930360) było w toku podczas przeglądu 28.11.2026. Wynik pilotażu nie oznacza akceptacji całej aplikacji.

Integracje nie zastępują dotychczasowego sterowania, wątków, executorów ani cyklu życia aplikacji. Ponowny odbiór wymaga aktualizacji przypiętego SHA i testów obu konsumentów. Walidacja natywna konsumentów i sprzętu: NOT_RUN. Wydanie 1.0.0 wymaga również decyzji licencyjnej i pozostałych bramek.
