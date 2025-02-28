# car-dataset


## Pre-processamento
### Sobre os dados
O dataset contem mais de 360 mil listagens de carros vendidos/a venda em um arquivo JSON. Originalmente ele nos dá os seguintes campos:
- listing_id: ID unico do anuncio
- created_at e updated_at, auto explicativo
- vehicle_plate: Hash d placa do carro
- has_declared_vin: Vendedor inseriu o chassis do veiculo
- vehicle_category: Hash da categoria do carro
- is_armored: Blindado
- color: Hash da cor
- gearbox: Hash do tipo de transmissão
- doors: Numero de portas
- milleage: quilometragem
- number_of_images: Numero de fotos no anuncio
- dealer_type: Tipo de vendedor
- dealer_id: ID unico do vendedor
- dealer_city e dealer_state, cidade e estado do vendedor
- diferentials: Array de diferenciais do anuncio
- equipaments: Array de equipamentos e opcionais do carro
- price: Valor anunciado
- fipe_price: Valor da tabela fipe do veiculo anunciado
- make_year: Ano de fabricação
- model_year: Ano do modelo
- brand_code: ID Fabricante
- model_code: ID Modelo
- model_version_code: ID Versão do modelo
### Problemas
- diferentials e equipaments: São arrays de strings. Precisavam ser parseados com regex e depois interpretados como strings separadas, senão eram enxergadas como uma string só
### Abordagens
- separando diferentials e equipaments: o primeiro gera +/- 40 features e o segundo +/- 200
- Conta-se a quantidade de intens diferenciais e equipamentos por instância para gerar duas novas features
- Elimina-se o registro de entrada e atualização do cadastro do veículo
- Outros hashes não são eliminados, pois podem aparacer repetidamente e indicar algo ainda não conhecido
- Faz-se o encoding dos hashes para transformar em números que indicam categorias
## Análises
### Orange
-Ferramenta de visualização de dados e processamento para análises
- Print do ambiente do Orange:
- ![image](https://github.com/user-attachments/assets/0d0423d8-d03d-4470-86d7-6c094e5a0f29)
### Correlations
- Correlação das features que não são variaveis categóricas:
- ![image](https://github.com/user-attachments/assets/ea503710-e311-457d-b100-c3beb9eb95f3)


### Fipe_Price x Price - Outlier detection
- Elimina-se todos os features menos Price Fipe_Price para projetarmos a detecção de ouliers:

- ![image](https://github.com/user-attachments/assets/3cf181be-c498-4a49-b569-8ae71ad503a1)

### Reproduzindo em python para encontrar o envelope de detecção
- Resultado:
- ![image](https://github.com/user-attachments/assets/704ccd02-9293-41ab-8026-102793018360)

### Eliminando erros de cadastramento
- Substitui-se os vazios ou inválidos
- ![image](https://github.com/user-attachments/assets/159c8078-ba7a-43f7-a326-cfa9fbfa244e)
- Resultado:
- ![image](https://github.com/user-attachments/assets/193be7ca-7e67-4867-b090-26e9e93a5754)

