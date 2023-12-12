import json

def criarUsuario(driver):
    nome = str(input("Nome: "))    
    email = str(input("Email: "))
    while True:
        cpf = str(input("CPF: "))
        with driver.session() as session:
            query = (
                "MATCH (u:Usuario {cpf: $cpf})"
                "RETURN u"
            )
            usuario = session.run(query, {"cpf": cpf})
            if usuario.peek() is not None:
                print("\nUsuário já cadastrado!")
                print("Digite outro CPF!\n")                
            else:
                break          
    senha = str(input("Senha: "))
    telefone = str(input("Número telefone: "))
    listaEndereco = []
    listaCompra = []
    listaFavorito = []
    key = "S"
    while key == "S":
        cep = str(input("CEP: "))
        ruaAvenida = str(input("Nome da rua ou avenida: "))
        numeroEndereco = str(input("Número endereço: "))
        bairro = str(input("Bairro: "))
        cidade = str(input("Cidade: "))
        estado = str(input("Estado(Sigla): "))
        endereco = {
            "cep": cep,
            "rua_avenida": ruaAvenida,
            "numero": numeroEndereco,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,            
            }
        listaEndereco.append(endereco)
        key = input("Deseja cadastrar um novo endereço(S/N)? ")        
    jsonListaEndereco = json.dumps(listaEndereco)
    jsonListaCompra = json.dumps(listaCompra)
    jsonListaFavorito = json.dumps(listaFavorito)
    with driver.session() as session:
        jsonListaEndereco = json.dumps(listaEndereco)
        jsonListaCompra = json.dumps(listaCompra)
        jsonListaFavorito = json.dumps(listaFavorito)
        usuario = {
            "cpf": cpf,
            "nome": nome,
            "listaEndereco": jsonListaEndereco,
            "telefone": telefone,
            "email": email,
            "senha": senha,        
            "listaCompra": jsonListaCompra,
            "listaFavorito": jsonListaFavorito
        }
        query = (
            "CREATE (u:Usuario {cpf: $cpf, nome: $nome, listaEndereco: $listaEndereco, telefone: $telefone, email: $email, senha: $senha, listaCompra: $listaCompra, listaFavorito: $listaFavorito})"
        )
        session.run(query, usuario)

def listarUsuario(driver):
    usuarioEscolhido = consultaUsuario(driver)    
    print(f"Nome: {usuarioEscolhido['nome']}")
    print(f"Cpf: {usuarioEscolhido['cpf']}")
    print(f"Email: {usuarioEscolhido['email']}")
    print(f"Senha: {usuarioEscolhido['senha']}")
    print(f"Telefone: {usuarioEscolhido['telefone']}")
    print("\nEndereços:")
    objetoListaEndereco = json.loads(usuarioEscolhido['listaEndereco'])
    for endereco in objetoListaEndereco:
        print(f"Cep: {endereco['cep']}")
        print(f"Rua/Avenida: {endereco['rua_avenida']}")
        print(f"Número: {endereco['numero']}")
        print(f"Bairro: {endereco['bairro']}")
        print(f"Cidade: {endereco['cidade']}")
        print(f"Estado: {endereco['estado']}")
        print("\n---------------------------------------\n")

def atualizarUsuario(driver):
    usuarioEscolhido = consultaUsuario(driver)
    novoNome = str(input("Nome: "))
    novoEmail = str(input("Email: "))
    novaSenha = str(input("Senha: "))
    novoTelefone = str(input("Número telefone: "))
    objetoAtualizacao = {
        "cpf": usuarioEscolhido['cpf'],        
        "novoNome": novoNome,
        "novoEmail": novoEmail,
        "novaSenha": novaSenha,
        "novoTelefone": novoTelefone                
    }
    with driver.session() as session:
        query = (
            "MATCH (u:Usuario {cpf: $cpf}) "
            "SET u.nome = $novoNome, u.email = $novoEmail, u.senha = $novaSenha, u.telefone = $novoTelefone "
            "RETURN u"
        )
        session.run(query, objetoAtualizacao)
    print(f'\nUsuário {novoNome} atualizado com sucesso!\n')

def deletarUsuario(driver):
    usuarioEscolhido = consultaUsuario(driver)
    with driver.session() as session:
        query = (
            "MATCH (u:Usuario {cpf: $cpf}) "
            "DELETE u"
        )
        session.run(query, {"cpf": usuarioEscolhido['cpf']})
    print(f'\nUsuário {usuarioEscolhido["nome"]} foi deletado com sucesso!\n')

def consultaUsuario(driver):
    while True:
        cpf = str(input("CPF do usuário: "))
        with driver.session() as session:
            query = (
                "MATCH (u:Usuario {cpf: $cpf})"
                "RETURN u"
            )
            usuario = session.run(query, {"cpf": cpf})
            if usuario.peek() is not None:
                record = usuario.single()
                usuarioEscolhido = record["u"]
                break
            else:
                print("Usuário não encontrado.")       
    return usuarioEscolhido