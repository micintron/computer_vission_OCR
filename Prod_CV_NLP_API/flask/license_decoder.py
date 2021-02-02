""" Net steps work : build code to fully decode a barcode on the back of a drivers licence 
    from the image 
    
"""
def decode_license(rawstring):
    decoded = {}
    dlstringarray = rawstring.split('\n')
    dlstringarray = dlstringarray[2:]
    dlstringarray = [line.strip() for line in dlstringarray]

    # remove 'ANSI' from first element (It's a fixed header)
    dlstringarray[0] = dlstringarray[0][5:]

    metadata = dlstringarray[0]

    dlstringarray.remove(metadata)

    IIN = metadata[0:6]  # Issuer Identification Number
    AAMVAV = metadata[6:8]  # AAMVA Version number
    JV = metadata[8:10]  # Jurisdiction Version number
    entries = metadata[10:12]  # Number of entries

    DL = metadata[12:14]

    offset = metadata[14:18]  # offset for this subfile
    subfile_length = metadata[18:22]

    DCA = metadata[27:]  # Jurisdiction specific vehicle class

    decoded['Issuer_Identification_Number'] = IIN
    decoded['AAMVA_Version_Number'] =  AAMVAV
    decoded['Jurisdiction_Version_Number'] =  JV
    decoded['Number_of_entries'] =  entries
    decoded['Type'] =  DL
    decoded['Offset_for_subfile'] =  offset
    decoded['Subfile_length'] = subfile_length
    decoded['Jurisdiction_specific_vehicle_class'] =  DCA

    print(dlstringarray)

    for field in dlstringarray:

        fieldID = field[0:3]
        fieldValue = field[3:]
        fieldValue = fieldValue.strip()
        fieldName = ''

        if fieldID == 'DCB':
            fieldName = 'jurisdiction_restriction_codes'
        elif fieldID == 'DCD':
            fieldName = 'jurisdiction_endorsement_codes'
        elif fieldID == 'DBA':
            fieldName = 'expiration_date'
        elif fieldID == 'DCS':
            fieldName = 'first_name'
        elif fieldID == 'DCT':
            fieldName = 'last_name'
        elif fieldID == 'DBD':
            fieldName = 'issue_date'
        elif fieldID == 'DBB':
            fieldName = 'birthdate'
        elif fieldID == 'DBC':
            fieldName = 'sex'  # 1 for male, 2 for female
        elif fieldID == 'DAY':
            fieldName = 'eye_color'
        elif fieldID == 'DAU':
            fieldName = 'height'
        elif fieldID == 'DAG':
            fieldName = 'address_line_1'
        elif fieldID == 'DAI':
            fieldName = 'city'
        elif fieldID == 'DAJ':
            fieldName = 'state'
        elif fieldID == 'DAK':
            fieldName = 'postal_code'
        elif fieldID == 'DAQ':
            fieldName = 'customer_id_number'
        elif fieldID == 'DCF':
            fieldName = 'document_discriminator'
        elif fieldID == 'DCG':
            fieldName = 'country_identification'
        elif fieldID == 'DCK':
            fieldName = 'inventory_control_number'

        if len(fieldName) > 0 and len(fieldValue) > 0:
            decoded[fieldName] = fieldValue
    
    return decoded