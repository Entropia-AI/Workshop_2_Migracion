import re
import emoji
import numpy as np

# Compiled Regular Expresions
# Get the Stopwords
STOP_WORDS = ['tuvieses', 'porque', 'hemos', 'nunca', 'pues', 'estarian', 'asi', 'todavia', 'entre', 'e',
              'estuvieran', 'sido', 'cuantos', 'trabajamos', 'ayer', 'otras', 'del', 'usas', 'haceis',
              'tendrias', 'mismos', 'estuvieron', 'ultimas', 'fui', 'todas', 'tuvieramos', 'propios', 'ha', 'haber',
              'tened', 'primera', 'tuvieron', 'tanto', 'desde', 'sobre', 'tenia', 'suyas',
              'algunos', 'hayais', 'tienen', 'intentais', 'podriamos', 'cinco', 'vas', 'actualmente', 'una',
              'tenian', 'modo', 'teniendo', 'saber', 'intento', 'hecho', 'sabeis', 'sigue',
              'mas', 'ciertas', 'estabais', 'segundo', 'ademas', 'estuvieses', 'arriba', 'ejemplo', 'tenidos',
              'conocer', 'estos', 'hoy', 'debe', 'grandes', 'tuvieseis', 'hubieras', 'bastante', 'salvo', 'delante',
              'supuesto', 'tendreis', 'seriamos', 'valor', 'hubieran', 'en', 'tuviera', 'ningun', 'ante',
              'tendras', 'consiguen', 'mayor', 'seremos', 'ud', 'estamos', 'tuya', 'arribaabajo', 'explico', 'no', 'otro',
              'habiendo', 'junto', 'cuanta', 'ver', 'vuestra', 'menudo', 'fuimos', 'voy', 'primero',
              'tambien', 'habido', 'dijo', 'tenida', 'aunque', 'seais', 'esto', 'algun', 'pronto', 'aun',
              'bueno', 'final', 'propio', 'haciendo', 'has', 'mientras', 'casi', 'ultima', 'dos',
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
              'serias', 'demas', 'le', 'largo', 'los', 'estando', 'cual', 'ampleamos', 'conseguir', 'verdadero', 'vamos',
              'muchas', 'contra', 'adelante', 'estuvieseis', 'dia', 'estuvimos', 'tenemos', 'hacen', 'durante', 'proximo', 'bien',
              'veces', 'fuese', 'emplear', 'alguna', 'podemos', 'buen', 'tengo', 'informo', 'tuvieran', 'raras', 'trabajo',
              'estan', 'solas', 'para', 'habidos', 'tercera', 'hayas', 'sos', 'buenos', 'entonces', 'tuvierais', 'manera',
              'cuando', 'podrias', 'hubimos', 'menciono', 'tendra', 'esos', 'siendo', 'tus', 'verdadera', 'aquel', 'mismas',
              'dentro', 'ti', 'diferentes', 'atras', 'estadas', 'pudo', 'habrian', 'pasada', 'lado', 'estuve', 'tengan',
              'usar', 'vosotras', 'sereis', 'habia', 'etc', 'cuanto', 'habras', 'seriais', 'nuestras', 'usa', 'mismo',
              'mi', 'momento', 'trabajas', 'incluso', 'intentan', 'ningunos', 'dicho', 'varios', 'el', 'toda', 'fue', 'hubo',
              'es', 'sentid', 'estemos', 'pais', 'breve', 'siente', 'estariais', 'llego', 'dar', 'excepto', 'tan', 'hube',
              'mis', 'unos', 'nuestro', 'detras', 'fueramos', 'habian', 'tres', 'luego', 'estare', 'comento', 'podria', 'tuviste',
              'intentamos', 'quiere', 'ello', 'suya', 'intenta', 'hubieses', 'estuviste', 'consigo', 'ese', 'encima', 'habias', 'teniamos',
              'embargo', 'al', 'habran', 'sentido', 'tener', 'habremos', 'la', 'tienes', 'habrias', 'me', 'debido', 'deben',
              'sentidas', 'todo', 'manifesto', 'podeis', 'hayamos', 'pasado', 'las', 'ella', 'estaras', 'intentar', 'estuviesen', 'cuatro',
              'tuyos', 'ojala', 'de', 'estara', 'cosas', 'estuviese', 'trabajan', 'total', 'verdad', 'estareis', 'mucho',
              'fuesen', 'veo', 'sois', 'igual', 'lejos', 'alla', 'mejor', 'su', 'yo', 'misma', 'buena',
              'deprisa', 'cierto', 'bajo', 'traves', 'estado', 'general', 'algunas', 'ambos', 'fin', 'propia', 'tenidas',
              'fueron', 'habriamos', 'dieron', 'mediante', 'realizar', 'ja', 'pero', 'donde', 'nos', 'o', 'considero',
              'pesar', 'respecto', 'eres', 'tendria', 'sabes', 'tuvimos', 'solos', 'ninguno', 'estuvieras', 'te', 'intentas',
              'tiene', 'vuestros', 'usted', 'ex', 'conmigo', 'vez', 'habriais', 'por', 'propias', 'y', 'nueva',
              'quizas', 'fuerais', 'mios', 'estaban', 'trabajais', 'quienes', 'existe', 'posible', 'habeis', 'hubieramos', 'varias',
              'estada', 'estais', 'seria', 'trata', 'tiempo', 'cuenta', 'consigues', 'habre', 'vos', 'parte', 'van',
              'existen', 'sabe', 'antes', 'suyo', 'tenga', 'ciertos', 'les', 'poner', 'ocho', 'vaya', 'podriais',
              'tras', 'tu', 'dado', 'estuviesemos', 'puedo', 'hablan', 'a', 'enseguida', 'fuisteis', 'tuyas', 'lo',
              'nuevo', 'hubisteis', 'sus', 'ustedes', 'sola', 'estuvisteis', 'pueda', 'ellos', 'unas', 'aquellos', 'estaran',
              'ultimo', 'haya', 'aquello', 'lugar', 'quedo', 'seras', 'siguiente', 'nuevas', 'sera', 'eramos', 'habiais',
              'bla', 'estuvo', 'tengas', 'acuerdo', 'siempre', 'estuvierais', 'qeu', 'hubieron', 'eran', 'tuviesen', 'aquellas',
              'cada', 'decir', 'todos', 'algo', 'peor', 'da', 'senalo', 'poder', 'ser', 'quien', 'sere',
              'fueras', 'ellas', 'hacia', 'soy', 'tarde', 'aqui', 'fueses', 'buenas', 'hubiera', 'hubiesemos', 'antano',
              'estados', 'cuales', 'fuesemos', 'pueden', 'haces', 'estar', 'realizo', 'mal', 'afirmo', 'estaba', 'hay',
              'como', 'enfrente', 'dejo', 'creo', 'tenido', 'usamos', 'tendran', 'vuestras', 'usais', 'podrian', 'aca',
              'tengais', 'poco', 'estaria', 'mio', 'estoy', 'pocas']


