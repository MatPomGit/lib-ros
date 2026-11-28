# Architektura lib-ros

Jednolity klient ROS 2 dla niezależnych aplikacji. Implementacja 0.2.0 obejmuje `RosClient`, discovery, odczyt, subskrypcje, timeout, QoS oraz backend natywny i mock. Klient udostępnia także publish, call, send_goal, transform, clock i health. Operacje wychodzące są domyślnie zablokowane.

Klient posiada własny kontekst rclpy, węzeł i executor; nie modyfikuje kontekstu globalnego. Nie uruchamia wątku w tle. Aplikacja wywołuje spin jawnie, a context manager zwalnia zasoby. Zamknięcie w callbacku jest odroczone do zakończenia wykonania callbacku, aby uniknąć blokady executora. Klient jest przeznaczony do obsługi z jednego wątku; mock pozwala wstrzykiwać dane z innego wątku.

Natywny backend zachowuje oryginalne komunikaty, a mock działa bez ROS. Nie deklaruje pełnej emulacji DDS, QoS ani typowania. Brak automatycznej normalizacji i zapisu. TF2 korzysta z bufora natywnego; zegary pozostają rozdzielone, a health raportuje lokalne liczniki, nie estymuje strat DDS. Sterowniki, middleware, planowanie ruchu i GUI pozostają poza biblioteką.

[Kontrakt](docs/contracts.md) | [Plan](docs/roadmap.md) | [Kompatybilność](docs/compatibility.md)
