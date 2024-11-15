import json
import requests
import sys


# Configuration parameters
ollama_url = 'http://URL:PORT/api/generate'  # Replace with your Ollama API URL
headers = {'Content-Type': 'application/json'}  # Adjust headers if necessary
model = 'phi3:14b'  # Model to use for generation
prompt_template = """Write me delimiter separated data. You will be creating {data_type} in the format \"{header}\". Generate {num_lines} lines.
ONLY respond with the delimiter separated data and do not include a header. Ensure that each data entry is separated by a newline.
Example: \"{example}\""""
max_lines = 200  # Maximum number of lines to generate
iteration_lines = 50  # Number of lines to generate in each iteration

def query_ollama(prompt: str):
    response = requests.post(ollama_url, headers=headers, json={'model': model,'prompt': prompt, 'stream': False})
    if response.status_code == 200:
        return json.loads(response.text)['response']
    else:
        raise Exception(f'Failed to query Ollama: {response.status_code} - {response.text}')
    
def print_help():
    print("""
          Usage: python generate_data_ollama.py <data_type>
          data_type: 'chores' or 'tools'
          """)
    
class ChoreDataGenerator:
    csv_header = 'chore_name|chore_description|total_time_minutes|frequency_days'
    data_type = 'chores'
    example = 'Replace the HVAC Filter|Replace the HVAC filter with a new one|30|90'

class ToolDataGenerator:
    csv_header = 'tool_name|tool_description'
    data_type = 'tools'
    example = '15mm Socket Wrench|A socket wrench with a 15mm socket'

def main():
    if len(sys.argv) != 2:
        print_help()
        sys.exit(1)

    if sys.argv[1] == 'tools':
        print('Using tool generator.')
        generator = ToolDataGenerator()
    elif sys.argv[1] == 'chores':
        print('Using chore generator.')
        generator = ChoreDataGenerator()
    else:
        print('Invalid data type.')
        print_help()
        sys.exit(1)
    
    prompt = prompt_template.format(data_type=generator.data_type, header=generator.csv_header, example=generator.example, num_lines=iteration_lines)
    output_file = f'generated_{generator.data_type}_data.csv'  # File where the data will be saved
    print(f'Using Prompt: {prompt}')
    
    with open(output_file, 'w') as file:
        file.write(generator.csv_header + '\n')

    generated_data = []
    while len(generated_data) < max_lines:
        data = query_ollama(prompt)
        for line in data.split('\n'):
            line = line.strip(' "')
            line_data = line.split('|')
            if len(line_data) != generator.csv_header.count('|') + 1:
                print(f'Skipping line: {line}')
                continue # Skip if the line does not have the correct number of columns

            # Check to see if the line[0] already exists in the generated_data
            if line_data[0] not in generated_data:
                generated_data.append(line_data[0])
                with open(output_file, 'a') as file:
                    file.write(line + '\n')
            else:
                print(f'Skipping duplicate line: {line}')
        print('Generated data length:', len(generated_data))
    print(f'Data saved to {output_file}')

if __name__ == '__main__':
    main()