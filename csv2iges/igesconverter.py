from pathlib import Path


class IgesFile:
    def __init__(self, points, lines, name='geometry'):
        self.points = points
        self.lines = lines
        self.name = name
    
    def write_file(self, path=''):
        p = Path(path)
        if p.name:
            self.name = p.stem 
        p = p.parent / (self.name + '.iges')            

        iges = self._generate()
        with open(p, 'w') as file:
            file.write(iges)

    def _generate(self):
        s = self._generate_start()
        g = self._generate_global()
        d = self._generate_data()
        p = self._generate_params()
        t = self._generate_termination()
        return ''.join([s,g,d,p,t])

    def _generate_start(self):
        return '                                                                        S      1\n'

    def _generate_global(self):
        return ('1H,,1H;,,12Hcsv2igesfile.iges,                                          G      1\n' +
                '5HANSYS,22H  19.4      UP20190416,,,,,,,1.0,6,,,,13H000203.140632,      G      2\n' +
                '1.0000E-04,,,,9,,;                                                      G      3\n' )
            
    def _generate_data(self):
        data = ''
        dindex = 1 
        pindex = 1

        for line in self.lines:
            param_str = self._fit(str(pindex), 8)
            data_str1  = self._fit(str(dindex), 7)
            data_str2  = self._fit(str(dindex+1), 7)

            data += f'     110{param_str}       0       1       0       0       0       0       1D{data_str1}\n'
            data += f'     110       1       0       1       0                               0D{data_str2}\n'
            
            dindex += 2
            pindex += 1 

        return data 
            
    def _generate_params(self):
        params = '' 
        index = 1 

        for line in self.lines.values():
            first_point = [float(i) for i in self.points[line[0]]]
            last_point  = [float(i) for i in self.points[line[1]]]
            
            text = '110, {}, {}, {}, {}, {}, {}, 0, 0;'.format(*first_point, *last_point)
            params += f'{self._fit(text, 63, align_left=True)} {self._fit(str(index), 8)}P{self._fit(str(index), 7)}\n'
            index += 2

        return params

    def _generate_termination(self):
        return 'S      1G      4D     12P      6                                        T      1\n'

    def _fit(self, text, padding, align_left=False):
        spaces = ' ' * (padding - len(text))

        if align_left:
            return text + spaces 
        else:
            return spaces + text
    

def load_csv(filename, plabel='points', llabel='lines'):
    points = dict()
    lines = dict()

    with open(filename, 'r') as file:
        for line in file.readlines():
            fields = line.split(';')

            if fields[1] == plabel:
                id_ = int(fields[0])
                x, y, z = map(float, fields[2:])
                points[id_] = (x,y,z)

            elif fields[1] == llabel:
                id_ = int(fields[0])
                start, end = map(int, fields[2:])
                lines[id_] = (start, end)
            
            else:
                raise ValueError('This file have unexpected inputs.')

    return points, lines


def from_csv(filename, **kwargs):
    points, lines = load_csv(filename, **kwargs)
    return IgesFile(points, lines)

