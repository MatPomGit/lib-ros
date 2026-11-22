# Architektura lib-ros

Ujednolicone kontrakty do odczytu telemetrii i komunikacji z ROS2 bez implementowania własnego ROS.

**Wejście:** jawnie nazwane źródło danych i jego konfiguracja. **Wyjście:** wersjonowany, zwalidowany rekord z metadanymi, czasem, jednostkami i statusem. Warstwy: `src/lib_ros/` → adapter sprzętu/systemu → kontrolowany odbiorca. Katalogi w `src/` zawierają obecnie tylko dokumentację planowanej implementacji.

Opakowuje istniejące ROS2/rclpy i typy komunikatów; nie implementuje middleware DDS, algorytmów autonomii, sterownika robota, planera ruchu ani centralnego schedulera. Komendy wykonawcze poza MVP.

Wspólny standard pomiarowy: ROS2 time + monotonic clock; geometry_msgs w SI (m, rad), frame_id z TF2. Konwersje jednostek i czasu muszą być jawne; brak niezbędnych metadanych skutkuje błędem zamiast niejawnego przybliżenia.

Szczegóły: [komponenty](docs/architecture/components.md), [przepływy danych](docs/architecture/data-flow.md), [kontrakt](docs/contracts.md), [ADR-0004](docs/adr/0004-boundaries.md).

**Status:** architektura PROPOSED; implementacja NOT_IMPLEMENTED, E2E NOT_RUN, release NOT_RELEASED.
