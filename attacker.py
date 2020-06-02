from abc import ABC, abstractmethod


class Attacker(ABC):

    @staticmethod
    def stringify_matrix(label, matrix):
        return f'{label}:\n' + '_'*matrix.ncolumns + f'\n{matrix.to_str()}\n'

    @abstractmethod
    def attack():
        raise NotImplementedError
