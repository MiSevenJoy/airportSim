import gym

if __name__ == '__main__':
    Baoan_Air = gym.make('AirportWorld-v0')
    Baoan_Air.reset()
    while True:
        Baoan_Air.step()
        Baoan_Air.done()

