# Kontrakt API 0.1.0

Eksperymentalne API Python; publiczne symbole rejestruje contracts/api.json.

- RosClient: konstruktor z node_name, namespace, domain_id oraz opcjonalnym backendem.
- topics(): lista TopicDescriptor(name, types); nodes(): lista par (nazwa, namespace).
- subscribe(topic, callback, message_type=None, qos=10): uchwyt Subscription z close() i context managerem.
- read(topic, timeout=5.0, message_type=None, qos=10): następny oryginalny komunikat; brak wiadomości przed terminem powoduje RosTimeout.
- spin_once(timeout=0.1), spin(), close(): jawny cykl życia; bez wątków w tle.
- MockBackend: deklaracja tematów i emit(topic, message) dla testów offline.

Topic musi być absolutny. Typ może być klasą lub nazwą ROS; brak typu wymaga jednoznacznego discovery. QoS to dodatnia głębokość lub sensor_data. Mock ogranicza kolejkę i odrzuca najstarsze dane; nie emuluje pełnych reguł DDS. Nie buforuje wiadomości sprzed subskrypcji.

RosError oznacza błąd klienta, RosUnavailable brak runtime/typu/tematu, RosTimeout przekroczenie czasu. Nieprawidłowe argumenty powodują ValueError lub TypeError. Natywne wyjątki rclpy i wyjątki callbacków mogą być propagowane.

API nie gwarantuje obecnie serializacji, synchronizacji zegarów ani transformacji. Oryginalny header i jednostki pozostają niezmienione. Komendy wykonawcze są poza 0.1.0.
