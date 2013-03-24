#!/usr/bin/env python
"""
SYNOPSIS
    This script finds frequent itemsets using the the A-Priori algorithm.

DESCRIPTION
    This script finds frequent itemsets using the the A-Priori algorithm.

    User inputs a file containing baskets of items (e.g. items that browsed
    or brought together.

    Each line in the file should represent a basket with items in the basket
    seperated by white-space.

    Here are two example lines.

      FRO11987 ELE17451 ELE89019 SNA90258 GRO99222
      ELE17451 GRO73461 DAI22896 SNA99873 FRO86643

    In this specific case, each string of 8 character represents the id of
    of a item in the basket.

    The script outputs:

      (1) Frequent itemsets of size 2 and 3. For each frequent
          itemset.

          Default output location: freq_itemsets.out

      (2) Association rules derived from the frequent itemsets along with
          the confidence, lift and conviction score of each rule.

          Default output location: rules.out

REFERENCES
    [1] Chapter 6 of "Mining of Massive Datasets" by Anand Rajaraman and 
        Jeff Ullman (accessible at http://i.stanford.edu/~ullman/mmds/book.pdf)

    [2] http://en.wikipedia.org/wiki/Apriori_algorithm

EXAMPLES
    Standard:
    python a_priori.py -i in/browsing.txt

    Run in check and verbose mode, and set support threshold to 500:
    python a_priori.py -i in/browsing.txt -c -v -s 500

AUTHOR
    Parin Sripakdeevong <sripakpa@stanford.edu>
"""

import sys
import time

import optparse

from a_priori_class import APriori


def main():

    global options

    a_priori = APriori(options.check, options.verbose)

    a_priori.set_support_threshold(options.support_threshold)

    a_priori.compute_freq_itemsets(options.data_file)

    a_priori.output_freq_itemsets(options.itemsets_outfile)

    a_priori.compute_rules()

    a_priori.output_rules(options.rules_outfile)


if __name__ == '__main__':

    start_time = time.time()

    usage = 'python a_priori.py -i <infile>'
    parser = optparse.OptionParser(usage=usage + globals()['__doc__'])

    parser.add_option("-i", "--data_file",
                      action="store", type="string", dest="data_file",
                      help="input basket data filename, required option")

    parser.add_option("--itemsets_out", action="store", type="string",
                      dest="itemsets_outfile", default="freq_itemsets.out",
                      help="frequent itemsets output filename")

    parser.add_option("--rules_out", action="store", type="string",
                      dest="rules_outfile", default="rules.out",
                      help="association rules output filename")

    parser.add_option("-s", "--support", action="store", type="int",
                      dest="support_threshold", default="100",
                      help="minimum support/count for itemset to be " +
                           "consider as frequent")

    parser.add_option("-v", "--verbose", action="store_true", default=False,
                      dest="verbose", help="verbose output")

    parser.add_option("-c", "--check", action="store_true", default=False,
                      dest="check", help="perform consistency checks")

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.error("leftover arguments=%s" % args)

    if not options.data_file:
        parser.error("option -i required")

    if options.verbose:
        print "-" * 50
        print time.asctime()
        print "data_file: %s" % options.data_file
        print "itemsets_outfile: %s" % options.itemsets_outfile
        print "rules_outfile: %s" % options.rules_outfile
        print "support_threshold: %s" % options.support_threshold
        print "check: %s" % options.check
        print "-" * 50

    main()
    if options.verbose:
        print time.asctime(),
        print ' | total_time = %.3f secs' % (time.time() - start_time)

    sys.exit(0)
