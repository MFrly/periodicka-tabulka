import csv
import json
import xml.etree.ElementTree as ET

# Načtení dat z CSV souboru
def load_elements(file_path):
    elements = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            elements.append(row)
    return elements

# Zobrazení všech vlastností prvku
def display_element(element):
    print("\nVlastnosti prvku:")
    for key, value in element.items():
        print(f"{key}: {value}")

# Vyhledávání prvku podle kritérií
def search_elements(elements, criterion, value):
    return [el for el in elements if el.get(criterion, '').lower() == value.lower()]

# Výběr prvků podle skupiny nebo periody
def filter_elements_by_group_or_period(elements, key, value):
    return [el for el in elements if el.get(key, '') == value]

# Výdaj průměrné relativní atomové hmotnosti

def calculate_average_mass(elements):
    masses = [float(el['AtomicMass']) for el in elements if el['AtomicMass'].replace('.', '', 1).isdigit()]
    return sum(masses) / len(masses) if masses else 0

# Generování HTML souboru
def generate_html(elements, file_path):
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write('<table border="1">\n')
        file.write('<tr>' + ''.join(f'<th>{key}</th>' for key in elements[0].keys()) + '</tr>\n')
        for element in elements:
            file.write('<tr>' + ''.join(f'<td>{value}</td>' for value in element.values()) + '</tr>\n')
        file.write('</table>\n')

# Generování JSON souboru
def generate_json(elements, file_path):
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(elements, file, indent=4)

# Generování XML souboru
def generate_xml(elements, file_path):
    root = ET.Element('Elements')
    for element in elements:
        el = ET.SubElement(root, 'Element')
        for key, value in element.items():
            child = ET.SubElement(el, key)
            child.text = value
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

# Generování Markdown souboru
def generate_markdown(elements, file_path):
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write('# Přehled chemických prvků\n\n')
        for element in elements:
            file.write(f"- **{element['Element']}** ({element['Symbol']}): Atomic Number {element['AtomicNumber']}\n")

# Hlavní menu aplikace
def main():
    elements = load_elements("elements.csv")

    while True:
        print("\nChemická databáze prvků")
        print("1. Zobrazit vlastnosti prvku")
        print("2. Vyhledat prvek podle kritéria")
        print("3. Zobrazit prvky podle skupiny nebo periody")
        print("4. Vypočítat průměrnou atomovou hmotnost")
        print("5. Generovat HTML soubor")
        print("6. Generovat JSON soubor")
        print("7. Generovat XML soubor")
        print("8. Generovat Markdown soubor")
        print("9. Ukončit")
        choice = input("Zvolte možnost: ")

        if choice == "1":
            query = input("Zadejte název prvku, symbol nebo protonové číslo: ")
            results = search_elements(elements, 'AtomicNumber', query) or \
                      search_elements(elements, 'Element', query) or \
                      search_elements(elements, 'Symbol', query)
            if results:
                for el in results:
                    display_element(el)
            else:
                print("Prvek nenalezen.")

        elif choice == "2":
            criterion = input("Zadejte kritérium (Element, Symbol, AtomicNumber): ")
            value = input("Zadejte hodnotu: ")
            results = search_elements(elements, criterion, value)
            if results:
                for el in results:
                    display_element(el)
            else:
                print("Prvek nenalezen.")

        elif choice == "3":
            key = input("Zadejte, zda chcete filtrovat podle skupiny (Group) nebo periody (Period): ")
            value = input("Zadejte hodnotu: ")
            results = filter_elements_by_group_or_period(elements, key, value)
            if results:
                for el in results:
                    display_element(el)
            else:
                print("Žádné prvky nenalezeny.")

        elif choice == "4":
            average_mass = calculate_average_mass(elements)
            print(f"Průměrná relativní atomová hmotnost: {average_mass:.2f}")

        elif choice == "5":
            file_path = "elements.html"
            generate_html(elements, file_path)
            print(f"HTML soubor byl vygenerován jako {file_path}.")

        elif choice == "6":
            file_path = "elements.json"
            generate_json(elements, file_path)
            print(f"JSON soubor byl vygenerován jako {file_path}.")

        elif choice == "7":
            file_path = "elements.xml"
            generate_xml(elements, file_path)
            print(f"XML soubor byl vygenerován jako {file_path}.")

        elif choice == "8":
            file_path = "elements.md"
            generate_markdown(elements, file_path)
            print(f"Markdown soubor byl vygenerován jako {file_path}.")

        elif choice == "9":
            print("Děkujeme za použití databáze.")
            break

        else:
            print("Neplatná volba. Zkuste to znovu.")

if __name__ == "__main__":
    main()
