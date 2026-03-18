import math
import pandas as pd
import os

class EnsaioAtrito:
    def __init__(self, distancia=3.03, angulo_graus=6.0, arquivo="ensaio_atrito.csv", separador=";"):
        self.d = distancia
        self.theta = math.radians(angulo_graus)
        self.g = 9.81
        self.arquivo = arquivo
        self.sep = separador
        
        if os.path.exists(self.arquivo):
            self.historico_df = pd.read_csv(self.arquivo, sep=self.sep)
        else:
            self.historico_df = pd.DataFrame()

    def adicionar_teste(self, nome_teste, massa, tempos):
        t_medio = sum(tempos) / len(tempos)
        a_exp = (2 * self.d) / (t_medio ** 2)
        self._processar_e_salvar(nome_teste, massa, t_medio, a_exp, "Cronômetro")

    def adicionar_teste_acelerometro(self, nome_teste, massa, aceleracoes):
        a_media = sum(aceleracoes) / len(aceleracoes)
        self._processar_e_salvar(nome_teste, massa, None, a_media, "Acelerômetro")

    def _processar_e_salvar(self, nome_teste, massa, tempo, aceleracao, metodo):
        # mu = (g*sin(theta) - a) / (g*cos(theta))
        numerador = (self.g * math.sin(self.theta)) - aceleracao
        denominador = self.g * math.cos(self.theta)
        mu = numerador / denominador
        
        novo_resultado = pd.DataFrame([{
            "Configuração": nome_teste,
            "Método": metodo,
            "Massa (kg)": massa,
            "Tempo Médio (s)": round(tempo, 3) if tempo else "N/A",
            "Aceleração (m/s²)": round(aceleracao, 4),
            "Coeficiente (µ)": round(mu, 4)
        }])
        
        self.historico_df = pd.concat([self.historico_df, novo_resultado], ignore_index=True)
        self.historico_df.to_csv(self.arquivo, index=False, sep=self.sep, encoding='utf-8-sig')
        print(f"Teste '{nome_teste}' ({metodo}) processado: µ = {round(mu, 4)}")

projeto = EnsaioAtrito(separador=";")

projeto.adicionar_teste("atrito_70_50_1561", 1.561, [2.87, 2.70, 2.86])
projeto.adicionar_teste("atrito_70_50_3754", 3.754, [2.80, 2.70, 3.14])
projeto.adicionar_teste("atrito_80_60_1561", 1.561, [2.97, 2.90, 2.87])
projeto.adicionar_teste("atrito_80_60_3754", 3.754, [2.93, 2.81, 2.77])
projeto.adicionar_teste("atrito_90_70_1561", 1.561, [2.73, 2.70, 2.68])
projeto.adicionar_teste("atrito_90_70_3754", 3.754, [2.77, 2.84, 2.70])

# projeto.adicionar_teste_acelerometro("atrito_70_50_1561", 1.561, [0.6897])
# projeto.adicionar_teste_acelerometro("atrito_70_50_3754", 3.754, [])
# projeto.adicionar_teste_acelerometro("atrito_80_60_1561", 1.561, [])
# projeto.adicionar_teste_acelerometro("atrito_80_60_3754", 3.754, [])
# projeto.adicionar_teste_acelerometro("atrito_90_70_1561", 1.561, [])
# projeto.adicionar_teste_acelerometro("atrito_90_70_3754", 3.754, [])