from argparse import ArgumentParser
import igesconverter


parser = ArgumentParser(description='Transform csv to iges.')
parser.add_argument('input', help='CSV file.')
parser.add_argument('-o', '--output', help='Output file name.', default='geometry.iges')
parser.add_argument('-p', '--plabel', help='Point label.')
parser.add_argument('-l', '--llabel', help='Line label.')
parser.add_argument('-s', '--splitter', help='Char used to separate values.')
parser.add_argument('--olavo', help='A set of parameters designed for Olavo.', default=False, const=True, nargs='?')

args = parser.parse_args()
kwargs = dict()

if args.olavo:
    kwargs['plabel'] = 'NODE'
    kwargs['llabel'] = 'BEAM'
    kwargs['splitter'] = ';'
    print('Seja bem vindo Dr. Olavo.')

if args.plabel:
    kwargs['plabel'] = args.plabel
if args.llabel:
    kwargs['llabel'] = args.llabel
if args.splitter:
    kwargs['splitter'] = args.splitter

try:
    iges = igesconverter.from_csv(args.input, **kwargs)
    iges.write_file(args.output)
except ValueError as e:
    print(e)