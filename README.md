# Running the Simulation

run command:

`python prop_2.py '{ "risk": "$400", "reward": "$25.49", "leverage": 1.0, "performance_post_costs": 1, "runs": 10000, "discretionary_buffer": 0, "trades_per_day": 5, "withdrawal_frequency_days": 0, "withdrawal_amount_dollars": 811, "run_years": 1, "eval": 1, "max_resets": 2, "show_dists": 0, "show_runs": 0, "mode": "tradeday_50k" }'`

Parameters:

- `risk`: The standard deviation of returns (see next section).
- `reward`: The mean return (see next section).
- `leverage`: Effectively, the number of mini contracts traded. `1.0` = 1 contract, `2.0` = 2 contracts, `0.1` = 1 micro. Values less than 1 will cause the program to use micro commissions and spreads for calculating transaction costs. Values such as 2.1 will not work correctly -- do not mix micros and minis.
- `performance_post_costs`: `1` means transaction costs are included in the risk and reward values, and will be added to equity values to compute total returns. `0` means they are not, and will be subtracted from equity values to compute total returns and simulate equity curves.
- `runs`: the number of accounts to simulate.
- `discretionary_buffer`: if the account equity is below this value (in dollars), no withdrawals will be made.
- `trades_per_day`: the number of trades per day; used to calculate transaction costs.
- `withdrawal_frequency_days`: if `0`, no withdrawals will be made. any other number signifies the amount of days between each withdrawal (e.g. `21` = 1 month).
- `withdrawal_amount_dollars`: the dollar amount of each withdrawal.
- `run_years`: the number of years for each run (each year is 256 trading days).
- `eval`: `1` if you want to include eval simulations and add eval costs to prop fees, `0` otherwise. personal accounts are unaffected by this setting.
- `max_resets`: the maximum number of reset fees to use when simulating evals.
- `show_dists`: `1` to show statistics in histogram form.
- `show_runs`: show a plot of the equity curve for each run (not recommended for if running more than e.g. 1000 runs).
- `mode`: sets the account rules (see next section). the available options are:

    - `personal_2k`: a personal account with $2000 in starting equity.
    - `tradeday_50k`: a tradeday 50k live account.
    - `apex_full_rithmic_50k`: a rithmic apex 50k account.
    - `topstep_live_50k`: a topstep 50k account

# Further Explanation of Some Parameters

The `risk` and `reward` parameters will be converted to log returns, relative to an ES contract valued at 5000 points (this can be changd in `prop_2.py`). These return values will then set the mean and standard deviation of a normal distribution, which will be sampled to generate the simulated equity curves. There are several modes of input:

    - basis points: e.g. `0.0004` means a 4 basis point risk or return
    - dollars: `$500` means a risk or reward value of $500.
    - ES multiplier: `1x` or `0.5x` means one or 1/2 times the risk or reward of ES. 
    - Binomial: `0.6:2` means 60% chance of two points. `0.51:1` means 51% chance of 1 point, and so on. This can be used for risk and reward alike. The point value should be positive, even for the risk parameter. For example reward = `0.6:2`, risk = `0.4:2` means a 60% win rate, 1:1 RR with R = 2 ES points.

The `mode` parameter serves as an index to a dictionary of values. This dictionary sits at the top of `prop_2.py`. You can edit these values as you see fit, e.g. to create a personal account with a different drawdown, or to change the profit sharing rate, to change the eval fees, and so on. For the existing profiles, any potentially-material rules that I am aware of, and that have been ignored, are noted in the comments.