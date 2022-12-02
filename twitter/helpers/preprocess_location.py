import pandas as pd

from decouple import config

from postal.expand import expand_address
from postal.normalize import normalize_string

import helpers.preprocess_text as pre_text

countries_iso_codes = ['BRA', 'MEX', 'COL', 'ARG', 'PER',
                       'VEN', 'CHL', 'ECU', 'GTM', 'BOL',
                       'DOM', 'HND', 'PRY', 'NIC', 'SLV',
                       'CRI', 'PAN', 'URY', 'BLZ', 'BRB',
                       'TTO', 'JAM', 'GUY', 'SUR', 'HTI']

iso_to_fips_codes = {
    "MEX": "MX", "ARG": "AR", "BOL": "BL", "CHL": "CI", "COL": "CO",
    "CRI": "CS", "HND": "HO", "ECU": "EC", "SLV": "ES", "GTM": "GT",
    "NIC": "NU", "PAN": "PM", "PRY": "PA", "DOM": "DR", "URY": "UY",
    "PER": "PE", "VEN": "VE", "BRA": "BR", "BLZ": "BH", "GUY": "GY",
    "HTI": "HA", "TTO": "TD", "BRB": "BB", "SUR": "NS", "JAM": "JM"
}

region_codes = {
    'LAC': 'Latinoamérica y Caribe',
    'CARIBE': 'Caribe',
    'ARG': 'Argentina',
    'BOL': 'Bolivia',
    'BRA': 'Brasil',
    'CHL': 'Chile',
    'COL': 'Colombia',
    'CRI': 'Costa Rica',
    'DOM': 'República Dominicana',
    'ECU': 'Ecuador',
    'GTM': 'Guatemala',
    'MEX': 'México',
    'PAN': 'Panamá',
    'PER': 'Perú',
    'PRY': 'Paraguay',
    'SLV': 'El Salvador',
    'URY': 'Uruguay',
    'VEN': 'Venezuela',
    'HND': 'Honduras',
    'NIC': 'Nicaragua',
    'TTO': 'Trinidad y Tobago',
    'BRB': 'Barbados',
    'BLZ': 'Belice'
}

stop_words_en = ["about", "above", "after", "again", "against", "ain",
                 "an", "any", "are", "aren", "arent", "as", "at", "be",
                 "because", "ben", "before", "being", "below", "betwen", "both",
                 "but", "by", "can", "couldn", "couldnt", "did", "didn", "didnt",
                 "does", "doesn", "doesnt", "doing", "don", "dont",
                 "down", "during", "each", "few", "for", "further",
                 "had", "hadn", "hadnt", "has", "hasn", "hasnt", "have",
                 "haven", "havent", "having", "he", "her", "here", "hers",
                 "herself", "him", "himself", "his", "how", "if",
                 "into", "is", "isn", "isnt", "it", "its", "its", "itself", "just",
                 "ma", "me", "mightn", "mightnt", "more", "most", "mustn", "mustnt", "my",
                 "myself", "nedn", "nednt", "nor", "not", "now", "off",
                 "on", "once", "only", "other", "our", "ours", "ourselves", "out",
                 "over", "own", "re", "same", "shan", "shant", "she", "shes",
                 "should", "shouldve", "shouldn", "shouldnt", "some", "such",
                 "than", "that", "thatl", "the", "their", "theirs", "them", "themselves",
                 "then", "there", "these", "they", "this", "those", "through",
                 "to", "under", "until", "up", "ve", "very", "was",
                 "wasn", "wasnt", "we", "were", "weren", "werent", "what",
                 "when", "where", "which", "while", "who", "whom", "why",
                 "wil", "with", "won", "wont", "wouldn", "wouldnt",
                 "you", "youd", "youl", "youre", "youve", "your",
                 "yours", "yourself", "yourselves", "else", "any\s?where", "every\s?where",
                 "town", "road", 'country',
                 'universe', 'space', 'stret', 'номер', 'border', 'another', 'atmosphere'
                 'mind', 'lake'
                 #"city", "do", "so", "state", "and", 'district', "of", "in", "from", "or"
                 ]

