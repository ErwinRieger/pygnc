
PyGnc - buchhaltung mit gnucash, aqbanking und python
======================================================

:tags: GnuCash, python
:slug: pygnc-buchhaltung-mit-gnucash-aqbanking-and-python

My Gnucash extensions for german small businesses using gnucash, aqbanking and python (https://github.com/ErwinRieger/ibr-gnc-module reloaded).

.. contents::

Github Mirror, Projekt Homepage
++++++++++++++++++++++++++++++++

Die aktuellen Quellen gibt es hier: `https://github.com/ErwinRieger/pygnc <https://github.com/ErwinRieger/pygnc>`_.

Projekt homepage: `http://www.ibrieger.de/pygnc-buchhaltung-mit-gnucash-aqbanking-and-python.html <http://www.ibrieger.de/pygnc-buchhaltung-mit-gnucash-aqbanking-and-python.html>`_.

Installation
+++++++++++++

Gnucash und aqbanking aus den quellen installieren.

Environment, source code verzeichnis
-------------------------------------

Zunächst suchen wir uns ein verzeichnis zum bauen der softwarepakete aus und weisen es der *PYGNCSRC* environment variable zu:

.. code-block:: sh

    # Where we build stuff
    export PYGNCSRC="$HOME/bh/source"

    mkdir -p "$PYGNCSRC"
    cd "$PYGNCSRC"

    # Get pygnc sources, and setup shell environment
    git clone git@github.com:ErwinRieger/pygnc.git
    . pygnc/bin/pygnc.env

Compilierung der abhängigkeiten
-------------------------------------

Aqbanking und Gwenhywfar:

.. code-block:: sh

    cd "$PYGNCSRC"
    tar xvf /tmp/gwenhywfar-4.99.22rc6.tar.gz
    tar xvf /tmp/aqbanking-5.99.40beta.tar.gz

    cd gwenhywfar-4.99.22rc6
    patch -p0 < $PYGNCSRC/pygnc/patches/gwenhywfar_exports.patch
    ./configure --enable-debug --prefix="$PREFIX"
    make -j5
    make install
    cd ..

    cd aqbanking-5.99.40beta
    ./configure --enable-debug --prefix="$PREFIX"
    make -j5
    make install
    cd ..


Gnucash:

:Note: todo...

.. code-block:: sh

    cd "$PYGNCSRC"


PyGnc aqbanking python interface:

.. code-block:: sh

    cd "$PYGNCSRC"
    cd pygnc/aqbankingNET-master
    sh make.sh

Einfacher test der aqbanking schnittstelle, das python script *test.py* listet alle in aqbanking konfigurierten konten auf:

.. code-block:: sh

    ➜  aqbankingNET-master git:(master) python test.py

    api is: <Swig Object of type 'AB_BANKING *' at 0x7f697b16a4e0>
    AQ init...
    gwen gui is:  <Swig Object of type 'GWEN_GUI *' at 0x7f697b16a510>
    Accounts: <Swig Object of type 'AB_IMEXPORTER_ACCOUNTINFO_LIST *' at 0x7f697b16a480> <type 'SwigPyObject'>
    Number of accounts: 6
    Account: <Swig Object of type 'AB_ACCOUNT_SPEC *' at 0x7f697b16a750> None
    Account: <Swig Object of type 'AB_ACCOUNT_SPEC *' at 0x7f697b16a780> None
    Account: <Swig Object of type 'AB_ACCOUNT_SPEC *' at 0x7f697b16a750> None
    Account: <Swig Object of type 'AB_ACCOUNT_SPEC *' at 0x7f697b16a780> None
    Account: <Swig Object of type 'AB_ACCOUNT_SPEC *' at 0x7f697b16a750> DExxxxxxxxxxxxxxxxxxxx
    Account: <Swig Object of type 'AB_ACCOUNT_SPEC *' at 0x7f697b16a780> None
    done ...


Benutzung
+++++++++++++

:Note: todo...


