# Specific to Twitter
users_reg = re.compile(r'([@])([\w]+)')
multiple_norm_users_reg = re.compile(r'(?:@user\s+)(?:@user\s+)+')

hashtags_reg = re.compile(r'[#][\w]+')
images_urls_reg = re.compile(r'[a-zA-Z0-9].twitter.com/[\w]*')

# General structures
urls_reg = re.compile(
    r'(?:http[s]?://|www\.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
mails_reg = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z-]+\.[a-zA-Z0-9-.]+')

# General elements
num_reg = re.compile(r'\d+')
# TODO: Keep the "..." (Reduce the .... to just "..." and ".." to ".")
# TODO: If there is "\w [.,:]", join it to \w.
duplicated_chars_reg = re.compile(r'(\S)(\1+)')
duplicated_signs_reg = re.compile(r'(\W)(\1+)')
duplicated_signs_sep_reg = re.compile(r'(\W) (?=\1+)')
written_laugh_reg = re.compile('\w*(?:[jh][ae]){2,}\w*')

# TODO: Be able to define the number of chars / letters
single_chars_reg = re.compile(r'^[^\s]{1} | [^\s]{1} | [^\s]{1}$')
single_chars_reg_capture = re.compile(r'(^[^\s]{1} | [^\s]{1} | [^\s]{1}$)')

