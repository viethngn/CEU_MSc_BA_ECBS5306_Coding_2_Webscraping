import src.const.ps_constants as const
from src.const.ps_pkm_special import SPECIAL_FORMS


def type_effectiveness_converter(eff_code):
    if eff_code == const.NORMAL_EF[0]:
        return const.NORMAL_EF[1]
    elif eff_code == const.SUPER_EF[0]:
        return const.SUPER_EF[1]
    elif eff_code == const.LESS_EF[0]:
        return const.LESS_EF[1]
    else:
        return const.NO_EF[1]


def remove_special_pkm_forms_from_battle_log(log):
    cleaned_log = log
    for base,special in SPECIAL_FORMS.items():
        for form in special:
            cleaned_log = cleaned_log.replace(form, base)
    return cleaned_log

