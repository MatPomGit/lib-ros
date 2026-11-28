# Przepływ danych

Aplikacja tworzy RosClient, odkrywa temat lub podaje typ, następnie subskrybuje i jawnie wykonuje spin. Backend zwraca oryginalny komunikat do callbacku; read tworzy tymczasową subskrypcję i usuwa ją również po timeout. Brak automatycznego zapisu, konwersji jednostek lub wysyłania telemetrii poza ROS. Mock przekazuje obiekty testowe wyłącznie w pamięci. Status dowodów syntetycznych i walidacji sprzętowej: [macierz zgodności](../compatibility.md).
