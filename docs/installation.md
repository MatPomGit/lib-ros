# Instalacja

Python 3.11+. W środowisku deweloperskim uruchom `python -m pip install .`. Pakiet nie deklaruje zależności runtime z PyPI.

Backend mock nie wymaga ROS. Dla natywnego backendu aktywuj zgodną instalację ROS 2 (np. Jazzy na Ubuntu 24.04) i użyj interpretera zgodnego z jej pakietami rclpy, rosidl_runtime_py oraz typami wiadomości. Nie instaluj przypadkowych pakietów rclpy z PyPI.

Przykład offline: `python examples/mock_read.py`.

Nie ma publicznego wydania. Licencja pozostaje niezatwierdzona.
