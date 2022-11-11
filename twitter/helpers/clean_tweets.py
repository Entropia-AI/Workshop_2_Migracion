
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


def clean_tweets_dataset(df_data, doc_column='tweet', clean_col='cleaned'):
    """Function that receives a dataframe with the tweets
    to clean previous to a model training.

    Args:
        df_data (pd.DataFrame): Tweets dataset, it needs to be on a column
        named tweet
        doc_column (str, optional): Name of the column to clean.
                                    Defaults to 'tweet'.
        clean_col (str, optional): Name of the resulting cleaned column.
                                    Defaults to 'cleaned'.
    Returns:
        pd.DataFrame: Cleaned dataset
    """

    # All to lower case
    df_data[clean_col] = df_data[doc_column].str.lower()

    # Remove numbers, emojis, non ascii chars and
    # replace accent chars by non accented
    df_data[clean_col] = df_data[clean_col].str.replace(r'\d+', '', regex=True)

    df_data[clean_col] = df_data[clean_col].str.normalize('NFKD')
    df_data[clean_col] = df_data[clean_col].str.encode('ascii',
                                                       errors='ignore')
    df_data[clean_col] = df_data[clean_col].str.decode('utf-8')
    df_data = df_data.astype({clean_col: 'str'})

    # Remove links, emails, images, mentions and hashtags
    df_data[clean_col] = df_data[clean_col].str.replace(r'[a-z].twitter.com/[\w]*',
                                                        ' ', regex=True)
    df_data[clean_col] = df_data[clean_col].str.replace(r'[a-z_.+-]+@[a-z-]+\.[a-z-.]+',
                                                        ' ', regex=True)
    df_data[clean_col] = df_data[clean_col].str.replace(r'https?://\S+|www\.\S+',
                                                        ' ', regex=True)
    df_data[clean_col] = df_data[clean_col].str.replace(r'@[^\s]+',
                                                        ' ', regex=True)
    # df_data[clean_col] = df_data[clean_col].str.replace(r'#[^\s]+',
    #                                                     ' ', regex=True)

    # Remove stopwords
    stpwrds_regex = r'\b(?:{})\b'.format('|'.join(STOP_WORDS))
    df_data[clean_col] = df_data[clean_col].str.replace(stpwrds_regex,
                                                        '', regex=True)

    # Remove text laughs (Jajaja or Hahahaha)
    df_data[clean_col] = df_data[clean_col].str.replace(r'\w*(?:[jh][ae]){2,}\w*',
                                                        '', regex=True)

    # Remove non alpahetic charas, single chars
    df_data[clean_col] = df_data[clean_col].str.replace(r'^.{1} | .{1} | .{1}$',
                                                        ' ', regex=True)
    df_data[clean_col] = df_data[clean_col].str.replace(r'[^a-z\s]',
                                                        ' ', regex=True)

    # Remove blank spaces and empty tweets
    df_data[clean_col] = df_data[clean_col].str.replace(r'\s{2,}',
                                                        ' ', regex=True)
    df_data[clean_col] = df_data[clean_col].str.strip()
    df_data = df_data[~ df_data[clean_col].isna()]
    df_data = df_data[df_data[clean_col] != '']

    return df_data
