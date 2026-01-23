"""
Точка входа для EXE-версии
"""

import sys
import os


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

src_path = os.path.join(base_path, 'src')
sys.path.insert(0, src_path)

from gui_app import main
main()