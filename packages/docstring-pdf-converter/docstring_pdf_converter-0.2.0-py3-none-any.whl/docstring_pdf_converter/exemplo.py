"""
Módulo de exemplo para o conversor de docstring para PDF.
"""

def funcao_exemplo(param1, param2):
    """
    Esta é uma função de exemplo.

    Args:
        param1 (int): O primeiro parâmetro.
        param2 (str): O segundo parâmetro.

    Returns:
        bool: O resultado da operação.
    """
    return param1 > 0 and param2 == "exemplo"

class ClasseExemplo:
    """
    Esta é uma classe de exemplo.
    """

    def __init__(self):
        """
        Inicializa a ClasseExemplo.
        """
        self.mensagem = "ClasseExemplo inicializada."

    def metodo_exemplo(self):
        """
        Este é um método de exemplo.

        Returns:
            str: Uma mensagem de exemplo.
        """
        return "Este é um método de exemplo."

    def metodo_com_parametros(self, param1, param2):
        """
        Este é um método de exemplo com parâmetros.

        Args:
            param1 (int): O primeiro parâmetro.
            param2 (str): O segundo parâmetro.

        Returns:
            bool: O resultado da operação.
        """

        return param1 > 0 and param2 == "exemplo"
