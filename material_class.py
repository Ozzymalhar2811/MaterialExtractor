import math
import requests
from bs4 import BeautifulSoup
#import re
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

URL = 'http://www.matweb.com/Search/MaterialGroupSearch.aspx?GroupID=236'

class ParamMats():
    def __init__(self, debug=False):
        self.debug = debug
        pass

    #The below function goes to the URL mentioned in line 11
    # and then converts the html webpage into string. 
    #then, the a list of all the rows is created
    #then from each row, a link to the subpage of the specific material is found and stored as a list

    def get_material_sheet_links(self):
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        material_table = soup.find('table', class_="tabledataformat t_ablegrid")
        rows = material_table.find_all('tr', class_='altrow')

        links = []
        for row in rows:
            for a in row.find_all('a', href=True):
                if a.text:
                    links.append(a['href'])

        return links
    #------------------------------------------------------------------------------------------------------------------------------#
    # This function is used to:
    # Take out material title from top of page
    # Take o ut entire data from all the rows of the page. 
    # The rows contain different properties and their values, store them in a list

    def get_params_for_materials(self, materilas_urls_list):
        base = "http://www.matweb.com"
        materials_with_metric_list = []
        for material_url in materilas_urls_list:
            m_url = base + material_url
            response = requests.get(m_url, headers=headers)
            msoup = BeautifulSoup(response.text, 'html.parser')
            title = msoup.find('title').text.strip()
            print(f" Fetching {title}")
            material_dict = {'Material': title}

            rows = msoup.find_all('tr', class_='altrow datarowSeparator')
            rows.extend(msoup.find_all('tr', class_='datarowSeparator'))
            metrics = []
            for row in rows:
                row_elems = []
                for count, tag in enumerate(row):
                    if count > 1:
                        continue
                    anc = tag.find('a')
                    if anc:
                        row_elems.append(anc.text.strip())
                    else:
                        row_elems.append(tag.text.strip())
                metrics.append(row_elems)


            metric_dict = {k: v for k, v in metrics}
            material_dict.update(metric_dict)
            materials_with_metric_list.append(material_dict)
        return materials_with_metric_list

    #------------------------------------------------------------------------------------------------------------------------------#

    # The below functions Cleans the data to keep only required nums
    # If sepc dat != ,a constant data is assume
    # Calculate n here itself so no need to read data again
    #Where n is the Ramberg-Osgood Coeffecient. 
    #A dictionary is created to store the property and its value
     
    def cleanup_data_and_find_n(self, data_frame):

        cleaned_up_data = []

        for index, row in data_frame.iterrows():
            print(f"Extracting data and Calculating n for {row['Material']}")
            e_max = self.clean_up_elongation_at_break(row['Elongation at Break'])
            e_max = e_max if not math.isnan(e_max) else 15.0

            S_ut = row['Tensile Strength, Ultimate']
            S_ut = float(S_ut) if not math.isnan(float(S_ut)) else None

            E = row['Modulus of Elasticity']
            E = float(E) if not math.isnan(float(E)) else 210.0

            S_y = row['Tensile Strength, Yield']
            S_y = float(S_y) if not math.isnan(float(S_y)) else None

            if not S_y or not S_ut:
                continue

            e_us = 100 * ((e_max/100) - (S_ut/(E * 1000)))
            n = (math.log(e_us/0.2)) / math.log(S_ut/S_y)

            cleaned_data = {
                'elongation_at_break': e_max,
                'tensile_strength_ultimate': S_ut,
                'tensile_strength_yield': S_y,
                'modulus_of_elasticity': E,
                'material': row['Material'],
                'n': n
            }
            cleaned_up_data.append(cleaned_data)

        return cleaned_up_data
    #------------------------------------------------------------------------------------------------------------------------------#

    #Call the needed values from the dictionary
    #To calculate the stresses at assumed points, and the respective strains,
    #Create an iterable object
    #Iterate through stresses in col a and strains on col b

    def calculate_arrays(self, data_dict):
        S_y = data_dict['tensile_strength_yield']
        S_ut = data_dict['tensile_strength_ultimate']
        n = data_dict['n']
        E = data_dict['modulus_of_elasticity']

        # Data for trial
        # E = 207.0
        # S_ut = 850.0
        # S_y = 750.0
        # e_max = 10.0
        # n = 30.9203909469753???

        a_result = []

        for index in range(1, 20):
            last_ele = a_result[-1] if len(a_result) > 0 else None
            if index == 1:
                a_result.append(0)
            elif index == 2:
                a_result.append(S_y/5)
            elif index in {3, 4, 5}:
                a_result.append(last_ele + (S_y/5))
            elif index in {6, 7, 8}:
                a_result.append(last_ele + (S_y * 0.05))
            elif index == 9:
                a_result.append(S_y)
            elif index in {10, 11, 12, 13, 14, 15, 16, 17, 18, 19}:
                a_result.append(last_ele + ((S_ut - S_y)*0.1))
            else:
                print("Something Wrong")

        b_result = []

        for index, a_val in enumerate(a_result):
            if index == 0:
                b_result.append(a_val)
            else:
                b_val = (a_val/(E * 1000)) + 0.002 * pow((a_val/S_y), n)
                b_result.append(b_val)

        result = zip(b_result, a_result)

        return list(result)
    #------------------------------------------------------------------------------------------------------------------------------#

    #Cleanup the name of the material to remove spaces
    #Create a csv file of the cleaned name containg only the array

    def create_csv_from_data(self, data_dicts_list):
        for material_dict in data_dicts_list:
            matrial_name = material_dict['material']
            printable_material_name = "".join(
                char for char in matrial_name if char.isalnum() or char == " ")
            printable_material_name = printable_material_name.replace(" ", "_")
            zipped_list = self.calculate_arrays(material_dict)
            df = pd.DataFrame(zipped_list)
            df.to_csv(f"{printable_material_name}.csv", header=False, index=False)

    #------------------------------------------------------------------------------------------------------------------------------#

    # In case the elongation at break is given as a range
    # Extract both the numbers (min and max) and take the max

    def clean_up_elongation_at_break(self, string_val):

        if type(string_val) is str:
            # clean_string = re.sub('\W+', '', string_val)
            num_list = []
            for s in string_val.split():
                try:
                    num_list.append(float(s))
                except ValueError:
                    pass

            return max(num_list)
        else:
            return string_val

    #------------------------------------------------------------------------------------------------------------------------------#
    def create_material_curve_csvs(self):
        links = self.get_material_sheet_links()
        materials_list = self.get_params_for_materials(links)
        materials_df = pd.DataFrame(materials_list)
        cleaned_data = self.cleanup_data_and_find_n(materials_df)
        self.create_csv_from_data(cleaned_data)
        