single_letter_reg = re.compile(r'^[a-zA-Z]{1} | [a-zA-Z]{1} | [a-zA-Z]{1}$')
single_letter_reg_capture = re.compile(
    r'(.*)(^[a-zA-Z]{1} | [a-zA-Z]{1} | [a-zA-Z]{1}$)(.*)')


alphabetic_chars_reg = re.compile(r'[^a-zA-Z\s]')
alphanumeric_reg = re.compile(r'[^a-zA-Z0-9\s]')
blank_spaces_reg = re.compile(r'\s{2,}')

# Spanish ortographic issues
dot_abstractions_reg = re.compile(r'(\b[a-zA-Z])\.(?=[a-zA-Z]\b|\s|$)')
space_abstractions_reg = re.compile(r'(\b[a-zA-Z])\s(?=[a-zA-Z]\b|\s|$)')
no_space_punctuation_char = re.compile(r'(\W)(\S)')
space_before_reg = re.compile(r'(\S)([\(\[\{¡¿\\/\"\'])')
no_space_after_reg = re.compile(r'([\(\[\{¡¿\\/\"\'])(\s*)')
space_after_reg = re.compile(r'([.:%,;?\}\)\]!\\/\"\'])(\S)')
no_space_before_reg = re.compile(r'(\s*)([.:%,;?\}\)\]!\\/\"\'])')
mispelled_que_reg = re.compile(r' (?:ke|qe|k|q) ')
mispelled_por_reg = re.compile(r' x ')


# Clean Text documents
# General Processing Text Functions
def initial_preprocessing(df_data, col_name='text',
                          flg_remove_emojis=True,
                          flg_lower=True):
    """Set all the documents as lowercase,
    remove accents/expecial_chars and remove
    duplicated chars.
    It will not return anything, but it will
    modofy the passed dataframe.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name.
                                  Defaults to 'text'.
        flg_remove_emojis (bool, optional): Remove or keep the
                                            found emojis.
                                            Default to False.
    """

    if(flg_lower):
        df_data[col_name] = df_data[col_name].str.lower()

    if(flg_remove_emojis):
        df_data[col_name] = df_data[col_name].str.normalize('NFD')
        df_data[col_name] = df_data[col_name].str.replace(r"([\u0300-\u036f]+)", r"",
                                                          regex=True)

    else:
        df_data[col_name] = df_data[col_name].str.normalize('NFKD')
        df_data[col_name] = df_data[col_name].str.encode('ascii',
                                                         errors='ignore')
        df_data[col_name] = df_data[col_name].str.decode('utf-8')

    df_data[col_name] = df_data[col_name].str.strip()
    df_data[col_name] = df_data[col_name].astype(str)


def normalize_abstractions(df_data, col_name='text',
                           flg_space=False):
    """Functiont that is in charge of normalize abstractions that
    that contains dots. Like: "U.S.A" or "D.C" into "USA" and "DC".

    With a flog, it is possible to normalize the abstractions that
    use a blank space instead of a dot. Example: "D C" into "DC".
    This could be useful when the text include actual words, in which
    each char is separataed: "H E L L O".

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Columna name. Defaults to 'text'.
        flg_space (bool, optional): If it is needed to also normalize
    """

    if(flg_space):
        df_data[col_name] = df_data[col_name].str.replace(space_abstractions_reg, r'\1',
                                                          regex=True)

    df_data[col_name] = df_data[col_name].str.replace(dot_abstractions_reg, r'\1',
                                                      regex=True)


