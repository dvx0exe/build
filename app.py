from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'davi123',  
    'database': 'personagens_bd'
}

class Personagem:
    def __init__(self, nome, idade, classe):
        self.__nome = nome
        self.__idade = idade
        self.__classe = classe
        self.__equipamento = []
        self.__roupas = []
        self.__vigor = 0
        self.__mente = 0
        self.__fortitude = 0
        self.__forca = 0
        self.__destreza = 0
        self.__inteligencia = 0
        self.__fe = 0
        self.__arcano = 0
        self.__build_escolhida = ""
        self.__raca = ""
        self.__sexo = ""

    def __str__(self):
        msg = f"Nome: {self.nome}\n"
        msg += f"Idade: {self.idade}\n"
        msg += f"Classe: {self.classe}\n"
        msg += f"Raça: {self.raca}\n"
        msg += f"Sexo: {self.sexo}\n"
        msg += f"Vigor: {self.vigor}\n"
        msg += f"Mente: {self.mente}\n"
        msg += f"Fortitude: {self.fortitude}\n"
        msg += f"Força: {self.forca}\n"
        msg += f"Destreza: {self.destreza}\n"
        msg += f"Inteligência: {self.inteligencia}\n"
        msg += f"Fé: {self.fe}\n"
        msg += f"Arcano: {self.arcano}\n"
        msg += "Equipamento: " + ", ".join(self.equipamento) + "\n"
        msg += "Roupa: " + ", ".join(self.roupas) + "\n"
        msg += f"Build escolhida: {self.build_escolhida}\n"
        return msg


    @property
    def nome(self):
        return self.__nome

    @property
    def idade(self):
        return self.__idade

    @property
    def classe(self):
        return self.__classe

    @property
    def vigor(self):
        return self.__vigor

    @vigor.setter
    def vigor(self, valor):
        self.__vigor = valor

    @property
    def mente(self):
        return self.__mente

    @mente.setter
    def mente(self, valor):
        self.__mente = valor

    @property
    def fortitude(self):
        return self.__fortitude

    @fortitude.setter
    def fortitude(self, valor):
        self.__fortitude = valor

    @property
    def forca(self):
        return self.__forca

    @forca.setter
    def forca(self, valor):
        self.__forca = valor

    @property
    def destreza(self):
        return self.__destreza

    @destreza.setter
    def destreza(self, valor):
        self.__destreza = valor

    @property
    def inteligencia(self):
        return self.__inteligencia

    @inteligencia.setter
    def inteligencia(self, valor):
        self.__inteligencia = valor

    @property
    def fe(self):
        return self.__fe

    @fe.setter
    def fe(self, valor):
        self.__fe = valor

    @property
    def arcano(self):
        return self.__arcano

    @arcano.setter
    def arcano(self, valor):
        self.__arcano = valor

    @property
    def equipamento(self):
        return self.__equipamento

    @equipamento.setter
    def equipamento(self, valor):
        self.__equipamento = valor

    @property
    def roupas(self):
        return self.__roupas

    @roupas.setter
    def roupas(self, valor):
        self.__roupas = valor

    @property
    def build_escolhida(self):
        return self.__build_escolhida

    @build_escolhida.setter
    def build_escolhida(self, valor):
        self.__build_escolhida = valor

    @property
    def raca(self):
        return self.__raca

    @raca.setter
    def raca(self, valor):
        self.__raca = valor

    @property
    def sexo(self):
        return self.__sexo
    
    @sexo.setter
    def sexo(self, valor):
        self.__sexo = valor

