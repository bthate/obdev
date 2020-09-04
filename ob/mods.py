from ob import k, get_mods
from ob.shl import set_completer

def load(event):
    if not event.args:
        event.reply("|".join({modules[x].split(".")[-1] for x in k.modules}))
        return
    mods = k.init(event.args[0])
    set_completer(k.cmds)
    if mods:
        event.reply("%s loaded" % ",".join([get_name(x) for x in mods]))

def unload(event):
    if not event.args:
        event.reply("|".join({modules[x].split(".")[-1] for x in k.modules}))
        return
    bot = k.fleet.get_bot(event.orig)
    name = event.args[0]
    for key in k.modules:
        mn = k.modules.get(key)
        if name in mn:
            try:
                k.handlers.remove(key)
                k.cmds.remove(key)
            except (RuntimeError, KeyError, ValueError):
                continue
    todo = []
    for key in k.table:
        if "mdl" in key:
            continue
        if name in key:
           todo.append(key)
    for key in todo:
        try:
            del k.table[key]
        except (KeyError, ValueError):
            event.reply("%s is not loaded." % name)
            return
    set_completer(k.cmds)
    event.reply("unload %s" % name)
