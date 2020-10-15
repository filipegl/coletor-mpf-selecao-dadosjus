import pandas as pd
from Util import get_month
from preprocess import process_new, process_old, final_process


class Contracheque:
    def __init__(self, month, year):
        self.month = get_month(month)
        self.year = year

    def __get_urls(self, remun_key, ideniz_key):
        return [
            'http://www.transparencia.mpf.mp.br/conteudo/contracheque/\
{2}/{1}/{2}_{1}_{0}.pdf'.format(self.month, self.year, remun_key),
            'http://www.transparencia.mpf.mp.br/conteudo/contracheque/verbas-inde\
nizatorias-e-outras-remuneracoes-temporarias/{2}/{1}/verbas-indenizatorias-e-outr\
as-remuneracoes-temporarias_{1}_{0}.pdf'
            .format(self.month, self.year, ideniz_key)
            ]

    def get_servidores_ativos(self, old=False):
        url_remuneracao, url_idenizatorias = self.__get_urls(
            'remuneracao-servidores-ativos',
            'servidores-ativos'
        )

        if (old):
            return process_old(url_remuneracao, 'servidor', True)
        else:
            return process_new(
                url_remuneracao, url_idenizatorias, 'servidor', True
            )

    def get_servidores_inativos(self, old=False):
        url_remuneracao, url_idenizatorias = self.__get_urls(
            'provento-servidores-inativos',
            'servidores-inativos'
        )

        if (old):
            return process_old(url_remuneracao, 'servidor', False)
        else:
            return process_new(
                url_remuneracao, url_idenizatorias, 'servidor', False
            )

    def get_membros_ativos(self, old=False):
        url_remuneracao, url_idenizatorias = self.__get_urls(
            'remuneracao-membros-ativos',
            'membros-ativos'
        )

        if (old):
            return process_old(url_remuneracao, 'membro', True)
        else:
            return process_new(
                url_remuneracao, url_idenizatorias, 'membro', True
            )

    def get_membros_inativos(self, old=False):
        url_remuneracao, url_idenizatorias = self.__get_urls(
            'provento-membros-inativos',
            'membros-inativos'
        )

        if (old):
            return process_old(url_remuneracao, 'membro', False)
        else:
            return process_new(
                url_remuneracao, url_idenizatorias, 'membro', False
            )

    def get_pensionistas(self, old=False):
        url_remuneracao, url_idenizatorias = self.__get_urls(
            'valores-percebidos-pensionistas',
            'pensionistas'
        )

        if (old):
            return process_old(url_remuneracao, 'pensionista', False)
        else:
            return process_new(
                url_remuneracao, url_idenizatorias, 'pensionista', False
            )

    def get_colaboradores(self, old=False):
        url_remuneracao, url_idenizatorias = self.__get_urls(
            'valores-percebidos-colaboradores',
            'colaboradores'
        )

        if (old):
            return process_old(url_remuneracao, 'colaborador', True)
        else:
            return process_new(
                url_remuneracao, url_idenizatorias, 'colaborador', True
            )

    def get_all(self, old=False):
        memb_a = self.get_membros_ativos(old=old)
        serv_a = self.get_servidores_ativos(old=old)
        memb_i = self.get_membros_inativos(old=old)
        serv_i = self.get_servidores_inativos(old=old)
        colab = self.get_colaboradores(old=old)
        pens = self.get_pensionistas(old=old)

        return pd.concat(
            [memb_a, serv_a, memb_i, serv_i, colab, pens],
            ignore_index=True
            )

    def write_new_to_csv(self, output):
        df = self.get_all()
        df = final_process(df, self.month, self.year)
        df.to_csv(
            '{0}/contracheque_mpf_{1}_{2}.csv'.format(
                output, self.month, self.year
            ),
            index=False
        )
        return df

    def write_old_to_csv(self, output):
        df = self.get_all(old=True)
        df = final_process(df, self.month, self.year)
        df.to_csv(
            '{0}/contracheque_mpf_{1}_{2}.csv'.format(
                output, self.month, self.year
            ),
            index=False
        )
        return df
