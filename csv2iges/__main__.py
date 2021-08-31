from argparse import ArgumentParser
import igesconverter


parser = ArgumentParser(description='Transform csv to iges.')
parser.add_argument('input', help='CSV file.')
parser.add_argument('-o', '--output', help='IGES file name.', default='geometry.iges')

args = parser.parse_args()
iges = igesconverter.from_csv(args.input, plabel='NODE', llabel='BEAM')
iges.write_file(args.output)
