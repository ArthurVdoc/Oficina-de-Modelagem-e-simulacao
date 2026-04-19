#!/usr/bin/env python3
"""Calcula a função de transferência de um sistema de segunda ordem.

Este script suporta:
- Sistema massa-mola-amortecedor com entrada de força: G(s) = 1 / (m*s^2 + c*s + k)
- Sistema com excitação de deslocamento de base: G(s) = (c*s + k) / (m*s^2 + c*s + k)

Uso:
    python calcula_funcao_transferencia.py --m 1 --c 10 --k 5 --tipo forca
    python calcula_funcao_transferencia.py --m 1 --c 2 --k 4 --tipo base
"""

import argparse
import sympy as sp


def transfer_function_force(m, c, k):
    s = sp.symbols('s')
    return 1 / (m * s**2 + c * s + k)


def transfer_function_base_excitation(m, c, k):
    s = sp.symbols('s')
    return (c * s + k) / (m * s**2 + c * s + k)


def main():
    parser = argparse.ArgumentParser(
        description='Calcula a função de transferência de um sistema massa-mola-amortecedor.'
    )
    parser.add_argument('--m', type=float, default=1.0, help='massa m (kg)')
    parser.add_argument('--c', type=float, default=1.0, help='atrito c (N.s/m)')
    parser.add_argument('--k', type=float, default=1.0, help='rigidez k (N/m)')
    parser.add_argument(
        '--tipo', choices=['forca', 'base'], default='forca',
        help='tipo de entrada: "forca" para força aplicada F(s) ou "base" para deslocamento de base Y(s)'
    )

    args = parser.parse_args()
    m, c, k = args.m, args.c, args.k

    if args.tipo == 'forca':
        G = transfer_function_force(m, c, k)
        descricao = 'G(s) = X(s) / F(s)'
    else:
        G = transfer_function_base_excitation(m, c, k)
        descricao = 'G(s) = X(s) / Y(s)'

    s = sp.symbols('s')
    G_simplified = sp.simplify(G)

    print('\nFunção de transferência:')
    print(f'  {descricao}')
    print('  m =', m, 'c =', c, 'k =', k)
    sp.pprint(G_simplified)

    num = sp.simplify(sp.factor(sp.simplify(sp.series(sp.simplify(G_simplified), s, 0, 1).removeO())))
    # Exibir polinômios do numerador e denominador
    numerador = sp.simplify(sp.factor(sp.simplify(sp.simplify(G_simplified).as_numer_denom()[0])))
    denominador = sp.simplify(sp.factor(sp.simplify(sp.simplify(G_simplified).as_numer_denom()[1])))

    print('\nNumerador:')
    sp.pprint(numerador)
    print('\nDenominador:')
    sp.pprint(denominador)

    print('\nCoefs. do numerador:', sp.Poly(numerador, s).all_coeffs())
    print('Coefs. do denominador:', sp.Poly(denominador, s).all_coeffs())


if __name__ == '__main__':
    main()
