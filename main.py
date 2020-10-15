import argparse
from contracheque import Contracheque


def min_year(y):
    try:
        y = int(y)
    except ValueError:
        raise argparse.ArgumentTypeError('Year must be int')
    if y < 2015:
        raise argparse.ArgumentTypeError("No data before 2015")
    return y


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Coletor de dados de contracheque do MPF'
    )
    parser.add_argument(
        '-m',
        '--month',
        type=int,
        help='Month you want to consult',
        required=True,
        choices=range(1, 13),
        dest='month'
    )

    parser.add_argument(
        '-y',
        '--year',
        type=min_year,
        help='Year you want to consult',
        required=True,
        dest='year',
    )

    parser.add_argument(
        '-d',
        '--dir',
        type=str,
        help='CSV Output directory. Default: .',
        default='.',
        dest='dir_output'
    )

    args = parser.parse_args()
    cc = Contracheque(args.month, args.year)
    if (args.year > 2019):
        cc.write_new_to_csv(args.dir_output)
    elif (args.year < 2019):
        cc.write_old_to_csv(args.dir_output)
    else:
        if(args.month < 7):
            cc.write_old_to_csv(args.dir_output)
        else:
            cc.write_new_to_csv(args.dir_output)
