import unicodedata
import matplotlib.pyplot as plt
import numpy as np
import os

def remove_vowels_and_double_consonants(phrase):
    vowels = "aeiouy"
    seen_consonants = set()
    result = []
    
    normalized_phrase = unicodedata.normalize('NFD', phrase.lower())
    
    normalized_phrase = ''.join(
        c for c in normalized_phrase 
        if unicodedata.category(c) != 'Mn'
    )
    
    for char in normalized_phrase:
        if char in vowels:
            continue
        
        if char not in seen_consonants and char.isalpha():
            seen_consonants.add(char)
            result.append(char)
    
    return ''.join(result).upper()


def letter_to_number_mapping(letter):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    table = [alphabet[i:i+8] for i in range(0, len(alphabet), 8)]
    
    for row in table:
        if letter in row:
            return row.index(letter) + 1


def map_result_to_numbers(result):
    return [letter_to_number_mapping(letter) for letter in result]


def draw_sigil(number_mapping, filename):
    fig, ax = plt.subplots()

    ax.set_aspect('equal')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    point_positions = [
        (6, 7.5),
        (7.5, 6),
        (7.5, 4),
        (6, 2.5),
        (3.4, 2.5),
        (2.5, 4),
        (2.5, 6),
        (4, 7.5)
    ]
    
    line_connections = []
    drawn_connections = set() 
    for i in range(len(number_mapping) - 1):
        part_start = number_mapping[i]
        part_end = number_mapping[i + 1]
        
        if part_start == part_end:
            x1, y1 = point_positions[part_start - 1]
            if i > 0:
                x0, y0 = point_positions[number_mapping[i - 1] - 1]
                dx = x1 - x0
                dy = y1 - y0
                length = np.sqrt(dx**2 + dy**2)
                if length != 0:
                    dx /= length
                    dy /= length
                offset = 0.2
                x, y = x1 + dx * offset, y1 + dy * offset
            else:
                x, y = x1 + 0.3, y1 + 0.3  
            plt.scatter(x, y, color='black', s=30) 
            continue
        
        connection = (part_start, part_end)
        reverse_connection = (part_end, part_start)

        if connection in drawn_connections or reverse_connection in drawn_connections:
            thickness = 2
        else:
            thickness = 1
        
        drawn_connections.add(connection)
        drawn_connections.add(reverse_connection)
        
        line_connections.append((point_positions[part_start - 1], point_positions[part_end - 1], thickness))

    start_point = point_positions[number_mapping[0] - 1]
    plt.scatter(start_point[0], start_point[1], color='black', s=30) 

    for start, end, thickness in line_connections:
        x_values = [start[0], end[0]]
        y_values = [start[1], end[1]]
        plt.plot(x_values, y_values, color='black', linewidth=thickness) 

    last_start, last_end, last_thickness = line_connections[-1]
    dx = last_end[0] - last_start[0]
    dy = last_end[1] - last_start[1]
    length = np.sqrt(dx**2 + dy**2)
    if length != 0:
        dx /= length
        dy /= length
    perpendicular_dx = -dy * 0.3 
    perpendicular_dy = dx * 0.3
    plt.plot([last_end[0] - perpendicular_dx/2, last_end[0] + perpendicular_dx/2], 
             [last_end[1] - perpendicular_dy/2, last_end[1] + perpendicular_dy/2], 
             color='black', linewidth=2) 

    ax.axis('off')

    plt.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()


def main ():
    phrase = "I have several passive income streams that allow me to be free"
    result = remove_vowels_and_double_consonants(phrase)
    print(f"Processed result : {result}")
    number_mapping = map_result_to_numbers(result)
    print(f"Number mapping : {number_mapping}")

    output_dir = './sigils'
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{phrase}.png")

    draw_sigil(number_mapping, filename=filename)


if __name__ == "__main__":
    main()
