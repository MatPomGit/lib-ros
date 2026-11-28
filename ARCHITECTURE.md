# Architektura lib-ros

Jednolity klient ROS 2 dla niezależnych aplikacji. Implementacja 0.1.0 obejmuje `RosClient`, discovery, odczyt, subskrypcje, timeout, QoS oraz backend natywny i mock.

Klient posiada własny kontekst rclpy, węzeł i executor; nie modyfikuje kontekstu globalnego. Nie uruchamia wątku w tle. Aplikacja wywołuje spin jawnie, a context manager zwalnia zasoby. Zamknięcie w callbacku jest odroczone do zakończenia wykonania callbacku, aby uniknąć blokady executora. Klient jest przeznaczony do obsługi z jednego wątku; mock pozwala wstrzykiwać dane z innego wątku.

Natywny backend zachowuje oryginalne komunikaty, a mock działa bez ROS. Nie deklaruje pełnej emulacji DDS, QoS ani typowania. Brak automatycznej normalizacji i zapisu. Czas, TF2, diagnostyka oraz komunikacja dwukierunkowa są kolejnym etapem. Sterowniki, middleware, planowanie ruchu i GUI pozostają poza biblioteką.

[Kontrakt](docs/contracts.md) | [Plan](docs/roadmap.md) | [Kompatybilność](docs/compatibility.md)
