import servicos.produto as produto
import servicos.usuario as usuario


def criarCompra(driver):
    usuarioEscolhido = usuario.consultaUsuario(driver)
    cpfUsuario = {"cpf": usuarioEscolhido['cpf']}
    produtoEscolhido = produto.consultaProduto(driver)
    descricaoProduto = {"descricao": produtoEscolhido['descricao']}
    with driver.session() as session:
        params = {**descricaoProduto, **cpfUsuario}
        query = (
            "MATCH (u:Usuario) WHERE u.cpf = $cpf "
            "MATCH (p:Produto) WHERE p.descricao = $descricao "
            "MERGE (u)-[:COMPRA]->(p)"
        )
        session.run(query, params)

def listarCompra(driver):
    usuarioEscolhido = usuario.consultaUsuario(driver)
    print("\nProdutos Comprados:\n")
    with driver.session() as session:
        query = (
            "MATCH (u:Usuario {cpf: $cpf}) "
            "OPTIONAL MATCH (u)-[:COMPRA]->(p:Produto) "
            "RETURN u, COLLECT(p) as produtosComprados"
        )
        objetoUsuario = session.run(query, {"cpf": usuarioEscolhido['cpf']})
        record = objetoUsuario.single()
        produtosComprados = record["produtosComprados"]

        for produto in produtosComprados:
            print(f"Descrição: {produto['descricao']}")
            print(f"Preço: R${produto['preco']}")
            print(f"Quantidade: {produto['quantidade']}")
            print("\n---------------------------------------\n")