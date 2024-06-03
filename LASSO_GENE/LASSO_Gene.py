import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import LocalOutlierFactor
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, confusion_matrix
import statsmodels.api as sm

data = pd.read_csv("/content/GSE92724_processed_counts.csv")

numeric_columns = data.columns[1:]

threshold = 10
filtered_data = data.loc[(data[numeric_columns].sum(axis=1) > threshold), :]

scaler = StandardScaler()
normalized_data = scaler.fit_transform(filtered_data[numeric_columns].T).T

normalized_df = pd.DataFrame(normalized_data, index=filtered_data.index, columns=filtered_data[numeric_columns].columns)
normalized_df.insert(0, 'GeneID', filtered_data['GeneID'])

conditions = ['GSM2436515', 'GSM2436516', 'GSM2436517', 'GSM2436518']
controls = [col for col in normalized_df.columns[1:] if col not in conditions]

condition_mean = normalized_df[conditions].mean(axis=1)
control_mean = normalized_df[controls].mean(axis=1)

differential_expression = condition_mean - control_mean

de_genes = pd.DataFrame({
    'GeneID': normalized_df['GeneID'],
    'Differential Expression': differential_expression
})

de_genes['Regulation'] = np.where(de_genes['Differential Expression'] > 0, 'Upregulated', 'Downregulated')

de_genes.to_csv("/content/differentially_expressed_genes.csv", index=False)

upregulated_genes = de_genes[de_genes['Regulation'] == 'Upregulated']
downregulated_genes = de_genes[de_genes['Regulation'] == 'Downregulated']

plt.figure(figsize=(10, 8))
de_genes['Differential Expression'].plot(kind='hist', bins=50, title='Differential Expression Analysis')
plt.xlabel('Differential Expression Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

top_de_genes = de_genes.set_index('GeneID')['Differential Expression'].abs().nlargest(60).index
heatmap_data = normalized_df.set_index('GeneID').loc[top_de_genes, conditions + controls]
plt.figure(figsize=(14, 12))
sns.heatmap(heatmap_data, cmap='coolwarm', xticklabels=True, yticklabels=True, annot=True)
plt.title('Heatmap of Top 60 Differentially Expressed Genes')
plt.xlabel('Samples')
plt.ylabel('Genes')
plt.show()

pca = PCA(n_components=3)
pca_result = pca.fit_transform(normalized_df.iloc[:, 1:])
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2', 'PC3'])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pca_df['PC1'], pca_df['PC2'], pca_df['PC3'], c='blue', marker='o')
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
ax.set_title('3D PCA of RNA-seq Data')

X = normalized_df[numeric_columns]
y = differential_expression
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lasso_cv = LassoCV(cv=5, random_state=42).fit(X_train, y_train)
best_alpha = lasso_cv.alpha_

lasso = Lasso(alpha=best_alpha)
lasso.fit(X_train, y_train)

y_pred = lasso.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Best alpha: {best_alpha}')
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='r')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=3)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.title('Lasso Regression: True vs Predicted Differential Expression')
plt.grid(True)
plt.show()

coef = pd.Series(lasso.coef_, index=X.columns)
print("Lasso coefficients:")
print(coef.sort_values(ascending=False))

median_de = de_genes['Differential Expression'].median()
binary_target = (de_genes['Differential Expression'] > median_de).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, binary_target, test_size=0.2, random_state=42)

lasso = Lasso(alpha=best_alpha)
lasso.fit(X_train, y_train)
y_pred = lasso.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)

accuracy = accuracy_score(y_test, y_pred_binary)
print("Accuracy Score:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred_binary))

conf_matrix = confusion_matrix(y_test, y_pred_binary)
print("Confusion Matrix:")
print(conf_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()
print("Confusion Matrix:")
print(conf_matrix)

