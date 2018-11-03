

class topTenFinder:

    def __init__(self, file, lookup, category, out_file):
        # input file
        self.file = file

        # lookup table for finding the index of the catetory
        # for example {'occupations':'SOC_NAME'}
        self.lookup = lookup

        # the category, for example occupations
        self.category = category

        self.counter = {}

        # to count total number of certified H1B user
        self.total = 0

        # output file
        self.out_file = out_file

        # to store the top 10 names,
        # for exmaple ["SOFTWARE DEVELOPERS, APPLICATIONS", "ACCOUNTANTS AND AUDITORS"]
        self.top_ten_keys = []

    def open_file_load(self):
        with open(self.file) as f:
            try:
                header = f.readline().strip().split(';')
            except:
                raise ValueError('A header line is needed')

            # find the index of certified info (CASE_STATUS)
            # and the index of the category (e.g. SOC_NAME)
            index = -1
            index_certi = -1
            for i, category in enumerate(header):
                if category.lower() == self.lookup[self.category].lower():
                    index = i
                elif category.lower() == 'CASE_STATUS'.lower():
                    index_certi = i

            # if the index is -1 (not found), raise error
            if index_certi == -1:
                raise ValueError('CERTIFIED not found')
            elif index == -1:
                raise ValueError('{} not found'.format(self.lookup[self.category].upper()))

            # put values into self.counter
            line = f.readline()
            while line:
                line = line.strip().split(';')
                if line[index_certi].lower() == 'certified'.lower():
                    key = line[index].strip('"')
                    self.counter[key] = self.counter.get(key, 0) + 1
                    self.total += 1
                line = f.readline()

    # sort the counters so that self.top_ten_keys is filled by desired values
    def sort_reverse(self):
        self.top_ten_keys = sorted(
            self.counter.keys(),
            key=lambda x:(-self.counter[x], x)
        )[:(max(10, len(self.counter)))]

    def write_file(self):
        with open(self.out_file, 'w') as f:
            f.write(
                'TOP_{};NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'.format(
                    self.category.upper()
                )
            )
            for key in self.top_ten_keys:
                f.write(
                    '{};{};{}%\n'.format(
                        key, self.counter[key], round((self.counter[key]*100)/self.total, 1)
                    )
                )

    def process(self):
        self.open_file_load()
        self.sort_reverse()
        self.write_file()


if __name__ == '__main__':
    import sys
    file = sys.argv[1]
    out_file1 = sys.argv[2]
    out_file2 = sys.argv[3]
    lookup = {'occupations':'SOC_NAME', 'states': 'WORKSITE_STATE'}

    top_ten_finder = topTenFinder(file, lookup, 'occupations', out_file1)
    top_ten_finder.process()

    top_ten_finder2 = topTenFinder(file, lookup, 'states', out_file2)
    top_ten_finder2.process()
