# Prywatność i pochodzenie danych

**Status: PROPOSED / NOT_IMPLEMENTED.** Ten dokument definiuje wymagania
dla przyszłych adapterów `lib_ros`, a nie wdrożone zabezpieczenia.
Obecny `config/component.json` **nie zawiera** pól `data_classification`
ani `network_egress`. Nie należy z tego wywodzić potwierdzonej ochrony
danych, zgody na transmisję ani dostępu do urządzeń.

## Klasy danych i granice zaufania

| Dane ROS2 | Możliwa klasyfikacja | Wymagana decyzja przed użyciem |
| --- | --- | --- |
| Syntetyczny graf węzłów, nazwy topiców i typy | Techniczne, potencjalnie ujawniające topologię | Właściciel źródła, ograniczenie logowania nazw |
| Pozycje, trajektorie, mapy, identyfikatory robota | Poufne zależnie od środowiska | Uprawnienie do odczytu, odbiorca, retencja |
| Obraz, dźwięk, biometria, dane osób badanych | Potencjalnie osobowe lub wrażliwe | Ocena prawna i etyczna, minimalizacja, kontrola dostępu |
| Parametry połączenia, poświadczenia, identyfikatory urządzeń | Poufne lub tajne | Sekrety poza repo, bez publikacji w logach i artefaktach |

Klasyfikacja jest **kontekstowa**; nazwy topiców, `frame_id`, znaczniki
czasu, identyfikatory i metadane mogą ujawniać dane nawet bez payloadu.
Identyfikatory aparatury i parametry dostępowe należą do kontrolowanego
rejestru `devices`; repozytorium zawiera tylko abstrakcyjne kontrakty
i syntetyczne przykłady. Nie publikować danych uczestników, surowych
nagrań, sekretów ani prywatnych logów w Git, GitHub Actions, Issues lub Pages.

## Zasada odmowy dostępu i transmisji

Planowany adapter nie może domyślnie zapisywać, przesyłać ani eksportować
surowych danych. Przed pierwszym adapterem wymagany jest jawny kontrakt
konkretnego konsumenta: dozwolone źródła ROS domain/namespace/topic i URI,
kategorie danych, autoryzowany odbiorca, adresy/porty docelowe egress,
uprawnienia, limity rozmiaru i buforowania, okres retencji, zasady usuwania
oraz dowód zgody i zakres logowania. Brak któregokolwiek obowiązkowego
elementu oznacza `DENY` / `NOT_CONFIGURED`, a nie domyślne pozwolenie.
Wymaga to implementacji i testów przed obsługą rzeczywistych źródeł.

Granica konsument → adapter wymaga walidacji schematu, typu, URI, wielkości,
jednostek, `frame_id` i znaczników czasu. Granica adapter → ROS2/DDS
wymaga jawnej konfiguracji discovery/transportu oraz kontroli uprawnień
i egress stosownej do środowiska; samo użycie ROS2 nie zapewnia izolacji
sieciowej ani autoryzacji. Granica adapter → zapis/log/odbiorca domyślnie
nie dopuszcza payloadów i identyfikatorów w logach. Dane rzeczywiste nie
mogą trafiać do artefaktów CI.

## Dowody odbioru przed wdrożeniem

Wymagane są testy negatywne: odmowa nieautoryzowanego topicu, URI i
odbiorcy; brak niejawnego połączenia wychodzącego; odrzucenie brakującej
klasyfikacji i reguł retencji; ograniczenie rozmiaru; brak sekretów,
ścieżek i danych osób w logach. Testy integracyjne muszą dodatkowo
potwierdzić rzeczywistą konfigurację sieci oraz izolację ROS domain
na zatwierdzonym środowisku. Każdy wynik wymaga SHA, wersji ROS2,
źródła syntetycznego/rzeczywistego i raportu bez danych prywatnych.

**Aktualny stan:** implementacja `NOT_IMPLEMENTED`; testy zachowania
`NOT_RUN`; testy sprzętowe `NOT_RUN`. Wybór licencji, kontakt
bezpieczeństwa, klasyfikacja danych i zatwierdzony egress pozostają
bramkami przed wydaniem i integracją. Nie utożsamiać zielonego CI
szkieletu z potwierdzeniem tych zabezpieczeń.

Powiązania: [przepływ danych](architecture/data-flow.md),
[model zagrożeń](security/threat-model.md), [testy](testing.md).
