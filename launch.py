import logging
from logging import config as lc

from chizhov_borodin import ChizhovBorodin


logger = logging.getLogger()
lc.fileConfig(fname='logging.conf')


if __name__ == '__main__':

    params = [
        (2, 4),
        (2, 5),
        (3, 8),
    ]

    logger.info('starting Mc-Eliece attacker...')
    for pair in params:
        logger.info(f'invoking Chizhov-Borodin algorithm for r={pair[0]}, '
                    + f'm={pair[1]}')
        cb = ChizhovBorodin(*pair)
        m, p = cb.attack()
        logger.info(f'is attack successful? - {cb.check_attack(m, p)}')

    logger.info('shutting down Mc-Eliece attacker...')
