# main.py

from smactbot.smactbot import application


def main():
    # start
    application.run_polling(close_loop=True)


if __name__ == '__main__':
    main()
