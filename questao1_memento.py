import copy


class Tarefa:
    def __init__(self, titulo: str, descricao: str):
        self._titulo = titulo
        self._descricao = descricao

    def get_titulo(self) -> str:
        return self._titulo

    def set_titulo(self, titulo: str) -> None:
        self._titulo = titulo

    def get_descricao(self) -> str:
        return self._descricao

    def set_descricao(self, descricao: str) -> None:
        self._descricao = descricao

    def __str__(self) -> str:
        return f"{self._titulo} - {self._descricao}"


class MementoLista:
    def __init__(self, tarefas: list, acao: str):
        self._estado = copy.deepcopy(tarefas)
        self._acao = acao

    def get_estado(self) -> list:
        return copy.deepcopy(self._estado)

    def get_acao(self) -> str:
        return self._acao


class ListaDeTarefas:
    def __init__(self):
        self._tarefas: list[Tarefa] = []

    def adicionar(self, tarefa: Tarefa) -> None:
        self._tarefas.append(tarefa)

    def editar(self, indice: int, novo_titulo: str, nova_descricao: str) -> None:
        tarefa = self._tarefas[indice]
        tarefa.set_titulo(novo_titulo)
        tarefa.set_descricao(nova_descricao)

    def remover(self, indice: int) -> Tarefa:
        return self._tarefas.pop(indice)

    def salvar(self, acao: str) -> MementoLista:
        return MementoLista(self._tarefas, acao)

    def restaurar(self, memento: MementoLista) -> None:
        self._tarefas = memento.get_estado()

    def exibir(self) -> None:
        if not self._tarefas:
            print("   (lista vazia)")
        for i, t in enumerate(self._tarefas):
            print(f"   [{i}] {t}")


class Zelador:
    def __init__(self, lista: ListaDeTarefas):
        self._lista = lista
        self._historico: list[MementoLista] = []

    def backup(self, acao: str) -> None:
        self._historico.append(self._lista.salvar(acao))

    def desfazer(self) -> None:
        if not self._historico:
            print(">> Nada para desfazer.")
            return
        memento = self._historico.pop()
        self._lista.restaurar(memento)
        print(f">> Desfeito: {memento.get_acao()}")


class AppTarefas:
    def __init__(self):
        self.lista = ListaDeTarefas()
        self.zelador = Zelador(self.lista)

    def adicionar(self, titulo: str, descricao: str) -> None:
        self.zelador.backup(f"adicionar '{titulo}'")
        self.lista.adicionar(Tarefa(titulo, descricao))
        print(f">> Adicionada: {titulo}")

    def editar(self, indice: int, titulo: str, descricao: str) -> None:
        self.zelador.backup(f"editar tarefa {indice}")
        self.lista.editar(indice, titulo, descricao)
        print(f">> Editada tarefa {indice}")

    def remover(self, indice: int) -> None:
        self.zelador.backup(f"remover tarefa {indice}")
        removida = self.lista.remover(indice)
        print(f">> Removida: {removida.get_titulo()}")

    def desfazer(self) -> None:
        self.zelador.desfazer()

    def mostrar(self) -> None:
        self.lista.exibir()
        print()


if __name__ == "__main__":
    app = AppTarefas()

    app.adicionar("Estudar", "Revisar padrões de projeto")
    app.adicionar("Mercado", "Comprar café")
    app.mostrar()

    app.editar(0, "Estudar", "Fazer atividade de Memento e Observer")
    app.mostrar()

    app.remover(1)
    app.mostrar()

    app.desfazer()
    app.mostrar()

    app.desfazer()
    app.mostrar()

    app.desfazer()
    app.desfazer()
    app.mostrar()

    app.desfazer()
