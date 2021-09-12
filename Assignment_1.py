# This part, the symbol set is defined as the charactors from 32 to 126 in ASCII
# 1.1 Caesar Cipher
def caesar_cipher(message, shift, encrpt):
    # creat a list named list_de to store the decrypt
    list_de = []
    # creat a list named list_en to store the encrypt
    list_en = []

    if encrpt:  # when encrypt is true, it will encrypt the message
        for i in message:
            # to make sure about the charactor can be looped from 32 to 126 in ASCII
            temp = (ord(i) - 32 + int(shift)) % (126 - 32 + 1) + 32
            list_en.append(chr(temp))
        encrypt = ''.join(list_en)
        return encrypt
    else:   # when encrypt is false, it will decrypt the message
        for i in message:
            # to make sure about the charactor can be looped from 32 to 126 in ASCII
            temp = (ord(i) - 32 - int(shift)) % (126 - 32 + 1) + 32
            list_de.append(chr(temp))
    # convert the list_de to string
        decrypt = ''.join(list_de)
        return decrypt


# 1.2 Vigenere Cipher
def vigenere_cipher(message, keyword, encrpt):
    # creat a list named list_de to store the decrypt
    list_de = []
    # creat a list named list_en to store the encrypt
    list_en = []
    list_keyword = list(keyword)

    if encrpt:  # when encrypt is true, it will encrypt the message
        for i in range(len(message)):
            # reuse the function caesar_cipher() to get the encrypt for each charactor in the message
            list_en.append(caesar_cipher(message[i], ord(list_keyword[i % len(keyword)]), True))
        encrypt = ''.join(list_en)
        return encrypt
    else:   # when encrypt is false, it will decrypt the message
        for i in range(len(message)):
            # reuse the function caesar_cipher() to get the decrypt for each charactor in the message
            list_de.append(caesar_cipher(message[i], ord(list_keyword[i % len(keyword)]), False))
        decrypt = ''.join(list_de)
        return decrypt


# From this part, the symbol set will be redefined as '''ABCDEFGHIJKLMNOPQRSTUVWXYZ '''-from capital A to capital Z and with a space.
# 2.1
# the difference between this function and dycrypt_ceasar() in 2.4.1 is:
# 1).the range of the symbols
# 2).whether we need to ignore the spaces in cipher
# This function, the symbol set is defined as the characters from A to Z in ASCII and ignore all the spaces
def dycrypt_caesar_sipmlecrack(cipher, shift):

    message_capital = ''.join(cipher).upper()
    # creat a list named list_de to store the decrypt
    list_de = []

    for i in message_capital:
        # ignore
        if i == ' ':
            list_de.append(' ')
            continue
        # to make sure about the characters can be looped in the symbol set
        temp = ((ord(i) - 65) - int(shift)) % 26 + 65
        list_de.append(chr(temp))
    decrypt = ''.join(list_de)
    return decrypt


# 2.2
def frequency_analysis(message):
    # create a new dictionary to store every character's frequency in the message and all the values default as 0
    frequency_dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0,
                      'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0,
                      'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
                      'Y': 0, 'Z': 0, ' ': 0}
    # use function upper() to let each char in message be capital
    message_capital = ''.join(message).upper()

    for i in message_capital:
        # use function count to get the number of a char in the message and calculate its frequency
        frequency_dict[i] = (message_capital.count(i) / len(message_capital))

    return frequency_dict

# 2.3 Cross-Correlation
def Cross_Correlation(dict1, dict2):
    # get the dictionary from dict1 and dict2
    # the keys is value from the table in the assignment1
    # the values is set from the table in the assignment1
    dict_1 = dict.copy(dict1)
    dict_2 = dict.copy(dict2)

    # declare a vairable as double to store the cross_correlation between set1 and set2
    cross_correlation = 0
    for i in dict_1.keys():
        for j in dict_2.keys():
            if i == j:  # when two dictionaries have the same value, we can calculate its cross_correlation
                cross_correlation += dict_1[i] * dict_2[j]
                continue    # to end this loop to calculate the next value's cross_correlation
    return cross_correlation

# 2.4.1 Caeser Cracking

