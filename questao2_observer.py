from abc import ABC, abstractmethod


class Desconto(ABC):
    @abstractmethod
    def aplicar(self, preco: float, quantidade: int) -> float: ...

    @abstractmethod
    def descricao(self) -> str: ...


class DescontoEstudante(Desconto):
    def __init__(self, percentual: float = 50):
        self.percentual = percentual

    def aplicar(self, preco: float, quantidade: int) -> float:
        return preco * (1 - self.percentual / 100)

    def descricao(self) -> str:
        return f"Estudante ({self.percentual:.0f}% off)"


class DescontoQuantidade(Desconto):
    def __init__(self, minimo: int, percentual: float):
        self.minimo = minimo
        self.percentual = percentual

    def aplicar(self, preco: float, quantidade: int) -> float:
        if quantidade >= self.minimo:
            return preco * (1 - self.percentual / 100)
        return preco

    def descricao(self) -> str:
        return f"Quantidade ({self.percentual:.0f}% off a partir de {self.minimo} ingressos)"


class Observador(ABC):
    @abstractmethod
    def atualizar(self, ingresso: "Ingresso", evento: str, detalhe: str) -> None: ...


class Cliente(Observador):
    def __init__(self, nome: str):
        self.nome = nome

    def atualizar(self, ingresso, evento, detalhe):
        print(f"   [Cliente {self.nome}] Olá! O ingresso {ingresso.tipo} teve "
              f"{evento}: {detalhe}")


class Administrador(Observador):
    def __init__(self, nome: str):
        self.nome = nome

    def atualizar(self, ingresso, evento, detalhe):
        print(f"   [Admin {self.nome}] LOG -> {ingresso.tipo} | {evento.upper()} | {detalhe}")


class Ingresso:
    def __init__(self, tipo: str, preco: float):
        self.tipo = tipo
        self._preco = preco
        self._descontos: list[Desconto] = []
        self._observadores: list[Observador] = []

    def inscrever(self, obs: Observador) -> None:
        if obs not in self._observadores:
            self._observadores.append(obs)

    def desinscrever(self, obs: Observador) -> None:
        self._observadores.remove(obs)

    def _notificar(self, evento: str, detalhe: str) -> None:
        for obs in self._observadores:
            obs.atualizar(self, evento, detalhe)

    def get_preco(self) -> float:
        return self._preco

    def set_preco(self, novo_preco: float) -> None:
        antigo = self._preco
        self._preco = novo_preco
        self._notificar("mudança de preço",
                        f"R$ {antigo:.2f} -> R$ {novo_preco:.2f}")

    def adicionar_desconto(self, desconto: Desconto) -> None:
        self._descontos.append(desconto)
        self._notificar("novo desconto", desconto.descricao())

    def calcular_total(self, quantidade: int = 1) -> float:
        preco = self._preco
        for d in self._descontos:
            preco = d.aplicar(preco, quantidade)
        return preco * quantidade


class CadeiraPremium(Ingresso):
    def __init__(self, preco: float = 300.0):
        super().__init__("Cadeira Premium", preco)


class Arquibancada(Ingresso):
    def __init__(self, preco: float = 80.0):
        super().__init__("Arquibancada", preco)


class Camarote(Ingresso):
    def __init__(self, preco: float = 600.0):
        super().__init__("Camarote", preco)


if __name__ == "__main__":
    premium = CadeiraPremium()
    arquibancada = Arquibancada()
    camarote = Camarote()

    ana = Cliente("Ana")
    bruno = Cliente("Bruno")
    admin = Administrador("Carlos")

    premium.inscrever(ana)
    premium.inscrever(admin)
    arquibancada.inscrever(bruno)
    arquibancada.inscrever(admin)
    camarote.inscrever(admin)

    print("== Alteração de preço da Cadeira Premium ==")
    premium.set_preco(350.0)

    print("\n== Alteração de preço da Arquibancada ==")
    arquibancada.set_preco(70.0)

    print("\n== Novo desconto para estudantes na Arquibancada ==")
    arquibancada.adicionar_desconto(DescontoEstudante(50))

    print("\n== Novo desconto por quantidade no Camarote ==")
    camarote.adicionar_desconto(DescontoQuantidade(minimo=5, percentual=10))

    print("\n== Ana deixa de acompanhar a Premium e o preço muda de novo ==")
    premium.desinscrever(ana)
    premium.set_preco(320.0)

    print("\n== Totais ==")
    print(f"   2x Arquibancada (estudante): R$ {arquibancada.calcular_total(2):.2f}")
    print(f"   5x Camarote (quantidade):    R$ {camarote.calcular_total(5):.2f}")
    print(f"   1x Cadeira Premium:          R$ {premium.calcular_total(1):.2f}")
