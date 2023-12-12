def criarVendedor(driver):
    nome = str(input("Nome: "))
    while True:
        documento = str(input("Documento: "))
        with driver.session() as session:
            query = (
                "MATCH (v:Vendedor {documento: $documento})"
                "RETURN v"
            )
            vendedor = session.run(query, {"documento": documento})
            if vendedor.peek() is not None:
                    print("\nVendedor já cadastrado!")
                    print("Digite outro Documento!\n")                
            else:
                break       
    email = str(input("Email: "))           
    senha = str(input("Senha: "))
    with driver.session() as session:
        vendedor = {
            "documento": documento,
            "nome": nome,
            "email": email,
            "senha": senha
        }
        query = (
            "CREATE (v:Vendedor {documento: $documento, nome: $nome, email: $email, senha: $senha})"
        )
        session.run(query, vendedor)     
    print(f'\nVendedor {nome} inserido com sucesso!\n')

def listarVendedor(driver):
    vendedorEscolhido = consultaVendedor(driver) 
    print(f"Nome: {vendedorEscolhido['nome']}")
    print(f"Documento: {vendedorEscolhido['documento']}")
    print(f"Email: {vendedorEscolhido['email']}")
    print(f"Senha: {vendedorEscolhido['senha']}")
    print("\nProdutos:\n")
    with driver.session() as session:
        query = (
            "MATCH (v:Vendedor {documento: $documento}) "
            "OPTIONAL MATCH (v)-[:VENDE]->(p:Produto) "
            "RETURN v, COLLECT(p) as produtosVendidos"
        )

        vendedor = session.run(query, {"documento": vendedorEscolhido['documento']})
        record = vendedor.single()
        produtosVendidos = record["produtosVendidos"]
        for produto in produtosVendidos:
            print(f"Descrição: {produto['descricao']}")
            print(f"Preço: R${produto['preco']}")
            print(f"Quantidade: {produto['quantidade']}")
            print("\n---------------------------------------\n")

def consultaVendedor(driver):
    while True:
        documento = str(input("Documento do vendedor: "))
        with driver.session() as session:
            query = (
                "MATCH (v:Vendedor {documento: $documento})"
                "RETURN v"
            )
            vendedor = session.run(query, {"documento": documento})
            if vendedor.peek() is not None:
                record = vendedor.single()
                vendedorEscolhido = record["v"]
                break
            else:
                print("Vendedor não encontrado.")       
    return vendedorEscolhido