def get_caesar_shift(enc_message, expected_dist):
    # define the new symbol set and its length
    symbols = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ '''
    sym_len = len(symbols)
    # create an empty dictionary to store each character in cipher and its mapping frequency
    cipher_dict = {}
    # use function sorted() to make every char's frequency be in descending order
    cipher_dict.update(sorted(frequency_analysis(''.join(enc_message).upper()).items(), key=lambda a:a[1], reverse=True))

    # create an empty dictionary to store possible shift
    dict_shift = {}
    # use a loop (from shift = 1 to shift = 27) to calculate the cross_correlation for each shift
    # because the length of symbols is 27
    shift = 1
    for s in range(1, 28):
        res = 0
        for i in cipher_dict.keys():
            # to make sure about the characters can be looped in the symbol set
            tmp = (symbols.index(i) - s + 27) % 27
            # calculate the cross correlation
            res += cipher_dict[i] * expected_dist[symbols[tmp]]
        dict_shift[res] = s
    # The shift we need is the value of the largest element mapping in the dict_shift.keys()
    shift = dict_shift[max(dict_shift.keys())]
    return shift

# This function, the symbol set is the characters from A to Z and space and all shifts need to think about space
def dycrypt_caesar(cipher, shift):
    # define the new symbol set and its length
    symbols = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ '''
    sym_len = len(symbols)
    # creat a list named list_de to store the decrypt
    list_de = []

    for i in cipher:
        # to make sure about the characters can be looped in the symbol set
        temp = (symbols.index(i) - int(shift) + 27) % 27
        list_de.append(symbols[temp])
    decrypt = ''.join(list_de)
    return decrypt

# 2.4.2  Vigenere Cracking

def get_vigenere_keyword(enc_meeage, size, expected_dist):
    # define the new symbol set and its length
    symbols = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ '''
    sym_len = len(symbols)
    # create an empty dictionary to store each charactor in cipher and its mapping frequency
    cipher_dict = {}
    # use function sorted() to make every char's frequency be in descending order
    cipher_dict.update(sorted(frequency_analysis(''.join(enc_meeage).upper()).items()
                              , key=lambda a: a[1], reverse=True))

    # Keep the message in "size" columns
    # Each column can be regarded as a Ceasar Cipher because they have the same letter to encrypt
    # Divide the message into the required parts according to the order of the columns
    # create an empty dictionary to store the index of the letter in a keyword and its mapping cipher
    enc_meeage_dict = {}
    for i in range(1, size + 1):
        # create a list as temp to store the cipher with the same letter to encrypt
        lst_tmp = []
        for j in range(len(enc_meeage)):
            # to be sure that all the char in the same column can be added to lst_temp
            if j % size == i - 1:
                lst_tmp.append(enc_meeage[j])
        enc_meeage_dict[i] = str(''.join(lst_tmp))


    # create an empty list to store the shift for each cipher which's in the same columnn
    lst_shift = []
    for i in enc_meeage_dict.keys():
        str_cipher = ''.join(enc_meeage_dict[i])
        # reuse function get_caesar_shift() to get the most possible shift for the cipher
        lst_shift.append(get_caesar_shift(str_cipher, expected_dist))

    # create an empty list to store the letter for keyword
    lst_keyword = []
    for i in lst_shift:
        lst_keyword.append(symbols[i % 27])

    # get the keyword and retrun
    str_keyword = ''.join(lst_keyword)
    return str_keyword

def decrypt_vigenere(enc_message, keyword):
    # define the new symbol set and its length
    symbols = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ '''
    sym_len = len(symbols)
    # creat an empty list named list_en to store the encrypt
    list_de = []

    # set a loop for decrypt from 0 to len(cipher)-1
    for i in range(len(enc_message)):
        # shift depens on the current order for i and its value equals to i mod len(keyword)
        shift = symbols.index(keyword[i % len(keyword)])
        # to make sure about the characters can be looped in the symbol set
        cipher = symbols.index(enc_message[i])
        tmp = (cipher - shift + 27) % 27
        list_de.append(symbols[tmp])

    # get the decrypt and return
    decrypt = ''.join(list_de)
    return decrypt





