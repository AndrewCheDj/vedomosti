from matplotlib import pyplot as plt
import seaborn as sns
from joblib import dump, load

data_ved = load('vedomosti_archive.pkl')
print(data_ved.info())
data = data_ved[data_ved.columns[1:3]]
print(data)

data_ved.topic.apply(len).hist()
plt.show()
data_ved.text.apply(len).hist()
plt.show()
















