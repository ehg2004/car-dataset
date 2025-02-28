import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.covariance import EllipticEnvelope
from sklearn.linear_model import LinearRegression

#fontes:
#https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_anomaly_comparison.html#sphx-glr-auto-examples-miscellaneous-plot-anomaly-comparison-py


# Load dataset
dataset = "processed_dataset1.csv"  
df = pd.read_csv(dataset)

# deixando apenas features desejadas
df = df[["listing_id", "fipe_price", "price"]].dropna()

# Dados a serem analisados pelo estimador
X = df[["fipe_price", "price"]]

outlier_detector = EllipticEnvelope(contamination=0.01,support_fraction=0.2)
outlier_detector_fitted=outlier_detector.fit(X)
outlier_labels = outlier_detector_fitted.predict(X)

df["outlier"] = outlier_labels

# Plot dos dados originais
def plot_data(df, title):
    plt.figure(figsize=(8, 6))
    plt.scatter(df["fipe_price"], df["price"], c=df["outlier"], cmap="coolwarm", edgecolors="k")
    plt.xlabel("Fipe Price")
    plt.ylabel("Listed Price")
    plt.title(title)
    plt.colorbar(label="Outlier Label")
    plt.show()


# Plot dos dados originais com outliers detectados and limiar de decisão
def plot_data_with_decision_boundary(df, detector, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Scatter plot of data
    colors = np.array(["#377eb8" if label == 1 else "#ff7f00" for label in df["outlier"]])
    ax.scatter(df["fipe_price"], df["price"], c=colors, edgecolors="k", alpha=0.5)
    
    # Generate mesh grid for contour plot
    xx, yy = np.meshgrid(
        np.linspace(df["fipe_price"].min()-100000, df["fipe_price"].max()+100000, 100),
        np.linspace(df["price"].min()-100000, df["price"].max()+100000, 100)
    )
    Z = detector.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contour(xx, yy, Z, levels=[0], linewidths=2, colors="black")
    
    ax.set_xlabel("Fipe Price")
    ax.set_ylabel("Listed Price")
    ax.set_title(title)
    plt.show()

plot_data(df, "Fipe_Price x Price com outliers")
plot_data_with_decision_boundary(df, outlier_detector_fitted, "Fipe_Price x Price com Limiar de decisão ")

#corrige erros no cadastramento
for row in X.itertuples( ):
    #procura itens vazios ou não positivos
    if row.fipe_price<=0 or not isinstance(row.fipe_price,(int,float)):
        #substitui pelo equivalente na outra coluna
        df.at[row.Index, 'fipe_price'] = row.price 
    #procura itens vazios ou não positivos 
    if row.price<=0 or not isinstance(row.price,(int,float)):
        #substitui pelo equivalente na outra coluna
        df.at[row.Index, 'price'] = row.fipe_price  

plot_data_with_decision_boundary(df, outlier_detector_fitted, "Fipe_Price x Price com Limiar de decisão (erros eliminados) ")




# Testar o uso de ruído no detector
np.random.seed(42)
df_noisy = df.copy()
n_samples = len(df)
random_state = np.random.RandomState(42)
noise = random_state.normal(loc=0, scale=[df["fipe_price"].std() * 0.1, df["price"].std() * 0.1], size=(n_samples, 2))
df_noisy[["fipe_price", "price"]] += noise



X_noisy = df_noisy[["fipe_price", "price"]]
outlier_labels_noisy = outlier_detector_fitted.predict(X_noisy)
df_noisy["outlier"] = outlier_labels_noisy

plot_data(df_noisy, "Noisy Data with Outliers")
plot_data_with_decision_boundary(df, outlier_detector_fitted, "Original Data with Outliers and Decision Boundary")



# Regression plot
def plot_regression(df):
    X = df[["fipe_price"]]
    y = df["price"]
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(df["fipe_price"], df["price"], alpha=0.5, label="Data")
    plt.plot(df["fipe_price"], y_pred, color='red', linewidth=2, label="Regression Line")
    plt.xlabel("Fipe Price")
    plt.ylabel("Listed Price")
    plt.title("Fipe Price vs Listed Price Regression")
    plt.legend()
    plt.show()

plot_regression(df)
