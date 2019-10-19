
""" email to object scanner. """

import mailbox
import ob
import os

from ob import k
from ob.pst import Persist

bdmonths = ['Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
            'Sep', 'Oct', 'Nov', 'Dec']
monthint = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

class Email(Persist):

    """ email data. """

    def __init__(self):
        super().__init__()
        self.text = ""

def to_date(date):
    """ fetch date from string. """
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError):
        try:
            if "+" in res[4]:
                raise ValueError
            if "-" in res[4]:
                raise ValueError
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], monthint[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd

def mbox(event):
    """ scan emails from mbox. """
    if not event.args:
        event.reply("mbox <path>")
        return
    fn = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fn)
    nr = 0
    if os.path.isdir(fn):
        thing = mailbox.Maildir(fn, create=False)
    elif os.path.isfile(fn):
        thing = mailbox.mbox(fn, create=False)
    else:
        event.reply("need a mbox or maildir.")
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for m in thing:
        o = Email()
        ob.update2(o, m)
        try:
            sdate = os.sep.join(to_date(o.Date).split())
        except AttributeError:
            sdate = None
        o.text = ""
        for payload in m.walk():
            if payload.get_content_type() == 'text/plain':
                o.text += payload.get_payload()
        o.text = o.text.replace("\\n", "\n")
        if sdate:
            o.save(stime=sdate)
        else:
            o.save()
        nr += 1
    if nr:
        event.reply("ok %s" % nr)

def cor(event):
    """ analyse correspondence. """
    if not event.args:
        event.reply("cor <email>")
        return
    event.selector["From"] = event.args[0]
    nr = 0
    for email in k.db.all("obot.mbox.Email", event.selector):
        event.reply("%s %s" % (nr, ob.format(email, event.selector.keys())))
        nr += 1

def email(event):
    if not event.args:
        event.reply("email <match> attr1 attr2")
        return
    nr = 0
    s = event.selector
    s.update({"From": event.args[0]})
    if len(event.args) >= 2:
        nr = 0
        for arg in event.args[1:]:
            if arg.endswith("+"):
                arg = arg[:1]
                event.dkeys.append("text")
            elif arg.endswith("-"):
                arg = arg[:1]
                event.ignore = "text"
            else:
                event.dkeys.append(arg)
            s.update({"text": arg})
            
            if len(event.args) > 1:
                if arg in event.dkeys:
                    event.dkeys.remove(arg)
            if arg in s:
                del s[arg]
    event.dkeys.extend(["From", "Subject"])
    event.options = event.options + "t"
    nr = 0
    for o in k.db.find("obot.mbox.Email", s, event.index, event.delta):
        event.display(o, "%-3s" % str(nr))
        nr += 1
