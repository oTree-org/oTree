# these symbols are a fallback if we don't have an explicit rule
# for the currency/language combination.
# (most common situation is where the language is English)

CURRENCY_SYMBOLS = {
    'AED': 'AED',
    'ARS': '$',
    'AUD': '$',
    'BRL': 'R$',
    'CAD': '$',
    'CHF': 'CHF',
    # need to use yuan character here, that's what gets shown
    # on form inputs. but if you run a study in english, it will
    # still show 元, which is not ideal. but that is rare.
    'CNY': '元',
    'CZK': 'Kč',
    'DKK': 'kr',
    'EGP': 'ج.م.‏',
    'EUR': '€',
    'GBP': '£',
    'HKD': 'HK$',
    'HUF': 'Ft',
    'ILS': '₪',
    'INR': '₹',
    'JPY': '円',
    'KRW': '원',
    'MXN': '$',
    'MYR': 'RM',
    'NOK': 'kr',
    'PLN': 'zł',
    'RUB': '₽',
    'SEK': 'kr',
    'SGD': 'SGD',
    'THB': 'THB',
    'TRY': '₺',
    'TWD': '$',
    'USD': '$',
    'ZAR': 'R',
}


def get_currency_format(lc: str, LO: str, CUR: str) -> str:

    '''because of all the if statements, this has very low code coverage
    but it's ok'''

    ##############################
    # Languages with complex rules
    ##############################

    if lc == 'en':
        if CUR in ['USD', 'CAD', 'AUD']:
            return '$#'
        if CUR == 'GBP':
            return '£#'
        if CUR == 'EUR':
            return '€#'
        if CUR == 'INR':
            return '₹ #'
        if CUR == 'SGD':
            return '$#'
        # override for CNY/JPY/KRW, otherwise it would be written as 원10
        # need to use the chinese character because that's already what's used in
        # form inputs
        if CUR == 'CNY':
            return '#元'
        if CUR == 'JPY':
            return '#円'
        if CUR == 'KRW':
            return '#원'
        return '¤#'

    if lc == 'zh':
        if CUR == 'CNY':
            return '#元'
        if CUR == 'HKD':
            return 'HK$#'
        if CUR == 'TWD':
            return '$#'
        if CUR == 'SGD':
            return 'SGD#'
        return '¤#'

    if lc == 'de':
        if CUR == 'EUR':
            if LO == 'AT':
                return '€ #'
            return '# €'
        if CUR == 'CHF':
            return 'CHF #'
        return '¤ #'

    if lc == 'es':
        if CUR == 'ARS':
            return '$ #'
        if CUR == 'EUR':
            return '# €'
        if CUR == 'MXN':
            return '$#'
        return '# ¤'

    if lc == 'nl':
        if LO == 'BE':
            if CUR == 'EUR':
                return '# €'
            return '# ¤'
        # default NL
        if CUR == 'EUR':
            return '€ #'
        return '¤ #'

    if lc == 'pt':
        if CUR == 'BRL':
            return 'R$#'
        if CUR == 'EUR':
            return '# €'
        return '¤#'

    if lc == 'ar':
        if CUR == 'AED':
            return 'د.إ.‏ #'
        return '¤ #'

    #############################
    # Languages with simple rules
    #############################

    if lc == 'cs':
        if CUR == 'CZK':
            return '# Kč'
        return '# ¤'
    if lc == 'da':
        if CUR == 'DKK':
            return '# kr.'
        return '# ¤'
    if lc == 'fi':
        if CUR == 'EUR':
            return '# €'
        return '# ¤'
    if lc == 'fr':
        if CUR == 'EUR':
            return '# €'
        return '# ¤'
    if lc == 'he':
        if CUR == 'ILS':
            return '# ₪'
        return '# ¤'
    if lc == 'hu':
        if CUR == 'HUF':
            return '# Ft'
        return '# ¤'
    if lc == 'it':
        if CUR == 'EUR':
            return '# €'
        return '# ¤'
    if lc == 'ja':
        if CUR == 'JPY':
            return '#円'
        return '¤#'
    if lc == 'ko':
        if CUR == 'KRW':
            return '#원'
        return '¤#'
    if lc == 'ms':
        if CUR == 'MYR':
            return 'RM#'
        return '¤#'
    if lc == 'nb':
        if CUR == 'NOK':
            return 'kr #'
        return '¤ #'
    if lc == 'pl':
        if CUR == 'PLN':
            return '# zł'
        return '# ¤'
    if lc == 'ru':
        if CUR == 'RUB':
            return '# ₽'
        return '# ¤'
    if lc == 'sv':
        if CUR == 'SEK':
            return '# kr'
        return '# ¤'
    if lc == 'th':
        if CUR == 'THB':
            return 'THB#'
        return '¤#'
    if lc == 'tr':
        if CUR == 'TRY':
            return '# ₺'
        return '# ¤'
    if lc == 'zu':
        if CUR == 'ZAR':
            return 'R#'
        return '¤#'

    # fallback if it's another language, etc.
    return '# ¤'


