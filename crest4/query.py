#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
"""

# First party modules #
from plumbing.cache import property_cached

###############################################################################
class Query:
    """
    Represents a single sequence (for instance an OTU) along with
    all the information pertaining to it, such as its taxonomic assignment.

    Takes care of assigning taxonomy by using the results of the sequence
    similarity search and a phylogenetic tree as a N-ary directed graph.

    The query parameter is an object coming from biopython of type:
    'Bio.SearchIO._model.query.QueryResult'
    """

    def __init__(self, classify, query):
        # A reference to the parent object #
        self.classify = classify
        # An object containing all the hit results for this sequence #
        self.query = query
        # Get the name #
        self.name = self.query.id
        # Shortcut to the database used #
        self.db = self.classify.database
        # Shortcut to the algorithm used #
        self.algo = self.classify.search_algo

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object on '%s'>" % (self.__class__.__name__, self.name)

    #------------------------------ Properties -------------------------------#
    @property_cached
    def nodes(self):
        """
        This function will return the nodes numbers in the tree for which this
        sequence got at least one hit in a set. For example: {'1494'}
        """
        # Initialize the set that will hold all the nodes numbers we find #
        nodes = set()
        # Check there was at least one hit #
        if len(self.query.hits) == 0: return nodes
        # Get the score of the best hit #
        if self.algo == 'blast':   top_score = self.query.hsps[0].bitscore
        if self.algo == 'vsearch': top_score = self.query.hsps[0].ident_pct/100
        # Check if the score is good enough to proceed further #
        if top_score < self.classify.min_score: return nodes
        # Calculate the score-drop threshold based on the best hit #
        threshold = top_score * self.classify.score_frac
        # Iterate on the hits until falling below a threshold #
        for hsp in self.query.hsps:
            # Stop if the current bitscore is below our threshold #
            if self.algo == 'blast':   score = hsp.bitscore
            if self.algo == 'vsearch': score = hsp.ident_pct/100
            if score < threshold: break
            # Get the name (or ID) of the current hit e.g. 'DQ448783' #
            hit_id = hsp.hit_id
            # Get the corresponding node number in the tree e.g. '1494' #
            node = self.db.acc_to_node.get(hit_id, False)
            # Check that it was found #
            msg = f"The search hit '{hit_id}' was not found in the tree." \
                  f" The database '{self.db.dir_name}' is probably corrupted."
            if node is False: raise LookupError(msg)
            # Add it to the list #
            nodes.add(node)
        # Return #
        return nodes

    @property_cached
    def assigned_node(self):
        """
        This function will return the node in the tree at which the
        sequence was assigned. This could be the root of the tree or any
        other node. For example: <Tree at 0x15194b8d>
        This function can also return `False` when there are no results.
        """
        # If there are no hits #
        if len(self.nodes) == 0: return False
        # If there is only one hit, then get that node in the tree #
        if len(self.nodes) == 1:
            node_num, = self.nodes
            gen = self.db.tree.search_nodes(name=node_num)
            # Sanity check that the node was found #
            node = next(gen, False)
            msg = f"Node {node_num!r} not found in the tree."
            if node is False: raise LookupError(msg)
        # Retrieve the lowest common node if more than one hit #
        else:
            node = self.db.tree.common_ancestor(self.nodes)
        # Calculate the similarity fraction of the best alignment #
        if self.algo == 'blast':
            ident_num = self.query.hsps[0].ident_num
            algn_span = self.query.fragments[0]._aln_span
            similarity = ident_num / algn_span
        if self.algo == 'vsearch':
            similarity = self.query.hsps[0].ident_pct/100
        # Check the minimum similarity criteria for assigning at a given
        # level and proceed in an ascending fashion up
        # the tree until the similarity is satisfactory.
        while True:
            # Check that the similarity filter is activated #
            if not self.classify.min_smlrty: break
            # Check if we already got all the way up to the root #
            if node.is_root: break
            # Get the minimum value associated with this level #
            smlrty_min = float(self.db.node_to_name[node.name][1])
            # Check if we are above that minimum #
            if similarity > smlrty_min: break
            # Otherwise, go up one level for our classification #
            node = node.up
        # Return #
        return node

    def get_tax(self, node):
        """Function to get the taxonomy name of a node"""
        # Sanity check that the node has a name #
        msg = f"Node {node!r} doesn't have an ID associated."
        if not node.name: raise LookupError(msg)
        return self.db.node_to_name[node.name][0]

    @property_cached
    def taxonomy(self):
        """
        This function will return a list containing the assigned taxonomy.

        For instance:
            ['root', 'Main genome', 'Bacteria', 'Bacteria (superkingdom)',
             'Terrabacteria', 'Actinobacteria', 'Actinobacteria (class)',
             'Micrococcales', 'Micrococcaceae']
        """
        # Check if there were no hits #
        if self.assigned_node is False: return ["No hits"]
        # The taxonomic name of the current node #
        name = self.get_tax(self.assigned_node)
        # Traverse the tree up to the root #
        tree_path = self.assigned_node.ancestors()
        # Get the name of every parent along the way #
        return [name] + [self.get_tax(parent) for parent in tree_path]

    @property_cached
    def tax_string(self):
        """
        This function will return a single comma-separated string containing
        the full assigned taxonomy along with the original name of the
        sequence classified.
        """
        # Make a semicolon separated string #
        tax = '; '.join(reversed(self.taxonomy))
        # Add the name of the query to the beginning line #
        return self.name + '\t' + tax + '\n'