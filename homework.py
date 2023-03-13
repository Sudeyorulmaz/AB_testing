import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp , shapiro , levene , kendalltau, \
    f_oneway , kruskal, ttest_ind

# Veriyi hazırlama ve analiz etme


df_control = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("ab_testing.xlsx",sheet_name="Test Group")

pd.set_option("display.max_columns",None)
unnamed=df_test.loc[:,df_test.columns.str.contains("Unnamed")]
df_test.drop(unnamed,axis=1,inplace= True)
unnamed1=df_control.loc[:,df_control.columns.str.contains("Unnamed")]
df_control.drop(unnamed1,axis=1,inplace=True)


def check(dataframe,head=5):

    print("########Shape###########")
    print(dataframe.shape)
    print("########types###########")
    print(dataframe.dtypes)
    print("########head############")
    print(dataframe.head(head))
    print("#########tail#############")
    print(dataframe.tail())
    print("########quantiles########")
    print(dataframe.quantile([0, 0.05,0.50,0.95,0.99,1]).T)

check(df_test)
check((df_control))

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test],axis=0,ignore_index=False)


# A/B testinin hipotezinin tanımlanması
# H0 : M1 = M2 Maximum bidding ilE average bidding uygulanan gruplarının satın alma ortlamaları arasında istaitksel olarak fark yoktur.
# H1 : M1 != M2 ... yoktur.
# pvalue < 0.05 ise H0 reddedilemez.

df.groupby("group").agg({"Purchase": "mean"})

# Hipotez testinin gerçekleştirilmesi ve varsayım kontrolü

# Normallik varsayımı
# H0 : Normallik varsayımı sağlanmaktadır.
# H1 : ... sağlanmamaktadır.

test_stat , pvalue = shapiro(df.loc[df["group"]== "control","Purchase"])
print("Test stat: = %.4f, p-value: = %.4f" % (test_stat,pvalue))

test_stat , pvalue = shapiro(df.loc[df["group"]== "test","Purchase"])
print("Test stat: = %.4f, p-value: = %.4f" % (test_stat,pvalue))

# H0 reddedilemez. Normallik varsayımı sağlanmaktadır.

# Varyans homojenliği
# H0 : Varyanslar homojendir.
# H1 : ... değildir.
test_stat,pvalue = levene(df.loc[df["group"]== "control","Purchase"],
                          df.loc[df["group"]=="test","Purchase"])
print("Test stat: = %.4f, p-value: = %.4f" % (test_stat,pvalue))
# H0 reddedilemez. Varyanslar homojendir.

# Varsayımlar sağlandığından dolayı bağımsız iki örneklem t testi kullanılır.(Parametrik test)

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control","Purchase"],
                              df.loc[df["group"]=="test","Purchase"],
                              equal_var=True)
print("Test stat: = %.4f, p-value: = %.4f" % (test_stat,pvalue))

# H0 reddedilemez.Kontrol ve test gruplarının satın alma ortalamaları arasında istatiksel olarak anlamlı bir farklılık yoktur.