'''
This file was built by taking common currencies and reverse engineering
the rules using Babel:

curs = [('ar_AE', 'AED'),
 ('ar_EG', 'EGP'),
 ('cmn', 'SGD'),
 ('cs', 'CZK'),
 ('da_DK', 'DKK'),
 ('de', 'EUR'),
 ('de_AT', 'EUR'),
 ('de_CH', 'CHF'),
 ('en_AU', 'AUD'),
 ('en_CA', 'CAD'),
 ('en_GB', 'GBP'),
 ('en_IE', 'EUR'),
 ('en_IN', 'INR'),
 ('en_US', 'USD'),
 ('es_AR', 'ARS'),
 ('es_ES', 'EUR'),
 ('es_MX', 'MXN'),
 ('fi_FI', 'EUR'),
 ('fr_FR', 'EUR'),
 ('he', 'ILS'),
 ('hu_HU', 'HUF'),
 ('it_IT', 'EUR'),
 ('ja', 'JPY'),
 ('ko_KR', 'KRW'),
 ('ms_MY', 'MYR'),
 ('nl_BE', 'EUR'),
 ('nl_NL', 'EUR'),
 ('no', 'NOK'),
 ('pl', 'PLN'),
 ('pt_BR', 'BRL'),
 ('pt_PT', 'EUR'),
 ('ru', 'RUB'),
 ('sv_SE', 'SEK'),
 ('th', 'THB'),
 ('tr_TR', 'TRY'),
 ('zh_CN', 'CNY'),
 ('zh_HK', 'HKD'),
 ('zh_TW', 'TWD'),
 ('zu', 'ZAR')]

for lc, CUR in curs:
    if '_' in lc:
        la, LO = lc.split('_')
    else:
        la, LO = lc, ''
    locale = Locale.parse(lc)
    pattern = locale.currency_formats['standard'].pattern.replace('\\xa4', ' ').replace('#,##0.00', '#')    
    formatted = fc(1.00, currency=CUR, locale=lc)
    print('{}\t{}\t{}\t{}'.format(la, LO, CUR, formatted))

ar	AE	AED	د.إ.‏ 1.00
ar	EG	EGP	ج.م.‏ 1.00
cmn		SGD	SGD1.00
cs		CZK	1,00 Kč
da	DK	DKK	1,00 kr.
de		EUR	1,00 €
de	AT	EUR	€ 1,00
de	CH	CHF	CHF 1.00
en	AU	AUD	$1.00
en	CA	CAD	$1.00
en	GB	GBP	£1.00
en	IE	EUR	€1.00
en	IN	INR	₹ 1.00
en	US	USD	$1.00
es	AR	ARS	$ 1,00
es	ES	EUR	1,00 €
es	MX	MXN	$1.00
fi	FI	EUR	1,00 €
fr	FR	EUR	1,00 €
he		ILS	1.00 ₪
hu	HU	HUF	1,00 Ft
it	IT	EUR	1,00 €
ja		JPY	￥1
ko	KR	KRW	₩1
ms	MY	MYR	RM1.00
nl	BE	EUR	1,00 €
nl	NL	EUR	€ 1,00
no		NOK	kr 1,00
pl		PLN	1,00 zł
pt	BR	BRL	R$1,00
pt	PT	EUR	1,00 €
ru		RUB	1,00 ₽
sv	SE	SEK	1,00 kr
th		THB	THB1.00
tr	TR	TRY	1,00 ₺
zh	CN	CNY	￥1.00
zh	HK	HKD	HK$1.00
zh	TW	TWD	$1.00
zu		ZAR	R1.00

Almost all currencies just put the negative sign in front:

ar	AE	AED -د.إ.‏ 1.00
ar	EG	EGP -ج.م.‏ 1.00
cmn		SGD	-SGD1.00
cs		CZK	-1,00 Kč
da	DK	DKK	-1,00 kr.
de		EUR	-1,00 €
de	AT	EUR	-€ 1,00
de	CH	CHF	CHF-1.00
en	AU	AUD	-$1.00
en	CA	CAD	-$1.00
en	GB	GBP	-£1.00
en	IE	EUR	-€1.00
en	IN	INR	-₹ 1.00
en	US	USD	-$1.00
es	AR	ARS	-$ 1,00
es	ES	EUR	-1,00 €
es	MX	MXN	-$1.00
fi	FI	EUR	-1,00 €
fr	FR	EUR	-1,00 €
he		ILS	-1.00 ₪
hu	HU	HUF	-1,00 Ft
it	IT	EUR	-1,00 €
ja		JPY	-￥1
ko	KR	KRW	-₩1
ms	MY	MYR	-RM1.00
nl	BE	EUR	-1,00 €
nl	NL	EUR	€ -1,00
no		NOK	-kr 1,00
pl		PLN	-1,00 zł
pt	BR	BRL	-R$1,00
pt	PT	EUR	-1,00 €
ru		RUB	-1,00 ₽
sv	SE	SEK	-1,00 kr
th		THB	-THB1.00
tr	TR	TRY	-1,00 ₺
zh	CN	CNY	-￥1.00
zh	HK	HKD	-HK$1.00
zh	TW	TWD	-$1.00
zu		ZAR	-R1.00

In English:

# comment: this is maybe not optimal for our use, 
because experiments in non-USD currencies are usually run locally, 
where people are already familiar with the currency. 
In Canada, people don't write 'CA$1.00', they just write $1.00.

AED en_US AED1.00
EGP en_US E£1.00
SGD en_US $1.00
CZK en_US Kč1.00
DKK en_US kr1.00
EUR en_US €1.00
EUR en_US €1.00
CHF en_US CHF1.00
AUD en_US A$1.00
CAD en_US CA$1.00
GBP en_US £1.00
EUR en_US €1.00
INR en_US ₹1.00
USD en_US $1.00
ARS en_US $1.00
EUR en_US €1.00
MXN en_US MX$1.00
EUR en_US €1.00
EUR en_US €1.00
ILS en_US ₪1.00
HUF en_US Ft1.00
EUR en_US €1.00
JPY en_US ¥1
KRW en_US ₩1
MYR en_US RM1.00
EUR en_US €1.00
EUR en_US €1.00
NOK en_US kr1.00
PLN en_US zł1.00
BRL en_US R$1.00
EUR en_US €1.00
RUB en_US ₽1.00
SEK en_US kr1.00
THB en_US ฿1.00
TRY en_US ₺1.00
CNY en_US CN¥1.00
HKD en_US HK$1.00
TWD en_US NT$1.00
ZAR en_US R1.00

'''