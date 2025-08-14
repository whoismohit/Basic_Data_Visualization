import csv
import os

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def read_csv(filename):
    """Read CSV and return headers + data (numeric only)."""
    data = []
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                try:
                    data.append((row[0], float(row[1])))
                except ValueError:
                    print(f"{Colors.RED}Skipping invalid row: {row}{Colors.END}")
        return headers, data
    except FileNotFoundError:
        print(f"{Colors.RED}File not found: {filename}{Colors.END}")
        return None, []

def display_bar_chart(data, scale=1):
    """Display bar chart in ASCII with scaling."""
    print(f"\n{Colors.BOLD}BAR CHART{Colors.END}")
    for label, value in data:
        bar = '█' * int(value / scale)
        print(f"{Colors.CYAN}{label:<15}{Colors.END} | {bar} {Colors.YELLOW}({value}){Colors.END}")

def display_line_chart(data, scale=1):
    """Display a cleaner, aligned ASCII line chart."""
    print(f"\n{Colors.BOLD}LINE CHART{Colors.END}")
    max_val = max(value for _, value in data)
    height = int(max_val / scale)
    col_width = 4  # Fixed width for alignment

    # Draw chart top to bottom
    for level in range(height, 0, -1):
        line = ''
        for _, value in data:
            if int(value / scale) >= level:
                line += f"{'●':<{col_width}}"
            else:
                line += f"{' ':<{col_width}}"
        print(f"{Colors.BLUE}{line}{Colors.END}")

    # Draw labels under chart
    labels_line = ''.join(f"{label[:3]:<{col_width}}" for label, _ in data)  # 3 letters max for neatness
    print(f"{Colors.YELLOW}{labels_line}{Colors.END}")


def visualize_data(data):
    """Ask chart questions and display output."""
    while True:
        # Sorting
        sort_choice = input("Sort by value? (y/n): ").strip().lower()
        if sort_choice == 'y':
            order = input("Ascending (a) or Descending (d)?: ").strip().lower()
            reverse = (order == 'd')
            data.sort(key=lambda x: x[1], reverse=reverse)

        # Scaling
        scale = input("Enter scale factor (default 1): ").strip()
        scale = float(scale) if scale else 1

        # Chart type
        chart_type = input("Bar chart (b) or Line chart (l)?: ").strip().lower()
        if chart_type == 'b':
            display_bar_chart(data, scale)
        else:
            display_line_chart(data, scale)

        # Repeat with same data?
        again = input("\nDo you want to visualize again with the same data? (y/n): ").strip().lower()
        if again != 'y':
            break

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colors.HEADER}=== Basic Data Visualization Tool ==={Colors.END}")

    filename = input("Enter CSV filename (with .csv): ").strip()
    headers, data = read_csv(filename)
    if not data:
        return

    visualize_data(data)

if __name__ == "__main__":
    main()
