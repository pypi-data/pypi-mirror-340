def a3a():
    import pandas as pd

    # Create the DataFrame
    data = pd.DataFrame({
        'player': ['A', 'B', 'C', 'D', 'E'],
        'game1': [18, 22, 10, 14, 17],
        'game2': [5, 7, 9, 3, 6],
        'game3': [1, 8, 10, 6, 4],
        'game4': [9, 8, 10, 9, 3]
    })

    print("To create data\n")
    print(data)

    # Save the DataFrame to a CSV file
    data.to_csv('sample.csv', index=False)

    print("\nTo load data\n")
    df = pd.read_csv('sample.csv')
    print(df)




