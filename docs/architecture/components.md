# Moduły

RosClient udostępnia discovery, telemetry i cykl życia. NativeBackend deleguje do rclpy, MockBackend do ograniczonych kolejek w pamięci. Oba są wybierane przez konstruktor klienta. TopicDescriptor i wyjątki stanowią wspólne typy.

Czas, TF2, health oraz komunikacja dwukierunkowa pozostają planowane. Nie implementujemy ponownie DDS ani sterowników.
