def get_title_graph(f):
    filename = f.split("\\")
    i = 0
    while i < (len(filename) - 1):
        del filename[i]

    name_csv = filename[0]
    name_csv = name_csv.split(".")
    del name_csv[-1]
    name = name_csv[0]
    name = name.split("-")

    # patient cart / start date string
    patientcart_startdate = name[1]
    patientcart_startdate = patientcart_startdate.split("_")
    del patientcart_startdate[-1]

    # endate string
    enddate = name[-1]
    enddate = enddate.split("_")
    del enddate[-1]

    # string
    number_serie = name[0]
    patient_cart = patientcart_startdate[0]
    start_date = patientcart_startdate[-1]

    # convert date in nice
    start_date = start_date[:4] + " " + start_date[4:]
    start_date = start_date[:7] + "/" + start_date[7:]


    title = " Serial number: " + number_serie + " Patient cart no: " + patient_cart + " Date: " + start_date

    return title


get_title_graph(r'C:\Users\arthur.herbette\Box\Arthur\csv\DX11247-1_20230725_152651-20230725_154306.csv')
