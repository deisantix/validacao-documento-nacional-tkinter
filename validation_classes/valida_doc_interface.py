from abc import ABCMeta, abstractmethod


class IByteBank(metaclass=ABCMeta):

    def __str__(self):
        return self._mascara()

    @staticmethod
    @abstractmethod
    def eh_valido(alguma_coisa_para_validar):
        pass

    @abstractmethod
    def _mascara(self):
        pass