stop_words = ['tuvieses', 'porque', 'hemos', 'nunca', 'pues', 'estarian', 'asi', 'todavia', 'entre',
              'estuvieran', 'sido', 'cuantos', 'trabajamos', 'ayer', 'otras', 'usas', 'haceis',
              'tendrias', 'mismos', 'estuvieron', 'ultimas', 'fui', 'todas', 'tuvieramos', 'propios', 'ha', 'haber',
              'tened', 'primera', 'tuvieron', 'tanto', 'desde', 'sobre', 'tenia', 'suyas',
              'algunos', 'hayais', 'tienen', 'intentais', 'podriamos', 'cinco', 'vas', 'actualmente', 'una',
              'tenian', 'modo', 'teniendo', 'saber', 'intento', 'hecho', 'sabeis', 'sigue',
              'mas', 'ciertas', 'estabais', 'segundo', 'ademas', 'estuvieses', 'arriba', 'ejemplo', 'tenidos',
              'conocer', 'estos', 'hoy', 'debe', 'grandes', 'tuvieseis', 'hubieras', 'bastante', 'salvo', 'delante',
              'supuesto', 'tendreis', 'seriamos', 'valor', 'hubieran', 'en', 'tuviera', 'ningun', 'ante',
              'tendras', 'consiguen', 'mayor', 'seremos', 'ud', 'estamos', 'tuya', 'arribaabajo', 'explico', 'otro',
              'habiendo', 'junto', 'cuanta', 'ver', 'vuestra', 'menudo', 'fuimos', 'voy', 'primero',
              'tambien', 'habido', 'dijo', 'tenida', 'aunque', 'seais', 'esto', 'algun', 'pronto', 'aun',
              'bueno', 'final', 'propio', 'haciendo', 'has', 'mientras', 'casi', 'ultima',
              'tuvieras', 'hacerlo', 'dias', 'adrede', 'que', 'sino', 'tendriais', 'teneis', 'estarias',
              'muy', 'erais', 'empleas', 'segun', 'tuvo', 'hizo', 'saben', 'nadie', 'soyos',
              'hubieseis', 'sintiendo', 'je', 'podra', 'siete', 'nada', 'demasiado', 'encuentra', 'estabas',
              'aseguro', 'somos', 'estuvieramos', 'agrego', 'hubierais', 'nosotros', 'alrededor',
              'contigo', 'debajo', 'teniais', 'pocos', 'dio', 'partir', 'trabajar', 'sin', 'cierta', 'habiamos', 'esas',
              'estabamos', 'tuve', 'son', 'sea', 'trabaja', 'hayan', 'suyos', 'un', 'hacer', 'tendremos', 'dan',
              'claro', 'cerca', 'estes', 'eso', 'tuviesemos', 'sentidos', 'cualquier', 'ahora', 'hace', 'muchos', 'ultimos',
              'proximos', 'habla', 'eras', 'gueno', 'parece', 'vosotros', 'seamos', 'despues', 'tendre', 'horas', 'empleais',
              'habra', 'nuevos', 'temprano', 'nosotras', 'alguno', 'considera', 'tendriamos', 'usan', 'queremos', 'ir', 'tuyo',
              'estuviera', 'solo', 'este', 'expreso', 'primer', 'hacemos', 'uso', 'tuvisteis', 'hubiste', 'km', 'tenias',
              'quiza', 'esta', 'si', 'ahi', 'alli', 'despacio', 'esa', 'puede', 'conseguimos', 'tendrian', 'lleva',
              'hago', 'dicen', 'anterior', 'hubiese', 'diferente', 'fuera', 'seas', 'anadio', 'primeros', 'estariamos', 'repente',
              'emplean', 'nuestra', 'empleo', 'con', 'sabemos', 'mias', 'poca', 'serian', 'principalmente', 'mucha', 'seis',
              'habidas', 'ninguna', 'fuiste', 'apenas', 'uno', 'ningunas', 'menos', 'fueran', 'habria', 'he', 'esteis',
              'realizado', 'podran', 'llevar', 'fueseis', 'era', 'medio', 'mia', 'consigue', 'os', 'nuestros', 'tengamos',
              'aquella', 'va', 'vuestro', 'se', 'segunda', 'estad', 'otra', 'solamente', 'ni', 'tal', 'hubiesen',
              'seran', 'cuantas', 'tampoco', 'sentida', 'tuviese', 'hicieron', 'han', 'dijeron', 'habida', 'aproximadamente', 'vais',
              'otros', 'dice', 'gran', 'esten', 'estaremos', 'hasta', 'estas', 'indico', 'habreis', 'sean', 'ya',
              'serias', 'demas', 'le', 'largo', 'estando', 'cual', 'ampleamos', 'conseguir', 'verdadero', 'vamos',
              'muchas', 'contra', 'adelante', 'estuvieseis', 'dia', 'estuvimos', 'tenemos', 'hacen', 'durante', 'proximo', 'bien',
              'veces', 'fuese', 'emplear', 'alguna', 'podemos', 'buen', 'tengo', 'informo', 'tuvieran', 'raras', 'trabajo',
              'estan', 'solas', 'para', 'habidos', 'tercera', 'hayas', 'sos', 'entonces', 'tuvierais', 'manera',
              'cuando', 'podrias', 'hubimos', 'menciono', 'tendra', 'esos', 'siendo', 'tus', 'verdadera', 'aquel', 'mismas',
              'dentro', 'ti', 'diferentes', 'atras', 'estadas', 'pudo', 'habrian', 'pasada', 'lado', 'estuve', 'tengan',
              'usar', 'vosotras', 'sereis', 'habia', 'etc', 'cuanto', 'habras', 'seriais', 'nuestras', 'usa', 'mismo',
              'mi', 'momento', 'trabajas', 'incluso', 'intentan', 'ningunos', 'dicho', 'varios', 'toda', 'fue', 'hubo',
              'es', 'sentid', 'estemos', 'pais', 'breve', 'siente', 'estariais', 'llego', 'dar', 'excepto', 'tan', 'hube',
              'mis', 'unos', 'nuestro', 'detras', 'fueramos', 'habian', 'luego', 'estare', 'comento', 'podria', 'tuviste',
              'intentamos', 'quiere', 'ello', 'suya', 'intenta', 'hubieses', 'estuviste', 'consigo', 'ese', 'encima', 'habias', 'teniamos',
              'embargo', 'habran', 'sentido', 'tener', 'habremos', 'tienes', 'habrias', 'debido', 'deben',
              'sentidas', 'todo', 'manifesto', 'podeis', 'hayamos', 'pasado', 'ella', 'estaras', 'intentar', 'estuviesen', 'cuatro',
              'tuyos', 'ojala', 'estara', 'cosas', 'estuviese', 'trabajan', 'total', 'verdad', 'estareis', 'mucho',
              'fuesen', 'veo', 'sois', 'igual', 'lejos', 'alla', 'mejor', 'su', 'yo', 'misma', 'buena',
              'deprisa', 'cierto', 'bajo', 'traves', 'algunas', 'ambos', 'fin', 'propia', 'tenidas',
              'fueron', 'habriamos', 'dieron', 'mediante', 'realizar', 'ja', 'pero', 'donde', 'nos', 'o', 'considero',
              'pesar', 'respecto', 'eres', 'tendria', 'sabes', 'tuvimos', 'solos', 'ninguno', 'estuvieras', 'te', 'intentas',
              'tiene', 'vuestros', 'usted', 'ex', 'conmigo', 'vez', 'habriais', 'por', 'propias',
              'quizas', 'fuerais', 'mios', 'estaban', 'trabajais', 'quienes', 'existe', 'posible', 'habeis', 'hubieramos', 'varias',
              'estada', 'estais', 'seria', 'trata', 'tiempo', 'cuenta', 'consigues', 'habre', 'vos', 'parte', 'van',
              'existen', 'sabe', 'antes', 'suyo', 'tenga', 'ciertos', 'les', 'poner', 'ocho', 'vaya', 'podriais',
              'tras', 'tu', 'dado', 'estuviesemos', 'puedo', 'hablan', 'a', 'enseguida', 'fuisteis', 'tuyas', 'lo',
              'hubisteis', 'sus', 'ustedes', 'sola', 'estuvisteis', 'pueda', 'ellos', 'unas', 'aquellos', 'estaran',
              'ultimo', 'haya', 'aquello', 'lugar', 'quedo', 'seras', 'siguiente', 'nuevas', 'sera', 'eramos', 'habiais',
              'bla', 'estuvo', 'tengas', 'acuerdo', 'siempre', 'estuvierais', 'qeu', 'hubieron', 'eran', 'tuviesen', 'aquellas',
              'cada', 'decir', 'todos', 'algo', 'peor', 'senalo', 'poder', 'ser', 'quien', 'sere',
              'fueras', 'ellas', 'hacia', 'soy', 'tarde', 'aqui', 'fueses', 'buenas', 'hubiera', 'hubiesemos', 'antano',
              'cuales', 'fuesemos', 'pueden', 'haces', 'estar', 'realizo', 'mal', 'afirmo', 'estaba', 'hay',
              'como', 'enfrente', 'dejo', 'creo', 'tenido', 'usamos', 'tendran', 'vuestras', 'usais', 'podrian', 'aca',
              'tengais', 'poco', 'estaria', 'mio', 'estoy', 'pocas']

