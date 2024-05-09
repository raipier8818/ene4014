class Table:
    # Table class for printing tables for dynamic length data
    
    # Set table information (name, columns, align right columns)
    def __init__(self, table_name:str, columns:list, align_right_col_idxs:list = []):
        self.table_name = table_name
        
        columns.insert(0, "")
        self.columns = columns
        self.align_right_col_idxs = align_right_col_idxs
        self.data = []
        self.index = 0
        self.max_lengths = []
        for i in range(len(columns)):
            self.max_lengths.append(len(columns[i]))
        
        
    def insert(self, values:list):
        values.insert(0, self.index)
        if len(values) != len(self.columns):
            raise Exception("Invalid number of values")
        
        # Update max lengths
        for i in range(len(values)):
            if len(str(values[i])) > self.max_lengths[i]:
                self.max_lengths[i] = len(str(values[i]))
        
        # Insert values
        self.data.append(values)
        self.index += 1
    
    def print_table(self):        
        # Print header line
        header_line = "+"
        for i in range(len(self.columns)):
            header_line += "-" * (self.max_lengths[i] + 2) + "+"
        print(header_line)
        
        # Print column names
        column_line = "|"
        for i in range(len(self.columns)):
            if self.align_right_col_idxs and i in self.align_right_col_idxs:
                column_line += " " * (self.max_lengths[i] - len(self.columns[i]) + 1) + self.columns[i] + " |"
            else:
                column_line += " " + self.columns[i] + " " * (self.max_lengths[i] - len(self.columns[i])) + " |"
        print(column_line)
        
        # Print header line
        print(header_line)
        
        # Print data
        for row in self.data:
            row_line = "|"
            for i in range(len(row)):
                if self.align_right_col_idxs and i in self.align_right_col_idxs:
                    row_line += " " * (self.max_lengths[i] - len(str(row[i])) + 1) + str(row[i]) + " |"
                else:
                    row_line += " " + str(row[i]) + " " * (self.max_lengths[i] - len(str(row[i]))) + " |"
            print(row_line)
        # Print header line
        print(header_line)
        