import pandas as pd
from datetime import datetime, timedelta
import os
import importlib.resources as pkg_resources


class diasuteis:
    def __init__(self):
        # Lê o arquivo de dentro do pacote instalado
        with pkg_resources.open_text(__package__, 'DNU.txt') as file:
            self.dias_nao_uteis = [line.strip() for line in file if line.strip()]
        self.dnu = pd.to_datetime(self.dias_nao_uteis, format='%d/%m/%Y').normalize()

    def is_dia_util(self, date):
        """Verifica se a data fornecida é um dia útil (desconsidera fins de semana e DNU)."""
        # Normaliza a data para que a comparação seja justa
        date = pd.to_datetime(date).normalize()
        # Se a data cair em um fim de semana ou estiver na lista de datas não úteis, retorna False.
        return not (date in self.dnu.values or date.weekday() >= 5)

    def get_dia_util(self, date, days_offset=0):
        """
        Calcula o dia útil ajustado a partir de uma data de referência,
        pulando finais de semana e datas marcadas como não úteis.
        """
        # Normaliza a data de início
        date = pd.to_datetime(date).normalize()
        # Enquanto ainda houver deslocamento ou a data não for dia útil, continua o loop.
        while days_offset != 0 or not self.is_dia_util(date):
            # Incrementa ou decrementa 1 dia conforme o sinal de days_offset
            date += timedelta(days=1 if days_offset >= 0 else -1)
            # Não se esqueça de normalizar após a alteração (garante que a hora continue zerada)
            date = date.normalize()
            # Se a nova data é útil, atualiza o offset
            if self.is_dia_util(date):
                days_offset += 1 if days_offset < 0 else -1
        return date

    def hoje(self, days_offset=0):
        """
        Retorna o dia útil de hoje com deslocamento (positivo ou negativo) em dias úteis.
        Exemplo:
            du.hoje()      --> retorna o dia útil de hoje;
            du.hoje(-1)    --> retorna o último dia útil;
            du.hoje(+2)    --> retorna o dia útil daqui a dois dias úteis.
        """
        # Garante que a data "hoje" esteja normalizada (sem hora) para evitar comparações erradas
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        dia_util = self.get_dia_util(base_date, days_offset)
        return dia_util.strftime('%Y-%m-%d')

    def qntdu(self, data_inicio, data_fim):
        """
        Retorna a quantidade de dias úteis entre duas datas.
        Aceita datas no formato 'YYYY-MM-DD' ou variáveis datetime.
        """
        data_inicio = pd.to_datetime(data_inicio).normalize()
        data_fim = pd.to_datetime(data_fim).normalize()

        if data_inicio > data_fim:
            raise ValueError("A data de início não pode ser maior que a data de fim.")

        dias = pd.date_range(start=data_inicio, end=data_fim)
        dias_uteis = [dia for dia in dias if self.is_dia_util(dia)]
        return len(dias_uteis)

    def help(self):
        print("""
        Funções disponíveis:

        1. du.hoje(days_offset=0):
            Retorna o dia útil de hoje com deslocamento (positivo ou negativo) em dias úteis.
            Exemplo: 
                du.hoje() retorna o dia útil de hoje.
                du.hoje(-1) retorna o último dia útil.
                du.hoje(+2) retorna o dia útil daqui a dois dias úteis.

        2. du.qntdu(data_inicio, data_fim):
            Retorna a quantidade de dias úteis entre duas datas.
            Aceita datas no formato 'YYYY-MM-DD' ou variáveis datetime.
            Exemplo:
                du.qntdu('2024-01-01', '2024-01-10') retorna a quantidade de dias úteis entre as datas.

        Criador: Lucas Soares (lanceluks@gmail.com)
        """)

    def criador(self):
        print("Lucas Soares, lanceluks@gmail.com")
