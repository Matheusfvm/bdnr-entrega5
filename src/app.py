from neo4j import GraphDatabase
import servicos.usuario as usuario
import servicos.vendedor as vendedor
import servicos.produto as produto
import servicos.compra as compra

URI = "neo4j+s://11929b28.databases.neo4j.io"
AUTH = ("neo4j", "FJsxTA0mAG_yeNh7Jar0MO_QonztYvonJ2D6VaP7ONU")

driver = GraphDatabase.driver(URI, auth=AUTH)

key = 0
sub = 0
while key != 'S':
    print("\n1 - Usuário")
    print("2 - Vendedor")
    print("3 - Produto")
    print("4 - Compra")
    key = input("\nDigite a opção desejada?(S para sair) ").upper()

    if key == '1':
        print("\n-----------------")
        print("\nMenu do Usuário\n")
        print("1 - Criar Usuário")
        print("2 - Listar Usuário")
        sub = input("\nDigite a opção desejada? (V para voltar) ").upper()

        if sub == "1":
            print("\n----INSERIR USUÁRIO----\n")
            usuario.criarUsuario(driver)
            
        elif sub == "2":
            print("\n----LISTAR USUÁRIO----\n")
            usuario.listarUsuario(driver)

    elif key == '2':
        print("\n-----------------")
        print("\nMenu do Vendedor\n")
        print("1 - Criar Vendedor")
        print("2 - Listar Vendedor")
        sub = input("\nDigite a opção desejada? (V para voltar) ").upper()

        if sub == "1":
            print("\n----INSERIR VENDEDOR----\n")
            vendedor.criarVendedor(driver)
            
        elif sub == "2":
            print("\n----LISTAR VENDEDOR----\n")
            vendedor.listarVendedor(driver)
        
    elif key == '3':
        print("\n-----------------")
        print("\nMenu do Produto\n") 
        print("1 - Criar Produto")
        print("2 - Listar Produto")
        sub = input("\nDigite a opção desejada? (V para voltar) ").upper()

        if sub == "1":
            print("\n----INSERIR PRODUTO----\n")
            produto.criarProduto(driver)
        
        elif sub == "2":
            print("\n----LISTAR PRODUTO----\n")
            produto.listarProduto(driver)
        
    elif key == '4':
        print("\n-----------------")
        print("\nMenu da Compra\n")
        print("1 - Comprar um Produto")
        print("2 - Listar Compras")
        sub = input("\nDigite a opção desejada? (V para voltar) ").upper()

        if sub == "1":
            print("\n----COMPRAR UM PRODUTO----\n")
            compra.criarCompra(driver)
        
        if sub == "2":
            print("\n----LISTAR COMPRAS----\n")
            compra.listarCompra(driver)
    elif key == "S":
        break
