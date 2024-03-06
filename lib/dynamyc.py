import random
def find_cheapest_path(costs):
    n = len(costs)
    dp = [[0 for i in range(n)] for i in range(n)]
    for i in range(n - 1, 1):
        dp[i][0] = costs[i][0] + costs[i + 1][0]
    for i in range(1, n):
        dp[n - 1][i] = costs[n - 1][i] + costs[n - 1][i - 1]
def generate_random_table(size, spread):
    table = []
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            # Generate a random number within the specified spread
            random_number = random.randint(1, spread)
            
            # Append the random number to the row
            row.append(random_number)
        
        # Append the row to the table
        table.append(row)

    return table

