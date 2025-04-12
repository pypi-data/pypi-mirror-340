import dataclasses
import json, dill
import os
from pathlib import Path
from rich import markup

from typing import Optional, Union, Any
from collections.abc import Callable
import traceback
from contextlib import contextmanager
import builtins

import nodriver

from image_crawler_utils.log import Log



##### Empty class


class Empty:
    """
    An empty placeholder class, mainly for checking if a parameter is used.
    """

    pass


##### Shortened file name


def attempt_name_len() -> int:
    try:
        return (os.get_terminal_size().columns - 10) // 5
    except:
        return 10


def shorten_file_name(
    file_name: str,
    name_len: int=attempt_name_len(),
) -> str:
    """
    Shorten file name for displaying on console.

    Parameters:
        file_name (str): Name of the file.
        name_len (int, optional): Maximum length allowed. Set to None (default) will use IMAGE_NAME_LEN above.
    
    Returns:
        Shortened file name.
    """

    if len(file_name) < name_len:
        return file_name
    else:
        return Path(file_name).stem[:(name_len - len('... '))] + '... ' + Path(file_name).suffix


##### Dir check


def check_dir(dir_path: str, log: Log=Log()) -> None:
    """
    Create the directory when not existing.
    Raise an error when failed.

    Parameters:
        dir_path (str): Directory path.
        log (crawler_utils.log.Log, optional): Logging config.
    """

    test_dir_path = dir_path.strip()
    try:
        if len(test_dir_path) == 0:  # Current directory
            return
        if not os.path.exists(test_dir_path):
            os.makedirs(test_dir_path)
            log.info(f'Path [repr.filename]{markup.escape(os.path.abspath(test_dir_path))}[reset] created.', extra={"markup": True})
    except Exception as e:
        output_msg_base = f'Creation of path [repr.filename]{markup.escape(os.path.abspath(test_dir_path))}[reset] FAILED'
        log.critical(f"{output_msg_base}.\n{traceback.format_exc()}", output_msg=f"{output_msg_base} because {e}", extra={"markup": True})
        raise OSError(output_msg_base)


##### Save and load dataclass (for configs)


def save_dataclass(
        dataclass,
        file_name: str,
        file_type: Optional[str]=None,
        encoding: str='UTF-8',
        log: Log=Log(),
    ) -> Optional[tuple[str, str]]:
    """
    Save a dataclass into a file.
    ONLY WORKS IF the dataclass can be JSON serialized.

    Parameters:
        dataclass (A dataclass): The dataclass to be saved.
        file_name (str): Name of file. Suffix (.json / .pkl) is optional.
        file_type (str, Optional): If suffix not found in `file_name`, designate file type manually.
        encoding (str): Encoding of JSON file (if saved as .json).
        log (crawler_utils.log.Log, optional): Logging config.

    Returns:
        (Saved file name, Absolute path of the saved file), or None if failed.
    """
    
    path, file_name = os.path.split(file_name)
    check_dir(path, log)
    try:
        if file_type is None:
            if '.' in file_name:
                ftype = os.path.splitext(file_name)[1][1:].lower()
            else:
                raise ValueError('You must set file_type if file_name does not have a suffix!')
        else:
            ftype = file_type
        ftype = ftype.strip().replace('.', '').lower()

        if ftype == 'json':
            f_name = os.path.join(path, f"{file_name}.json")
            f_name = f_name.replace(".json.json", ".json")  # If .json is already contained in file_name, skip it
            with open(f_name, "w", encoding=encoding) as f:
                json.dump(dataclasses.asdict(dataclass), f, indent=4, ensure_ascii=False)
                log.info(f'{type(dataclass).__name__} dataclass has been saved at [repr.filename]{markup.escape(os.path.abspath(f_name))}[reset]', extra={"markup": True})
                return f_name, os.path.abspath(f_name)
        elif ftype == 'pkl':
            f_name = os.path.join(path, f"{file_name}.pkl")
            f_name = f_name.replace(".pkl.pkl", ".pkl")  # If .pkl is already contained in file_name, skip it
            with open(f_name, "wb") as f:
                dill.dump(dataclass, f)
                log.info(f'{type(dataclass).__name__} dataclass has been saved at [repr.filename]{markup.escape(os.path.abspath(file_name))}[reset]', extra={"markup": True})
                return f_name, os.path.abspath(f_name)
        else:
            raise ValueError('file_type must be one of "json" or "pkl".')
        
    except Exception as e:
        log.error(f'Failed to save dataclass at [repr.filename]{markup.escape(os.path.abspath(file_name))}[reset] because {e}\n{traceback.format_exc()}', extra={"markup": True})
        return None


