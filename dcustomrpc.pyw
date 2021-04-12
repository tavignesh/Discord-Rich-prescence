# coding=utf-8
import time
import pypresence
import ruamel.yaml
import os
import logging
import threading
from io import StringIO
# Imports go here.

# Imports tkinter if it can.
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    tk = messagebox = None

cycle = True
# Sets whether we are cycling games.


class ConfigNotFound(Exception):
    pass
# The config not found exception.


class ConfigOpenError(Exception):
    pass
# The exception when the config cannot be opened.


class ClientIDNotProvided(Exception):
    pass
# The exception when a client ID is not provided.


def dict2class(_dict: dict):
    class DictBasedClass:
        def __getattribute__(self, item):
            self.__getattr__(item)

    for key in _dict:
        setattr(DictBasedClass, key, _dict[key])

    return DictBasedClass
# Converts a dictionary to a class.


def load_config(config_location: str):
    if not os.path.isfile(config_location):
        raise ConfigNotFound(
            "Could not find the config."
        )

    try:
        with open(config_location, "r", encoding="utf8") as file_stream:
            loaded_file = ruamel.yaml.load(file_stream, Loader=ruamel.yaml.Loader)
    except ruamel.yaml.YAMLError:
        raise ConfigOpenError(
            "The YAML config seems to be malformed."
        )
    except FileNotFoundError:
        raise ConfigNotFound(
            "Could not find the config."
        )
    except IOError:
        raise ConfigOpenError(
            "Could not open the config file."
        )

    return dict2class(loaded_file)
# Loads the config.


logger = logging.getLogger("dcustomrpc")
# Sets the logger.


current_dir = os.path.dirname(os.path.abspath(__file__))
# The current_dir folder for DCustomRPC.


# Tries to show a error.
def try_show_error_box(exception):
    if tk:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "DCustomRPC", "{}".format(exception)
        )


def listening_sleeper(_time):
    global cycle
    ticks = _time / 0.1
    count = 0
    while cycle and count != ticks:
        try:
            time.sleep(0.1)
            count += 1
        except KeyboardInterrupt:
            cycle = False
            return
# Listens and sleeps.


def connect_client(client: pypresence.Presence):
    logger.info("Connecting the client.")
    while True:
        try:
            client.connect()
        except Exception as e:
            logger.exception("Failed to connect! Waiting 5 seconds.", exc_info=e)
            try_show_error_box(e)
            time.sleep(5)
        else:
            logger.info("Connected!")
            break


log_stream = StringIO()
# The stream of the logger.


# The main script that is executed.
def main():
    logging.basicConfig(
        level=logging.INFO
    )

    formatting = logging.Formatter(
        "%(levelname)s:%(name)s:%(message)s"
    )

    log = logging.StreamHandler(log_stream)
    log.setLevel(logging.INFO)
    log.setFormatter(formatting)
    logger.addHandler(log)

    logger.info("Loading the config.")
    config = load_config(current_dir + "/config.yaml")

    try:
        client_id = config.client_id
    except AttributeError:
        raise ClientIDNotProvided(
            "No client ID was provided in the config."
        )

    try:
        game_cycle = config.game_cycle
        logger.info("Found a list of games to cycle.")
    except AttributeError:
        game_cycle = {
            "time_until_cycle": 10,
            "games": [
                {
                    "state": "No cycle found.",
                    "details": "Nothing to cycle."
                }
            ]
        }

    if not config.enable_gui:
        logger.info("Disabling GUI.")
        # noinspection PyGlobalUndefined
        global tk
        # noinspection PyGlobalUndefined
        global messagebox
        tk = messagebox = None
        logger.info("Disabled GUI.")

    client = pypresence.Presence(
        client_id,
        pipe=0
    )

    connect_client(client)

    games = game_cycle.get("games", [
        {
            "state": "No cycle found.",
            "details": "Nothing to cycle."
        }
    ])
    total_games = len(games)
    time_until_cycle = game_cycle.get(
        "time_until_cycle", 10)
    while cycle:
        for game, i in zip(games, range(total_games)):
            if not cycle:
                break

            try:
                if total_games == 1:
                    client.update(**game)
                else:
                    ct = int(round(time.time()))
                    client.update(**game, party_size=[i+1, total_games], start=ct, end=ct+time_until_cycle)
                logger.info("Changed the game.")
                listening_sleeper(time_until_cycle)
            except TypeError as e:
                logger.exception("The game is formatted wrong.", exc_info=e)
            except (BrokenPipeError, pypresence.InvalidID):
                logger.error("Discord has been quit! Reopening client.")
                client.close()
                client = pypresence.Presence(
                    client_id,
                    pipe=0
                )
                connect_client(client)
            except Exception as e:
                try_show_error_box(e)
                logger.exception("Failed to update game! Waiting 5 seconds.", exc_info=e)
                time.sleep(5)

    client.close()


# Flushes the log every 15 minutes.
def flush_log_every_15_minutes():
    while True:
        time.sleep(900)
        log_stream.truncate(0)
        log_stream.seek(0)


if __name__ == '__main__':
    threading.Thread(
        target=flush_log_every_15_minutes,
        daemon=True
    ).start()

    try:
        main()
    except Exception as exc:
        try_show_error_box(exc)
        logger.exception(exc)
# Starts the script.