def remove_duplicated_chars(df_data, col_name='text',
                            opt_keep_chars=None,
                            flg_only_non_letters=False):
    """Remove all the duplicated chars.
    For example: Holaaaaaa -> Hola

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
        flg_only_non_letters (bool, optional): Deduplicate only chars
                                               that are not alphanumeric.
                                               Default to False.
    """

    if(flg_only_non_letters):
        df_data[col_name] = df_data[col_name].str.replace(duplicated_signs_sep_reg, r'\1',
                                                          regex=True)
        df_data[col_name] = df_data[col_name].str.replace(duplicated_signs_reg, r'\1',
                                                          regex=True)

    else:
        if(opt_keep_chars is None):
            # TODO: Deal with contractions like EE UU
            df_data[col_name] = df_data[col_name].str.replace(duplicated_chars_reg, r'\1',
                                                              regex=True)
        else:

            tmp_reg = re.compile(f'([^{opt_keep_chars}])(\\1+)')
            df_data[col_name] = df_data[col_name].str.replace(
                tmp_reg, r'\1', regex=True)

            tmp_reg = re.compile(f'([{opt_keep_chars}])(\\1+)')
            df_data[col_name] = df_data[col_name].str.replace(
                tmp_reg, r'\1\1', regex=True)


def normalize_written_laughs(df_data, col_name='text',
                             flg_remove=False):
    """Normalize the "jajaja" or "hahaha" to just "jaja", so it
    serves as input to the models or it could be completly removed.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
        flg_remove (bool, optional): Remove or just normalize the
                                     laughs.
    """
    str_replace = 'jaja'

    if(flg_remove):
        str_replace = ' '

    df_data[col_name] = df_data[col_name].str.replace(written_laugh_reg, str_replace,
                                                      regex=True)


def emojis_between_spaces(df_data, col_name='text'):
    """With regular expressions, puts all the emojis between
    blank spaces.

    Args:
        df_data (pd.DataFrame): Data to pre-process.
        col_name (str, optional): Column name.
                                  Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(emoji.get_emoji_regexp(),
                                                      r" \1 ", regex=True)


def separate_emojis_column(df_data, col_name='text'):
    """Function that extract all the emojis from each document
    of a given column, deduplicate them and merge them in a string.
    Finally, it store them on a column namede: {col_name}_emojis.

    Args:
        df_data (pd.DataFrame): Data to pre-process.
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    emojis_col = f'{col_name}_emojis'

    # Extract all the emojis form each document
    # Deduplicate them and store them as string
    srs_tmp = df_data[col_name].str.extractall(emoji.get_emoji_regexp())
    srs_tmp = srs_tmp[0].reset_index().groupby('level_0')[0].apply(set)
    srs_tmp = srs_tmp.apply(lambda emoji: ' '.join(emoji))

    df_data[emojis_col] = srs_tmp


def spaces_before_after_punctuation(df_data, col_name='text'):
    """Add spaces after the corresponding punctuations chars or before.

    Args:
        df_data (pd.DataFrame): Data to pre-process.
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(
        no_space_after_reg, r'\1', regex=True)

    df_data[col_name] = df_data[col_name].str.replace(
        no_space_before_reg, r'\2', regex=True)

    df_data[col_name] = df_data[col_name].str.replace(
        space_before_reg, r'\1 \2', regex=True)

    df_data[col_name] = df_data[col_name].str.replace(
        space_after_reg, r'\1 \2', regex=True)


def spelling_errors_norm(df_data, col_name='text'):
    """Correct some common spelling erros, using regex.

    Args:
        df_data (pd.DataFrame): Data to pre-process.
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(mispelled_que_reg,
                                                      ' que ',
                                                      regex=True)

    df_data[col_name] = df_data[col_name].str.replace(mispelled_por_reg,
                                                      ' por ',
                                                      regex=True)


