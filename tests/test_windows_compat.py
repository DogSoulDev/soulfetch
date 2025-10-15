import sys
import platform

def test_windows_compat():
    assert platform.system() == "Windows", "El sistema operativo debe ser Windows para compatibilidad total."
    assert sys.getwindowsversion().major >= 10, "Se recomienda Windows 10 o superior."
