===============================
xldigest
===============================


.. image:: https://img.shields.io/travis/hammerheadlemon/xldigest.svg
        :target: https://travis-ci.org/hammerheadlemon/xldigest


Digest Excel files


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

python configure.py --static --sysroot=$SYSROOT --no-tools --no-qsci-api --no-designer-plugin --no-qml-plugin --configuration=pyqt5-linux.cfg --sip-incdir=/home/lemon/code/src/sip-4.18.1/siplib --qmake=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake py_incdir=/usr/local/include/python3.5m


/home/lemon/code/src/Python-3.5.2/Include

What we are doing is building static packages needed. See http://pyqt.sourceforge.net/Docs/pyqtdeploy/static_builds.html#docstrings

This guide is also for creating a LINUX executable at this stage. Amenedments and notes will be added when creating a Windows executable, which is my ultimate aim for the project.

1. Download latest version of sip (https://sourceforge.net/projects/pyqt/files/sip/sip-4.19/sip-4.19.tar.gz/download)
2. Download latest version of PyQt5 (https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.7.1/PyQt5_gpl-5.7.1.tar.gz/download)
3. Download Python source code (https://www.python.org)
4. Untar/unzip files into a directory.
5. Create a sysroot directory and an environment variable pointing to it (export SYSROOT=/home/lemon/Desktop...etc)
6. Install pyqtdeploy (do this with pip, create a python3 virtualenv and pip install pyqtdeploy. Make sure you have PyQt5 and sip installed in the env first; sip will be installed automatically on installing PyQt5)

We're not building Qt from source here, so we're missing that out from the instructions on the above web page.

7. Start with Python. Go into the source directory and `pyqtdeploycli --package python configure` (we don't need --target if we're doing this on a Linux machine). Make sure you have activated the virtualenv with the pyqtdeploy install. If pip installs from a cache and the exectuable doesn't work, just `pip uninstall <package>` then `pip install --no-cache <package>`.

8. `qmake SYSROOT=$SYSROOT`
9. `make`
10. `make install`

Now we're going to build a static version of `sip`

11. Change to source directory.
12. `pyqtdeploycli --package sip configure` - again, we're not including `--target` option.
13. `python configure.py --static --sysroot=$SYSROOT --no-tools --use-qmake --configuration=sip-linux.cfg`
14. `qmake`; `make`; `make install`

Now, onto PyQt5.

15. Into the source directory and do the following:
16. `pyqtdeploycli --package pyqt5 configure`

Now, this is where the commands for me varied from the tutorial.

16. `python configure.py --static --sysroot=$SYSROOT --no-tools --no-qsci-api --no-designer-plugin --no-qml-plugin --configuration=pyqt5-linux.cfg --sip-incdir=/home/<PATH-TO>/sip-4.19/siplib --qmake=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake py_incdir=/usr/local/include/python3.5m --sip=/home/lemon/.virtualenvs/xldigest-pyqt/bin/sip`

The options I added were `--sip-indcdir` to point to the `siplib` directory in the sip source directory, rather than use the Debian header files which were out of date; `--qmake` to ensure it was picking up the right executable; `--sip` to point to working sip "binary" in *another* virtualenv (because I couldn't get one installed in my current one - this is something that needs to be looked at) and `py_indcdir` to point to the `include` directory on my machine. I did a lot of fannying around with this until I got things to work. You might want to install sip system-wide, or into your virtualenv FROM SOURCE rather than pip to ensure the correct version.

Accept the license Ts & Cs.

17. `make`
18. `make install`
19. Now to create the `.pro` file that will be used by `qmake` to create the necessary `Makefile` to build everything. use `pyqtdeploy <PROJECT>.pdy` to open a GUI.
20. Application Source tab: give it a name, set either a main script file or entry point (depending on how your PyQt application is configured. My test example used a main file rather than main() function, so I chose "Main script file".

Select Target Python version and PyQt. Click Scan... to find your files, then select them.

qmake tab: left blank

PyQt Modules: select the ones that your application uses or imports. Imports should work automatically.

Standard Library: select any Standard Library imports in your application.

Other packages: use this to select external dependencies. Not tested this.

Other extension modules: blank for my test.

Locatios: Interpreter for me was "python3" The rest are left at default as they depend on the SYSROOT env variable set earlier. "build" for Build directory - this is created in the next step. qmake I left blank as I run it manually next.

Build: click Build and hopefully everything will appear in your "build" directory.

21. Go into "build" and run `qmake`. This will create `Makefile`.

22. `make`

If everything goes to plan, your executable will be there!