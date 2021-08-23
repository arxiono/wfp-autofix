from airtable import Airtable
from decouple import config
import time

import json

'''
Misc: Paint the output with ASCI escape codes
'''
def paint(color_code):
    return f'\033[{color_code}m'

'''
Flip the booleans in here to turn the modules on or off
'''
fix_postcode = True
#fix_resourceName = False
fix_resourceAddress = True

def plus_code_validates(pluscode):
    return pluscode is not None and len(pluscode)>7 and '+' in pluscode[:10] and pluscode.count('+') == 1

'''
fetch base OS variables
'''
AIRTABLE_API_KEY = config('AIRTABLE_API_KEY', default='type key here') # e.g. "key7BGxXXXXXX"
BASE_ID = config('BASE_ID', default='type id here') # e.g.  "appznp4mtNe1LXXX"
TABLE_NAME = config('TABLE_NAME', default='tpye table name here')  # e.g. "Resources"
VIEW_NAME=config('VIEW_NAME', default='type view name here') # e.g. "Grid view"

'''
authenticate and fetch airtable
'''
airtable = Airtable(BASE_ID, TABLE_NAME, AIRTABLE_API_KEY)
get_all_from_table = airtable.get_all(view=VIEW_NAME)

'''
Switch class for state/WP check
'''
class stateswitch:

    def switch(self, state_wp_string):
        default = "Incorrect state name/punctuation!"
        return getattr(self, 'case_' + state_wp_string, lambda: default)()

    def case_KL(self):
        if postcode >= 50000 or postcode <= 60000:
            print("Kuala Lumpur postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Putrajaya(self):
        if postcode >= 62300 or postcode <= 62988:
            print("Putrajaya postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Labuan(self):
        if postcode >= 87000 or postcode <= 87033:
            print("Labuan postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Selangor(self):
        if postcode >= 40000 or postcode <= 48300:
            print("Selangor postcode " + postcode_string + ": Passed")
        elif postcode >= 63000 or postcode <= 68100:
            print("Selangor postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Terengganu(self):
        if postcode >= 20000 or postcode <= 24300:
            print("Terengganu postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Sarawak(self):
        if postcode >= 93000 or postcode <= 98859:
            print("Sarawak postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Sabah(self):
        if postcode >= 88000 or postcode <= 91309:
            print("Sabah postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Kedah(self):
        if postcode >= 5000 or postcode <= 9810:
            print("Kedah postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Kelantan(self):
        if postcode >= 15000 or postcode <= 18500:
            print("Kelantan postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_NS(self):
        if postcode >= 70000 or postcode <= 73509:
            print("Negeri Sembilan postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_PP(self):
        if postcode >= 10000 or postcode <= 144000:
            print("Pulau Pinang postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Johor(self):
        if postcode >= 79000 or postcode <= 86900:
            print("Johor postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Melaka(self):
        if postcode >= 75000 or postcode <= 78309:
            print("Melaka postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Perlis(self):
        if postcode >= 1000 or postcode <= 2000:
            print("Perlis postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Perak(self):
        if postcode >= 30000 or postcode <= 36810:
            print("Perak postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")

    def case_Pahang(self):
        if postcode >= 25000 or postcode <= 28800:
            print("Pahang postcode " + postcode_string + ": Passed")
        elif postcode >= 39000 or postcode <= 39200:
            print("Pahang (Cameron Highlands) postcode " + postcode_string + ": Passed")
        elif postcode == 49000:
            print("Pahang (Fraser's Hill) postcode " + postcode_string + ": Passed")
        elif postcode == 69000:
            print("Pahang (Genting Highlands) postcode " + postcode_string + ": Passed")
        else:
            print("Invalid postcode and state/WP pair!")


ss = stateswitch()

'''
Variables
'''
append_zero = "0"
append_flag = " [FLAGGED]"
append_emptAddrFlagA = "[EMPTY_ADDRESS]"
append_emptAddrFlagB = " [EMPTY_ADDRESS]"
append_emptPosFlag = "[EMPTY_POSTCODE]"
old_pstcode = ""
fixed_pstcode = ""
flagged_string = ""
sliced_string = ""
state_wp_string = ""
postcode = 0
count = 1
record_dict = {}

'''
loop over records in table
'''
for i,record in enumerate(get_all_from_table):
    record_id_string = record.get('id')
    resource_name = record.get('fields').get('Resource Name')
    freeform_address = record.get('fields').get('Freeform Address')
    postcode_raw = record.get('fields').get('Postcode')
    state_wp = record.get('fields').get('State/WP')
    print(paint('96') + "-------------------------------------------" + paint(0))
    print("ROW COUNT = " + str(count))
    print("[DEBUG] RECORD ID: " + record_id_string)
    print("[DEBUG] TABLE NAME: " + TABLE_NAME)
    if fix_resourceAddress == True:
        if freeform_address == None:
            print(paint('93') + "ROW>>" + str(count) + " [?] Resource have no address." + paint(0))
            freeform_address = append_emptAddrFlagA
            print(paint('92') + "NEW RESOURCE ADDRESS STRING: " + freeform_address + paint(0))
        elif freeform_address == 'N/A':
            print(paint('93') + "ROW>>" + str(count) + " [?] Resource have no address and reasoning for its absence. (string = " + freeform_address + ")" + paint(0))
            flagged_string = freeform_address + append_emptAddrFlagB
            freeform_address = flagged_string
            print(paint('92') + "NEW RESOURCE ADDRESS STRING: " + freeform_address + paint(0))
        elif freeform_address[0] == '?':
            if len(freeform_address) > 1:
                print(paint('93') + "ROW>>" + str(count) + " [?] Resource have no address but have reasoning for its absence. (string = " + freeform_address + ")" + paint(0))
            else:
                print(paint('93') + "ROW>>" + str(count) + " [?] Resource have no address and reasoning for its absence. (string = " + freeform_address + ")" + paint(0))
        else:
            print("RESOURCE ADDRESS: " + freeform_address)
            if freeform_address[-1] == ' ':
                print(paint('31') + "ROW>>" + str(count) + " [!] Illegal spacing detected at address: " + freeform_address + "." + paint(0))
                sliced_string = freeform_address[:-2] + freeform_address[-1:]
                freeform_address = sliced_string
                print(paint('34') + "ROW>>" + str(count) + " [#] " + paint(0) + paint('90') + "Eliminated residue space at the end of the address." + paint(0))
    if fix_postcode == True:
        if postcode_raw != None:
            postcode_string = str(postcode_raw)
            print("RESOURCE POSTCODE: " + postcode_string)
            if len(postcode_string) == 4:
                print(paint('35') + "Postcode 4 chars hit!" + paint(0))
                old_pstcode = postcode_string
                fixed_pstcode = append_zero + old_pstcode
                print(paint('31') + "ROW>>" + str(count) + " [!] Incorrect postcode {" + old_pstcode + "} detected, changed to {" + fixed_pstcode + "}." + paint(0))
                postcode_raw = fixed_pstcode
                print(paint('92') + "NEW POSTCODE STRING: " + postcode_raw + paint(0))
                '''
                compare the address after the fix
                '''
                state_wp_string = str(state_wp)
                print("STATE/WP NAME: " + state_wp_string)
                if state_wp_string != "None":
                    if state_wp_string == "Kuala Lumpur":
                        state_wp_string = "KL"
                        ss.switch(state_wp_string)
                    elif state_wp_string == "Negeri Sembilan":
                        state_wp_string = "NS"
                        ss.switch(state_wp_string)
                    elif state_wp_string == "Pulau Pinang":
                        state_wp_string = "PP"
                        ss.switch(state_wp_string)
                    else:
                        ss.switch(state_wp_string)
            if len(postcode_string) == 5:
                print(paint('32') + "Postcode 5 chars hit!" + paint(0))
                state_wp_string = str(state_wp)
                print("STATE/WP NAME: " + state_wp_string)
                if state_wp_string != "None":
                    if state_wp_string == "Kuala Lumpur":
                        state_wp_string = "KL"
                        ss.switch(state_wp_string)
                    elif state_wp_string == "Negeri Sembilan":
                        state_wp_string = "NS"
                        ss.switch(state_wp_string)
                    elif state_wp_string == "Pulau Pinang":
                        state_wp_string = "PP"
                        ss.switch(state_wp_string)
                    else:
                        ss.switch(state_wp_string)
        else:
            print(paint('93') + "ROW>>" + str(count) + " [?] Postcode is not stated." + paint(0))
            postcode_raw = append_emptPosFlag
            print(paint('92') + "NEW POSTCODE STRING: " + postcode_raw + paint(0))
    '''
    Update the fields within Airtable
    '''
    update_field = {
        'Freeform Address': freeform_address,
        'Postcode': postcode_raw
    }
    update_result = airtable.update(record_id_string, update_field)
    print("UPDATE: done!")
    count+=1
    time.sleep(0.3)

print(paint('96') + "-------------------------------------------" + paint(0))