cardinal_points_es = '(?:norte|sur|este|oeste|central)'
cardinal_points_en = '(?:north|west|east|south|central)'
continents_es = '(?:africa|europ[ea]|america|asia|oceania|australia)'

america_prefix = '(?:latino?|centro|central|meso|suda?|ibero|sur|norte|hispano|pana)'

continents_regex = [f'{cardinal_points_es} de {continents_es}', f'{continents_es} del {cardinal_points_es}',
                    f'{continents_es}\s?{cardinal_points_es}',
                    f'{cardinal_points_en}\s?(?:africa|europa|america|asia|oceania|australia)',
                    f'{cardinal_points_es}\s?(?:africa|europa|america|asia|oceania|australia)',
                    '^\w*(?:europ|america|africa)\w*$',

                    '(?:north|west|east) africa', '(?<!south )\\bafrica\\b',
                    'union europea', 'european union', '\\beuropean\\b', '\\beurope[oa]?\\b', '\\beuropa\\b',
                    f'{america_prefix}\s?america', 'american?\s?latina?', '\\blatam\\b', '\\blas americas\\b',
                    '\\basia\\b', '\\boceania\\b', '\\baustralia\\b',
                    '\\bcontinente americano\\b', '\\bamerican?\\b',
                    '\\bpolo (?:norte|sur)\\b']

