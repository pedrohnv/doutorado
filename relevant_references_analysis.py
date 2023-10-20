# -*- coding: utf-8 -*-
"""
Research Question: What are the methods used to calculate the electric field
within and around an operating high voltage substation to determine if they
are under the safe levels for humans? Are they validated by experimental
measurement which establish the limit of their applicability?

Inclusion and exclusion criteria: The papers considered relevant are the ones
that present or cite a method for calculation of the electric field inside or
near a substation's equipment such that it can be used to assess whether that
field is under the safe levels for humans or not. Any paper that does not
calculate the electric field or calculates it only upon the surface of specific
equipment (such as a grading electrode) will be excluded from the review.

Meta-analysis factors:
- The paper is indeed relevant according to the criteria established in the
Plan and justify if it is deemed irrelevant;
- The method that it uses;
- Does the calculation presents any error estimate?
- Is there any comparison to experimental measurements?
- Is there any comparison with other methodologies or software?
- Is it a transient field analysis?
- Does it take into consideration the presence of a human body?
- Does it calculate the fields near (less than 2 m) equipment or conductive surfaces?
- At what heights are the calculations done?
- [TODO] What is the size of the calculation area?
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import bibtexparser

sns.set()
sns.set_theme(style="whitegrid")
dpi = 300

#%% Carregar dados relevantes
#filepath = "relevant_references.bib"
filepath = "metodos_calc.bib"
with open(filepath, 'r', encoding='utf-8') as f:
    bib = bibtexparser.load(f)

df = pd.DataFrame.from_dict(bib.entries)
df = df[(df['relevance'] == 'relevant')]

# 'Sebo1978Model' e 'Sebo1979Scale' são considerados duplicados, remover 1
n = df[(df['ID'] == 'Sebo1978Model')].index[0]
df = df.drop(index=n)

# excluir o ieee_c95_3 por ser muito amplo
n = df[(df['ID'] == 'ieee_c95_3')].index[0]
df = df.drop(index=n)

df = df.reset_index(drop=True)
df = df.convert_dtypes()
N = len(df)
#years = pd.to_numeric(df.loc[:, ('year')])
years = np.array(df.loc[:, ('year')], dtype=int)
df.loc[:, ('year')] = years


#%% Considera humano
human = df.loc[:, ('human')].astype('category')
df.loc[:, ('humano')] = human.cat.rename_categories({'yes' : 'sim', 'no' : 'não', 'robot' : 'robô'})

print(human.value_counts())

plt.figure()
ax = sns.histplot(df, x='year', discrete=True, hue='humano', multiple='stack', palette="tab10")
ax.set_ylabel("Contagem")
ax.set_xlabel("Ano")
sns.move_legend(ax, loc='upper left', title="Humano?")
minor_ticks = range(years.min(), years.max()+1)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.6, linestyle="--")
ax.grid(which='major', alpha=0.9)
plt.show()
plt.savefig("metodos_humano", dpi=dpi)

#%% Calcula próximo a equipamento
near = df.loc[:, ('near')]
df.loc[:, ('near')] = near.astype('category').cat.rename_categories({'yes' : 'sim', 'no' : 'não'})

# plt.figure()
# ax = sns.histplot(near, discrete=True)
# ax.set_xlabel("Considera proximidadde a equipamento?")
# ax.set_ylabel("Contagem")
# plt.show()
print(near.value_counts())

plt.figure()
ax = sns.histplot(df, x='year', discrete=True, hue='near', multiple='stack', palette="tab10")
ax.set_ylabel("Contagem")
ax.set_xlabel("Ano")
sns.move_legend(ax, loc='upper left', title="Próximo a equipamento?")
minor_ticks = range(years.min(), years.max()+1)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.6, linestyle="--")
ax.grid(which='major', alpha=0.9)
plt.show()
plt.savefig("metodos_proximo", dpi=dpi)

#%% Faz cálculo transitório?
transient = df['transient'].astype('category')

# plt.figure()
# ax = sns.histplot(transient, discrete=True)
# ax.set_xlabel("Faz cálculo transitório?")
# ax.set_ylabel("Contagem")
# plt.show()

#%% Qual tipo de comparação? Medição ou outro modelo?
''' df.loc[:, ('comparison')].astype('category')
['FEM, measurement', 'cdegs', 'comsol', 'measurement', 'measurement, fem',
 'measurement, simplified model', 'no', 'simplified or more complex model']
'''

comparison = df.loc[:, ('comparison')]
s1 = pd.Series(np.ndarray(N), dtype="string")
s2 = pd.Series(np.ndarray(N), dtype="string")
s3 = pd.Series(np.ndarray(N), dtype="string")
yes = "yes"
no = "no"
for i in range(N):
    try:
        if "measurement" in comparison[i]:
            s1[i] = yes
        else:
            s1[i] = no
    except TypeError:
        s1[i] = no
        
    try:
        c = comparison[i].lower()
        if "fem" in c or "cdegs" in c or "comsol" in c or "model" in c:
            s2[i] = yes
        else:
            s2[i] = no
    except AttributeError:
        s2[i] = no
        
    if s1[i] == yes and s2[i] == yes:
        s3[i] = "ambos"
    elif s1[i] == no and s2[i] == yes:
        s3[i] = "outro modelo"
    elif s1[i] == yes and s2[i] == no:
        s3[i] = "medição"
    else:
        s3[i] = "nenhuma"
    

df['comp2'] = pd.Categorical(s3, ['medição','outro modelo','ambos','nenhuma'])


# plt.figure()  # essa figura pode ser uma tabela
# ax = sns.histplot(df.loc[:, ('comp2')], discrete=True)
# ax.set_xlabel("Faz que comparação?")
# ax.set_ylabel("Contagem")
# plt.show()
print(df['comp2'].value_counts())

plt.figure()
ax = sns.histplot(df, x='year', discrete=True, hue='comp2', multiple='stack', palette="tab10")
ax.set_ylabel("Contagem")
ax.set_xlabel("Ano")
sns.move_legend(ax, loc='upper left', title="Comparação")
minor_ticks = range(years.min(), years.max()+1)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.6, linestyle="--")
ax.grid(which='major', alpha=0.9)
plt.show()
plt.savefig("metodos_comparacao", dpi=dpi)

#%% Método (modelo) usado
''' np.unique(method)
['analytical', 'bem', 'csm', 'csm, bem', 'csm, fem', 'csm, ga',
'csm, mom', 'csm, oddm', 'csm, scale', 'fem', 'fem, impedance',
'fit', 'interpolation', 'mom', 'mom, bem',
'mom, fem, gmt, vsie, fdtd, admittance, impedance, longwave, ebcm, sie',
'scale', 'spfd, admittance']
'''

method = df.loc[:, ('method')]
csm = pd.Series(["csm" in method[i].lower() for i in range(N)])
fem = pd.Series(["fem" in method[i].lower() for i in range(N)])
mom = pd.Series(["mom" in method[i].lower() or "bem" in method[i].lower() for i in range(N)])
other = np.logical_not(csm + fem + mom)

df2 = pd.DataFrame(np.transpose([csm, fem, mom, other]), columns=["CSM", "FEM", "MoM", "Outro"])
method2 = df2.dot(df2.columns + '_').str.rstrip('_')
method2[0] = "Outro"  # IEEE Standard, shouldn't count
df['method2'] = method2
print(df['method2'].value_counts())

plt.figure()
ax = sns.histplot(df, x='year', discrete=True, hue='method2', multiple='stack', palette="tab10")
ax.set_ylabel("Contagem")
ax.set_xlabel("Ano")
sns.move_legend(ax, loc='upper left', title="Método")
minor_ticks = range(years.min(), years.max()+1)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.6, linestyle="--")
ax.grid(which='major', alpha=0.9)
plt.show()
plt.savefig("metodos_modelo", dpi=dpi)


# plt.figure()
# ax = sns.histplot(df, x='method2', discrete=True)
# plt.show()

#%% Método vs. humano

plt.figure()
ax = sns.histplot(df, x='method2', shrink=.7, discrete=True, hue='humano', multiple='stack', palette="tab10")
ax.set_ylabel("Contagem")
ax.set_xlabel("Método")
sns.move_legend(ax, loc='upper right', title="humano?")
plt.show()
plt.savefig("metodos_modelo_humano", dpi=dpi)

#%% Método vs. equipamento

plt.figure()
ax = sns.histplot(df, x='method2', shrink=.7, discrete=True, hue='near', multiple='stack', palette="tab10")
ax.set_ylabel("Contagem")
ax.set_xlabel("Método")
sns.move_legend(ax, loc='upper right', title="Próximo a equipamento?")
plt.show()
plt.savefig("metodos_modelo_proximo", dpi=dpi)

#%% Estimativa do erro?
print(df[df['error'] != no].error)
# 7 artigos com estimativa do erro, todos comparam a N valores na fronteira...
# Eu não gosto disso. Qual a "densidade" necessária para se ter confiança?
