# Strategia testów

Weryfikację przeprowadzać etapami od syntetycznych fixture do rzeczywistego środowiska; wynik szablonu nie jest dowodem obsługi urządzeń.

1. Mock grafu, typów topic i wyników discovery.
2. QoS compatibility, timeout i rozłączenia w trakcie subskrypcji.
3. Timestampy ROS oraz skoki /clock, opóźnienia.
4. Transformacja TF2 z testem frame_id i quaternionów.
5. E2E w odizolowanym kontenerze ROS2, bez rzeczywistego robota i bez sterowania aktuatorami.

Planowany raport powinien zawierać finalny SHA, polecenie testowe, host/runtime, parametry i jednostki, źródło danych, `PASS/FAIL/NOT_RUN`, log ograniczony do metadanych oraz ewentualną niepewność pomiarową. Testy sprzętowe tylko po preflight i z jawnie wskazanym źródłem; nie używać stałych runnerów dla niezaufanego kodu.

Kontrole obecnego szkieletu:

```bash
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
python -m unittest discover -s tests -v
```
