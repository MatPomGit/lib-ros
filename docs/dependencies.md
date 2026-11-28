# Zależności

Pakiet Python nie deklaruje zależności runtime z PyPI. Backend mock korzysta z biblioteki standardowej.

Backend natywny ładuje rclpy i rosidl_runtime_py z aktywnego środowiska ROS 2. Typy komunikatów muszą być dostępne w tym środowisku. Build korzysta z setuptools (PEP 517). Wersje i licencje zależności środowiska ROS oraz ich zgodność ABI pozostają do weryfikacji przed wydaniem. Brak lockfile środowiska ROS; macierz będzie przypięta po teście integracyjnym.
