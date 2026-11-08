import re


def limpar(documento):
    """Remove pontuação e espaços, preservando letras para o CNPJ alfanumérico."""
    return re.sub(r"[^A-Za-z0-9]", "", str(documento or "")).upper()


def formatar(doc):
    """Formata CPF ou CNPJ durante a digitação, inclusive CNPJ alfanumérico."""
    valor = limpar(doc)
    if any(letra.isalpha() for letra in valor) or len(valor) > 11:
        valor = valor[:14]
        partes = [valor[:2], valor[2:5], valor[5:8], valor[8:12], valor[12:]]
        separadores = [".", ".", "/", "-"]
    else:
        valor = valor[:11]
        partes = [valor[:3], valor[3:6], valor[6:9], valor[9:]]
        separadores = [".", ".", "-"]

    resultado = partes[0]
    for indice, parte in enumerate(partes[1:]):
        if not parte:
            break
        resultado += separadores[indice] + parte
    return resultado


def validar_cpf(cpf):
    cpf = limpar(cpf)
    if not cpf.isdigit() or len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    numeros = [int(digito) for digito in cpf]
    soma = sum(numero * peso for numero, peso in zip(numeros[:9], range(10, 1, -1)))
    resto = soma % 11
    digito_1 = 0 if resto < 2 else 11 - resto
    if digito_1 != numeros[9]:
        return False

    soma = sum(numero * peso for numero, peso in zip(numeros[:10], range(11, 1, -1)))
    resto = soma % 11
    digito_2 = 0 if resto < 2 else 11 - resto
    return digito_2 == numeros[10]


def validar_cnpj(cnpj):
    """Valida CNPJ numérico ou alfanumérico (14 posições, 2 verificadores numéricos)."""
    cnpj = limpar(cnpj)
    if len(cnpj) != 14 or not cnpj[:12].isalnum() or not cnpj[8:12].isdigit():
        return False
    if not cnpj[12:].isdigit() or len(set(cnpj)) == 1:
        return False

    # Cada caractere da base é convertido pelo valor ASCII menos 48,
    # conforme a regra oficial do CNPJ alfanumérico.
    valores = [ord(caractere) - 48 for caractere in cnpj[:12]]
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(valor * peso for valor, peso in zip(valores, pesos_1))
    resto = soma % 11
    digito_1 = 0 if resto < 2 else 11 - resto
    if digito_1 != int(cnpj[12]):
        return False

    valores_com_dv1 = valores + [digito_1]
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(valor * peso for valor, peso in zip(valores_com_dv1, pesos_2))
    resto = soma % 11
    digito_2 = 0 if resto < 2 else 11 - resto
    return digito_2 == int(cnpj[13])