class Heroi(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Heroi")
        self.vigor = 14
        self.mente = 9
        self.fortitude = 12
        self.forca = 16
        self.destreza = 9
        self.inteligencia = 7
        self.fe = 8
        self.arcano = 11
        self.equipamento = ["Machado de batalha", "Escudo de couro"]

class Bandido(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Bandido")
        self.vigor = 10
        self.mente = 11
        self.fortitude = 10
        self.forca = 9
        self.destreza = 13
        self.inteligencia = 9
        self.fe = 8
        self.arcano = 14
        self.equipamento = ["Faca", "Arco curto"]

class Astrologo(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Astrologo")
        self.vigor = 9
        self.mente = 15
        self.fortitude = 9
        self.forca = 8
        self.destreza = 12
        self.inteligencia = 16
        self.fe = 7
        self.arcano = 9
        self.equipamento = ["Cajado", "Grimório"]

class Guerreiro(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Guerreiro")
        self.vigor = 15
        self.mente = 10
        self.fortitude = 14
        self.forca = 16
        self.destreza = 12
        self.inteligencia = 8
        self.fe = 9
        self.arcano = 7
        self.equipamento = ["Espada longa", "Escudo de metal"]

class Prisioneiro(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Prisioneiro")
        self.vigor = 11
        self.mente = 12
        self.fortitude = 11
        self.forca = 11
        self.destreza = 14
        self.inteligencia = 14
        self.fe = 6
        self.arcano = 9
        self.equipamento = ["Estoque", "Correntes"]

class Confessor(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Confessor")
        self.vigor = 10
        self.mente = 13
        self.fortitude = 10
        self.forca = 10
        self.destreza = 12
        self.inteligencia = 13
        self.fe = 16
        self.arcano = 9
        self.equipamento = ["Maça", "Tomo sagrado"]

class Miseravel(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Miseravel")
        self.vigor = 10
        self.mente = 10
        self.fortitude = 10
        self.forca = 10
        self.destreza = 10
        self.inteligencia = 10
        self.fe = 10
        self.arcano = 10
        self.equipamento = ["Porrete"]

class Vagabundo(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Vagabundo")
        self.vigor = 11
        self.mente = 10
        self.fortitude = 10
        self.forca = 10
        self.destreza = 13
        self.inteligencia = 9
        self.fe = 14
        self.arcano = 7
        self.equipamento = ["Adaga", "Escudo pequeno"]

class Profeta(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Profeta")
        self.vigor = 10
        self.mente = 14
        self.fortitude = 8
        self.forca = 11
        self.destreza = 10
        self.inteligencia = 7
        self.fe = 16
        self.arcano = 10
        self.equipamento = ["Lança", "Talismã"]

class Samurai(Personagem):
    def __init__(self, nome, idade):
        super().__init__(nome, idade, "Samurai")
        self.vigor = 12
        self.mente = 11
        self.fortitude = 13
        self.forca = 15
        self.destreza = 15
        self.inteligencia = 9
        self.fe = 8
        self.arcano = 8
        self.equipamento = ["Katana", "Arco longo"]

class Builds:
    @staticmethod
    def build_heroi(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Herói (1-3): ")
        
        if escolha == "1":
            personagem.forca += 20
            personagem.vigor += 18
            personagem.fortitude += 15
            personagem.roupas.append("Armadura de Cavaleiro")
            personagem.equipamento.append("Espada Lendária")
            build_nome = "Força do Destino"
        elif escolha == "2":
            personagem.forca += 18
            personagem.destreza += 16
            personagem.vigor += 14
            personagem.roupas.append("Cota de Malha Real")
            personagem.equipamento.append("Machado de Guerra")
            build_nome = "Espírito Indomável"
        elif escolha == "3":
            personagem.forca += 22
            personagem.vigor += 16
            personagem.fortitude += 14
            personagem.roupas.append("Túnica do Herói")
            personagem.equipamento.append("Martelo de Guerra")
            build_nome = "Herói Ancestral"
        else:
            print("Build inválida para Herói! Usando 'Nenhuma' como padrão.")
        
        return build_nome

    @staticmethod
    def build_bandido(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Bandido (1-3): ")
        if escolha == "1":
            personagem.destreza += 20
            personagem.arcano += 12
            personagem.vigor += 10
            personagem.roupas.append("Manto das Sombras")
            personagem.equipamento.append("Adaga Silenciosa")
            build_nome = "Sombra Ardilosa"
        elif escolha == "2":
            personagem.destreza += 18
            personagem.mente += 16
            personagem.vigor += 12
            personagem.roupas.append("Vestimenta Leves")
            personagem.equipamento.append("Espada Curta")
            build_nome = "Lâmina Veloz"
        elif escolha == "3":
            personagem.destreza += 19
            personagem.arcano += 14
            personagem.vigor += 11
            personagem.roupas.append("Capuz do Ladrão")
            personagem.equipamento.append("Punhal de Assassino")
            build_nome = "Golpe Furtivo"
        else:
            print("Build inválida para Bandido!")
        return build_nome

    @staticmethod
    def build_astrologo(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Astrólogo (1-3): ")
        if escolha == "1":
            personagem.inteligencia += 22
            personagem.mente += 20
            personagem.arcano += 15
            personagem.roupas.append("Robe Celestial")
            personagem.equipamento.append("Cajado da Aurora")
            build_nome = "Visão Estelar"
        elif escolha == "2":
            personagem.inteligencia += 20
            personagem.mente += 18
            personagem.arcano += 18
            personagem.roupas.append("Manto do Cosmos")
            personagem.equipamento.append("Vara Arcana")
            build_nome = "Mente Cósmica"
        elif escolha == "3":
            personagem.inteligencia += 24
            personagem.mente += 16
            personagem.arcano += 16
            personagem.roupas.append("Túnica de Estrelas")
            personagem.equipamento.append("Cajado Estelar")
            build_nome = "Conjurador Celestial"
        else:
            print("Build inválida para Astrólogo!")
        return build_nome

    @staticmethod
    def build_guerreiro(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Guerreiro (1-3): ")
        if escolha == "1":
            personagem.forca += 18
            personagem.destreza += 15
            personagem.vigor += 16
            personagem.roupas.append("Armadura de Ferro")
            personagem.equipamento.append("Espada Grande")
            build_nome = "Fúria de Batalha"
        elif escolha == "2":
            personagem.forca += 16
            personagem.destreza += 18
            personagem.vigor += 14
            personagem.roupas.append("Cota de Aço")
            personagem.equipamento.append("Sabre de Aço")
            build_nome = "Disciplina de Aço"
        elif escolha == "3":
            personagem.forca += 17
            personagem.vigor += 20
            personagem.fortitude += 15
            personagem.roupas.append("Armadura Pesada")
            personagem.equipamento.append("Machado Pesado")
            build_nome = "Guardião de Ferro"
        else:
            print("Build inválida para Guerreiro!")
        return build_nome

    @staticmethod
    def build_prisioneiro(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Prisioneiro (1-3): ")
        if escolha == "1":
            personagem.destreza += 18
            personagem.inteligencia += 14
            personagem.vigor += 12
            personagem.roupas.append("Vestimenta de Recluso")
            personagem.equipamento.append("Estoc Ágil")
            build_nome = "Redenção Sombria"
        elif escolha == "2":
            personagem.forca += 16
            personagem.destreza += 16
            personagem.vigor += 14
            personagem.roupas.append("Roupas de Fuga")
            personagem.equipamento.append("Espada Curta")
            build_nome = "Liberdade Conquistada"
        elif escolha == "3":
            personagem.destreza += 20
            personagem.mente += 12
            personagem.vigor += 12
            personagem.roupas.append("Manto do Rebelde")
            personagem.equipamento.append("Adaga Rápida")
            build_nome = "Espírito Rebelde"
        else:
            print("Build inválida para Prisioneiro!")
        return build_nome

    @staticmethod
    def build_confessor(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Confessor (1-3): ")
        if escolha == "1":
            personagem.fe += 22
            personagem.vigor += 16
            personagem.inteligencia += 10
            personagem.roupas.append("Vestes Sagradas")
            personagem.equipamento.append("Espada Sagrada")
            build_nome = "Devoto da Luz"
        elif escolha == "2":
            personagem.fe += 20
            personagem.fortitude += 18
            personagem.vigor += 14
            personagem.roupas.append("Armadura do Confessor")
            personagem.equipamento.append("Martelo Sagrado")
            build_nome = "Guardião da Fé"
        elif escolha == "3":
            personagem.fe += 24
            personagem.vigor += 14
            personagem.inteligencia += 12
            personagem.roupas.append("Manto do Redentor")
            personagem.equipamento.append("Cajado Divino")
            build_nome = "Redentor Sagrado"
        else:
            print("Build inválida para Confessor!")
        return build_nome

    @staticmethod
    def build_miseravel(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Miserável (1-3): ")
        if escolha == "1":
            personagem.forca += 14
            personagem.vigor += 18
            personagem.mente += 12
            personagem.roupas.append("Traje do Renascido")
            personagem.equipamento.append("Porrete Modificado")
            build_nome = "Renascido na Dor"
        elif escolha == "2":
            personagem.forca += 16
            personagem.vigor += 16
            personagem.destreza += 12
            personagem.roupas.append("Vestimenta do Sobrevivente")
            personagem.equipamento.append("Clava de Adversidade")
            build_nome = "Caminho da Adversidade"
        elif escolha == "3":
            personagem.vigor += 20
            personagem.mente += 14
            personagem.fortitude += 12
            personagem.roupas.append("Armadura Resiliente")
            personagem.equipamento.append("Maça Pesada")
            build_nome = "Espírito Resiliente"
        else:
            print("Build inválida para Miserável!")
        return build_nome

    @staticmethod
    def build_vagabundo(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Vagabundo (1-3): ")
        if escolha == "1":
            personagem.destreza += 18
            personagem.vigor += 14
            personagem.arcano += 12
            personagem.roupas.append("Manto do Errante")
            personagem.equipamento.append("Espada Curta")
            build_nome = "Sombra Ardilosa"
        elif escolha == "2":
            personagem.destreza += 16
            personagem.vigor += 16
            personagem.forca += 14
            personagem.roupas.append("Capa do Andarilho")
            personagem.equipamento.append("Sabre Tempestuoso")
            build_nome = "Lâmina Veloz"
        elif escolha == "3":
            personagem.destreza += 17
            personagem.vigor += 15
            personagem.forca += 13
            personagem.roupas.append("Traje Errante")
            personagem.equipamento.append("Adaga Versátil")
            build_nome = "Golpe Furtivo"
        else:
            print("Build inválida para Vagabundo!")
        return build_nome

    @staticmethod
    def build_profeta(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Profeta (1-3): ")
        if escolha == "1":
            personagem.fe += 24
            personagem.mente += 16
            personagem.arcano += 14
            personagem.roupas.append("Vestes do Profeta")
            personagem.equipamento.append("Lança Profética")
            build_nome = "Devoto da Luz"
        elif escolha == "2":
            personagem.fe += 22
            personagem.arcano += 18
            personagem.mente += 14
            personagem.roupas.append("Manto Visionário")
            personagem.equipamento.append("Cajado Oracular")
            build_nome = "Guardião da Fé"
        elif escolha == "3":
            personagem.fe += 26
            personagem.arcano += 16
            personagem.vigor += 12
            personagem.roupas.append("Túnica do Selo")
            personagem.equipamento.append("Espada dos Destinos")
            build_nome = "Redentor Sagrado"
        else:
            print("Build inválida para Profeta!")
        return build_nome

    @staticmethod
    def build_samurai(personagem):
        build_nome = "Nenhuma"
        escolha = input("Digite o número da build desejada para Samurai (1-3): ")
        if escolha == "1":
            personagem.destreza += 20
            personagem.vigor += 16
            personagem.forca += 14
            personagem.roupas.append("Armadura do Samurai")
            personagem.equipamento.append("Uchigatana")
            build_nome = "Caminho do Samurai"
        elif escolha == "2":
            personagem.destreza += 18
            personagem.vigor += 14
            personagem.forca += 13
            personagem.roupas.append("Vestimenta de Combate")
            personagem.equipamento.append("Katana Ligeira")
            build_nome = "Lâmina Veloz"
        elif escolha == "3":
            personagem.destreza += 17
            personagem.vigor += 18
            personagem.forca += 15
            personagem.roupas.append("Traje do Honorável")
            personagem.equipamento.append("Katana Ancestral")
            build_nome = "Golpe Furtivo"
        else:
            print("Build inválida para Samurai!")
        return build_nome

class TextBuild:
    @staticmethod
    def text_Heroi():
        return """
        ================================================== BUILDS PARA HERÓI ==================================================
        1 - Força do Destino
        Descrição: Build focada em alta força e vigor, ideal para combates diretos.
        Atributos recomendados: Força +20, Vigor +18, Fortitude +15.
        Roupas: Armadura de Cavaleiro (Vigor +2, Fortitude +1).
        Armas: Espada Lendária (Força +3, Vigor +1).
        ----------------------------------------------------------------------------------------------------
        2 - Espírito Indomável
        Descrição: Combina força bruta com agilidade para ataques rápidos e certeiros.
        Atributos recomendados: Força +18, Destreza +16, Vigor +14.
        Roupas: Cota de Malha Real (Destreza +2, Vigor +1).
        Armas: Machado de Guerra (Força +2, Destreza +2).
        ----------------------------------------------------------------------------------------------------
        3 - Herói Ancestral
        Descrição: Foco em combate corpo a corpo com ênfase na resistência e no dano físico.
        Atributos recomendados: Força +22, Vigor +16, Fortitude +14.
        Roupas: Túnica do Herói (Força +1, Vigor +1).
        Armas: Martelo de Guerra (Força +4, Fortitude +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Bandido():
        return """
        ================================================== BUILDS PARA BANDIDO ==================================================
        1 - Sombra Ardilosa
        Descrição: Especialista em furtividade e ataques surpresa, explorando brechas inimigas.
        Atributos recomendados: Destreza +20, Arcano +12, Vigor +10.
        Roupas: Manto das Sombras (Destreza +2, Arcano +1).
        Armas: Adaga Silenciosa (Destreza +3, Arcano +1).
        ----------------------------------------------------------------------------------------------------
        2 - Lâmina Veloz
        Descrição: Build com foco em velocidade e precisão, perfeita para golpes rápidos.
        Atributos recomendados: Destreza +18, Agilidade +16, Vigor +12.
        Roupas: Vestes Leves (Destreza +2, Agilidade +1).
        Armas: Espada Curta (Destreza +3, Agilidade +1).
        ----------------------------------------------------------------------------------------------------
        3 - Golpe Furtivo
        Descrição: Aproveita ataques críticos e golpes de surpresa para eliminar o adversário.
        Atributos recomendados: Destreza +19, Arcano +14, Vigor +11.
        Roupas: Capuz do Ladrão (Arcano +2, Destreza +1).
        Armas: Punhal de Assassino (Destreza +3, Arcano +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Astrologo():
        return """
        ================================================== BUILDS PARA ASTRÓLOGO ==================================================
        1 - Visão Estelar
        Descrição: Concentra-se em inteligência e mente para conjurar feitiços devastadores.
        Atributos recomendados: Inteligência +22, Mente +20, Arcano +15.
        Roupas: Robe Celestial (Inteligência +2, Mente +2).
        Armas: Cajado da Aurora (Inteligência +3, Arcano +2).
        ----------------------------------------------------------------------------------------------------
        2 - Mente Cósmica
        Descrição: Equilíbrio entre magia ofensiva e defesa mental, ideal para controlar a batalha.
        Atributos recomendados: Inteligência +20, Mente +18, Arcano +18.
        Roupas: Manto do Cosmos (Mente +2, Arcano +2).
        Armas: Vara Arcana (Inteligência +3, Mente +1).
        ----------------------------------------------------------------------------------------------------
        3 - Conjurador Celestial
        Descrição: Especialista em encantamentos à distância com feitiços precisos.
        Atributos recomendados: Inteligência +24, Mente +16, Arcano +16.
        Roupas: Túnica de Estrelas (Inteligência +2, Arcano +1).
        Armas: Cajado Estelar (Inteligência +4, Mente +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Guerreiro():
        return """
        ================================================== BUILDS PARA GUERREIRO ==================================================
        1 - Fúria de Batalha
        Descrição: Build agressiva focada em ataques devastadores e alto dano físico.
        Atributos recomendados: Força +18, Destreza +15, Vigor +16.
        Roupas: Armadura de Ferro (Força +1, Vigor +2).
        Armas: Espada Grande (Força +4, Destreza +1).
        ----------------------------------------------------------------------------------------------------
        2 - Disciplina de Aço
        Descrição: Equilíbrio entre técnica e poder, usando espada com precisão letal.
        Atributos recomendados: Força +16, Destreza +18, Vigor +14.
        Roupas: Cota de Aço (Destreza +2, Vigor +1).
        Armas: Sabre de Aço (Força +3, Destreza +2).
        ----------------------------------------------------------------------------------------------------
        3 - Guardião de Ferro
        Descrição: Concentra-se na defesa robusta e em contra-ataques poderosos.
        Atributos recomendados: Força +17, Vigor +20, Fortitude +15.
        Roupas: Armadura Pesada (Vigor +3, Fortitude +2).
        Armas: Machado Pesado (Força +3, Fortitude +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Prisioneiro():
        return """
        ================================================== BUILDS PARA PRISIONEIRO ==================================================
        1 - Redenção Sombria
        Descrição: Aproveita a agilidade e astúcia do prisioneiro para golpes furtivos.
        Atributos recomendados: Destreza +18, Inteligência +14, Vigor +12.
        Roupas: Vestimenta de Recluso (Destreza +2, Inteligência +1).
        Armas: Estoc Ágil (Destreza +3, Inteligência +1).
        ----------------------------------------------------------------------------------------------------
        2 - Liberdade Conquistada
        Descrição: Equilibra força e destreza para superar adversidades.
        Atributos recomendados: Força +16, Destreza +16, Vigor +14.
        Roupas: Roupas de Fuga (Força +1, Destreza +2).
        Armas: Espada Curta (Força +2, Destreza +2).
        ----------------------------------------------------------------------------------------------------
        3 - Espírito Rebelde
        Descrição: Foca em ataques rápidos e evasão para surpreender o inimigo.
        Atributos recomendados: Destreza +20, Mente +12, Vigor +12.
        Roupas: Manto do Rebelde (Destreza +2, Mente +1).
        Armas: Adaga Rápida (Destreza +3, Mente +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Confessor():
        return """
        ================================================== BUILDS PARA CONFESSOR ==================================================
        1 - Devoto da Luz
        Descrição: Build centrada em fé para curas e ataques divinos com foco em milagres.
        Atributos recomendados: Fé +22, Vigor +16, Inteligência +10.
        Roupas: Vestes Sagradas (Fé +2, Vigor +1).
        Armas: Espada Sagrada (Fé +3, Vigor +1).
        ----------------------------------------------------------------------------------------------------
        2 - Guardião da Fé
        Descrição: Equilibra defesa e ataque usando o poder da fé para abater inimigos.
        Atributos recomendados: Fé +20, Resistência +18, Vigor +14.
        Roupas: Armadura do Confessor (Fé +2, Resistência +1).
        Armas: Martelo Sagrado (Fé +3, Resistência +1).
        ----------------------------------------------------------------------------------------------------
        3 - Redentor Sagrado
        Descrição: Transforma a fé em dano e suporte com bênçãos e milagres.
        Atributos recomendados: Fé +24, Vigor +14, Inteligência +12.
        Roupas: Manto do Redentor (Fé +2, Inteligência +1).
        Armas: Cajado Divino (Fé +4, Vigor +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Miseravel():
        return """
        ================================================== BUILDS PARA MISERÁVEL ==================================================
        1 - Renascido na Dor
        Descrição: Transforma a adversidade em poder com equilíbrio físico e mental.
        Atributos recomendados: Força +14, Vigor +18, Mente +12.
        Roupas: Traje do Renascido (Vigor +2, Mente +1).
        Armas: Porrete Modificado (Força +2, Vigor +1).
        ----------------------------------------------------------------------------------------------------
        2 - Caminho da Adversidade
        Descrição: Resistência e uso da dor para impulsionar ataques.
        Atributos recomendados: Força +16, Vigor +16, Destreza +12.
        Roupas: Vestimenta do Sobrevivente (Força +1, Vigor +2).
        Armas: Clava de Adversidade (Força +3, Destreza +1).
        ----------------------------------------------------------------------------------------------------
        3 - Espírito Resiliente
        Descrição: Maximiza resistência física e mental para batalhas prolongadas.
        Atributos recomendados: Vigor +20, Mente +14, Fortitude +12.
        Roupas: Armadura Resiliente (Vigor +3, Fortitude +1).
        Armas: Maça Pesada (Força +2, Fortitude +2).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Vagabundo():
        return """
        ================================================== BUILDS PARA VAGABUNDO ==================================================
        1 - Errante das Sombras
        Descrição: Explora mobilidade e ataques surpresa para confundir inimigos.
        Atributos recomendados: Destreza +18, Vigor +14, Arcano +12.
        Roupas: Manto do Errante (Destreza +2, Arcano +1).
        Armas: Espada Curta (Destreza +3, Vigor +1).
        ----------------------------------------------------------------------------------------------------
        2 - Andarilho da Tempestade
        Descrição: Combina velocidade e força para golpes relâmpago e evasão rápida.
        Atributos recomendados: Destreza +16, Vigor +16, Força +14.
        Roupas: Capa do Andarilho (Destreza +2, Força +1).
        Armas: Sabre Tempestuoso (Destreza +3, Força +1).
        ----------------------------------------------------------------------------------------------------
        3 - Destino Errante
        Descrição: Versátil equilibrando agilidade com força bruta para diferentes situações.
        Atributos recomendados: Destreza +17, Vigor +15, Força +13.
        Roupas: Traje Errante (Destreza +2, Vigor +1).
        Armas: Adaga Versátil (Destreza +3, Força +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Profeta():
        return """
        ================================================== BUILDS PARA PROFETA ==================================================
        1 - Voz do Apocalipse
        Descrição: Canaliza profecias destrutivas e feitiços devastadores com fé.
        Atributos recomendados: Fé +24, Mente +16, Arcano +14.
        Roupas: Vestes do Profeta (Fé +2, Arcano +1).
        Armas: Lança Profética (Fé +3, Mente +1).
        ----------------------------------------------------------------------------------------------------
        2 - Visões do Futuro
        Descrição: Prevê e manipula o campo de batalha com rituais místicos.
        Atributos recomendados: Fé +22, Arcano +18, Mente +14.
        Roupas: Manto Visionário (Arcano +2, Mente +1).
        Armas: Cajado Oracular (Fé +3, Arcano +1).
        ----------------------------------------------------------------------------------------------------
        3 - Selo do Destino
        Descrição: Altera o rumo do combate com rituais antigos e poder místico.
        Atributos recomendados: Fé +26, Arcano +16, Vigor +12.
        Roupas: Túnica do Selo (Fé +2, Vigor +1).
        Armas: Espada dos Destinos (Fé +4, Arcano +1).
        ----------------------------------------------------------------------------------------------------
        """

    @staticmethod
    def text_Samurai():
        return """
        ================================================== BUILDS PARA SAMURAI ==================================================
        1 - Caminho do Bushido
        Descrição: Precisão e disciplina com espadas, mantendo honra e equilíbrio.
        Atributos recomendados: Destreza +20, Vigor +16, Força +14.
        Roupas: Armadura do Samurai (Destreza +2, Vigor +1).
        Armas: Uchigatana (Destreza +3, Força +1).
        ----------------------------------------------------------------------------------------------------
        2 - Espírito Cortante
        Descrição: Ataques rápidos e cortes precisos priorizando agilidade.
        Atributos recomendados: Destreza +18, Vigor +14, Força +13.
        Roupas: Vestimenta de Combate (Destreza +2, Vigor +1).
        Armas: Katana Ligeira (Destreza +3, Força +1).
        ----------------------------------------------------------------------------------------------------
        3 - Honra Eterna
        Descrição: Tradição e poder para defesas sólidas e contra-ataques precisos.
        Atributos recomendados: Destreza +17, Vigor +18, Força +15.
        Roupas: Traje do Honorável (Vigor +2, Força +1).
        Armas: Katana Ancestral (Destreza +3, Força +1).
        ----------------------------------------------------------------------------------------------------
        """
    
class BuildManager:
    @classmethod
    def aplicar_build(cls, personagem, build_escolhida):
        build_method = getattr(cls, f"build_{personagem.classe.lower()}", None)
        if build_method:
            return build_method(personagem, build_escolhida)
        return "Nenhuma"

    # Herói
    @staticmethod
    def build_heroi(personagem, build_escolhida):
        builds = {
            '1': ("Força do Destino", {'forca': 20, 'vigor': 18, 'fortitude': 15}),
            '2': ("Espírito Indomável", {'forca': 18, 'destreza': 16, 'vigor': 14}),
            '3': ("Herói Ancestral", {'forca': 22, 'vigor': 16, 'fortitude': 14})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Bandido
    @staticmethod
    def build_bandido(personagem, build_escolhida):
        builds = {
            '1': ("Sombra Ardilosa", {'destreza': 20, 'arcano': 12, 'vigor': 10}),
            '2': ("Lâmina Veloz", {'destreza': 18, 'mente': 16, 'vigor': 12}),
            '3': ("Golpe Furtivo", {'destreza': 19, 'arcano': 14, 'vigor': 11})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Adicione métodos para outras classes seguindo o mesmo padrão
    # Astrologo
    @staticmethod
    def build_astrologo(personagem, build_escolhida):
        builds = {
            '1': ("Visão Estelar", {'inteligencia': 22, 'mente': 20, 'arcano': 15}),
            '2': ("Mente Cósmica", {'inteligencia': 20, 'mente': 18, 'arcano': 18}),
            '3': ("Conjurador Celestial", {'inteligencia': 24, 'mente': 16, 'arcano': 16})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Guerreiro
    @staticmethod
    def build_guerreiro(personagem, build_escolhida):
        builds = {
            '1': ("Fúria de Batalha", {'forca': 18, 'destreza': 15, 'vigor': 16}),
            '2': ("Disciplina de Aço", {'forca': 16, 'destreza': 18, 'vigor': 14}),
            '3': ("Guardião de Ferro", {'forca': 17, 'vigor': 20, 'fortitude': 15})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Prisioneiro
    @staticmethod
    def build_prisioneiro(personagem, build_escolhida):
        builds = {
            '1': ("Redenção Sombria", {'destreza': 18, 'inteligencia': 14, 'vigor': 12}),
            '2': ("Liberdade Conquistada", {'forca': 16, 'destreza': 16, 'vigor': 14}),
            '3': ("Espírito Rebelde", {'destreza': 20, 'mente': 12, 'vigor': 12})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Confessor
    @staticmethod
    def build_confessor(personagem, build_escolhida):
        builds = {
            '1': ("Devoto da Luz", {'fe': 22, 'vigor': 16, 'inteligencia': 10}),
            '2': ("Guardião da Fé", {'fe': 20, 'fortitude': 18, 'vigor': 14}),
            '3': ("Redentor Sagrado", {'fe': 24, 'vigor': 14, 'inteligencia': 12})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Miseravel
    @staticmethod
    def build_miseravel(personagem, build_escolhida):
        builds = {
            '1': ("Renascido na Dor", {'forca': 14, 'vigor': 18, 'mente': 12}),
            '2': ("Caminho da Adversidade", {'forca': 16, 'vigor': 16, 'destreza': 12}),
            '3': ("Espírito Resiliente", {'vigor': 20, 'mente': 14, 'fortitude': 12})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Vagabundo
    @staticmethod
    def build_vagabundo(personagem, build_escolhida):
        builds = {
            '1': ("Errante das Sombras", {'destreza': 18, 'vigor': 14, 'arcano': 12}),
            '2': ("Andarilho da Tempestade", {'destreza': 16, 'vigor': 16, 'forca': 14}),
            '3': ("Destino Errante", {'destreza': 17, 'vigor': 15, 'forca': 13})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Profeta
    @staticmethod
    def build_profeta(personagem, build_escolhida):
        builds = {
            '1': ("Voz do Apocalipse", {'fe': 24, 'mente': 16, 'arcano': 14}),
            '2': ("Visões do Futuro", {'fe': 22, 'arcano': 18, 'mente': 14}),
            '3': ("Selo do Destino", {'fe': 26, 'arcano': 16, 'vigor': 12})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    # Samurai
    @staticmethod
    def build_samurai(personagem, build_escolhida):
        builds = {
            '1': ("Caminho do Bushido", {'destreza': 20, 'vigor': 16, 'forca': 14}),
            '2': ("Espírito Cortante", {'destreza': 18, 'vigor': 14, 'forca': 13}),
            '3': ("Honra Eterna", {'destreza': 17, 'vigor': 18, 'forca': 15})
        }
        return BuildManager.aplicar_modificadores(personagem, build_escolhida, builds)

    @staticmethod
    def aplicar_modificadores(personagem, build_escolhida, builds):
        build = builds.get(str(build_escolhida))
        if not build:
            return "Nenhuma"
        
        nome, modificadores = build
        for atributo, valor in modificadores.items():
            setattr(personagem, atributo, getattr(personagem, atributo) + valor)
        
        return nome
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (login, senha) VALUES (%s, %s)", 
                      (data['login'], data['senha']))
        conn.commit()
        return jsonify({"success": True, "message": "Usuário registrado!"})
    except Error as err:
        return jsonify({"success": False, "error": str(err)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, senha FROM usuarios WHERE login = %s", (data['login'],))
        user = cursor.fetchone()

        if user and user['senha'] == data['senha']:
            return jsonify({"success": True, "user_id": user['id']})
        else:
            return jsonify({"success": False, "error": "Credenciais inválidas"})
    except Error as err:
        return jsonify({"success": False, "error": str(err)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/characters', methods=['POST'])
def create_character():
    data = request.json
    conn = None
    try:
        classe = data['classe']
        classes = {
            'Heroi': Heroi,
            'Bandido': Bandido,
            'Astrologo': Astrologo,
            'Guerreiro': Guerreiro,
            'Prisioneiro': Prisioneiro,
            'Confessor': Confessor,
            'Miseravel': Miseravel,
            'Vagabundo': Vagabundo,
            'Profeta': Profeta,
            'Samurai': Samurai
        }
        
        if classe not in classes:
            return jsonify({"success": False, "error": "Classe inválida!"}), 400
            
        personagem = classes[classe](data['nome'], data['idade'])
        personagem.raca = data.get('raca', '')
        personagem.sexo = data.get('sexo', '')
        
        # Aplicar build
        build_escolhida = data.get('build_escolhida', '')
        build_nome = BuildManager.aplicar_build(personagem, build_escolhida)
        personagem.build_escolhida = build_nome
        
        # Converter listas para strings
        equipamento_str = ", ".join(personagem.equipamento)
        roupas_str = ", ".join(personagem.roupas)
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO personagens 
            (usuario_id, nome, idade, classe, raca, sexo, vigor, mente, fortitude, 
             forca, destreza, inteligencia, fe, arcano, build_escolhida, equipamento, roupas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['user_id'], personagem.nome, personagem.idade, personagem.classe, 
            personagem.raca, personagem.sexo, personagem.vigor, personagem.mente, 
            personagem.fortitude, personagem.forca, personagem.destreza, 
            personagem.inteligencia, personagem.fe, personagem.arcano, 
            personagem.build_escolhida, equipamento_str, roupas_str
        ))
        conn.commit()
        return jsonify({"success": True, "message": "Personagem criado!"})
        
    except Error as err:
        return jsonify({"success": False, "error": str(err)})
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/builds/<classe>')
def get_build_text(classe):
    text_method = getattr(TextBuild, f"text_{classe}", None)
    if text_method:
        return text_method()
    return ""

@app.route('/api/characters/<int:user_id>')
def get_characters(user_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personagens WHERE usuario_id = %s", (user_id,))
        characters = cursor.fetchall()
        return jsonify({"success": True, "characters": characters})
    except Error as err:
        return jsonify({"success": False, "error": str(err)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personagens WHERE id = %s", (character_id,))
        conn.commit()
        return jsonify({"success": True, "message": "Personagem excluído!"})
    except Error as err:
        return jsonify({"success": False, "error": str(err)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
