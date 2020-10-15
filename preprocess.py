import pandas as pd
import tabula
import re
from map_colum import ideniz, remun, remun_old
from Util import ordered_columns


def get_remun_dfs(url_remuneracao):
    remuneracao_dfs = tabula.read_pdf(
        url_remuneracao,
        pages='all',
        pandas_options={'header': None},
        lattice=True
    )
    return remuneracao_dfs


def get_dfs(url_remuneracao, url_idenizatorias):
    remuneracao_dfs = get_remun_dfs(url_remuneracao)
    idenizatorias_dfs = tabula.read_pdf(
        url_idenizatorias,
        pages='all',
        pandas_options={'header': None},
        lattice=True
    )
    return remuneracao_dfs, idenizatorias_dfs


def process_new(url_remuneracao, url_idenizatorias, _type, active):
    remuneracao_dfs, idenizatorias_dfs = \
        get_dfs(url_remuneracao, url_idenizatorias)

    rem_df = process_remuneracao_new(remuneracao_dfs)
    ideniz_df = process_idenizatorias(idenizatorias_dfs)
    merged_df = pd.merge(rem_df, ideniz_df, on=['reg'], how='outer')
    merged_df['type'] = _type
    merged_df['active'] = active

    return merged_df


def process_old(url_remuneracao, _type, active):
    remuneracao_dfs = get_remun_dfs(url_remuneracao)

    rem_df = process_remuneracao_old(remuneracao_dfs)

    rem_df['type'] = _type
    rem_df['active'] = active
    return rem_df


def clean_money(m):
    m = re.sub(r'-|\.|R\$|\(|\)', '', str(m))
    m = m.replace(',', '.')
    return float(m)


def process_remuneracao_old(remuneracao_dfs):
    remuneracao_df = pd \
        .concat(remuneracao_dfs, ignore_index=True) \
        .dropna() \
        .reset_index(drop=True) \
        .rename(columns={
            remun_old['nome']: 'name',
            remun_old['cargo']: 'role',
            remun_old['lotacao']: 'workplace',
            remun_old['rem_cargo']: 'wage',
            remun_old['brutos']: 'income_total',
            remun_old['total_descontos']: 'discounts_total',
            remun_old['previdenciaria']: 'discounts_prev_contribution',
            remun_old['teto']: 'discounts_ceil_retention',
            remun_old['imposto_renda']: 'discounts_income_tax',
            remun_old['confianca']: 'funds_trust_position',
            remun_old['grat_natal']: 'funds_eventual_benefits',
            remun_old['idenizacoes']: 'perks_total',
            remun_old['outras_rem_temporarias']: 'funds_others_total'
        })

    for categ in remuneracao_df.columns[4:]:
        remuneracao_df[categ] = remuneracao_df[categ].apply(clean_money)

    remuneracao_df['funds_eventual_benefits'] += \
        remuneracao_df[remun['ferias_constitucional']] + \
        remuneracao_df[remun['abono_permanencia']]

    remuneracao_df['funds_total'] = remuneracao_df['funds_trust_position'] + \
        remuneracao_df['funds_eventual_benefits']

    remuneracao_df['reg'] = ''
    remuneracao_df['perks_food'] = 0.0
    remuneracao_df['perks_transportation'] = 0.0
    remuneracao_df['perks_pre_school'] = 0.0
    remuneracao_df['perks_birth'] = 0.0
    remuneracao_df['perks_housing'] = 0.0
    remuneracao_df['perks_subsistence'] = 0.0
    remuneracao_df['funds_personal_benefits'] = 0.0
    remuneracao_df['funds_gratification'] = 0.0
    remuneracao_df['perks_housing'] = 0.0
    remuneracao_df['perks_housing'] = 0.0

    remuneracao_df = remuneracao_df.drop(columns=[
        col for col in remuneracao_df.columns if type(col) == int
    ])

    return remuneracao_df


