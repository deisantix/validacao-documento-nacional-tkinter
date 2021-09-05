# Interface de Cadastro - Tkinter
Uma simples interface de cadastro feito com Tkinter (Python) para validar informações pessoais como: nome, data de nascimento, CPF, endereço, etc

Sabe quando você entra em um site e tem que fazer um cadastro completo com suas informações pessoais? Eu fiz isso usando Tkinter, para fins próprios de estudo.

A interface é super simples, porém inteiramente funcional. A validação das informações é feita através de classes próprias para cada categoria, levando em conta syntaxe e existência em banco de dados, no caso do cep, estado e cidade, por exemplo. A maioria das classes usam RegEx para validar a syntaxe das informações, por exemplo CPF que tem que seguir o formato xxx.xxx.xxx-xx ou apenas 11 dígitos.

A maioria das bibliotecas são built-ins do Python, exceto por algumas que são facilmentes instaladas com `pip`. São elas:

- `email_validator`

- `validate_docbr` Onde usei as classes CPF e CNPJ para validar os respectivos.

Esse projeto foi feito especialmente para treinar conceitos e me familiar com um framework de interface. O código pode não estar organizado e construído da forma mais eficiente.
