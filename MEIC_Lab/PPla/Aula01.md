# Introdução ao MiniZinc

# Variaveis

```
Tipos básicos:
> int, float, bool, strings

Variaveis de parametros (constantes):

<TIPO> : <NOME>

e.g:
string : response;

Se for um int ou float também podes fazer isto

<l> .. <u> : <NOME>
(lower e upper bound fixos)
```

# Restrições
```
constraint <expressão>

e.g
constraint média >= 9.5;
```

# Resoluções
```

#1: Ver as que satisfazem o problema
solve satisfy; 

#2: Ver as que maximizam uma expressão
solve maximize <expressão>

#3: Ver as que minimizam uma expressão
solve minimize <expressão>
```

# Output

```
Serve para meter bonito mas não falámos disto ainda
```