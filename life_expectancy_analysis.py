def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def process_data(lines):
    min_life_expectancy = float('inf')
    max_life_expectancy = float('-inf')
    data = []

    min_life_info = ()
    max_life_info = ()

    for line in lines[1:]:  # Skip the header
        parts = line.strip().split(',')
        try:
            country = parts[0]
            year = int(parts[2])
            life_expectancy = float(parts[3])
        except ValueError as e:
            print(f"Skipping line due to error: {line.strip()} - {e}")
            continue

        data.append((country, year, life_expectancy))

        if life_expectancy < min_life_expectancy:
            min_life_expectancy = life_expectancy
            min_life_info = (country, year, life_expectancy)

        if life_expectancy > max_life_expectancy:
            max_life_expectancy = life_expectancy
            max_life_info = (country, year, life_expectancy)

    return min_life_info, max_life_info, data

def analyze_year(data, year):
    year_data = [entry for entry in data if entry[1] == year]
    if not year_data:
        return None, None, None, None

    total_life_expectancy = sum(entry[2] for entry in year_data)
    average_life_expectancy = total_life_expectancy / len(year_data)

    min_entry = min(year_data, key=lambda x: x[2])
    max_entry = max(year_data, key=lambda x: x[2])

    return average_life_expectancy, min_entry, max_entry

def find_largest_drop(data):
    country_year_data = {}
    for entry in data:
        country, year, life_expectancy = entry
        if country not in country_year_data:
            country_year_data[country] = []
        country_year_data[country].append((year, life_expectancy))

    largest_drop = 0
    largest_drop_info = None

    for country, values in country_year_data.items():
        values.sort()  # Sort by year
        for i in range(1, len(values)):
            drop = values[i-1][1] - values[i][1]
            if drop > largest_drop:
                largest_drop = drop
                largest_drop_info = (country, values[i-1][0], values[i][0], drop)

    return largest_drop_info

def main():
    # File path to the dataset
    file_path = r'D:\Users\J.I Traders\Desktop\life_expantancy\life-expectancy11.csv'
    lines = read_data(file_path)

    # Process data
    min_life_info, max_life_info, data = process_data(lines)

    # User input for year analysis
    year = int(input('Enter the year of interest: '))

    # Display overall min and max life expectancy with country and year info
    print(f'\nThe overall max life expectancy is: {max_life_info[2]} from {max_life_info[0]} in {max_life_info[1]}')
    print(f'The overall min life expectancy is: {min_life_info[2]} from {min_life_info[0]} in {min_life_info[1]}\n')

    # Analyze data for the specified year
    avg_life_expectancy, min_entry, max_entry = analyze_year(data, year)

    if avg_life_expectancy is not None:
        print(f'For the year {year}:')
        print(f'The average life expectancy across all countries was {avg_life_expectancy:.2f}')
        print(f'The max life expectancy was in {max_entry[0]} with {max_entry[2]:.2f}')
        print(f'The min life expectancy was in {min_entry[0]} with {min_entry[2]:.2f}')
    else:
        print(f'No data available for the year {year}')

    # Find the largest drop in life expectancy
    largest_drop_info = find_largest_drop(data)
    if largest_drop_info:
        country, year1, year2, drop = largest_drop_info
        print(f'\nThe largest drop in life expectancy was in {country} from {year1} to {year2} with a drop of {drop:.2f} years.')

if __name__ == "__main__":
    main()

