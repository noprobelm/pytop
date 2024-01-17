from .app import Pytop


def main():
    pytop = Pytop(watch_css=True)
    pytop.run()


if __name__ == "__main__":
    main()
