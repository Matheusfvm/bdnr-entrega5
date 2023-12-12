import servicos.vendedor as vendedor


def criarProduto(driver):
    while True:
        descricao = str(input("Descrição: "))
        with driver.session() as session:
            query = (
                "MATCH (p:Produto {descricao: $descricao})"
                "RETURN p"
            )
            produto = session.run(query, {"descricao": descricao})
            if produto.peek() is not None:
                    print("\nProduto já cadastrado!")
                    print("Digite outra Descrição!\n")                
            else:
                break            
    preco = str(input("Preço(R$): "))
    while True:
        validacao = is_float(preco)
        if validacao:
            precoValidado = float(preco)
            break
        else:
            print("\nDigite uma valor valido!\n")
            preco = str(input("Digite o preço(R$): "))
    quantidadeProduto = str(input("Quantidade: "))
    while True:
        if quantidadeProduto.isnumeric():
            quantidadeValidada = int(quantidadeProduto)
            break
        else:
            print("\nDigite um número inteiro!\n")
            quantidadeProduto = str(input("Digite a quantidade: "))
    vendedorEscolhido = vendedor.consultaVendedor(driver)
    documentoVendedor = {"documento": vendedorEscolhido['documento']}
    with driver.session() as session:
        produto = {
            "descricao": descricao,
            "preco": precoValidado,
            "quantidade": quantidadeValidada
        }
        params = {**produto, **documentoVendedor}
        query = (
            "MATCH (v:Vendedor {documento: $documento}) "
            "CREATE (p:Produto {descricao: $descricao, preco: $preco, quantidade: $quantidade})"
            "MERGE (v)-[:VENDE]->(p)"
            )
        session.run(query, params)        
    print(f'\nProduto cadastrado com sucesso!\n')

def listarProduto(driver):
    produtoEscolhido = consultaProduto(driver)    
    print(f"Descrição: {produtoEscolhido['descricao']}")
    print(f"Preço: {produtoEscolhido['preco']}")
    print(f"Quantidade: {produtoEscolhido['quantidade']}")    

def consultaProduto(driver):
    while True:
        descricao = str(input("Descrição do produto: "))
        with driver.session() as session:
            query = (
                "MATCH (p:Produto {descricao: $descricao})"
                "RETURN p"
            )
            produto = session.run(query, {"descricao": descricao})
            if produto.peek() is not None:
                record = produto.single()
                produtoEscolhido = record["p"]
                break
            else:
                print("Produto não encontrado.")       
    return produtoEscolhido

def is_float(texto):
    try:
        float(texto)
        return True
    except ValueError:
        return False