cardinal_regex = ['(?:(?:al|del|frontera|region) )?norte (?:de )?(?!santander)',
                  f'zona {cardinal_points_es}',

                  f'^(?:[ae]l )?{cardinal_points_es}(?: del?)?\\b',
                  f'\\b[ae]l {cardinal_points_es}$',
                  f'\\bdel {cardinal_points_es}$',
                  '^\w*(?:norte|oeste|este|sur(?!iname?))\w*$',
                  '^(?:norte|oeste|este|sur(?!iname?))$',
                  '(?:noreste|noroeste|sureste|suroeste)']

planets_regex = ["marte", "venus", "mercurio", "neptuno", "urano", "jupiter", "saturno", "pluton",
                 "mars", "venus", "mercury", "neptune", "uranus", "jupiter", "saturn", "pluto"]


weird_regex = ['\\b(?:el)? continente\\b', '\\bcontinent\\b', '(?:d?el )?mundo', '(?:d?el )?sofa',
               '(?:(?:la|planeta) )?tierr?a', '(?:(?:la|otra|esta) )?galaxia',
               '(?:la )?via\s?lactea', 'universal', 'somewhere(?: in)?',
               'everywhere', '\\benero\\b', '\\baqui\\b', '(?:d?el )?universo', 'planet earth',
               '(?:d?el )?infierno', '(?:d?el )?cielo', '^\w*corazon\w*$', 'el corazon de',
               '\\bfacebook\\b', '\\binstagram\\b', '\\btwitter\\b', '\\btumblr\\b']

# TODO(Noe): Add probouns expressions


