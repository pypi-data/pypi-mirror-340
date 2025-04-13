def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
import seaborn as sns
import matplotlib.pyplot as plt
# Data
x = [15, 20, 25, 30, 35, 40]
y = [150, 180, 220, 250, 270, 300]
# Scatter plot
sns.scatterplot(x=x, y=y)
plt.title('Sales vs Advertising Spend')
plt.show()

    '''
    print(code)