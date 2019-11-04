""" event callback dispatcher. """

import inspect
import logging
import ob
import os
import pkgutil
import queue
import time
import threading

from ob.cls import Cfg, Register
from ob.err import ENOTIMPLEMENTED
from ob.ldr import Loader
from ob.pst import Persist
from ob.thr import Launcher
from ob.tms import days
from ob.trc import get_exception
from ob.utl import get_name
from ob.cls import get_type

def __dir__():
    return ("Handler",)

class Handler(Loader, Launcher):

    """ event Handler class. """

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._outqueue = queue.Queue()
        self._queue = queue.Queue()
        self._ready = threading.Event()
        self._stopped = False
        self._threaded = False
        self._type = get_type(self)
        self.cfg = Cfg()
        ob.update(self.cfg, {"prompt": True, "verbose": True})
        self.classes = []
        self.cmds = {}
        self.handlers = []
        self.modules = {}
        self.names = {}
        self.sleep = False
        self.state = ob.Object()
        self.state.last = time.time()
        self.state.nrsend = 0

    def dispatch(self, event):
        try:
           event.parse()
        except ENOTXT:
           event.ready()
           return
        event._func = self.get_cmd(event.chk)
        event.orig = event.orig or repr(self)
        if event._func:
            event._func(self, event)
            event.show()
        event.ready()

    def get_cmd(self, cmd):
        """ return matching function. """
        func = self.cmds.get(cmd, None)
        if not func and self.cfg.autoload:
            mn = self.names.get(cmd, None)
            if mn:
                self.load_mod(mn)
        return self.cmds.get(cmd, None)

    def get_handler(self, cmd):
        func = self.handler.get(cmd, None)
        if not func and self.cfg.autoload:
            mn = self.names.get(cmd, None)
            if mn:
                self.load_mod(mn)
        return self.cmds.get(cmd, None)

    def handle(self, e):
        """ return the event to be handled. """
        thrs = []
        for h in self.handlers:
            h(self, e)
        self.dispatch(e)

    def handler(self):
        """ basic event handler routine. """
        while not self._stopped:
            e = self._queue.get()
            if not e:
                break
            try:
                self.handle(e)
            except Exception as ex:
                logging.error(get_exception())
        logging.warning("stop %s" % get_name(self))
        self._ready.set()

    def input(self):
        """ start a input loop. """
        while not self._stopped:
            e = self.poll()
            self.put(e)

    def load_mod(self, mn, force=True):
        """ load module and scan for functions. """
        mod = super().load_mod(mn, force=force)
        self.scan(mod)
        return mod

    def output(self):
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if txt:
                if self.sleep:
                    if (time.time() - self.state.last) < 3.0:
                        time.sleep(1.0 * (self.state.nrsend % 10))
                self._say(channel, txt, type)

    def poll(self):
        """ poll for an event. """
        raise ENOTIMPLEMENTED

    def put(self, event):
        """ put event on queue. """
        self._queue.put_nowait(event)

    def register(self, handler):
        """ register a handler for a command. """
        logging.warning("register %s" % get_name(handler))
        if handler not in self.handlers:
            self.handlers.append(handler)

    def say(self, channel, txt, type="chat"):
        print(txt)

    def scan(self, mod):
        """ scan a module for commands/callbacks. """
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    self.cmds[key] = o
                    self.modules[key] = o.__module__
                elif o.__code__.co_argcount == 2 and key not in self.handlers:
                    self.register(o)
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Persist):
                t = get_type(o)
                if t not in self.classes:
                    self.classes.append(t)
                w = t.split(".")[-1].lower()
                if w not in self.names:
                    self.names[w] = str(t)

    def start(self, output=True):
        """ start this handler. """
        logging.warning("start %s" % get_name(self))
        if output:
            self.launch(self.output)
        self.launch(self.handler)
        self.input()

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def sync(self, other):
        self.handlers = other.handlers
        self.cmds.update(other.cmds)

    def walk(self, pkgname):
        """ scan package for module to load. """
        mod = self.load_mod(pkgname)
        mods = [mod,]
        try:
            mns = pkgutil.iter_modules(mod.__path__, mod.__name__+".")
        except:
            mns = pkgutil.iter_modules([mod.__file__,], mod.__name__+".")
        for n in mns:
            skip = False
            for ex in self.cfg.exclude.split(","):
                if ex and ex in n[1]:
                    skip = True
                    break
            if skip:
                continue
            logging.warn("load %s" % str(n[1]))
            try:
                mods.append(self.load_mod(n[1], force=True))
            except ModuleNotFoundError:
                logging.debug(get_exception())
        return mods
