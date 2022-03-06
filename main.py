import sys

from Environment import env_base

if __name__ == '__main__':
    Baoan_Air = env_base.Env_Base()
    Baoan_Air.reset()
    while True:
        Baoan_Air.step()
        Baoan_Air.done()
        # print('a')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
