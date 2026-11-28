# Strategia testów

CI buduje wheel, instaluje go, uruchamia testy unittest oraz przykład mock. Testy obejmują discovery, odczyt, timeout, QoS, ograniczone kolejki, zamykanie klienta i odrzucanie zagnieżdżonego spin/read.

Osobny job uruchamia test rzeczywistej komunikacji ROS 2 Jazzy w oficjalnym kontenerze bez sieci zewnętrznej i bez urządzeń. Test wykorzystuje syntetyczny publisher String, sprawdza graf DDS, odczyt, subskrypcję, QoS sensor_data, timeout i zamknięcie z callbacku. Log zawiera SHA i digest obrazu. Wynik należy odczytać z Actions dla konkretnego SHA, nie z samej obecności testu.

Lokalne testy offline:

```bash
python -m pip install .
python -m unittest discover -s tests -v
python examples/mock_read.py
```

Dalsze testy TF2, czasu, operacji dwukierunkowych i rzeczywistych konsumentów należą do kolejnych etapów. Test kontenerowy nie stanowi walidacji sprzętowej.