def remove_multiple_blank_spaces(df_data, col_name='text'):
    """Strip multiple blank spaces.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(blank_spaces_reg, ' ',
                                                      regex=True)
    df_data[col_name] = df_data[col_name].str.strip()


# def remove_stopwords(df_data, col_name='text', opt_stopwords=None):
#     """Remove the stopwords from a pandas column.

#     Args:
#         df_data (pd.DataFrame): Data to pre-process
#         col_name (str, optional): Column name. Defaults to 'text'.
#     """

#     if(opt_stopwords is None):
#         lst_stopwords = STOP_WORDS
#     else:
#         lst_stopwords = opt_stopwords

#     stpwrds_regex_start = r'^({})\b(.*)'.format('|'.join(lst_stopwords))
#     stpwrds_regex_start = re.compile(stpwrds_regex_start, flags=re.IGNORECASE)
#     stpwrds_regex_between = r'(.*)\b({})\b(.*)'.format('|'.join(lst_stopwords))
#     stpwrds_regex_between = re.compile(stpwrds_regex_between, flags=re.IGNORECASE)
#     stpwrds_regex_end = r'(.*)\b({})$'.format('|'.join(lst_stopwords))
#     stpwrds_regex_end = re.compile(stpwrds_regex_end, flags=re.IGNORECASE)

#     df_data[col_name] = df_data[col_name].str.replace(stpwrds_regex_start, '',
#                                                       regex=True)
#     df_data[col_name] = df_data[col_name].str.replace(stpwrds_regex_between, '',
#                                                       regex=True)
#     df_data[col_name] = df_data[col_name].str.replace(stpwrds_regex_end, '',
#                                                       regex=True)

#     # Remove unwatned blanks spaces
#     df_data[col_name] = df_data[col_name].str.replace(blank_spaces_reg, ' ',
#                                                     regex=True)
#     df_data[col_name] = df_data[col_name].str.strip()

def remove_stopwords(df_data, col_name='text',
                     opt_stopwords=None,
                     flg_by_word=True):
    """Remove the stopwords from a pandas column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    if(opt_stopwords is None):
        lst_stopwords = STOP_WORDS
    else:
        lst_stopwords = opt_stopwords

    if(flg_by_word):
        lst_stopwords = map(lambda word: f'\\b{word}\\b', lst_stopwords)

    lst_stopwords = re.compile('|'.join(lst_stopwords), flags=re.IGNORECASE)

    df_data[col_name] = df_data[col_name].str.replace(lst_stopwords, '',
                                                      regex=True)

    # Remove unwatned blanks spaces
    df_data[col_name] = df_data[col_name].str.replace(blank_spaces_reg, ' ',
                                                      regex=True)
    df_data[col_name] = df_data[col_name].str.strip()


def remove_single_chars(df_data, col_name='text'):
    """Remove the single chars (ALL VALID CHARS) from a given column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_tmp = df_data[col_name].str.extractall(single_chars_reg_capture)
    while(df_tmp.shape[0] > 0):

        df_data[col_name] = df_data[col_name].str.replace(single_chars_reg, ' ',
                                                          regex=True)
        df_tmp = df_data[col_name].str.extractall(single_chars_reg_capture)


