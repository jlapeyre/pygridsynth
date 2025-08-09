import argparse
import mpmath

from .gridsynth import gridsynth_gates, tally_stats

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('theta', type=str)
    parser.add_argument('epsilon', type=str)
    parser.add_argument('--dps', type=int, default=128)
    parser.add_argument('--dtimeout', '-dt', type=int, default=200)
    parser.add_argument('--ftimeout', '-ft', type=int, default=50)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--time', '-t', action='store_true')
    parser.add_argument('--showtimeouts', '-to', action='store_true')
    parser.add_argument('--showgraph', '-g', action='store_true')

    args = parser.parse_args()
    mpmath.mp.dps = args.dps
    mpmath.mp.pretty = True
    theta = mpmath.mpmathify(args.theta)
    epsilon = mpmath.mpmathify(args.epsilon)

    factor_stats = {
        "ints_that_timedout" : [],
        "diophantine_timedout": [],
    }
    gates = gridsynth_gates(theta=theta, epsilon=epsilon,
                            factoring_timeout=args.ftimeout,
                            diophantine_timeout=args.dtimeout,
                            verbose=args.verbose, measure_time=args.time,
                            show_graph=args.showgraph, factor_stats=factor_stats)
    print(gates)
    if args.showtimeouts:
        print()
        tallied = tally_stats(factor_stats)
        print("Integers timed out factoring:")
        print(tallied["ints_that_timedout"])
        print()
        print("Integers at diophantine timeout:")
        print(factor_stats["diophantine_timedout"])
    return gates


if __name__ == "__main__":
    main()
