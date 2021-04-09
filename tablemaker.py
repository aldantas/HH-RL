from tabulate import tabulate


class TableMaker(object):
    def __init__(self, filepath, header, bg_color='gray!30'):
        self.latex_file = open(filepath, 'w', newline='')
        self.header = header
        self.bg_color = bg_color
        self.table = []

    def writerow(self, values, bold_mask=None, bg_mask=None):
        if bold_mask is None:
            bold_mask = [False] * len(values)
        if bg_mask is None:
            bg_mask = [False] * len(values)
        row = []
        for value, is_bold, is_bg in zip(values, bold_mask, bg_mask):
            cell_str = value
            if is_bold:
                cell_str = '\\textbf{'+cell_str+'}'
            if is_bg:
                cell_str = '\\cellcolor{'+self.bg_color+'}{'+cell_str+'}'
            row.append(cell_str)
        self.table.append(row)

    def save(self, caption):
        # table_fmt = 'latex_raw' if self.colored else 'latex'
        table_fmt = 'latex_raw'
        tabular = tabulate(self.table, headers=self.header, tablefmt=table_fmt)
        self.latex_file.write('\\begin{table}\n')
        self.latex_file.write('\\centering\n')
        self.latex_file.write('\\caption{'+caption+'}\n')
        self.latex_file.write(tabular)
        self.latex_file.write('\\end{table}')
        self.latex_file.close()
