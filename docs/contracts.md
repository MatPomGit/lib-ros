# Kontrakt API 0.2.0

Eksperymentalne API Python; publiczne symbole rejestruje [contracts/api.json](../contracts/api.json).

| Metoda | Semantyka |
| --- | --- |
| `RosClient(*, node_name="lib_ros", namespace="/", domain_id=None, backend=None, allow_writes=False, use_sim_time=False)` | Osobny kontekst i executor; domyślnie backend natywny i tryb tylko do odczytu. |
| `topics()`, `services()` | Lista TopicDescriptor(name, types). |
| `nodes()` | Lista par (nazwa, namespace). |
| `subscribe(topic, callback, *, message_type=None, qos=10)` | Subscription z close() i context managerem. |
| `read(topic, *, timeout=5.0, message_type=None, qos=10)` | Następny oryginalny komunikat albo RosTimeout. |
| `spin_once(timeout=0.1)`, `spin()`, `close()` | Jawna obsługa callbacków i cyklu życia. |
| `publish(topic, message, *, qos=10)` | Publikacja oryginalnego komunikatu, bez gwarancji dostarczenia. |
| `call(service, request, *, service_type, timeout=5.0)` | Odpowiedź usługi. |
| `send_goal(action, goal, *, action_type, timeout=30.0)` | ActionResult(status, result); odrzucony cel zgłasza RosError. |
| `transform(target, source, *, stamp_ns=None, timeout=5.0)` | Transformacja TF2 target <- source; None oznacza najnowszą. |
| `clock()` | ClockSnapshot: ROS, wall i monotonic w ns, flaga czasu symulowanego. |
| `health()` | ConnectionHealth: lokalna gotowość, graf, subskrypcje, liczniki wiadomości, timeouty, regresje zegara i lokalne straty. |

Publish, call i send_goal wymagają allow_writes=True; nie jest to mechanizm autoryzacji DDS ani zabezpieczenie aktuatora. Operacje blokujące w callbackach są odrzucane. Klient jest przeznaczony do jednego wątku aplikacji, bez własnego wątku w tle. Close w callbacku odracza zwolnienie zasobów do końca operacji. Timeout jest budżetem monotonicznym, nie gwarancją twardego czasu rzeczywistego ani anulowania operacji zdalnej; nie ma automatycznych ponowień.

Nazwy topiców, usług i akcji muszą być absolutne; typ może być klasą lub nazwą ROS, a brak typu w subskrypcji wymaga jednoznacznego discovery. QoS to dodatnia głębokość lub sensor_data. Oryginalne typy, jednostki i header pozostają niezmienione; brak automatycznej serializacji i synchronizacji zegarów. Health nie estymuje strat DDS (local_drops=None dla backendu natywnego).

## Mock i wymienne backendy

MockBackend przyjmuje topics, nodes oraz opcjonalne services, actions, transforms i ros_clock. Emit dostarcza wiadomości do aktualnych subskrypcji, bez historii, w ograniczonych kolejkach FIFO z odrzucaniem najstarszych danych. Kolejki są obsługiwane rotacyjnie. Mock nie emuluje pełnych reguł DDS ani typów. Handlery usług i akcji są synchroniczne: timeout=0 blokuje ich wywołanie, wynik otrzymany po terminie jest odrzucany z RosTimeout, ale handler nie jest przerywany i jego skutki mogą pozostać. Nie jest to twardy limit czasu wykonania.

Własny backend przekazany przez backend= musi zapewniać name, local_drops oraz metody topics, nodes, subscribe(topic, callback, message_type, qos) zwracającą funkcję anulowania, spin_once(timeout), close, ready, publish(topic, message, qos), services, call(name, request, service_type, timeout), send_goal(name, goal, action_type, timeout), transform(target, source, stamp_ns, timeout), clock. Wyniki i wyjątki powinny odpowiadać typom publicznym. Backend nie jest współdzielony między klientami. Jest to eksperymentalny kontrakt strukturalny, bez dodatkowej klasy bazowej.

RosError oznacza błąd klienta, RosUnavailable brak runtime/typu/tematu, RosTimeout przekroczenie czasu, RosWriteDisabled brak opt-in. Nieprawidłowe argumenty powodują ValueError lub TypeError. Natywne wyjątki rclpy i wyjątki callbacków mogą być propagowane.

Test public_api sprawdza eksporty, wersję wheel i metody klienta. Aplikacje integrują się przez publiczne API, bez importowania _native i _mock. Do 1.0.0 kontrakt pozostaje eksperymentalny.
