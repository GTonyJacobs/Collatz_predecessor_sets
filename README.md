# Collatz predecessor sets

This is a repository for some code relating to a project where I'm investigating predecessor sets under the Syracuse version of the Collatz map. See https://www.reddit.com/r/Collatz/comments/1j0o70j/densities_of_predecessor_sets_revisited/ for details.

There are three files here, in the /scripts/ folder:

* count_preds_by_ratio.py is the program that verifies the formula P(m,k)
* preds_of_N_under_CN_theoretical.py is the program that implements the P(m,k) formula to predict how many preds of N you expect to see under CN.
* preds_of_N_under_CN_empirical.py is the program that attempts to verify the predictions of the previous program.
