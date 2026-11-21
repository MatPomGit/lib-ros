# Moduły i odpowiedzialność

| Moduł | Zadanie | Ważny szczegół | Status |
| --- | --- | --- | --- |
| `lib_ros.discovery` | Odczyt grafu ROS2: nody, topic, typy i serwisy | Capability discovery, timeout, QoS i brak side-effect | PLANNED |
| `lib_ros.telemetry` | Subskrypcje i kontrolowana normalizacja komunikatów | Jawne typy, jednostki, frame_id i identyfikacja źródła | PLANNED |
| `lib_ros.time` | ROS time, wall time, monotonic time, korelacja zegarów | Wykrycie skoku /clock i jawna tolerancja synchronizacji | PLANNED |
| `lib_ros.frames` | Integracja TF2, orientacje i pozycje w układach odniesienia | Nie mieszać map/odom/base_link; walidować quaterniony | PLANNED |
| `lib_ros.health` | Diagnostyka węzłów, QoS, kolejki i utrata pakietów | Raport obserwowalności bez ukrytych działań naprawczych | PLANNED |

Opakowuje istniejące ROS2/rclpy i typy komunikatów; nie implementuje middleware DDS, algorytmów autonomii, sterownika robota, planera ruchu ani centralnego schedulera. Komendy wykonawcze poza MVP.

Typy i wyjątki stanowią **propozycję** w [kontrakcie](../contracts.md). Nie tworzyć drugiej implementacji już dostępnego middleware lub modelu inferencji.
