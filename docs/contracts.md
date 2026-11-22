# Docelowy kontrakt danych i API

**Status: PROPOSED / NOT_IMPLEMENTED.** `contracts/api.json` zachowuje puste `public_entrypoints`, ponieważ biblioteka nie udostępnia jeszcze wykonywalnych symboli.

| Typ logiczny | Zakres pól | Kontrakt |
| --- | --- | --- |
| `ROSContext` | domain_id, namespace, node_name, distribution | PLANNED |
| `TopicDescriptor` | name, type, qos_profile, direction | PLANNED |
| `StampedTelemetry` | topic, header_stamp, receive_monotonic_s, frame_id, payload_ref | PLANNED |
| `ConnectionHealth` | graph_snapshot, heartbeat, drops, errors | PLANNED |

Wspólne wymagania: jawne źródło danych i identyfikator żądania, model błędów (`INVALID_INPUT`, `UNAVAILABLE`, `TIMEOUT`, `UNSUPPORTED`, `DATA_LOSS`), limit bufora i granica odpowiedzialności za zapis. Jednostki muszą być określone w schemacie: ROS2 time + monotonic clock; geometry_msgs w SI (m, rad), frame_id z TF2.

Nie zakładać prawidłowego timestampu przy odbiorze. Zwracany status ma rozróżniać brak źródła, pusty wynik, niską jakość oraz brak danych. Wersjonowanie i publiczne symbole zostaną zatwierdzone przy pierwszej implementacji. Zmiana niekompatybilna po pojawieniu się odbiorców wymaga kontroli SemVer i migracji.
