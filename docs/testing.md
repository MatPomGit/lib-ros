# Strategia testów

CI buduje wheel, instaluje go, uruchamia testy unittest oraz przykład mock. Testy obejmują discovery, odczyt, timeout, QoS, ograniczone kolejki, zamykanie klienta i odrzucanie zagnieżdżonego spin/read.

Osobny job uruchamia test rzeczywistej komunikacji ROS 2 Jazzy w oficjalnym kontenerze bez sieci zewnętrznej i bez urządzeń. Test wykorzystuje syntetyczny publisher String, sprawdza graf DDS, odczyt, subskrypcję, QoS sensor_data, timeout i zamknięcie z callbacku. Log zawiera SHA i digest obrazu. Wynik należy odczytać z Actions dla konkretnego SHA, nie z samej obecności testu.

Lokalne testy offline:

```bash
python -m pip install .
python -m unittest discover -s tests -v
python examples/mock_read.py
```

Testy TF2, czasu i operacji dwukierunkowych są zaimplementowane. Natywne testy konsumentów i sprzętu pozostają NOT_RUN. Test kontenerowy nie stanowi walidacji sprzętowej.

Etap 2 dodaje testy mock publikacji, usług, akcji, TF2, zegarów, liczników i blokady operacji wychodzących. Natywny test rozszerzony używa wyłącznie String, AddTwoInts, Fibonacci i statycznej transformacji; bez aktuatorów. Obraz CI doinstalowuje pakiety example_interfaces i tf2_ros_py przed uruchomieniem offline. Brak testu synchronizacji fizycznych zegarów, anulowania akcji i walidacji sprzętowej.

## Reprodukowalność

Bazowy obraz ROS 2 Jazzy jest przypięty do digestu `sha256:5147d3ae250ce754afd399f6bfec15b33dd4e473ca357e30432a3182031bfad6`, odczytanego z [udanego joba natywnego](https://github.com/MatPomGit/lib-ros/actions/runs/46153876157/job/141006145055). Pakiety APT są nadal pobierane z bieżącego repozytorium, a runner i zależności narzędzi budowania nie są w pełni zamrożone. Przypięcie obrazu ogranicza zmienność, lecz nie gwarantuje identycznego artefaktu bit po bicie. CI rejestruje wersje zainstalowanych pakietów ROS i hash wheel. Testy regresyjne mock obejmują także rotację kolejek oraz odrzucanie spóźnionych wyników handlerów.
