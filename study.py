from    bisect                  import  bisect_left
from    numpy                   import  mean, percentile, std
import  plotly.graph_objects    as      go
from    polars                  import  read_csv
from    random                  import  randint
from    sys                     import  argv


# python study.py 10000 50 2000


def run(days, returns, n_samples, equity):

    length  = len(days) - 1
    results = []

    for i in range(n_samples):

        remaining_days      = 256
        total_return        = 0
        remaining_equity    = equity
        
        while(True):

            k                   =  randint(0, length)
            remaining_days      -= days[k]
            total_return        += returns[k]
            remaining_equity    += returns[k] 

            if remaining_equity < 0 or remaining_days < 0:

                break

        results.append(total_return)
    
    return sorted(results)


if __name__ == "__main__":

    df          = read_csv("./out.csv")
    n_samples   = int(argv[1])
    equity      = int(argv[2])

    results = run(list(df["run_days"]), list(df["return"]), n_samples, equity)

    mu          = mean(results)
    sigma       = std(results)
    p_breakeven = bisect_left(results, 0) / len(results)
    p10         = percentile(results, 10)
    p20         = percentile(results, 20)
    p30         = percentile(results, 30)
    p40         = percentile(results, 40)
    p50         = percentile(results, 50)
    p60         = percentile(results, 60)
    p70         = percentile(results, 70)
    p80         = percentile(results, 80)
    p90         = percentile(results, 90)
    p95         = percentile(results, 95)
    p99         = percentile(results, 99)
    p100        = percentile(results, 100)

    print(f"mean:        {mu:0.2f}")
    print(f"stdev:       {sigma:0.2f}")
    print(f"p_breakeven: {p_breakeven:0.2f}")
    print(f"p_10:        {p10:0.2f}")
    print(f"p_20:        {p20:0.2f}")
    print(f"p_30:        {p30:0.2f}")
    print(f"p_40:        {p40:0.2f}")
    print(f"p_50:        {p50:0.2f}")
    print(f"p_60:        {p60:0.2f}")
    print(f"p_70:        {p70:0.2f}")
    print(f"p_80:        {p80:0.2f}")
    print(f"p_90:        {p90:0.2f}")
    print(f"p_95:        {p95:0.2f}")
    print(f"p_99:        {p99:0.2f}")
    print(f"p_100:       {p100:0.2f}")

    fig = go.Figure()

    fig.add_trace(go.Histogram(x = results, histnorm = "probability density", nbinsx = 100))
    fig.add_vline(x = 0, line_color = "red")

    fig.show()
