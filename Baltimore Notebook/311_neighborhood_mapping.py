"""
:param mapping empty dict to add to
:df is the 311 csv
:csa is the json object that maps CSA areas to smaller neighborhoods: 'Data/csa_to_neighborhood_map.json'

"""


def map_311_to_csa(mapping, df, csa):
    found = False
    for row_num, series in df.iterrows():
        neighborhood = series["Neighborhood"]
        for csa_area, sub_neighborhood_list in csa.items():
            for sub_neighborhood in sub_neighborhood_list:
                if sub_neighborhood.lower() in neighborhood.lower():
                    csa_match = csa_area
                    found = True
                    break
            if found == True:
                found = False
                try:
                    mapping[csa_match].append(int(row_num))
                except Exception as e:
                    mapping[csa_match] = [int(row_num)]

                break
