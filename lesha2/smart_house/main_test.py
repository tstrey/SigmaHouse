"""Main module."""
from core.app_test import App
import sys
sys.path.append('/core')
sys.path.append('/devices')



try:
    from secrets import secret_config
except ImportError:
    print("ERROR: Configuration not defined")
    raise RuntimeError("No secrets.py to import")

DEBUG = True


def main():
    """App entry point."""
    with App(name="/app_test", config=secret_config, debug=DEBUG) as app:
        try:
            app.run()
        except RuntimeError as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
