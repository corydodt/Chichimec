"""
The cycle script runs twistd -n repeatedly on a project, restarting each time
a source file changes.
"""
import sys, os

from twisted.python import usage


class Options(usage.Options):
    synopsis = "cycle-{options[projectName]}"
    optParameters = [[long, short, default, help], ...]

    # def parseArgs(self, ...):

    # def postOptions(self):
    #     """Recommended if there are subcommands:"""
    #     if self.subCommand is None:
    #         self.synopsis = "{replace} <subcommand>"
    #         raise usage.UsageError("** Please specify a subcommand (see \"Commands\").")


def run(argv=None):
    if argv is None:
        argv = sys.argv
    o = Options()
    try:
        o.parseOptions(argv[1:])
    except usage.UsageError, e:
        if hasattr(o, 'subOptions'):
            print str(o.subOptions)
        else:
            print str(o)
        print str(e)
        return 1

    return 0


if __name__ == '__main__': sys.exit(run())
