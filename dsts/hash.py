#!/usr/bin/env python

#------------------------------------------------------------------
# Description: Rabin & Karp fingerprint generator class
# Author: Angelos Molfetas (2013)
# Copyright: The University of Melbourne (2013)
# Licence: BSD licence, see attached LICENCE file
# -----------------------------------------------------------------

#from Queue import Queue
from collections import deque as Queue


class RK_hash_generator:
    """ Rabin & Karp fingerprint generator """
    def __init__(self, blockSize, hashRange):
        """ Initialise Rolling hash """
        if type(blockSize) is int:
            self.block_size = blockSize
        else:
            raise TypeError('Block Size should be an integer value')
        self.prev_hash = 0  # Previous used hash
        self.base = 10
        self.chars = None
        if type(hashRange) is int:
            self.hash_range = hashRange
        else:
            raise TypeError('Hash Range should be an integer value')

    def incremental(self, next_char):
        """ Calculates hash of byte sequence and stores it in the hash table. Use 'hash_block_with_history' method first to
        instantiate generator history before using this method. """
        try:
            previous_char = self.chars.popleft()
        except AttributeError:  # Self.chars not defined, no history defined
            raise RuntimeWarning('No history defined, hash_block_with_history should be called first')
        try:
            self.prev_hash = ((self.prev_hash - ord(previous_char) * pow(self.base, self.block_size - 1)) * self.base + ord(next_char))
        except TypeError:
            raise TypeError('Incremental buffer should be of size one')
        self.chars.append(next_char)
        return self.prev_hash % self.hash_range

    def hash_block(self, byte_sequence):
        """ Calculates hash of byte sequence """
        #if len(byte_sequence) != self.block_size:
        #    raise BufferError('Byte sequence is %s long instead of %s' % (len(byte_sequence), self.block_size))
        return self._hash_block_unconstrained(byte_sequence) % self.hash_range

    def hash_block_with_history(self, byte_sequence):
        """ Calculate hash of byte sequence """
        if len(byte_sequence) != self.block_size:  # length of byte sequence must match specified block size
            raise BufferError('Byte sequence is %s long instead of %s' % (len(byte_sequence), self.block_size))
        self.prev_hash = self._hash_block_unconstrained(byte_sequence)
        self.chars = Queue()  # Queue is used to store history
        for char in byte_sequence:
            self.chars.append(char)
        return self.prev_hash % self.hash_range

    def _hash_block_unconstrained(self, byte_sequence):
        """ Calculates hash of byte sequence without modulo"""
        h = 0      # initial hash value, starts at zero
        multiplier = self.block_size - 1
        for byte in byte_sequence:
            h += (ord(byte) * pow(self.base, multiplier))
            multiplier -= 1
        return h
