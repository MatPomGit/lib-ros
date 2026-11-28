# Macierz zgodności

| Środowisko | Cel | Status |
| --- | --- | --- |
| Python 3.11+ | Pakiet i mock | VALIDATION_PENDING |
| Linux / ROS 2 Jazzy / Python 3.12 | Backend referencyjny, test syntetyczny w CI | VALIDATION_PENDING |
| Windows | Mock, bez deklaracji ROS | NOT_RUN |
| Aplikacje i urządzenia | E2E | NOT_RUN |

Natywny backend wymaga interpretera ABI zgodnego z instalacją ROS. Nie deklarujemy zweryfikowanej kompatybilności sprzętowej ani międzyaplikacyjnej.

Wersja 0.2.0 dodaje komunikację wychodzącą i TF2. Wynik wersji 0.1.0 nie stanowi dowodu dla nowego SHA. Wsparcie innych dystrybucji i aplikacji pozostaje NOT_RUN.