def process_remuneracao_new(remuneracao_dfs):
    remuneracao_df = pd \
        .concat(remuneracao_dfs, ignore_index=True) \
        .dropna() \
        .reset_index(drop=True) \
        .rename(columns={
            remun['matricula']: 'reg',
            remun['nome']: 'name',
            remun['cargo']: 'role',
            remun['lotacao']: 'workplace',
            remun['rem_cargo']: 'wage',
            remun['brutos']: 'income_total',
            remun['total_descontos']: 'discounts_total',
            remun['previdenciaria']: 'discounts_prev_contribution',
            remun['teto']: 'discounts_ceil_retention',
            remun['imposto_renda']: 'discounts_income_tax',
            remun['confianca']: 'funds_trust_position',
            remun['grat_natal']: 'funds_eventual_benefits',
            remun['verbas_idenizatorias']: 'perks_total'

        })

    for categ in remuneracao_df.columns[4:]:
        remuneracao_df[categ] = remuneracao_df[categ].apply(clean_money)

    remuneracao_df['funds_eventual_benefits'] += \
        remuneracao_df[remun['ferias_constitucional']] + \
        remuneracao_df[remun['abono_permanencia']]

    remuneracao_df['reg'] = remuneracao_df['reg'].apply(lambda x: str(int(x)))

    remuneracao_df = remuneracao_df.drop(columns=[
        col for col in remuneracao_df.columns if type(col) == int
    ])

    return remuneracao_df


def process_idenizatorias(idenizatorias_dfs):
    idenizatorias_df = pd \
        .concat(idenizatorias_dfs, ignore_index=True) \
        .dropna() \
        .reset_index(drop=True) \
        .rename(columns={
            ideniz['matricula']: 'reg',
            ideniz['alimentacao']: 'perks_food',
            ideniz['transporte']: 'perks_transportation',
            ideniz['creche']: 'perks_pre_school',
            ideniz['natalidade']: 'perks_birth',
            ideniz['aux_moradia']: 'perks_housing',
            ideniz['ajuda_custo']: 'perks_subsistence',
            ideniz['transporte_mobiliario']: 'perks_others_total',
            ideniz['total_temporarias']: 'funds_total',
            ideniz['grat_pericia_projeto']: 'funds_gratification',
            ideniz['outras_retroativas_temporarias']: 'funds_others_total',
            ideniz['noturno']: 'funds_personal_benefits'
        }) \
        .drop(columns=[ideniz['nome'], ideniz['cargo'], ideniz['lotacao']])

    for categ, col in idenizatorias_df.items():
        idenizatorias_df[categ] = col.apply(clean_money)

    idenizatorias_df['perks_others_total'] += \
        idenizatorias_df[ideniz['abono_pecuniario']] + \
        idenizatorias_df[ideniz['premio_pecunia']]

    idenizatorias_df['funds_gratification'] += \
        idenizatorias_df[ideniz['grat_exercicio_cumulativo']] + \
        idenizatorias_df[ideniz['grat_encargo_curso_concurso']] + \
        idenizatorias_df[ideniz['grat_local']]

    idenizatorias_df['funds_others_total'] += \
        idenizatorias_df[ideniz['outras_remuneratorias']]

    idenizatorias_df['funds_personal_benefits'] += \
        idenizatorias_df[ideniz['atividade_penosa']] + \
        idenizatorias_df[ideniz['insalubridade']]

    idenizatorias_df['reg'] = \
        idenizatorias_df['reg'].apply(lambda x: str(int(x)))

    idenizatorias_df = idenizatorias_df.drop(columns=[
        col for col in idenizatorias_df.columns if type(col) == int
    ])

    return idenizatorias_df


def final_process(df, month, year):
    df['aid'] = 'mpf'
    df['month'] = month
    df['year'] = year
    df['perks_health'] = 0.0
    df['funds_daily'] = 0.0
    df['funds_origin_pos'] = 0.0
    df['discounts_others_total'] = 0.0

    df['perks_total'] = df['perks_total'].fillna(0.0)
    df['funds_total'] = df['funds_total'].fillna(0.0)
    df['discounts_total'] = df['discounts_total'].fillna(0.0)
    df['discounts_prev_contribution'] = \
        df['discounts_prev_contribution'].fillna(0.0)

    df = df[ordered_columns]
    return df
