import random
def find_cheapest_path(costs):
    n = len(costs)
    dp = [[0 for _ in range(n)] for _ in range(n)]
    
    # Compute the costs for moving left from the bottom row
    for j in range(1, n):
        dp[n - 1][j] = dp[n - 1][j-1] + costs[n - 1][j]
    
    # Compute the costs for moving up from the right column
    for i in range(n-2, -1, -1):
        dp[i][n-1] = dp[i+1][n-1] + costs[i][n-1]
    
    # Compute the costs for the remaining cells
    for i in range(n-2, -1, -1):
        for j in range(1, n):
            dp[i][j] = min(dp[i+1][j], dp[i][j-1]) + costs[i][j]
    
    print(*dp, sep = "\n")
    print(*costs, sep = "\n")
    return dp[0][n - 1]
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

