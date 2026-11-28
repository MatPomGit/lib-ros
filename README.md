# lib-ros

Lekka biblioteka Python do komunikacji aplikacji z ROS 2. Nie wymaga zależności od konkretnego robota, aplikacji ani GUI.

**Status:** implementacja eksperymentalna 0.1.0, bez publicznego wydania i bez potwierdzonej walidacji natywnej ROS 2.

## Szybki start

W środowisku deweloperskim:

```bash
python -m pip install .
```

```python
from lib_ros import MockBackend, RosClient

backend = MockBackend({"/demo": "std_msgs/msg/String"})
with RosClient(backend=backend) as ros:
    with ros.subscribe("/demo", print):
        backend.emit("/demo", "hello")
        ros.spin_once(0)
```

Natywny backend wymaga aktywnego środowiska ROS 2 i zgodnego interpretera Python.

```python
from lib_ros import RosClient

with RosClient() as ros:
    print(ros.topics())
    msg = ros.read("/scan", message_type="sensor_msgs/msg/LaserScan",
                   qos="sensor_data", timeout=5)
```

Domyślnie klient jest tylko do odczytu. Callbacki wykonywane są podczas jawnego `spin_once` lub `spin`. Klient jest obsługiwany z jednego wątku; zamknięcie w callbacku jest odroczone do końca spin. Bez podania typu wymagany jest jednoznacznie wykryty topic; odkrywanie grafu DDS jest asynchroniczne.

Dokumentacja: [instalacja](docs/installation.md), [API](docs/contracts.md), [architektura](ARCHITECTURE.md), [plan](docs/roadmap.md), [testy](docs/testing.md). Licencja i wydanie pozostają niezatwierdzone.