def preprocessing_location_string(df_data):
    """Preprocess the user location to eliminate the amount
    of strings to normalize. 

    All to lower case, remove urls, emails, duplicated chars, 
    normalize address expresions, etc.

    Args:
        df_data (pd.DataFrame): User locations to preprocess.

    Returns:
        pd.DataFrame: Clean and preprocesed user locations.
    """
    new_col = 'author_location_processed'

    pre_text.initial_preprocessing(df_data, new_col,
                                   flg_remove_emojis=True,
                                   flg_lower=True)

    pre_text.remove_urls(df_data, new_col)
    pre_text.remove_emails(df_data, new_col)
    pre_text.remove_urls(df_data, new_col)
    pre_text.remove_numbers(df_data, new_col)

    pre_text.remove_duplicated_chars(df_data, new_col)
    pre_text.remove_multiple_blank_spaces(df_data, new_col)

    # Custom replace, to get ride of extra symbols
    df_data[new_col] = df_data[new_col].str.replace(r'[\/\\_#-]', ',',
                                                    regex=True)
    df_data[new_col] = df_data[new_col].str.strip(',. ')

    pre_text.normalize_abstractions(df_data, new_col, flg_space=True)
    pre_text.spaces_before_after_punctuation(df_data, new_col)
    pre_text.remove_non_alphanumeric(df_data, new_col,
                                     opt_keep_chars='\.,')

    pre_text.remove_single_letters(df_data, new_col)
    pre_text.remove_multiple_blank_spaces(df_data, new_col)

    # Remove weird expressions from the users
    pre_text.remove_stopwords(df_data, new_col,
                              opt_stopwords=continents_regex,
                              flg_by_word=False)
    pre_text.remove_stopwords(df_data, new_col,
                              opt_stopwords=cardinal_regex,
                              flg_by_word=False)
    pre_text.remove_stopwords(df_data, new_col,
                              opt_stopwords=planets_regex)
    pre_text.remove_stopwords(df_data, new_col,
                              opt_stopwords=weird_regex,
                              flg_by_word=False)

    # Column rwith no stopwords
    pre_text.remove_stopwords(df_data, new_col,
                              opt_stopwords=stop_words)

    pre_text.remove_multiple_blank_spaces(df_data, new_col)
    df_data[new_col] = df_data[new_col].str.strip()

    index_keep = pre_text.remove_empty_strs_and_duplicates(df_data, new_col)
    df_data = df_data.loc[index_keep].copy()

    # Apply the expand by trhe address parse
    df_data[new_col] = df_data[new_col].apply(normalize_string)
    df_data[new_col] = df_data[new_col].apply(lambda loc: expand_address(loc,
                                                                         expand_numex=False))
    df_data[new_col] = df_data[new_col].apply(lambda expand: expand[0]
                                              if len(expand) > 0 else '')

    df_data[new_col] = df_data[new_col].str.strip()
    index_keep = pre_text.remove_empty_strs_and_duplicates(df_data, new_col)
    df_data = df_data.loc[index_keep].copy()

    return df_data


def validate_author_locations(df_data):
    """Validate that the user location string is valid.
    It does not have invalid countries names, weird 
    expression in english, multiple countries, etc. 
    Bassically, any sitatution in which the HERE API
    could not find a trustful result.

    Args:
        df_data (pd.DataFrame): User locations to validate.

    Returns:
        pd.DataFrame: Validated user locations. With a boolean column.
    """

    location_col = "author_location_processed"

    # Get regex from valid and invalid countries
    df_countries = pd.read_csv("./resources/countries_data.csv",
                               sep='\t',
                               usecols=['ISO_2', 'ISO_3',
                                        'name_short_es', 'regex_es',
                                        'regex_en'])

    df_countries['regex_big'] = df_countries.apply(lambda row: set([row.regex_es,
                                                                    row.regex_en]),
                                                   axis=1)
    df_countries['regex_big'] = df_countries['regex_big'].apply('|'.join)
    df_countries['regex_big'] = df_countries['regex_big'].astype(str)

    df_valid = df_countries[df_countries['ISO_3'].isin(
        countries_iso_codes)]
    df_invalid = df_countries[~df_countries['ISO_3'].isin(
        countries_iso_codes)]

    valid_regs = '(' + '|'.join(df_valid['regex_big']) + ')'
    invalid_regs = '(' + '|'.join(df_invalid['regex_big']) + ')'

    # Mark the ones that contians more than one valid country
    df_tmp = df_data[location_col].str.extractall(valid_regs).reset_index()
    df_tmp = df_tmp.groupby(['level_0'])[0].apply(set).apply(len)

    df_data['multiple_valids'] = (df_tmp > 1)
    df_data['multiple_valids'] = df_data['multiple_valids'].fillna(False)

    # Mark those with invalid countries
    df_data['invalid_countries'] = df_data[location_col].str.contains(invalid_regs[1:-1],
                                                                      regex=True)

    # Mark those that have english stopwords
    reg_en_stpw = '|'.join(map(lambda word: f'\\b{word}\\b',
                               stop_words_en))
    df_data['in_english'] = df_data[location_col].str.contains(reg_en_stpw)

    # Mark those that do not have a useful length
    df_data['not_useful_length'] = df_data[location_col].str.contains(r'^\w{1,3}$',
                                                                      regex=True)
    df_data['not_useful_chars'] = df_data[location_col].str.contains(r'^ *(?:\w +)+(?:\w *)$',
                                                                     regex=True)

    # Get the final filter
    df_data['author_location_is_valid'] = ~(df_data['multiple_valids'] +
                                            df_data['invalid_countries'] +
                                            df_data['not_useful_length'] +
                                            df_data['not_useful_chars'] +
                                            df_data['in_english'])

    df_data = df_data[[location_col,
                       'author_location_is_valid']]

    return df_data
