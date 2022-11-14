import re
import ast
import requests
import numpy as np
import pandas as pd
import concurrent.futures as cf

from tqdm.notebook import tqdm
from itertools import repeat
from unidecode import unidecode as udc


def get_location_with_here_api(api_key, query):
    """Function in charge of making the request to the HERE API
    (https://developer.here.com/develop/rest-apis). It autocompletes
    the address, as well as separate the country, state and or city.

    Args:
        api_key (str): Credential for the API
        query (str): User location pre-processed

    Returns:
        list: A list with the normalized data
    """

    # Variables for making the request
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    query = re.sub(r"\s", "+", udc(query.lower()))

    PARAMS = {'apikey': api_key,
              'q': query,
              'lang': 'es-MX'}

    # Get request
    req_response = requests.get(url=URL, params=PARAMS)
    resp_data = req_response.json()

    try:
        result_dict = resp_data['items'][0]

        country_code = result_dict['address'].get('countryCode')
        country_name = result_dict['address'].get('countryName')
        state_name = result_dict['address'].get('state')
        state_code = result_dict['address'].get('stateCode')
        county_name = result_dict['address'].get('county')
        city = result_dict['address'].get('city')
        district = result_dict['address'].get('district')

        postal_code = result_dict['address'].get('postalCode')

        latitude = result_dict['position'].get('lat')
        longitude = result_dict['position'].get('lng')

        query_score = result_dict['scoring'].get('queryScore')
        field_score = result_dict['scoring'].get('fieldScore')

        return [country_code, country_name,
                state_name, state_code, county_name,
                city, district, postal_code,
                latitude, longitude,
                query_score, str(field_score)]

    except IndexError as ie:
        pass

    except Exception as e:
        print(e)

    return None


def clean_rows(row):
    """Leaves only the location data that the
    API found in the original query.

    Args:
        row (pd.Series): User location results.

    Returns:
        pd.Series: User locations cleaned.
    """
    if('district' in row['valid_regions']):
        pass

    elif('city' in row['valid_regions']):
        row[['norm_district']] = None

    elif('county' in row['valid_regions']):
        row[['norm_city', 'norm_district']] = None

    elif('state' in row['valid_regions']):
        row[['norm_county', 'norm_city',
             'norm_district']] = None

    elif('country' in row['valid_regions']):
        row[['norm_fed_division',
             'norm_fed_division_code', 'norm_county',
             'norm_city', 'norm_district']] = None

    return row


def normalize_subset(df_data, api_key):
    """Makes the call to the HERE API per each 
    row on the given dataframe.

    Args:
        df_data (pd.DataFrame): User locations to normalize.
        api_key (str): HERE APIs key.

    Returns:
        pd.DataFrame: Normalized usuer locations.
    """
    new_cols = ['norm_country_code', 'norm_country', 'norm_fed_division',
                'norm_fed_division_code', 'norm_county', 'norm_city',
                'norm_district', 'norm_postal_code', 'norm_latitude',
                'norm_longitude', 'here_query_score', 'here_field_score']

    for index, row in tqdm(df_data.iloc[:, [0]].iterrows()):
        # TODO(Noe): Add a backup file

        norm_result = get_location_with_here_api(api_key, row[0])
        df_data.loc[index, new_cols] = norm_result

    return df_data


def normalize_user_location_here_api(df_data, api_key):
    """Separates into subsets the user locations and 
    applies in a MultiThread logic the normalization to 
    take advantage of the max 5 request per second of the HERE API.

    Args:
        df_data (pd.DataFrame): User locations to normalize.
        api_key (str): HERE APIs key.

    Returns:
        pd.DataFrame: Normalized usuer locations.
    """
    print(f"{len(df_data)} user locations to normalize")

    if(len(df_data) > 200):

        data_split = np.array_split(df_data, 4)

        with cf.ThreadPoolExecutor() as tp:
            df_data = tp.map(normalize_subset,
                             data_split, repeat(api_key))

        # Concat all the pandas dataframes
        df_data = pd.concat(df_data)

    else:
        df_data = normalize_subset(df_data,
                                   api_key)


    # Get those strings which the API returned NULL
    df_none = df_data[df_data['norm_country_code'].isna()]
    df_data = df_data[~df_data['norm_country_code'].isna()]
    
    # TODO: Add that all the empty strings equals None or all the Nones equals empty strings

    # Check the found fields (geo-regions)
    df_data['valid_regions'] = df_data['here_field_score'].copy()
    df_data['valid_regions'] = df_data['valid_regions'].apply(ast.literal_eval)

    valid_geo = ['country', 'state', 'county', 'city', 'district']
    df_data['valid_regions'] = df_data['valid_regions'].apply(
        lambda score_dict: filter(lambda item: item[0] in valid_geo and item[1] >= 0.75,
                                  score_dict.items()))
    df_data['valid_regions'] = df_data['valid_regions'].apply(
        lambda obj: list(dict(obj).keys()))

    # Discard those that are just districts
    df_data['valid_regions'] = df_data['valid_regions'].apply(
        lambda lst: [] if lst == ['district'] else lst)

    # Discard those that are just invalid districts
    invalid_districts = (df_data['valid_regions'].apply(lambda x: x == ['district'])) * \
        (df_data['here_query_score'] < 0.90)
    df_data.loc[invalid_districts, 'valid_regions'] = False
    df_data['valid_regions'] = df_data['valid_regions'].apply(
        lambda x: x if x else [])

    # Clean the data
    df_data.loc[(~df_data['valid_regions'].apply(bool)),
                df_data.columns[1:]] = None
    df_invalids = df_data[df_data['norm_country_code'].isna()]

    df_data = df_data[~df_data['norm_country_code'].isna()]
    df_data = df_data.apply(clean_rows, axis=1)

    df_data['valid_regions'] = df_data['valid_regions'].astype(str)

    return df_data, df_invalids, df_none
