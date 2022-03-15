CoinTracker-CSV-Formatter

This is a Python script to convert FTX trades history into a csv format accepted by CoinTracker.

To create virtual env for Python dependancies:
For Windows:
    py -3 -m venv .venv
For macOS/Linux:
    python3 -m venv .venv

Install the packages (example):
    # Don't use with Anaconda distributions because they include matplotlib already.

    # macOS
    python3 -m pip install matplotlib

    # Windows (may require elevation)
    python -m pip install matplotlib

    # Linux (Debian)
    apt-get install python3-tk
    python3 -m pip install matplotlib

In Visual Studio Code, don't forget to select venv python interpreter.