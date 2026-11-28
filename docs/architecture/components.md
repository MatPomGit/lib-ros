# Moduły

RosClient udostępnia discovery, telemetry i cykl życia. NativeBackend deleguje do rclpy, MockBackend do ograniczonych kolejek w pamięci. Oba są wybierane przez konstruktor klienta. TopicDescriptor i wyjątki stanowią wspólne typy.

Wersja 0.2.0 dodaje czas, TF2, health i komunikację dwukierunkową. Nadal jedna fasada, z opt-in do operacji wychodzących. Nie implementujemy ponownie DDS ani sterowników.
