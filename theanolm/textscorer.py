#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import theano
import theano.tensor as tensor
import numpy
from theanolm.exceptions import NumberError

class TextScorer(object):
    """Text Scoring Using a Neural Network Language Model
    """

    def __init__(self, network, classes_to_ignore, profile=False):
        """Creates a Theano function self.score_function that computes the
        log probabilities predicted by the neural network for the words in a
        mini-batch.

        self.score_function takes as arguments two matrices, the input word IDs
        and mask, and returns a matrix of word prediction log probabilities. The
        matrices are indexed by time step and word sequence, output containing
        one less time step, since the last time step is not predicting any word.

        :type network: Network
        :param network: the neural network object

        :type classes_to_ignore: list of ints
        :param classes_to_ignore: list of class IDs that will be ignored when
                                  computing the cost

        :type profile: bool
        :param profile: if set to True, creates a Theano profile object
        """

        inputs = [network.minibatch_input, network.minibatch_mask]
        logprobs = tensor.log(network.prediction_probs)
        # The logprobs are valid only for timesteps that have a valid target
        # output, i.e. the next word is not masked out. We assume that the first
        # time step is never masked out.
# XXX        logprobs = logprobs * network.minibatch_mask[1:]
        mask = network.minibatch_mask[1:]
        for class_id in classes_to_ignore:
            mask *= tensor.neq(network.minibatch_input[1:], class_id)
        logprobs *= mask
        self.score_function = theano.function(inputs, logprobs, profile=profile)

    def score_batch(self, word_ids, membership_probs, mask):
        """Computes the log probabilities predicted by the neural network for
        the words in a mini-batch.

        :type word_ids: numpy.ndarray of an integer type
        :param word_ids: a 2-dimensional matrix, indexed by time step and
                         sequence, that contains the word IDs

        :type membership_probs: numpy.ndarray of a floating point type
        :param membership_probs: a 2-dimensional matrix, indexed by time step
                                 and sequences, that contains the class
                                 membership probabilities of the words

        :type mask: numpy.ndarray of a floating point type
        :param mask: a 2-dimensional matrix, indexed by time step and sequence,
                     that masks out elements past the sequence ends.

        :rtype: list of lists
        :returns: logprob of each word in each sequence
        """

        result = []

        # A matrix of neural network logprobs of each word in each sequence.
        logprobs = self.score_function(word_ids, mask)
        # Add logprobs from class membership of each word in each sequence. We
        # don't compute any probability at the last time step.
        logprobs += numpy.log(membership_probs[:-1])
        for seq_index in range(logprobs.shape[1]):
            seq_logprobs = logprobs[:,seq_index]
            seq_mask = mask[1:,seq_index]
# XXX            seq_logprobs = [lp for lp, m in zip(seq_logprobs, seq_mask)
# XXX                            if m >= 0.5]
            seq_logprobs = seq_logprobs[seq_mask == 1]
            if numpy.isnan(sum(seq_logprobs)):
                raise NumberError("Sequence logprob has NaN value.")
            result.append(seq_logprobs)

        return result

    def compute_perplexity(self, batch_iter):
        """Computes the perplexity of text read using the given iterator.

        ``batch_iter`` is an iterator to the input data. On each call it creates
        a tuple of three 2-dimensional matrices, all indexed by time step and
        sequence. The first matrix contains the word IDs, the second one
        contains class membership probabilities, and the third one masks out
        elements past the sequence ends.

        :type batch_iter: BatchIterator
        :param batch_iter: an iterator that creates mini-batches from the input
                           data

        :rtype: float
        :returns: perplexity, i.e. exponent of negative log probability
                  normalized by the number of words
        """

        total_logprob = 0
        num_words = 0

        for word_ids, membership_probs, mask in batch_iter:
            logprobs = self.score_batch(word_ids, membership_probs, mask)
            for seq_logprobs in logprobs:
                total_logprob += sum(seq_logprobs)
                num_words += len(seq_logprobs)
        cross_entropy = -total_logprob / num_words
        return numpy.exp(cross_entropy)

    def score_sequence(self, word_ids, membership_probs):
        """Computes the log probability of a word sequence.

        :type word_ids: list of ints
        :param word_ids: list of word IDs

        :type membership_probs: list of floats
        :param membership_probs: list of class membership probabilities

        :rtype: float
        :returns: log probability of the sentence
        """

        # Create 2-dimensional matrices representing the transposes of the
        # vectors.
        word_ids = numpy.array([[x] for x in word_ids]).astype('int64')
        membership_probs = numpy.array([[x] for x in membership_probs]).astype(
            theano.config.floatX)
# XXX        mask = numpy.ones_like(membership_probs)
        mask = numpy.ones(word_ids.shape, numpy.int8)

        logprob = self.score_function(word_ids, mask).sum()
        # Add the logprob of class membership of each word.
        logprob += numpy.log(membership_probs[:-1]).sum()
        if numpy.isnan(logprob):
            raise NumberError("Sentence logprob has NaN value.")
        return logprob
