def get_month(number):
    month = ''
    if number == 1:
        month = 'Janeiro'
    elif number == 2:
        month = 'Fevereiro'
    elif number == 3:
        month = 'Marco'
    elif number == 4:
        month = 'Abril'
    elif number == 5:
        month = 'Maio'
    elif number == 6:
        month = 'Junho'
    elif number == 7:
        month = 'Julho'
    elif number == 8:
        month = 'Agosto'
    elif number == 9:
        month = 'Setembro'
    elif number == 10:
        month = 'Outubro'
    elif number == 11:
        month = 'Novembro'
    elif number == 12:
        month = 'Dezembro'
    else:
        raise Exception("Mês inválido")

    return month


ordered_columns = [
    'aid', 'month', 'year', 'reg', 'name', 'role', 'type', 'workplace',
    'active', 'income_total', 'wage', 'perks_total', 'perks_food',
    'perks_food', 'perks_pre_school', 'perks_health', 'perks_birth',
    'perks_housing', 'perks_subsistence', 'perks_others_total',
    'funds_total', 'funds_personal_benefits', 'funds_eventual_benefits',
    'funds_trust_position', 'funds_daily', 'funds_gratification',
    'funds_origin_pos', 'funds_others_total', 'discounts_total',
    'discounts_prev_contribution', 'discounts_ceil_retention',
    'discounts_income_tax', 'discounts_others_total'
]
