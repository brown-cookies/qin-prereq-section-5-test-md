Out of all the programs, this is by far the easiest, I just kinda compute the expected output using
calculator and write it down and use `assert a == b`, for exact arithmetic calculation. Separate situations
like in `billable_units` to test calculation when packaging is either `crated` or `loose`. I had a mistake here
in `test_total_pence_with_discount_applied` where i initially asserted `assert result == 200.69` forgetting that
the currency used is `pence` which is why there's a function that convert `pence` to `pounds`.