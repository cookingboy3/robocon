# lumberjack shared logging library
# really stupid simple logging
from colorama import init, Fore


class Lumberjack:
    """Simple logging for simple people (read: me)

    args:
    caller - full name of caller, as provided by caller.
    callershort - shortened (pref 4 capital characters) version of caller name
    loglevel - logging level between 0 and 2 (from least to most verbose)
    """
    def __init__(self, caller, callershort, loglevel):
        self._caller = caller
        self._callershort = callershort
        self._loglevel = loglevel
        self._wngcount = 0
        self._errcount = 0
        self._dbgcount = 0
        init()

    def dbg(self, logstring):
        """Print super-verbose debug logging."""
        if self._loglevel >= 2:
            print(Fore.CYAN + f"[{self._callershort}-DBG] " + Fore.RESET + f"{logstring}")
        self._dbgcount += 1

    def wng(self, logstring):
        """Print a warning that won't be shown at the lowest level."""
        if self._loglevel >= 1:
            print(Fore.YELLOW + f"[{self._callershort}-WNG] " + Fore.RESET + f"{logstring}")
        self._wngcount += 1

    def err(self, logstring):
        """Print very bad error."""
        print(Fore.RED + f"[{self._callershort}-ERR] " + Fore.RESET + f"{logstring}")
        self._errcount += 1

    def out(self, logstring):
        """Make some normal output that you want the user to see."""
        print(f"[{self._callershort}] {logstring}")

    def showcounters(self):
        print(Fore.RED + f"Errors:   {self._errcount}" + Fore.RESET)
        print(Fore.YELLOW + f"Warnings: {self._wngcount}" + Fore.RESET)
        print(Fore.CYAN + f"Info:     {self._dbgcount}" + Fore.RESET)
