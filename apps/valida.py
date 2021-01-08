""" Refatorar e colocar as validações backend aqui """


def validacampo(campo):
    """ valida campo vazio """
    return not campo.strip()


def validasenha(senha, senha2):
    """ Valida se Senha são Iguais """
    return senha != senha2

def senhainvalida(senha):
    return senha != senha