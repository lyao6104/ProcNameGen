# ProcNameGen

This is a tool that procedurally generates names. It went through a few iterations before I finally settled on using a Markov chain, so the implementation is _kind of messy_, to say the least.
Nevertheless, it does seem to work reasonably well from what I've seen.

## Features

The tool allows you to scan a list of names to create a language from the given data. Up to third-order Markov chains are allowed.

You are also able to train languages to achieve a better probability distribution. The program will generate a name, and allow you to choose whether or not it is good. Marking a name as good will slightly increase the probability of those particular segments being chosen, and vice versa.
Additionally, an average length of "good" names for each language is tracked, and the tool uses this average length to help it determine when to stop picking segments for a name (note that it will never stop a name before the minimum segment count is reached, nor will it keep going after the maximum).

Once you have a language you're satisfied with, you can also choose to generate names only. You are able to select how many names are generated in each batch.

## Usage

This tool requires `pipenv` and `make`.

To scan names, use the `make scan` rule. To train a language, use `make train`.
To only generate names, use `make run`.
