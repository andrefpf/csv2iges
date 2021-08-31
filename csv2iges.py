import numpy as np 


def fit(text, spaces, align_left=False):
    spacer = ' ' * (spaces - len(text))

    if align_left:
        return text + spacer 
    else:
        return spacer + text

def create_header(filename):
    header =  '                                                                        S      1\n'
    header += f'1H,,1H;,,12Hcsv2igesfile.iges,                                         G      1\n'
    header += '5HANSYS,22H  19.4      UP20190416,,,,,,,1.0,6,,,,13H000203.140632,      G      2\n'
    header += '1.0000E-04,,,,9,,;                                                      G      3\n'

    return header

def create_data(points, lines):
    data = ''
    
    dindex = 1 
    pindex = 1

    for line in lines:
        param_str = fit(str(pindex), 8)
        data_str1  = fit(str(dindex), 7)
        data_str2  = fit(str(dindex+1), 7)

        data += f'     110{param_str}       0       1       0       0       0       0       1D{data_str1}\n'
        data += f'     110       1       0       1       0                               0D{data_str2}\n'
        
        dindex += 2
        pindex += 1 
    
    return data 

def create_params(points, lines):
    params = '' 

    index = 1 

    for line in lines.values():
        first_point = [float(i) for i in points[line[0]]]
        last_point = [float(i) for i in points[line[1]]]
        
        text = '110, {}, {}, {}, {}, {}, {}, 0, 0;'.format(*first_point, *last_point)
        params += f'{fit(text, 63, align_left=True)} {fit(str(index), 8)}P{fit(str(index), 7)}\n'
        index += 2

    return params

def create_termination():
    return 'S      1G      4D     12P      6                                        T      1\n'

def create_iges(points, lines, filename='geometry.iges'):
    header = create_header(filename)
    data   = create_data(points, lines)
    params = create_params(points, lines)
    end    = create_termination()
    return ''.join([header, data, params, end])


def load_data(filename):
    points = dict()
    lines = dict()

    with open(filename, 'r') as file:
        for line in file.readlines():
            fields = line.split(';')

            if fields[1] == 'NODE':
                id_ = int(fields[0])
                x, y, z = map(float, fields[2:])
                points[id_] = (x,y,z)

            elif fields[1] == 'BEAM':
                id_ = int(fields[0])
                start, end = map(int, fields[2:])
                lines[id_] = (start, end)
            
            else:
                raise ValueError('This file have unexpected inputs.')

    return points, lines


def transform_file(filename, output='geometry.iges'):
    points, lines = load_data(filename)
    data = create_iges(points, lines, output)

    with open(output, 'w') as file:
        file.write(data)


from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description='Transform csv to iges.')
    parser.add_argument('input', help='CSV file.')
    parser.add_argument('-o', '--output', help='IGES file name.', default='geometry.iges')

    args = parser.parse_args()
    transform_file(args.input, args.output)

