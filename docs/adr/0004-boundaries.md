# ADR-0004: odpowiedzialność lib-ros

Data: 2026-11-21  
Status: proposed

## Kontekst

Ujednolicone kontrakty do odczytu telemetrii i komunikacji z ROS2 bez implementowania własnego ROS. Bez odrębnej granicy repozytorium podobne funkcje byłyby powielane w aplikacjach i bibliotekach.

## Proponowana decyzja

Opakowuje istniejące ROS2/rclpy i typy komunikatów; nie implementuje middleware DDS, algorytmów autonomii, sterownika robota, planera ruchu ani centralnego schedulera. Komendy wykonawcze poza MVP. Repozytorium utrzymuje jedynie warstwę adaptacji i spójne metadane. Wykorzystuje istniejące SDK/backendy po weryfikacji ich licencji. Szczegóły jednostek: ROS2 time + monotonic clock; geometry_msgs w SI (m, rad), frame_id z TF2.

## Alternatywy

- Implementacja wszystkiego w konsumentach: duplikacja i brak wspólnego kontraktu.
- Jeden megaprojekt dla wszystkich sensorów i inferencji: rozmyte granice oraz nadmierne zależności.

## Konsekwencje

Osobne testy wersjonowanego API; żadne wsparcie sprzętowe nie jest zadeklarowane przed testem. Ryzyko utrzymania adapterów i konieczność synchronizacji wersji z konsumentami.
