#!/usr/bin/env python


class APriori(object):
    """APriori class

    This class:
        (1) implements the A-priori algorithm to find frequent itemsets
        (2) generate the association rules from teh frequent itemsets and
            score them using the confidence, lift and conviction metric.

    Parameters
    ----------
    check: bool, optional
        perform consistency checks

    verbose: bool, optional
        verbose output

    support_threshold: integer
        minimum support/count for an itemset to be consider
        as frequent

    Attributes
    ----------
    total_basket: integer
        total number of baskets

    freq_itemsets: dictionary
        dict containing all frequent itemsets of size 1, 2 or 3.
        The dictionary maps the itemsets to its support/count

    rules: list of dict()
        list of association rule. A association rule is implemented as a
        dictionary  with the following keys.
            A: set A in the association rule A --> B
            B: set B in the association rule A --> B
            conf: confidence score of the association rule
            lift: lift score of the association rule
            conv: conviction score of the association
    """

    def __init__(self, check=False, verbose=False):
        """Initiate variables in KMeans class."""
        self.check = check
        self.verbose = verbose
        self.support_threshold = 100
        self.total_basket = 0
        self.freq_itemsets = None
        self.rules = None

    # Public methods
    def set_support_threshold(self, support_threshold):
        """Set the support threshold parameter."""
        self.support_threshold = support_threshold

    def compute_freq_itemsets(self, data_file):
        """Compute itemsets of size 2 and 3 with support greater than or equal
        to support_threshold.

        Parameters
        ----------
        data_file: string
            location of the file containing the basket data file. Each line
            correspond to a basket with items in the basket seperated by
            white-space.
        """

        freq_singletons = self.get_singletons(data_file)

        freq_doubletons = self.get_doubletons(data_file, freq_singletons)

        freq_tripletons = self.get_tripletons(data_file, freq_doubletons)

        self.freq_itemsets = dict()

        self.freq_itemsets.update(freq_singletons)
        self.freq_itemsets.update(freq_doubletons)
        self.freq_itemsets.update(freq_tripletons)

    def output_freq_itemsets(self, output_filename):
        """Output frequent itemsets of sizes 2 and 3 to file.

        Parameters
        ----------
        output_filename: string
            filename to output the frequent itemsets.

        Notes
        -----
        One itemsets per line. Items in the itemset are seperated by
        whitespace.
        """

        f = open(output_filename, 'w')

        for itemsets in self.freq_itemsets:

            if len(itemsets) == 1:  # ignore singletons
                continue

            for item in itemsets:
                f.write(item + ' ')
            f.write('\n')

        f.close()

    def compute_rules(self):
        """Generate the associate rules and compute their confidence, lift
           and conviction score."""

        self.rules = list()

        # Generate association rules A --> B,
        for itemsets in self.freq_itemsets:

            # Case where size of A is 1 or 2 and size of B is 1.
            if len(itemsets) > 1:
                for item in itemsets:

                    rule = dict()
                    rule['A'] = frozenset(itemsets.difference({item}))
                    rule['B'] = frozenset({item})
                    rule['conf'] = self.confidence_score(rule['A'], rule['B'])
                    rule['lift'] = self.lift_score(rule['A'], rule['B'])
                    rule['conv'] = self.conviction_score(rule['A'], rule['B'])

                    self.rules.append(rule)

            # Case where size of A is 1 and size of B is 2.
            if len(itemsets) > 2:
                for item in itemsets:

                    rule = dict()
                    rule['A'] = frozenset({item})
                    rule['B'] = frozenset(itemsets.difference({item}))
                    rule['conf'] = self.confidence_score(rule['A'], rule['B'])
                    rule['lift'] = self.lift_score(rule['A'], rule['B'])
                    rule['conv'] = self.conviction_score(rule['A'], rule['B'])

                    self.rules.append(rule)

        if self.verbose:
            for n, rule in enumerate(self.rules):
                print "#%4d %s" % (n, rule)

    def output_rules(self, output_filename):
        """Output the association rules with the top 10 confidence, lift or
        conviction for both itemes of size 2 and size 3."""

        f = open(output_filename, 'w')

        # sort the list of dictionary by confidence score
        self.rules = sorted(self.rules, key=lambda r: r["conf"], reverse=True)

        f.write('top 10 confidence rules, (itemsets size = 2):\n')
        self.print_top_rules(f, itemset_size=2)

        f.write('top 10 confidence rules, itemsets size = 3\n')
        self.print_top_rules(f, itemset_size=3)

        # sort the list of dictionary by lift score
        self.rules = sorted(self.rules, key=lambda r: r["lift"], reverse=True)

        f.write('top 10 lift rules (itemsets size = 2):\n')
        self.print_top_rules(f, itemset_size=2)

        f.write('top 10 lift rules (itemsets size = 3):\n')
        self.print_top_rules(f, itemset_size=3)

        # sort the list of dictionary by conviction score
        self.rules = sorted(self.rules, key=lambda r: r["conv"], reverse=True)

        f.write('top 10 conviction rules (itemsets size = 2):\n')
        self.print_top_rules(f, itemset_size=2)

        f.write('top 10 conviction rules (itemsets size = 3):\n')
        self.print_top_rules(f, itemset_size=3)

        #import pdb; pdb.set_trace();

    # Private methods
    def get_singletons(self, data_file):
        """Compute single element itemsets with support >= support_threshold.

        Notes
        -----
        Also compute the total number of baskets.
        """

        hash_table = dict()  # item names to integers
        counts = list()  # item counts
        max_items = 0

        self.total_basket = 0

        # read though data and count the support of each item.
        for line in open(data_file, 'r'):

            basket = line.split()

            self.total_basket += 1

            for item in basket:

                if item not in hash_table:
                    hash_table[item] = max_items
                    counts.append(0)
                    max_items += 1

                item_index = hash_table[item]
                counts[item_index] += 1

        if self.check and len(counts) != max_items:
            raise AssertionError("len(counts) != max_items")

        # Find singleton with with support >= support_threshold.
        freq_singletons = dict()

        for item in hash_table:

            item_index = hash_table[item]

            if counts[item_index] >= self.support_threshold:
                # Use frozenset since it is immutable and therefore hashable
                singleton = frozenset({item})

                if self.check and singleton in freq_singletons:
                    print "key = ", key
                    print "singleton = ", singleton
                    raise ValueError("Duplicated singleton.")


                if self.verbose:
                        print "adding %s " % singleton,
                        print "with support %4d " % counts[item_index],
                        print "to freq_singleton"

                freq_singletons[singleton] = counts[item_index]

        return freq_singletons

    def get_doubletons(self, data_file, freq_singletons):
        """Compute 2-element itemsets with support >= support_threshold."""

        # Store item_names to item_index with a hash table.
        hash_table = dict()

        # Store counts of item-pairs as a hash table with
        # {item_1_index, item_2_index} as the search key.
        pair_counts = dict()

        max_items = 0

        for line in open(data_file, 'r'):

            basket = line.split()

            for n_1, item_1 in enumerate(basket):
                for n_2, item_2 in enumerate(basket):

                    # Avoid duplicates pair and identical item pair.
                    if n_1 >= n_2:
                        continue

                    # Using monotonicity of itemset property for screening.
                    # If either {item_1} or {item_2} is not a freq itemset
                    # then {item_1, item_2} cannot be a freq itemset.
                    if frozenset({item_1}) not in freq_singletons:
                        continue
                    if frozenset({item_2}) not in freq_singletons:
                        continue

                    if item_1 not in hash_table:
                        hash_table[item_1] = max_items
                        max_items += 1

                    if item_2 not in hash_table:
                        hash_table[item_2] = max_items
                        max_items += 1

                    item_1_index = hash_table[item_1]
                    item_2_index = hash_table[item_2]

                    key = frozenset({item_1_index, item_2_index})

                    if key not in pair_counts:
                        pair_counts[key] = 0

                    pair_counts[key] += 1

        # Find doubleton with with support >= support_threshold.
        freq_doubletons = dict()

        for item_1 in hash_table:
            for item_2 in hash_table:

                if frozenset({item_1}) not in freq_singletons:
                    continue
                if frozenset({item_2}) not in freq_singletons:
                    continue

                item_1_index = hash_table[item_1]
                item_2_index = hash_table[item_2]

                if item_1_index >= item_2_index:
                    continue

                key = frozenset({item_1_index, item_2_index})

                if key not in pair_counts:
                    continue

                if pair_counts[key] >= self.support_threshold:
                    doubleton = frozenset({item_1, item_2})

                    if self.check and doubleton in freq_doubletons:
                        print "key = ", key
                        print "doubleton = ", doubleton
                        raise ValueError("Duplicated doubleton.")

                    if self.verbose:
                        print "adding %s " % doubleton,
                        print "with support %4d " % pair_counts[key],
                        print "to freq_doubletons"

                    freq_doubletons[doubleton] = pair_counts[key]

        return freq_doubletons

    def get_tripletons(self, data_file, freq_doubletons):
        """Compute 3-element itemsets with support >= support_threshold.

        Notes
        -----
        This function is somewhat redundant with get_doubletons(). Could c
        reate a generalize function to get frequent itemset of size j (>=2)
        where the input is the data_file and the frequent itemset of size
        i = j - 1
        """

        # Store item_names to item_index with a hash table.
        hash_table = dict()  # Item names to integers

        # Store counts of item-triplets as a hash table with
        # {item_1_index, item_2_index, item_3_index} as the search key.
        triplet_counts = dict()

        max_items = 0

        for line in open(data_file, 'r'):

            basket = line.split()

            for n_1, item_1 in enumerate(basket):
                for n_2, item_2 in enumerate(basket):
                    for n_3, item_3 in enumerate(basket):

                        # Avoid duplicates triplets and identical triplets
                        if n_1 >= n_2:
                            continue
                        if n_2 >= n_3:
                            continue

                        if frozenset({item_1, item_2}) not in freq_doubletons:
                            continue
                        if frozenset({item_1, item_3}) not in freq_doubletons:
                            continue
                        if frozenset({item_2, item_3}) not in freq_doubletons:
                            continue

                        if item_1 not in hash_table:
                            hash_table[item_1] = max_items
                            max_items += 1

                        if item_2 not in hash_table:
                            hash_table[item_2] = max_items
                            max_items += 1

                        if item_3 not in hash_table:
                            hash_table[item_3] = max_items
                            max_items += 1

                        item_1_index = hash_table[item_1]
                        item_2_index = hash_table[item_2]
                        item_3_index = hash_table[item_3]

                        key = frozenset({item_1_index,
                                         item_2_index,
                                         item_3_index})

                        if key not in triplet_counts:
                            triplet_counts[key] = 0

                        triplet_counts[key] += 1

        # Find tripleton with with support >= support_threshold.
        freq_tripletons = dict()

        for item_1 in hash_table:
            for item_2 in hash_table:
                for item_3 in hash_table:

                    if frozenset({item_1, item_2}) not in freq_doubletons:
                        continue
                    if frozenset({item_1, item_3}) not in freq_doubletons:
                        continue
                    if frozenset({item_2, item_3}) not in freq_doubletons:
                        continue

                    item_1_index = hash_table[item_1]
                    item_2_index = hash_table[item_2]
                    item_3_index = hash_table[item_3]

                    if item_1_index >= item_2_index:
                        continue
                    if item_2_index >= item_3_index:
                        continue

                    key = frozenset({item_1_index,
                                     item_2_index,
                                     item_3_index})

                    if key not in triplet_counts:
                        continue

                    if triplet_counts[key] >= self.support_threshold:
                        tripleton = frozenset({item_1, item_2, item_3})

                        if self.check and tripleton in freq_tripletons:
                            print "key = ", key
                            print "tripleton = ", tripleton
                            raise ValueError("Duplicated tripleton.")

                        if self.verbose:
                            print "adding %s " % tripleton,
                            print "with support %4d " % triplet_counts[key],
                            print "to freq_tripletons"

                        freq_tripletons[tripleton] = triplet_counts[key]

        return freq_tripletons

    def confidence_score(self, set_A, set_B):
        """Compute confidence(A -> B)."""

        set_AB = frozenset(set_A.union(set_B))

        support_AB = float(self.freq_itemsets[set_AB])

        support_A = float(self.freq_itemsets[set_A])

        score = support_AB / support_A

        return score

    def lift_score(self, set_A, set_B):
        """Compute lift(A -> B)."""

        set_AB = frozenset(set_A.union(set_B))

        support_AB = float(self.freq_itemsets[set_AB])
        support_A = float(self.freq_itemsets[set_A])
        support_B = float(self.freq_itemsets[set_B])

        numerator = support_AB * float(self.total_basket)

        denominator = support_A * support_B

        score = numerator / denominator

        return score

    def conviction_score(self, set_A, set_B):
        """Compute lift(A -> B)."""

        set_AB = frozenset(set_A.union(set_B))

        support_AB = float(self.freq_itemsets[set_AB])
        support_A = float(self.freq_itemsets[set_A])
        support_B = float(self.freq_itemsets[set_B])

        numerator = 1.0 - support_B / float(self.total_basket)

        denominator = 1.0 - support_AB / support_A

        if support_AB == support_A:
            return 9999.9999

        score = numerator / denominator

        return score

    def print_top_rules(self, f, itemset_size):
        """Print top 10 rules with specific itemsize."""

        f.write("#   set_A   set_B   confidence   lift   conviction\n")

        count = 0

        for rule in self.rules:

            if len(rule["A"]) + len(rule["B"]) != itemset_size:
                continue

            count += 1

            set_A_str = "{"
            for item in rule["A"]:
                set_A_str += item + ", "
            set_A_str = set_A_str[:len(set_A_str) - 2]  # remove last ", ".
            set_A_str += "}"

            set_B_str = "{"
            for item in rule["B"]:
                set_B_str += item + ", "
            set_B_str = set_B_str[:len(set_B_str) - 2]  # remove last ", ".
            set_B_str += "}"

            line = "%2d. " % count
            line += "%s --> %s " % (set_A_str, set_B_str)
            line += "%9.4f " % rule["conf"]
            line += "%9.4f " % rule["lift"]
            line += "%9.4f " % rule["conv"]

            f.write(line + '\n')

            if count == 10:
                break

        f.write('\n\n')
