#!/usr/bin/env python

import os;
import re;
import subprocess as sp;
import sys;

def main():
    match = [];
    param = False;
    args = [];
    files = [];
    hard = False;
    recursive = False;
    verbose = False;

    for arg in sys.argv[1:]:
        match = re.match(r"-(\w+)", arg);
        if(match):
            if(param):
                raise Exception("\x1B[31mError:\x1B[0m " +\
                "Invalid value " + match.group(0) +\
                " after parameter " + args[-1] + ".");
            if(re.search(r"f", match.group(1))):
                args.append("-f");
            if(re.search(r"v", match.group(1))):
                args.append("-v");
                verbose = True;
            if(re.search(r"r", match.group(1))):
                recursive = True;
        else:
            match = re.match(r"--(\w+)", arg);
            if(match):
                if(param):
                    raise Exception("\x1B[31mError:\x1B[0m " +\
                    "Invalid value " + match.group(0) +\
                    " after parameter " + args[-1] + ".");
                if(match.group(1)=="null"):
                    param = True;
                    args.append("--null");
                elif(match.group(1)=="verbose"):
                    verbose = True;
                elif(match.group(1)=="hard"):
                    hard = True;
            else:
                if(param):
                    param = False;
                    args[-1] = args[-1] + " \"" + arg + "\"";
                else:
                    files.append(arg);

    if(not os.path.exists(os.environ["HOME"] + "/.trash")):
        if(verbose):
            print("\x1B[34mInfo:\x1B[0m .trash file does not " +\
            "exist! Creating one...");
        try:
            sp.run(["mkdir", os.environ["HOME"] + "/.trash"],
            check=True);
        except Exception as error:
            raise Exception("\x1B[31mError:\x1B[0m Error " +\
            "while running the command:\n\n\tmkdir $HOME/.trash" +\
            "\n\nException: " + str(error));

    old_files = [];
    for filename in files:
        if(os.path.isdir(filename) and not recursive):
            raise Exception("\x1B[31mError:\x1B[0m " + filename +\
            " is a directory.");
        if(os.path.exists(os.environ["HOME"] + "/.trash/" +\
        filename)):
            old_files.append(filename);
    if(verbose and old_files):
        print("\x1B[33mWarning:\x1B[0m Removing these files from " +\
        ".trash:\n");
        for filename in old_files:
            print("\t" + filename);
        ans = input("\nProceed? [Y/n] ");
        if(ans=="Y"):
            for filename in old_files:
                try:
                    sp.run(["rm", "-rf", os.environ["HOME"] +\
                    "/.trash/" + filename], check=True);
                except Exception as error:
                    raise Exception("\x1B[31mError:\x1B[0m Error " +\
                    "while running the command:\n\n\trm -rf " +\
                    "$HOME/.trash/" + filename +\
                    "\n\nException: " + str(error));
        else:
            return;
    else:
        for filename in old_files:
            try:
                sp.run(["rm", "-rf", os.environ["HOME"] +\
                "/.trash/" + filename], check=True);
            except Exception as error:
                raise Exception("\x1B[31mError:\x1B[0m Error " +\
                "while running the command:\n\n\trm -rf " +\
                "$HOME/.trash/" + filename +\
                "\n\nException: " + str(error));
    
    command = (" " + " ".join(args) if args else "") + " " +\
    " ".join(files);
    if(hard):
        if(recursive):
            command = " -r" + command;
        command = "rm" + command;
    else:
        command = "mv" + command + " -t " + os.environ["HOME"] +\
        "/.trash";

    if(files):
        if(verbose):
            print("\x1B[34mInfo:\x1B[0m Running:\n");
            print("\t" + command);
            ans = input("\nProceed? [Y/n] ");
            if(ans=="Y"):
                try:
                    sp.run(command.split(" "), check=True);
                except Exception as error:
                    raise Exception("\x1B[31mError:\x1B[0m Error " +\
                    "while running the command:\n\n\t" + command +\
                    "\n\nException: " + str(error));
        else:
            try:
                sp.run(command.split(" "), check=True);
            except Exception as error:
                raise Exception("\x1B[31mError:\x1B[0m Error " +\
                "while running the command:\n\n\t" + command +\
                "\n\nException: " + str(error));

    return;

main();
