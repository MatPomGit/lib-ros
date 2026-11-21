# lib-ros

Ujednolicone kontrakty do odczytu telemetrii i komunikacji z ROS2 bez implementowania własnego ROS.

**Status:** architektura i struktura źródeł, **NOT_IMPLEMENTED**. To biblioteka planowana, bez zainstalowanego pakietu, urządzeń podłączonych do testów i wydania.

## Moduły

| Moduł | Zakres | Status |
| --- | --- | --- |
| [discovery](src/lib_ros/discovery/README.md) | Odczyt grafu ROS2: nody, topic, typy i serwisy | PLANNED |
| [telemetry](src/lib_ros/telemetry/README.md) | Subskrypcje i kontrolowana normalizacja komunikatów | PLANNED |
| [time](src/lib_ros/time/README.md) | ROS time, wall time, monotonic time, korelacja zegarów | PLANNED |
| [frames](src/lib_ros/frames/README.md) | Integracja TF2, orientacje i pozycje w układach odniesienia | PLANNED |
| [health](src/lib_ros/health/README.md) | Diagnostyka węzłów, QoS, kolejki i utrata pakietów | PLANNED |

Opakowuje istniejące ROS2/rclpy i typy komunikatów; nie implementuje middleware DDS, algorytmów autonomii, sterownika robota, planera ruchu ani centralnego schedulera. Komendy wykonawcze poza MVP.

Dokumentacja techniczna: [architektura](ARCHITECTURE.md), [kontrakt API](docs/contracts.md), [walidacja](docs/testing.md), [roadmap](docs/roadmap.md), [prywatność](docs/privacy.md). Rejestr publicznego API w [contracts/api.json](contracts/api.json) pozostaje pusty, dopóki nie powstanie kod. Nie opublikowano wydania ani Pages.
