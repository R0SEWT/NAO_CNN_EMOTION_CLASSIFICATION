# -*- coding: utf-8 -*-
"""
Main orchestrator for NAO - Modular version (ASCII safe)
=======================================================

This file only orchestrates the complete therapy session, delegating work to
four helper modules:

* **config.py**        – global parameters & child profile
* **nao_actions.py**   – NAO gestures / speech
* **perception.py**    – image capture & emotion detection
* **therapy_phases.py**– three-phase therapy logic

All printable strings here are ASCII‑only to avoid Windows cp850 encoding
issues on Python 2.7 consoles.
"""
from __future__ import print_function, unicode_literals

import sys, time
from config.config import CHILD, TESTING_ON_PC
from scripts.therapy.therapy_phases import run_session


def main():
    banner = "=== NAO Therapy Session - PC mode: {} ===".format(TESTING_ON_PC)
    print(banner)
    run_session(child_profile=CHILD, pc_mode=TESTING_ON_PC)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
