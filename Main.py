from Page import Page
from Tree import BTree
import time

def main():

        bt = BTree(4)
        bt.insert(5) # inserir chave
        bt.insert(15)
        bt.insert(20)
        bt.insert(30)
        print(bt)
        bt.insert(10)
        print(bt)
        bt.remove(15) # remover chave, se não existe, retorna um erro.
        print(bt)
        print(bt.contains(35))  # pesquisar elemento por chave, retorna true se está inserido, false se não está.


if __name__ == '__main__':
	main()
