##############################################################################
#
# An example of inserting images into a worksheet using the XlsxWriter
# Python module.
#
# Copyright 2013-2018, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter


# Create an new Excel file and add a worktee180619715.jpegsheet.
workbook = xlsxwriter.Workbook('images.xlsx')
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 30)

# Insert an image.
worksheet.write('A2', 'Insert an image in a cell:')
worksheet.insert_image('B2', 'tee180619715.jpeg')

# Insert an image offset in the cell.
worksheet.write('A12', 'Insert an image with an offset:')
worksheet.insert_image('B12', 'tee180619715.jpeg', {'x_offset': 15, 'y_offset': 10})

# Insert an image with scaling.
worksheet.write('A23', 'Insert a scaled image:')
worksheet.insert_image('B23', 'tee180619715.jpeg', {'x_scale': 0.5, 'y_scale': 0.5})

workbook.close()