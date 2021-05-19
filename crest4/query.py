#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair.
GNUv3 Licensed.
Contact at www.sinclair.bio
Created in May 2021.
"""

# First party modules #
from plumbing.cache import property_cached

###############################################################################
class Query:
    """
    Represents a single sequence (for instance an OTU) along with
    all the information pertaining to it, such as its taxonomic assignment.

    Takes care of assigning taxonomy for by using the results of
    the sequence similarity search and a phylogenetic tree as a N-ary
    directed graph.
    """

    def __init__(self, classify, query):
        # Save attributes #
        self.classify = classify
        self.query = query
        # Get the name #
        self.name = self.query.id
        # Shortcut to the database used #
        self.db = self.classify.database

    def __repr__(self):
        """A simple representation of this object to avoid memory addresses."""
        return "<%s object on '%s'>" % (self.__class__.__name__, self.name)

    #------------------------------ Properties -------------------------------#
    @property_cached
    def nodes(self):
        """
        This function will return the nodes in the tree for which this
        sequence got at least one hit in a set.
        """
        # Initialize the set that will hold all the nodes we find #
        nodes = set()
        # Check there was at least one hit #
        if len(self.query.hits) == 0: return nodes
        # Get the score of the best hit #
        top_score = self.query.hsps[0].bitscore
        # Check if the score is good enough to proceed further #
        if top_score < self.classify.min_score: return nodes
        # Calculate the score threshold based on the best hit #
        threshold = top_score * self.classify.score_frac
        # Iterate on the hits until falling below a threshold #
        for hsp in self.query.hsps:
            # Stop if the current bitscore is below our threshold #
            if hsp.bitscore < threshold: break
            # Get the name of the current hit #
            name = hsp.hit_id
            # Get the corresponding node name in the tree #
            node = self.db.acc_to_node.get(name)
            # Check that it was found #
            if node is None:
                msg = "The search hit '%s' was not found in the tree of %s."
                raise Exception(msg % (node, self.db.short_name))
            # Add it to the list #
            nodes.add(node)
        # Return #
        return nodes

    @property_cached
    def assigned_node(self):
        """
        This function will return the node in the tree at which the
        sequence was assigned. This could be the root of the tree or any
        other node.
        This function can also return `False` when there was no results.
        """
        # If there are no hits #
        if len(self.nodes) == 0: return False
        # If there is only one hit then get that node in the tree #
        if len(self.nodes) == 1:
            name, = self.nodes
            node = self.db.tree.search_nodes(name=name)[0]
        # Retrieve the lowest common node if more than one hit #
        else:
            node = self.db.tree.get_common_ancestor(self.nodes)
        # Calculate the similarity fraction of the best alignment #
        ident_num = self.query.hsps[0].ident_num
        algn_span = self.query.fragments[0]._aln_span
        similarity = ident_num / algn_span
        # Check the minimum similarity criteria for assigning at a given
        # level and proceed descending the tree until the similarity is
        # satisfactory
        while True:
            # Check that the similarity filter is activated #
            if True: break
            # Check if we already got to the root #
            if node is self.db.tree.root: break
            # Check that there is a minimum associated #
            if node.name not in self.tree.assignmentMin:
                msg = "Missing a minimum score"
                raise Exception(msg)
            # Check that we are below that minimum #
            if self.db.tree.assMin[node.name] > similarity:
                break
            # Otherwise go up one level for our classification #
            node = self.db.tree.get_parent(node)
        # Return #
        return node

    @property_cached
    def taxonomy(self):
        """
        This function will xxx.
        """
        # Check if there was no hits #
        if self.assigned_node is False: return ["No hits"]
        # Traverse the tree up to the root
        tree_path = self.assigned_node.iter_ancestors()
        # Get name of every parent along the way #
        return [self.db.node_to_name[parent.name][0] for parent in tree_path]

    @property_cached
    def tax_string(self):
        """
        This function will xxx.
        """
        # Make a comma separated string #
        tax = ','.join(reversed(self.taxonomy))
        # Add the name of the query to the line #
        return self.name + '\t' + tax + '\n'