if __name__=='__main__':
    # assign some value to variables as samples
    message = "I am a wfu student"

    cipher1 = "plorefrphevgl wbof ner va uvtu qrznaq naq vg qbrf abg frrz yvxr gur " \
             "arrq sbe zber frphevgl cebsrffvbanyf vf tbvat naljurer va gur " \
             "sberfrrnoyr shgher"

    cipher2 = "Cqn arpqcb xo nenah vjw jan mrvrwrbqnm fqnw cqn arpqcb xo xwn vjw jan cqanjcnwnm"

    cipher3 = "JAMPWFAUIFAHJSI"

    # required expected_dist of the question
    expected_dist = {' ': .1828846265,'E': .1026665037, 'T': .0751699827, 'A': .0653216702, 'O': .0615957725,
                    'N': .0571201113,'I': .0566844326,'S': .0531700534,'R': .0498790855,'H': .0497856396,
                    'L': .0331754796,'D': .0328292310,'U': .0227579536,'C': .0223367596,'M': .0202656783,
                    'F': .0198306716,'W': .0170389377, 'G': .0162490441,'P': .0150432428,'Y': .0142766662,
                    'B': .0125888074,'V': 0.0079611644, 'K': 0.0056096272,'X': 0.0014092016,'J': 0.0009752181,
                    'Q': 0.0008367550,'Z': 0.0005128469}

    # test samples for get_vigenere_keyword() and dycrypt_vigenere ()
    m1 = "PFAAP T FMJRNEDZYOUDPMJ AUTTUZHGLRVNAESMJRNEDZYOUDPMJ YHPD NUXLPASBOIRZTTAHLTM QPKQCFGBYPNJMLO " \
         "GAFMNUTCITOMD BHKEIPAEMRYETEHRGKUGU TEOMWKUVNJRLFDLYPOZGHR RDICEEZB NMHGP " \
         "FOYLFDLYLFYVPLOSGBZFAYFMTVVGLPASBOYZHDQREGAMVRGWCEN YP ELOQRNSTZAFPHZAYGI LVJBQSMCBEHM AQ VUMQNFPHZ AMTARA " \
         "YOTVU LTULTUNFLKZEFGUZDMVMTEDGBZFAYFMTVVGLCATFFNVJUEIAUTEEPOG LANBQSMPWESMZRDTRTLLATHBZSFGFMLVJB " \
         "UEGUOTAYLLHACYGEDGFMNKGHR FOYDEMWHXIPPYD NYYLOHLKXYMIK AQGUZDMPEX QLZUNRKTMNQGEMCXGWXENYTOHRJDD " \
         "NUXLBNSUZCRZT RMVMTEDGXQMAJKMTVJTMCPVNZTNIBXIFETYEPOUZIETLL IOBOHMJUZ YLUP " \
         "FVTTUZHGLRVNAESMHVFSRZTMNQGWMNMZMUFYLTUN VOMTVVGLFAYTQXNTIXEMLQERRTYLCKIYCSRJNCIFETXAIZTOA GVQ GZYP FVTOE " \
         "ZHC QPLDIQLGESMTHZIFVKLCATFFNVJUEIAULLA KTORVTBZAYPSQ AUEUNRGNDEDZTRODGYIPDLLDI NTEHRPKLVVLPD "
    m2 = "TEZHRAIRGMQHNJSQPTLNZJNEVMQHRXAVASLIWDNFOELOPFWGZ UHSTIRGLUMCSW GTTQCSJULNLQK OHL " \
         "MHCMPWLCEHTFNUHNPHTSFFADJHTLNBYORWEFRYE PIISO K ZQR " \
         "GMPTLQCSPRMOCMKESMTYLUTFRMIEOWXXFMWECCLWSQGWUASSWFGTTMYSGUL QNQGEFGTTIDSWMOAGMKEOQL U KOVN  " \
         "AMZHZRGACMKHZRHSQLKLBMJAXTKLVRGFCBTLNAM SMYAHEGIEHTKNFOELNBMWFGORHWTPAY MVOSGUVUSPD "
    m3 = "HYMUANDCHQNHOPOK ZDBFBQVZUTY QVZTYLFAHNRCFBZVA QCHVVUIP  KLZ " \
         "FYHRHNHCQOHMKUKOTQXLIXYROHMUEEOVEVCVIMQPIWBCPTMM CKSQNCNIBFFZCNVPORZZ EL BMXTGAORVY " \
         "CKPBFTEFXHYMUANDCHQNHOXXIHV NYFXMUPCOHQW  VETQCVLWBOENUAPVORZNIHFRZIF KKHVTFIIBBTMUTG " \
         "WDWFOIVOZVUMCKMQKVSGPOJPZ NYFXMUTTYXDQHGBAPJIUSGQGQABAVXREUZ HOCCHJUDIXTHMUTSTZTFAP TQNVCGXFVKIGPFHZWH " \
         "CKSQNCNIBFFZCNVXQZWGEVOXT UFKKPDKCANXPDLUMGAXTIF CMDBQXAVFCD UATBOFZCVCQTQIHDBLUJMH ELBJICNBMTH INCI " \
         "OHCDGKHZNCADITQQHFQOARACOPXPJAVCMBFIHQHGQWVZUOTDPDQTEFXRHQGEBDFEBJSBLFQJOSKKTI " \
         "UCQJDVACTQOGQKVNBQPAMUAFSPDAVGGXCWHNHKPOZV OTJPJQINBCCHHZCQKCCQX TBPIWHSBLFQWNHGOOHMQATAGQQH " \
         "CASZACOPXHYMUATQXWQXICIOZVNENIXXMHCGXGO NEOPOWIXEBQWVHLIUHOENURQDIVHYAVYOZVDEEQXEVUMCIXTQIUUIMQ " \
         "ZNVXHEHYIUOIFAUNGRFRTUNGQKEZESBCIDKNIQKPBQNYBIXAMUMKPRBIMSKCXTINIQKOENUFC " \
         "TQZZCQDBZACOPXXCIAEUXHEHVLNLKQINTC ZVZM VLOV XARBOUMNEEQXEVUCQJDRVCEUXHYIN ROCJMXTBQFRQHIPDORTAOTFHYUM " \
         "CKSQBMETXSRAV YF BHWEBAXWNZRGKHZINEFXXDHNHGFFQNCENAGQNLOOXREUJAPFTIHNHCQOIB FGOOWZIMBQWVH IPYBTQVLBOXISM " \
         "QCOSMCNIXTNXFOKQTUHBEP TQQN KPOYQAHNVOZUJOTQPDAUTQXTD ORGXHYIN FYHRHCSBOTTMCVGAOEVFYBCFEUUTTRGJMY " \
         "ULIHKZSBYBUHJRQQTTAZDBAIHQHGBRGV "

    # 2.1  Simple Cracks by Hands
    # dycrypt_caesar_sipmlecrack()
    # take the sample 2.1 in the assianment_1 as a test cipher and name it as cipher2
    # the difference between this function and dycrypt_ceasar() in 2.4.1 is:
    # 1).the range of the symbols
    # 2).whether we need to ignore the spaces in cipher
    # This function, the symbol set is defined as the characters from A to Z in ASCII and ignore all the spaces
    print('# 2.1  Simple Cracks by Hands')
    shitf_caesar = 1
    while shitf_caesar < 28:
        dycrypt_cae = dycrypt_caesar_sipmlecrack(cipher2, shitf_caesar)
        # to show all of the steps for decrypting this cipher
        print("Step", shitf_caesar, ": ", dycrypt_cae)
        shitf_caesar += 1
    print('')


    # 2.2 Frequency Analysis
    # frequency_analysis()
    # take "AB CD" in the assignment_1 2.2 as a test input
    print('# 2.2 Frequency Analysis')
    print(frequency_analysis('AB CD'))
    print('')



    # 2.3 Cross-Correlation
    # Cross-Correlation()
    # take set_1, set_2, set_3 and "ABCDE" in the assignment_1 2.2 as a test input
    # create dictionaties to calculate the cross correlation easily
    print('2.3 Cross-Correlation')
    set_1 = {'A': 0.012, 'B': 0.003, 'C': 0.01, 'D': 0.1, 'E': 0.02, 'F': 0.001}
    set_2 = {'A': 0.001, 'B': 0.012, 'C': 0.003, 'D': 0.01, 'E': 0.1, 'F': 0.02}
    set_3 = {'A': 0.1, 'B': 0.02, 'C': 0.001, 'D': 0.012, 'E': 0.003, 'F': 0.01}
    print(Cross_Correlation(set_1, set_2))
    print(Cross_Correlation(set_2, set_3))
    print(Cross_Correlation(set_1, set_3))
    print('')



    # 2.4.1 Caeser Cracking
    # get_caesar_shift()
    # dycrypt_caesar()
    # take cipher3 as a test input and use function decrypt_ceasar() to get decrypt
    print('2.4.1 Caeser Cracking')
    shift = get_caesar_shift(cipher3, expected_dist)
    print(shift)
    # This function, the symbol set is the characters from A to Z and space and all shifts need to think about space
    dycrypt_caesar = dycrypt_caesar(cipher3, shift)
    print(dycrypt_caesar)
    print('')



    # 2.4.2 Vigenere Cracking
    # get_vigenere_keyword()
    # dycrypt_vigenere()
    print('2.4.2V igenere Cracking')
    # set a possible range for keyword's size and find a meaningful keyword
    for size in range(1, 20):
        key_word = get_vigenere_keyword(m3, size, expected_dist)
        print("The size is ", size, ", and the keyword is ",key_word)
    # use dycrypt_vigenere() and take m3 as cipher to get its keyword and its decrypt
    dycrypt_vigenere = decrypt_vigenere(m3, "PRIVACY")
    print(dycrypt_vigenere)