def load_dataclass(
        dataclass_to_load,
        file_name: str,
        file_type: Optional[str]=None,
        encoding: str='UTF-8',
        log: Log=Log(),
    ) -> Any:
    """
    Load a the file into variable "dataclass_to_load".
    The dataclass should be the same as the one you once saved.

    Parameters:
        dataclass (A dataclass): The dataclass to be loaded.
        file_name (str): Name of the file.
        file_type (str, Optional): If suffix not found in `file_name`, designate file type manually.
        encoding (str): Encoding of JSON file (if loaded from .json).
        log (crawler_utils.log.Log, optional): Logging config.

    Returns:
        Loaded dataclass_to_load, or None if failed.
    """
    
    try:
        if file_type is None:
            if '.' in file_name:
                ftype = os.path.splitext(file_name)[1][1:].lower()
            else:
                raise ValueError('You must set file_type if file_name does not have suffix!')
        else:
            ftype = file_type
        ftype = ftype.strip().replace('.', '').lower()
        
        if ftype == 'json':
            with open(file_name, "r", encoding=encoding) as f:
                dataclass_dict = json.load(f)
                for fields in dataclasses.fields(dataclass_to_load):
                    setattr(dataclass_to_load, fields.name, dataclass_dict[fields.name])
                log.info(f'{type(dataclass_to_load).__name__} dataclass has been loaded from [repr.filename]{markup.escape(os.path.abspath(file_name))}[reset]', extra={"markup": True})
                return dataclass_to_load
        elif ftype == 'pkl':
            with open(file_name, "rb") as f:
                dataclass = dill.load(f)
                for fields in dataclasses.fields(dataclass_to_load):
                    setattr(dataclass_to_load, fields.name, getattr(dataclass, fields.name))
                log.info(f'{type(dataclass_to_load).__name__} dataclass has been loaded from [repr.filename]{markup.escape(os.path.abspath(file_name))}[reset]', extra={"markup": True})
                return dataclass_to_load
        else:
            raise ValueError('file_type must be one of "json" or "pkl".')
        
    except Exception as e:
        log.error(f'Failed to load data from [repr.filename]{markup.escape(os.path.abspath(file_name))}[reset] because {e}\n{traceback.format_exc()}', extra={"markup": True})
        return None


##### nodriver-related funcs


async def set_up_nodriver_browser(
    proxies: Optional[Union[dict, Callable]]=None, 
    headless: bool=True,
    window_width: Optional[int]=None,
    window_height: Optional[int]=None,
    no_image_stylesheet: bool=False,
) -> nodriver.Browser:
    """
    Set up a nodriver.
    WARNING: nodriver use async functions. This function is async as well!

    Parameters:
        proxies (dict, function; optional): The proxies used when settings up chromium.
        headless (bool): Not to display window when running.
        window_width (int, optional): Width of window when displayed. Set to None will maximize window.
        window_height (int, optional): Height of window when displayed. Set to None will maximize window.
        no_image_stylesheet (bool): Do not fetch images and stylesheet when loading webpages.

    Returns:
        The nodriver.
    """

    browser_args = []

    if proxies is not None:
        use_proxies = proxies() if callable(proxies) else proxies
        
        if "://" in list(use_proxies.values())[0]:
            browser_args.append("--proxy-server={}".format(list(use_proxies.values())[0]))
        elif "http" in use_proxies.keys() or "https" in use_proxies.keys():
            browser_args.append("--proxy-server=http://{}".format(list(use_proxies.values())[0]))
        else:
            raise TypeError('Proxy must be one of http-type or socks-type.')
        
    if headless:
        browser_args.append("--disable-gpu")
        browser_args.append("--headless=new")
    else:
        if window_width is not None and window_height is not None:
            browser_args.append(f"--window-size={window_width},{window_height}")
        else:
            browser_args.append("--start-maximized")
    
    config = nodriver.Config(browser_args=browser_args)
    
    try:
        browser = await nodriver.start(
            config=config,
        )
    except:  # Try restarting with no_sandbox=True when running as Linux root user
        browser_args.append("--no-sandbox")
        config = nodriver.Config(browser_args=browser_args)
        browser = await nodriver.start(
            config=config,
        )

    
    if no_image_stylesheet:
        pattern_list = [
            nodriver.cdp.fetch.RequestPattern(
                url_pattern='*',
                resource_type=resource,
            ) for resource in nodriver.cdp.network.ResourceType
            if resource in [
                nodriver.cdp.network.ResourceType.IMAGE,
                nodriver.cdp.network.ResourceType.STYLESHEET,
            ]
        ]
        await browser.connection.send(nodriver.cdp.fetch.enable(patterns=pattern_list))

    return browser


##### Suppress print output


@contextmanager
def suppress_print():
    """
    Suppress built-in print so that it may not output anything.

    Use this function like:
    >>> with suppress_print():
    >>>     # suppressed print()
    """

    def silent_print(*args, **kwargs):
        pass
    original_print = print
    builtins.print = silent_print
    try:
        yield
    finally:
        builtins.print = original_print
    