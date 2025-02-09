# Descrição
Ferramenta para exportar anúncios do site Imóveis SC para uma tabela.


# Instalação

```
git clone https://github.com/nesvera/imoveis-sc-to-table.git
pip3 install -r requirements.txt
```

# Como funciona

1. Accesse o site [imóveis-sc](https://www.imoveis-sc.com.br)
2. Use a ferramenta para criar um filtro com as especificações do imóvel
3. Clique em buscar
4. Copie a URL que aparece no browser

Exemplo:
```
https://www.imoveis-sc.com.br/blumenau/comprar/apartamento/agua-verde_boa-vista_bom-retiro_centro_itoupava-seca_jardim-blumenau_ponta-aguda_ribeirao-fresco_velha_victor-konder_vila-formosa_vila-nova/quartos/2?ordenacao=menor-preco&valor=300000-450000&area=48-&suites=1
```

5. Abra o arquivo ``imoveis_sc_crawler.py``
6. Altere a variável ``url``com o URL que você copiou acima
7. Salve o arquivo
8. Execute o script

```
python3 imoveis_sc_crawler.py
```

9. Abra o arquivo ``imoveis.xlsx ``
10. Você pode marcar as colunas ``changed``, ``viewed``, ``disliked`` e ``deleted`` com ``x```
11. Salve o arquivo quando finalizar
12. Você pode executar o script do passo 5 quantas vezes quiser para atualizar a tabela com dados novos do site
