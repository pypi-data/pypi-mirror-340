# duanbima

Biblioteca que contém o calendário ANBIMA desde 2001 até 2099.

## Instalação

Você pode instalar esta biblioteca usando:

pip install duanbima

## Importando

from duanbima import diasuteis

## Funções

du.hoje() - Retorna o dia útil D0

du.hoje(-1) - Retorna D-1 

du.hoje(1) - Retorna D+1

du.qntdu({data_inicio}, {datafim})  - Retorna a quantidade de dias úteis entre as datas

du.help() - Todos os comandos da biblioteca.
