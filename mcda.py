import argparse as ap
from interface.definitions import MCDAProblem
from topsis.topsis import topsis # xD
from electre.electre_is import electre_is


def main():
    electre_root = 'input_files/electre_test_input/%s.csv'
    topsis_path = 'input_files/topsis_test_input/%s.csv'

    parser = ap.ArgumentParser(description='Electre IS and Topsis Interface')
    parser.add_argument('-m', '--method', type=str, help='Metoda do uruchomiena {electre_is,topsis}',
                        default='electre_is', action='store', choices=['electre_is', 'topsis'], dest='method')
    parser.add_argument('-alt', '--alternatives', type=str, help='Sciezka do pliku csv z macierza rankingu',
                        default=electre_root % 'testAlternatives', action='store', dest='perfTable')
    parser.add_argument('-w', '--weights', type=str, help='Sciezka do pliku csv z wagami kryteriow',
                        default=electre_root % 'weights', action='store', dest='weights')
    parser.add_argument('-v', '--vetos', type=str, help='Sciezka do pliku csv z progami weta dla kryteriow',
                        default=electre_root % 'vetos', action='store', dest='vetos')
    parser.add_argument('-p', '--preference', help='Sciezka do pliku csv z progami preferencji dla kryteriow',
                        default=electre_root % 'preference', action='store', dest='pref')
    parser.add_argument('-i', '--indifference', help='Sciezka do pliku csv z progami nierozroznialnosci dla kryteriow',
                        default=electre_root % 'indifference', action='store', dest='indif')
    parser.add_argument('-d', '--directions', help='Sciezka do pliku csv z kierunkami optymalizacji kryteriow',
                        default=topsis_path % 'directions', action='store', dest='dirs')
    parser.add_argument('-sep', '--separator', help='Separator w plikach csv',
                        default=',', action='store', dest='delimiter')

    args = parser.parse_args()

    problem = MCDAProblem()
    problem.read_performance_table(args.perfTable, delimiter=args.delimiter)
    problem.read_criteria_weights(args.weights, delimiter=args.delimiter)

    switch = {
        'topsis': topsis_flow,
        'electre_is': electre_is_flow
    }

    switch[args.method](problem, args)


def topsis_flow(problem, args):
    problem.read_criteria_directions(args.dirs, delimiter=args.delimiter)

    ret = topsis(problem)
    print('Best alternative is: %s' % ret.name)


def electre_is_flow(problem, args):
    problem.read_veto_thresholds(args.vetos, delimiter=args.delimiter)
    problem.read_preference(args.pref, delimiter=args.delimiter)
    problem.read_indifference(args.indif, delimiter=args.delimiter)

    best_alternatives, graph = electre_is(problem)

    if len(best_alternatives):
        print('Najlepsze alternatywy')
        print(', '.join(alt.name for alt in best_alternatives))
    else:
        print('Dla zadanych parametrow brak rozwiazan')
        print('struktura grafu (indeksowana od zera):')
        print(graph)


if __name__ == '__main__':
    main()
