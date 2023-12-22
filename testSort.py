from csvsort import csvsort
# sort this CSV on the 5th and 3rd columns (columns are 0 indexed)
csvsort('saved_db_1m.csv', [1], output_filename='saved_db_1m_sorted.csv' , has_header=False)


# # sort this CSV with no header on 4th column and save results to separate file
# csvsort('test2.csv', [3], output_filename='test3.csv', has_header=False)
# # sort this TSV on the first column and use a maximum of 10MB per split
# csvsort('test3.tsv', [0], max_size=10, delimiter='\t')
# # sort this CSV on the first column and force quotes around every field (default is csv.QUOTE_MINIMAL)
# import csv
# csvsort('test4.csv', [0], quoting=csv.QUOTE_ALL)