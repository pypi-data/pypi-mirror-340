def a6a():   
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    def generate_dataset(n):
        x = []
        y = []
        random_x1 = np.random.rand()
        random_x2 = np.random.rand()
        for i in range(n):
            x1 = i
            x2 = i / 2 + np.random.rand() * n
            x.append([1, x1, x2])  # Including a bias term for completeness
            y.append(random_x1 * x1 + random_x2 * x2 + 1)  # Linear combination
        return np.array(x), np.array(y)

    x, y = generate_dataset(200)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x[:, 1], x[:, 2], y, label='y', s=5, color='blue')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Y')
    ax.legend()
    ax.view_init(45, 0)

    plt.show()



