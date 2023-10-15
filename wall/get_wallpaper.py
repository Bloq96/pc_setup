#!/usr/bin/env python3

"""
Gets wallpaper from Bing picture of day.

Classes:

Functions:
    main();

Misc variables:
    __author__
    __email__
    __version__
"""

__authour__="Bloq96";
__email__="";
__version__="1.0.0";

import argparse;
import json;
import os;
import re;
import requests;
import subprocess as sp;
import sys;

def main():
    """
    Gets wallpaper from Bing picture of day.
    """
    parse = argparse.ArgumentParser(prog="Get Wallpaper",\
    description=main.__doc__, epilog="");
    parse.add_argument("--version", action="version",\
    help="Version of the script.", version=__version__);
    args = parse.parse_args();

    domain = "http://bing.com";
    resource = "/HPImageArchive.aspx?format=js&mkt=en-IN&n=1";

    try:
        response = requests.get(domain + resource);
    except Exception as err:
        print("\x1B[32mget_wallpaper \x1B[31mError:\x1B[0m " +\
        "Unable to fetch image of day.", file=sys.stderr);
        print(str(err), file=sys.stderr);
        return;
    if(response.status_code == 200):
        data = json.loads(response.text);
    else:
        print("\x1B[32mget_wallpaper \x1B[31mError:\x1B[0m " +\
        "Unable to fetch image of day.", file=sys.stderr);
        return;

    try:
        response = requests.get(domain + data["images"][0]["url"],\
        stream=True);
    except Exception as err:
        print("\x1B[32mget_wallpaper \x1B[31mError:\x1B[0m " +\
        "Unable to fetch image of day.", file=sys.stderr);
        print(str(err), file=sys.stderr);
        return;
    if(response.status_code == 200):
        with open("wallpaper.jpg", "wb") as fp:
            for chunk in response:
                fp.write(chunk);
    else:
        print("\x1B[32mget_wallpaper \x1B[31mError:\x1B[0m " +\
        "Unable to fetch image of day.", file=sys.stderr);
        return;

    if(re.search(r"gnome", os.environ["DESKTOP_SESSION"].lower()) or\
    re.search(r"gnome", os.environ["XDG_SESSION_DESKTOP"].lower()) or\
    re.search(r"gnome", os.environ["XDG_CURRENT_DESKTOP"].lower())):
        sp.run("gsettings set org.gnome.desktop.background " +\
        "picture-uri file://" + os.getcwd() + "/wallpaper.jpg",
        shell=True);
    else:
        print("\x1B[32mget_wallpaper \x1B[31mError:\x1B[0m " +\
        "Unknown desktop environment.", file=sys.stderr);
        print(os.environ["XDG_SESSION_DESKTOP"].lower());
        return;

    return;

main();
