# Odbiorcy i integracja

Głównym referencyjnym konsumentem jest [app-ros-monitor](https://github.com/MatPomGit/app-ros-monitor), rzeczywista aplikacja diagnostyczna ROS 2. Integracje referencyjne nie zastępują kodu wykonawczego innych aplikacji.

| Repozytorium | Zakres | Stan |
| --- | --- | --- |
| [app-ros-monitor #1](https://github.com/MatPomGit/app-ros-monitor/pull/1) | Graf, read, subskrypcja, TF2, blokada zapisu; GUI i sesje | Scalony; [PASS natywny Jazzy](https://github.com/MatPomGit/app-ros-monitor/actions/runs/46157414747/job/141017031242) |
| [robo-vision #79](https://github.com/MatPomGit/robo-vision/pull/79) | Opcjonalny pilotaż mock | Scalony, nie jest obowiązkową platformą pilotażową |
| [alf-vis #32](https://github.com/MatPomGit/alf-vis/pull/32) | Opcjonalny pilotaż TF2 mock | Scalony, nie jest obowiązkową platformą pilotażową |

Kandydat app-ros-monitor 0.2.0-rc.1 (SHA `956867dab939be98ac66c7e53ac8a87dabfca28c`) używa dokładnie przypiętej biblioteki `302ea868aaece3732a7d8bbb1fd1ef57989c7c03` z PR #2. Job natywny buduje wheel lib-ros i instaluje go offline w izolowanym kontenerze ROS 2 Jazzy. Test syntetyczny potwierdza discovery, odczyt, subskrypcję, TF2 i odrzucenie publikacji. Niezależny job sprawdza metadane VCS, mock, GUI offscreen i instalację aplikacji.

Dla przyszłych zmian API podstawowym odbiorem konsumenckim jest jawne przypięcie nowego SHA w app-ros-monitor i ponowne wykonanie testów. Nie aktualizuj automatycznie historycznych snapshotów. Nie usuwaj istniejących integracji bez decyzji właściciela. Wyniki nie potwierdzają fizycznego sprzętu, natywnego GUI ani wszystkich funkcji konsumentów; licencja i wydanie pozostają otwarte.
