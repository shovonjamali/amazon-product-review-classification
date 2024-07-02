def add_to_excel(df, file_path, sheet_name='Sheet1'):
  wb = load_workbook(file_path)
  sheet = wb.active

  for data in df.values.tolist():
    sheet.append(data)

  wb.save(filename=file_path)
  wb.close()