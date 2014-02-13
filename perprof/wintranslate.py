"""
This translate the axis name in Windows.
"""

LANG='en'
def translate(_str):
    if _str == 'Performance Ratio':
        if LANG in ['en', 'en_US']:
            return 'Performance Ratio'
        elif LANG == ['pt', 'pt_BR', 'pt_PT']:
            return "Raz\~{a}o de Desempenho"
    elif _str == 'Problems solved':
        if LANG in ['en', 'en_US']:
            return 'Performance Ratio'
        elif LANG == ['pt', 'pt_BR', 'pt_PT']:
            return "Problemas resolvidos"
