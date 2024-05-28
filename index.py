# Example data (as provided in the prompt)
data = [
    14.1,
    14.4,
    14.7,
    14.8,
    15.3,
    15.6,
    16.1,
    16.6,
    17.3,
    14.2,
    14.4,
    14.7,
    14.9,
    15.3,
    15.7,
    16.2,
    17.2,
    17.3,
    14.3,
    14.4,
    14.8,
    15,
    15.4,
    15.7,
    16.4,
    17.2,
    17.8,
    14.3,
    14.4,
    14.8,
    15,
    15.4,
    15.9,
    16.4,
    17.2,
    21.9,
    14.3,
    14.6,
    14.8,
    15.2,
    15.5,
    15.9,
    16.5,
    17.2,
    22.4,
]

class_intervals = [
    (14, 15),
    (15, 16),
    (16, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (20, 21),
    (21, 22),
    (22, 23),
]


def calculate_frequencies(data, class_intervals):
    """
    Calculates the frequencies for each class interval in the given data.

    Args:
        data: A list of numerical values.
        class_intervals: A list of tuples representing class interval boundaries
                          (inclusive on the lower bound, strictly less than the upper bound).

    Returns:
        A dictionary where keys are class interval boundaries (tuples) and values
        are the corresponding frequencies.
    """

    frequency_table = {}
    for value in data:
        for lower_bound, upper_bound in class_intervals:
            if (frequency_table.get((lower_bound, upper_bound))) == None :
                frequency_table[(lower_bound, upper_bound)] = {
                    "frequency": 0,
                    "cumulative_frequency": 0,
                    "relative_frequency": 0,
                    "cumulative_relative_frequency": 0,
                }
            if (
                lower_bound <= value < upper_bound
            ):  # Check if value falls within the interval (inclusive lower bound, exclusive upper bound)
                frequency_table.get((lower_bound, upper_bound)).update(
                    {
                        "frequency": (
                            frequency_table[(lower_bound, upper_bound)]["frequency"] + 1
                        )
                    }
                )
                break  # Exit the inner loop once the interval is found

    return frequency_table


def update_cumulative_freq(frequencies):
    # prevInterval = class_intervals[0]
    # frequencies[prevInterval].update({"cumulative_frequency": frequencies[prevInterval]["frequency"]})
    frequencies = frequencies
    prevInterval = class_intervals[0]
    for bounds  in class_intervals[1:]:
        if frequencies[prevInterval]["cumulative_frequency"] == 0:
            frequencies[prevInterval].update({ "cumulative_frequency": frequencies[prevInterval]["frequency"]})
        frequencies[bounds].update({"cumulative_frequency": frequencies[bounds]["frequency"]  + frequencies[prevInterval]["cumulative_frequency"]})
        prevInterval = bounds
    return frequencies



def update_relative_frequencies(frequency_table, total_data_points):
    """
    Calculates the relative frequencies for each class interval.
    Args:
        frequency_table: A dictionary where keys are class interval boundaries (tuples)
                          and values are the corresponding frequencies.
        total_data_points: The total number of data points.

    Returns:
        A dictionary where keys are class interval boundaries (tuples) and values
        are the corresponding relative frequencies.
    """
    frequency_table = frequency_table
    total_data_points = len(data)  # Assuming data is the list containing all values
    for interval in class_intervals:
        frequency = frequency_table[interval]["frequency"]
        frequency_table[interval].update({"relative_frequency": frequency / total_data_points})
    # for interval, frequency in frequency_table.items():
    return frequency_table

def calculate_cumulative_relative_frequency(frequencies, data):

    frequencies
    total_data_points = len(data)
    cumulative_count = 0
    for interval in class_intervals:
        cumulative_count += frequencies[interval]["frequency"]
        
        frequencies[interval].update({"cumulative_relative_frequency": cumulative_count / total_data_points})
    return frequencies


header_string = f"{'Interval'}{" ":>6s}{'Frequency'}{" ":>6s}\t{'Cumulative Frequency':<28s}\t{'Relative Frequency':<35}\t{'Cumulative Relative Frequency':<50s}"

def printRow(row,key):
    data_row = f"{key}{" ":>6s}{row["frequency"]}{" ":>10s}\t{row["cumulative_frequency"]}{" ":>28s}\t{row["relative_frequency"]:.4f}{"":>33s}\t{row["cumulative_relative_frequency"]:.4f}"
    print(data_row)
    return


def printRows(tab):
    for row in tab:
        printRow(tab[row], row)


if __name__ == "__main__":

    tab =calculate_cumulative_relative_frequency(update_relative_frequencies(update_cumulative_freq(calculate_frequencies(data, class_intervals)), data),data)
    print(header_string)
    printRows(tab)
    print(data)
