from Algorithm import Algorithm
from ToraEngine import ToraEngine

Engine = None
if __name__ == '__main__':
    Engine = ToraEngine()
    Engine.addalgorithm(Algorithm)
    Engine.start()
else:
    print(Engine)