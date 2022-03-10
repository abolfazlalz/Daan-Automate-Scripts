import config
from daan import Daan


def main():
    data = config.get()
    d = Daan(data['username'], data['password'])
    d.load_lessons()
    d.close()


if __name__ == '__main__':
    main()
