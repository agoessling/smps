import sympy


def ccm():
  vo, vi, d, ns, np = sympy.symbols('V_o V_i D N_s N_p')
  volt_eqn = sympy.Eq(vo / vi, ns / np * d / (1 - d))
  sympy.pprint(volt_eqn)

  dIm, lm, fsw = sympy.symbols('ΔI_m L_m F_s')
  delta_i_eqn = sympy.Eq(dIm, vi / lm * d / fsw)
  sympy.pprint(delta_i_eqn)

  Im, Io = sympy.symbols('I_m I_o')
  Im_eqn = sympy.Eq(Im, Io * (vo / vi + ns / np))
  sympy.pprint(Im_eqn)


def main():
  sympy.init_printing()
  ccm()


if __name__ == '__main__':
  main()
