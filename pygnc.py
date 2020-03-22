#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
##################################################################################
#
#  PyGnc, gnucash python extensions for german small businesses.
#  Copyright (C) 2019 Erwin Rieger <erwin.rieger@ibrieger.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##################################################################################


"""
import gnucash, AB, est
"""

import sys, locale, traceback, datetime
import argparse

##################################################################################

# Init locale, use C locale for float conversions
locale.setlocale(locale.LC_NUMERIC, '')

##################################################################################

def main():

    #
    # Main Commandline parser:
    #
    parser = argparse.ArgumentParser(description='PyGnc, the Python Gnucash Extension.')

    parser.add_argument("-r", dest="report", type=argparse.FileType('w'), help="Output file for reports.")

    subparsers = parser.add_subparsers(dest="subcommand", help='sub-command help')

    today = datetime.date.today()
    lastMonth = datetime.date(today.year, today.month, 1) - datetime.timedelta(1)

    # 
    # Sub Commandline parser, abschluss report
    # 
    subparser = subparsers.add_parser("abschluss", help=u"Abschluss bericht erzeugen.")
    subparser.add_argument("gncfile", help="Input gnucash file.")
    # subparser.add_argument("anlage_nr", type=int, help="Anlagen nummer (ANL-NR, integer).")
    subparser.add_argument("-y", dest="y", action="store", type=int, help="Jahr der abschreibung, default: dieses jahr (%d)" % today.year, default = today.year)
    # subparser.add_argument("-a", dest="a", action="store", type=int, help="Anlagen nummer (ANL-NR, integer)")

    # 
    # Sub Commandline parser, afabuchung
    # 
    subparser = subparsers.add_parser("afabuchung", help=u"Erzeuge AFA buchung für anlagegut im gnucash jahrbuch")
    subparser.add_argument("gncfile", help="Input gnucash file.")
    subparser.add_argument("anlage_nr", type=int, help="Anlagen nummer (ANL-NR, integer).")
    subparser.add_argument("-y", dest="y", action="store", type=int, help="Jahr der abschreibung, default: dieses jahr (%d)" % today.year, default = today.year)
    # subparser.add_argument("-a", dest="a", action="store", type=int, help="Anlagen nummer (ANL-NR, integer)")

    # 
    # Sub Commandline parser, create "anlagenspiegel":
    # 
    subparser = subparsers.add_parser("afaspiegel", help=u"Erzeuge anlagenspiegel aus gnucash jahrbuch")
    subparser.add_argument("gncfile", help="Input gnucash file.")
    subparser.add_argument("-y", dest="y", action="store", type=int, help="Jahr der auswertung, default: dieses jahr (%d)" % today.year, default = today.year)

    # 
    # Funktion "book check" "buch check"
    # 
    subparser = subparsers.add_parser("bck", help=u"Buch Check, plausibilitäts prüfungen.")
    subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Funktion "Check import map, cimap", integritätsprüfung/korrektur des vom bayes importer wissens.
    # 
    subparser = subparsers.add_parser("cimap", help=u"Integritätsprüfung/korrektur des vom bayes importer wissens.")
    subparser.add_argument("gncfile", help="Input gnucash file.")

    # # 
    # # Sub Commandline parser, create transaction report "anlagen"
    # # 
    # subparser = subparsers.add_parser("afareport", help=u"Erzeuge buchungsreport anlagen.")
    # subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser, classifyData:
    # 
    subparser = subparsers.add_parser("classifyData", help=u"Daten für klassifizierung aus konto 1821 extrahieren")
    subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Funktion "book compare" "vergelich zweier gnucash bücher"
    # 
    parser_cmp = subparsers.add_parser("cmp", help=u"Buch Vergeleich, vergleich zweier gnucash bücher.")
    parser_cmp.add_argument("-ae", dest="accountExact", action="store_true",
        help=u"Genauer account vergleich, vergleiche zusätzlich description.")
    parser_cmp.add_argument("-knr", dest="knr", action="store", type=str, help = "Nur dieses konto vergleichen."),
    parser_cmp.add_argument("-i", dest="insert", action="store_true", help = "Insert missing transactions into book B."),
    parser_cmp.add_argument("orig", type=str, help=u"Original gnucash buch für vergleich.")
    parser_cmp.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser, csv export
    # 
    subparser = subparsers.add_parser("csvexport", help=u"Debug: export gnucash data into CSV file.")
    subparser.add_argument("gncfile", help="Gnucash file to export.")
    subparser.add_argument("year", type=int, help="Zu exportierender zeitraum.")
    subparser.add_argument("csvfile", help="CSV file to export.")

    # 
    # Sub Commandline parser, csv import
    # 
    subparser = subparsers.add_parser("csvimport", help=u"Debug: import CSV data into gnucash book to test CSV export.")
    subparser.add_argument("gncfile", help="Destination gnucash file.")
    subparser.add_argument("csvfile", help="CSV file to import.")
    subparser.add_argument("-y", dest="y", action="store", type=int, help="Jahr der auswertung, default: dieses jahr (%d)" % today.year, default = today.year)

    # 
    # Sub Commandline parser, getbalance:
    # 
    subparsers.add_parser("getbal", help=u"Abfrage kontostand")

    # 
    # Sub Commandline parser, gettransactions:
    # 
    subparser = subparsers.add_parser("gettrans", help=u"Abfrage kontoumsätze")
    subparser.add_argument("-d", dest="date", action="store", type=str, help=u"Start datum abfrage kontoumsätze.")
    subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Prüfe kontenrahmen durch vergleich mit steuerberater (textdatei).
    # 
    subparser = subparsers.add_parser("krvergleich", help="Vergleich kontenrahmen mit steuerberater (textdatei)")
    subparser.add_argument("gncfile", help="Input gnucash file.")
    subparser.add_argument("krtext", help="Input kontenrahmen textfile.")

    # 
    # Sub Commandline parser:
    # 
    parser_kvb = subparsers.add_parser("kvb", help="Einreichung belege krankenkasse (report+pdf)")
    parser_kvb.add_argument("-d", dest="date", action="store", type=str, help="Start-datum report.")
    parser_kvb.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser:
    # 
    subparser = subparsers.add_parser("pat", help=u"Perstistente Automat. Buchungen durchführen")
    subparser = subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser:
    # 
    subparser = subparsers.add_parser("playground", help="Playground for interactive python use")
    subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser, sepatransaction:
    # 
    subparser = subparsers.add_parser("sepatrans", help=u"Manuelle SEPA überweisung")
    subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser:
    # 
    parser_split = subparsers.add_parser("splityear", help="Split/extract yearly file from gnucash file")
    parser_split.add_argument("-y", dest="y", action="store", type=int, help="Split-Jahr, default: dieses jahr (%d)" % today.year,
        default = today.year)
    parser_split.add_argument("-o", dest="output", help="Output gnucash file (split).")
    parser_split.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser:
    # 
    subparser = subparsers.add_parser("undoBC", help=u"UNDO 'BuchungsCheck'")
    subparser = subparser.add_argument("gncfile", help="Input gnucash file.")

    # 
    # Sub Commandline parser, create "ustbericht":
    # 
    subparser = subparsers.add_parser("ustbericht", help=u"Umsatzsteuer verprobung.")
    subparser.add_argument("gncfile", help="Input gnucash file.")
    subparser.add_argument("-e", type=int, default=None, help="Ende-Voranmeldezeitraum für auswertung im laufenden jahr.")
    subparser.add_argument("-n", type=str, default="", help="Datei des nächsten jahres zum auslesen der vorsteuer vorjahr (alternative für '-N' option).")
    subparser.add_argument("-N", type=float, default=None, help="Depreciated, use '-NC'. Betrag vorsteuer vorjahr (alternative für '-n' option).")
    subparser.add_argument("-NC",type=float, default=None, help="Betrag vorsteuer vorjahr in Cent (alternative für '-n' option).")
    subparser.add_argument("-v", dest="v", action="store", type=int, help="Voranmeldezeitraum in monaten (1 oder 3).", choices=[1, 3], default=1)
    subparser.add_argument("-y", dest="y", action="store", type=int, help="Jahr der auswertung, default: dieses jahr (%d)" % today.year, default = today.year)

    # 
    # Sub Commandline parser, create "vabericht":
    # 
    subparser = subparsers.add_parser("vabericht", help=u"Bericht/check umsatzsteuer voranmeldungen.")
    subparser.add_argument("gncfile", help="Input gnucash file.")
    subparser.add_argument("-e", type=int, default=None, help="Ende-Voranmeldezeitraum für auswertung im laufenden jahr.")
    subparser.add_argument("-n", type=str, default="", help="Datei des nächsten jahres zum auslesen der vorsteuer vorjahr (alternative für '-N' option).")
    subparser.add_argument("-N", type=float, default=None, help="Depreciated, use '-NC'. Betrag vorsteuer vorjahr (alternative für '-n' option).")
    subparser.add_argument("-NC",type=float, default=None, help="Betrag vorsteuer vorjahr in Cent (alternative für '-n' option).")
    subparser.add_argument("-v", dest="v", action="store", type=int, help="Voranmeldezeitraum in monaten (1 oder 3).", choices=[1, 3], default=1)
    subparser.add_argument("-y", dest="y", action="store", type=int, help="Jahr der auswertung, default: dieses jahr (%d)" % today.year, default = today.year)

    # 
    # Sub Commandline parser:
    # 
    parser_vam = subparsers.add_parser("vam", help="UST Voranmeldung monatlich")
    parser_vam.add_argument("-m", dest="m", action="store", type=int, help="Monat der VA, default: letzer monat (%d)" % lastMonth.month,
        default = lastMonth.month)
    parser_vam.add_argument("-y", dest="y", action="store", type=int, help="Jahr der VA, default: jahr des letzten monats (%d)" % lastMonth.year,
        default = lastMonth.year)
    parser_vam.add_argument("gncfile", help="Input gnucash file.")

    if today.month > 3:
        lastMonth3 = datetime.date(today.year, today.month-3, 1)
    else:
        lastMonth3 = datetime.date(today.year-1, 12 - (3 - today.month), 1)

    # 
    # Sub Commandline parser:
    # 
    parser_vaq = subparsers.add_parser("vaq", help="UST Voranmeldung quartal")
    parser_vaq.add_argument("-m", dest="m", action="store", type=int, help="Start-Monat VA, default: start letzes quartal (%d)" % lastMonth3.month,
        default = lastMonth3.month)
    parser_vaq.add_argument("-y", dest="y", action="store", type=int, help="Start-Jahr VA, default: jahr des letzten quartals (%d)" % lastMonth3.year,
        default = lastMonth3.year)
    parser_vaq.add_argument("gncfile", help="Input gnucash file.")

    args = parser.parse_args()

    # print "Parsed args:", args

    exitcode = 0

    # todo: re-enable commands
    if args.subcommand:
        print "Command \"%s\" not implemented, yet. Exiting..." % args.subcommand

    return exitcode

    if args.subcommand == "abschluss":

        book = PyGncBook(args.gncfile, BOOK_READONLY)
        reporter = PyGncReporter(stdTrnFormat, args.report)

        book.abschluss(args.y, reporter)

        # book.save()

    elif args.subcommand == "afabuchung":

        book = PyGncBook(args.gncfile)

        afa = AFA(book)
        afa.afabuchung(args.y, args.anlage_nr)

        book.save()

    elif args.subcommand == "afaspiegel":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        afa = AFA(book)
        afa.afaspiegel(args.y)

    elif args.subcommand == "bck":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        if not book.bookCheck():
            exitcode = 1

    elif args.subcommand == "cimap":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        if not book.cimap():
            exitcode = 1

    elif args.subcommand == "classifyData":
        book = PyGncBook(args.gncfile, BOOK_READONLY)
        book.classifyData()

    elif args.subcommand == "cmp":

        bookA = PyGncBook(args.orig, BOOK_READONLY)

        if args.insert:
            bookB = PyGncBook(args.gncfile)
        else:
            bookB = PyGncBook(args.gncfile, BOOK_READONLY)

        if not bookA.bookCompare(bookB, args):
            exitcode = 1

        if args.insert:
            bookB.save()

    elif args.subcommand == "csvexport":

        book = PyGncBook(args.gncfile, BOOK_READONLY)
        book.csvExport(args.year, args.csvfile)

    elif args.subcommand == "csvimport":

        book = PyGncBook(args.gncfile)
        book.csvImport(args.y, args.csvfile)
        book.save()

    elif args.subcommand == "getbal":
        aq = AQ(sys.argv[0])
        aq.getBalance()

    elif args.subcommand == "gettrans":
        book = PyGncBook(args.gncfile)

        d = None
        if args.date:
            d = datetime.datetime.strptime(args.date, "%d.%m.%Y")
        book.getAQTransactions(d)
        book.save()

    elif args.subcommand == "krvergleich":
        book = PyGncBook(args.gncfile, BOOK_READONLY)
        book.krvergleich(args.krtext)

    elif args.subcommand == "kvb":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        d = datetime.datetime.strptime(args.date, "%d.%m.%Y")

        # format = argparse.Namespace()
        # format.widths = [ "%10s", "%70s", "%9s", "%9s", "%9s","%9s" ]
        reporter = PyGncReporter(stdTrnFormat, args.report)

        book.simpleReport(KV_KONTO, startDate=d, reporter=reporter)
       
        # Erzeuge kurzmitteilungen dokument:
        tex = open("kv_kurzmitteilung_template.tex").read()

        fn = args.report.name + ".tex"
        open(fn, "w").write(tex % (reporter.nTrans, reporter.getSum(0)))

    elif args.subcommand == "pat":
        book = PyGncBook(args.gncfile)
        if not book.persistentAutoTransactions(False):
            return 1
        book.save()

    elif args.subcommand == "playground":
        book = PyGncBook(args.gncfile, BOOK_READONLY)

        allacc = book.getAllAccountDictFullName()
        allAccNames = allacc.keys()
        allAccNames.sort()

        pprint.pprint(allAccNames)
        print "# acc: ", len(allAccNames)

        sortList = map(lambda x: (allacc[x].GetNumberOfSplits(), x, allacc[x]), allAccNames)
        sl = sorted(sortList, key=lambda x: x[0], reverse=True)

        pprint.pprint(sl[:10])

    elif args.subcommand == "sepatrans":
        book = PyGncBook(args.gncfile)
        book.sepaTransaction()
        print "NOT saving..."
        # book.save()

    elif args.subcommand == "splityear":
        # Create new book as a copy of the old one:
        assert(args.output)

        shutil.copy(args.gncfile, args.output)
        book = PyGncBook(args.output)

        # Erzeuge zunächst eröffnungsbuchungen AFA
        afa = AFA(book)
        afa.eroeffnungsBuchungen(args.y)

        book.splitYear(args.y)
        book.save()

    elif args.subcommand == "undoBC":
        book = PyGncBook(args.gncfile)
        book.undoBuchungsCheck()
        book.save()

    elif args.subcommand == "ustbericht":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        #
        # XXX momentan keine änderung des anmeldezeitraumes im jahr möglich.
        #
        startDate =  startOfYear(args.y)

        endzr = 12
        if args.e:
            endzr = args.e

        amzrs = AnmeldeZeitraeume()
        amzrs.initEqual(startDate, args.v, endzr)

        assert(not args.N)

        book.ustBericht(args.y, args.n, args.NC, amzrs)

    elif args.subcommand == "vabericht":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        #
        # XXX momentan keine änderung des anmeldezeitraumes im jahr möglich.
        #
        startDate =  startOfYear(args.y)

        endzr = 12
        if args.e:
            endzr = args.e

        amzrs = AnmeldeZeitraeume()
        amzrs.initEqual(startDate, args.v, endzr)

        assert(not args.N)

        book.vaBericht(args.y, args.n, args.NC, amzrs)

    elif args.subcommand == "vam" or args.subcommand == "vaq":

        book = PyGncBook(args.gncfile, BOOK_READONLY)

        if args.subcommand == "vam":
            (startDate, endDate) = getVADateRange(args.y, args.m, 1)
        else:
            (startDate, endDate) = getVADateRange(args.y, args.m, 3)

        # # datum/konto | beschreibung | wert | summe mwst | summe vorst. | summe va |
        # format = argparse.Namespace()
        # format.widths = [ "%10s", "%70s", "%9s", "%9s", "%9s","%9s" ]

        reporter = PyGncReporter(stdTrnFormat, args.report)
        book.voranmeldung(args.subcommand, startDate, endDate, reporter)

    else:
        parser.print_usage()

    return exitcode

##################################################################################

if __name__ == "__main__":

    try:
        exitcode = main()
    except SystemExit, ex:
        print "caught SystemExit", ex
        exitcode = ex.code
    except:
        print "caught Exception: ", traceback.format_exc()
        exitcode = 1

    sys.exit(exitcode)

