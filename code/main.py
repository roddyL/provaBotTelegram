# main.py

from smactbot.smactbot import application

from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This code in not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this code, you need to install an update version "
    )


def main():
    # start
    application.run_polling(close_loop=True)


if __name__ == '__main__':
    main()
    