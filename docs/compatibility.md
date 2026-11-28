# Macierz zgodności

Dowody dotyczą dokładnie wymienionych SHA, nie automatycznie każdego późniejszego commitu.

| Środowisko | Cel | Dowód |
| --- | --- | --- |
| Linux / Python 3.11 | Wheel, clean install, mock, API | [PASS](https://github.com/MatPomGit/lib-ros/actions/runs/46154536147), lib SHA `302ea868aaece3732a7d8bbb1fd1ef57989c7c03` |
| ROS 2 Jazzy | Natywny backend, syntetyczny DDS | [PASS](https://github.com/MatPomGit/lib-ros/actions/runs/46154536147), ten sam SHA |
| app-ros-monitor 0.2.0-rc.1 | Graf, odczyt, subskrypcja, TF2, write guard | [PASS](https://github.com/MatPomGit/app-ros-monitor/actions/runs/46157414747/job/141017031242), ten sam lib SHA; app SHA `956867dab939be98ac66c7e53ac8a87dabfca28c` |
| app-ros-monitor / Python 3.11 | Mock, Qt offscreen, instalacja | [PASS](https://github.com/MatPomGit/app-ros-monitor/actions/runs/46157414747/job/141017031448), te same SHA |
| Fizyczne roboty, inne dystrybucje ROS 2, Windows | E2E i kompatybilność | NOT_RUN |
| ROS 1 | Poza zakresem | UNSUPPORTED |

Python >=3.11 jest wymaganiem pakietu, a nie deklaracją testów wszystkich wersji. Natywny backend wymaga interpretera ABI zgodnego z ROS 2. Nowsze commity wymagają własnej walidacji. [Odbiorcy](consumers.md). Brak zgody na wydanie.
