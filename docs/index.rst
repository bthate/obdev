O B
###

| Welcome to  OB , the shell bot to write your own commands for -  see https://pypi.org/project/ob/ 

OB is a cli bot, a bot without irc that can accept commands on the shell.
OB  is the result of 20 years of programming bots, was there  in 2000, is here in 2020
OB has no copyright, no LICENSE and is placed in the public domain. 

I hope you enjoy using and programming OB till the point you start programming your own bots yourself. have fun coding ! ;]

INSTALL
=======

you can download with pip3 and install globally:

::

 > sudo pip3 install ob

you can also download the tarball and install from that, see https://pypi.org/project/ob/#files

OB has it's own CLI, you can run it by giving the ob command on the
prompt, with no arguments it will just return:

::

 $ ob
 $


with the -s options it will return with its own prompt and run as a shell:

::

 $ ob -s
 > cmd
 bus,cfg,cmd,dne,fnd,krn,log,mods,tdo,tsk,ver,wd


you can use ob with arguments to run a command directly:

::

 $ ob cmd
 cfg,cmd,dne,edt,fnd,krn,log,tdo,tsk,ver,wd

to use modules with the main bot use the mods= setter to have modules loaded and init function run.

::

 $ ob -s mods=obmod.irc,obmod.rss
 cmd,edt,fnd,irc,log,mbx,opr,rss,tdo,udp,usr

CODE
====

.. include:: source.rst

SERVICE
=======

OB can restart it self after reboot, if you need/want that you can install OKBOT 
as a service for the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/ob.service file:

::

 [Unit]
 Description=OB - 24/7 channel daemon
 After=network-online.target
 Wants=network-online.target

 [Service]
 ExecStart=/usr/local/bin/ob mods=obmod.irc,obmod.rss -w

 [Install]
 WantedBy=multi-user.target

then add ob service with:

::

 $ sudo systemctl enable ob
 $ sudo systemctl daemon-reload

to configure ob use the cfg (config) command (see above). use sudo for the system
daemon configuration files at /var/lib/ob:

::

 $ sudo ob cfg server=irc.freenode.net channel=\#dunkbots nick=okbot

then restart the ob service.

::

 $ sudo service ob stop
 $ sudo service ob start

if you don't want ob to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/ob.service

OB detects whether it is run as root or as a user. if it's root it
will use the /var/lib/ob/ directory and if it's user it will use ~/.ob

CONTACT
=======

you can contact me on IRC/freenode/#dunkbots or email me at bthate@dds.nl

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net 


.. toctree::
    :hidden:

    source