def remove_single_letters(df_data, col_name='text'):
    """Remove the single letters from a given column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_tmp = df_data[col_name].str.extractall(single_letter_reg_capture)
    while(df_tmp.shape[0] > 0):

        df_data[col_name] = df_data[col_name].str.replace(single_letter_reg, ' ',
                                                          regex=True)
        df_tmp = df_data[col_name].str.extractall(single_letter_reg_capture)


def remove_empty_strs_and_duplicates(df_data, col_name='text',
                                     flg_duplicates=True,
                                     opt_other_column=None):
    """Get ride of the empty strings and duplicated on a pandas column.
    Note that it will completely remove the rows from the pandas
    dataframe.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
        flg_duplicates (bool, optional): Flag to remove the
                                         duplicated strs.
                                         Default to True.
    """

    if(flg_duplicates):
        df_data = df_data.drop_duplicates(col_name)

    if(opt_other_column is not None):
        other_col = np.array(~df_data[opt_other_column].isna())

    else:
        other_col = np.array([True] * len(df_data))

    not_empty = np.array((~df_data[col_name].isna()) *
                         (df_data[col_name] != '') *
                         (df_data[col_name] != 'None') *
                         (df_data[col_name] != 'none') *
                         (df_data[col_name] != 'null') *
                         (~df_data[col_name].str.contains(r'^\w$', regex=True)))

    keep_rows = not_empty & other_col

    return df_data[keep_rows].index

# General Structures Functions


def remove_urls(df_data, col_name='text'):
    """Remove URLs from a string column. By deafault it will
    remove a general url, but if the "tweet_image" flag is passed
    as True. it will also remove the URL of images from Twitter.

    Args:
        df_data (pd.DataFrame): Data to pre-process.
        col_name (str, optional): Column name.
                                  Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(urls_reg, ' ',
                                                      regex=True)


def remove_emails(df_data, col_name='text'):
    """Remove all the e-mails from a pandas column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(mails_reg, ' ',
                                                      regex=True)


# General Elements Functions
def remove_numbers(df_data, col_name='text', replace_char=''):
    """Remove all the numbers from a pandas column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
    """

    df_data[col_name] = df_data[col_name].str.replace(num_reg,
                                                      replace_char,
                                                      regex=True)


def remove_non_alphanumeric(df_data, col_name='text',
                            flg_alphabetic=False,
                            opt_keep_chars=None):
    """It will remove all the chars that are not alphanumeric or
    blank spaces. It can be setted to just keep the letters with
    the flg_alphabetic option.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
        flg_remove (bool, optional): Keep just the letters.
                                     Default to False.
    """
    reg = alphanumeric_reg
    if(flg_alphabetic):
        reg = alphabetic_chars_reg

    if(opt_keep_chars is not None):
        reg = reg.pattern[:-1] + opt_keep_chars + ']'
        reg = re.compile(reg)

    df_data[col_name] = df_data[col_name].str.replace(reg, ' ',
                                                      regex=True)


# Twitter Elements Functions
def normalize_usermentions(df_data, col_name='text',
                           flg_symbol=False,
                           flg_norm_username=False,
                           flg_group_norm=True):
    """Remove all the user mentions from a pandas column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
        flg_symbol (bool, optional): Flag to remove just the symbol
                                     and keep the words.
                                     Default to False.
        flg_norm_username (bool, optional): Change the user mentions
                                            to just @user
    """

    if(not flg_symbol):
        if(not flg_norm_username):
            df_data[col_name] = df_data[col_name].str.replace(users_reg, ' ',
                                                              regex=True)
        else:
            df_data[col_name] = df_data[col_name].str.replace(users_reg, '@user ',
                                                              regex=True)

            if(flg_group_norm):
                df_data[col_name] = df_data[col_name].str.replace(multiple_norm_users_reg,
                                                                  '@users ',
                                                                  regex=True)

    else:
        df_data[col_name] = df_data[col_name].str.replace(users_reg, r' \2',
                                                          regex=True)


def remove_hashtags(df_data, col_name='text',
                    flg_symbol=False):
    """Remove all the hastags from a pandas column.

    Args:
        df_data (pd.DataFrame): Data to pre-process
        col_name (str, optional): Column name. Defaults to 'text'.
        flg_symbol (bool, optional): Flag to remove just the symbol
                                     and keep the words.
                                     Default to False.
    """

    if(not flg_symbol):
        df_data[col_name] = df_data[col_name].str.replace(hashtags_reg, ' ',
                                                          regex=True)
    else:
        df_data[col_name] = df_data[col_name].str.replace('#', ' ')
