# -*- coding: utf-8 -*-
"""
Проверка установленных библиотек
"""

def test_imports():
    print("=" * 50)
    print("Library Check")
    print("=" * 50)

    # OpenCV
    try:
        import cv2
        print(f"OK OpenCV: {cv.__version__}")
    except ImportError as e:
        print(f"ERROR OpenCV: {e}")

    # MediaPipe
    try:
        import mediapipe as mp
        print(f"OK MediaPipe: {mp.__version__}")
    except ImportError as e:
        print(f"ERROR MediaPipe: {e}")

    # NumPy
    try:
        import numpy as np
        print(f"OK NumPy: {np.__version__}")
    except ImportError as e:
        print(f"ERROR NumPy: {e}")

    # python-osc
    try:
        import pythonosc
        print(f"OK python-osc: installed")
    except ImportError as e:
        print(f"ERROR python-osc: {e}")

    # SciPy
    try:
        import scipy
        print(f"OK SciPy: {scipy.__version__}")
    except ImportError as e:
        print(f"ERROR SciPy: {e}")

    print("=" * 50)
    print("Check complete!")

if __name__ == "__main__":
    test_imports()