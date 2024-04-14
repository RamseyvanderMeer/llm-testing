from dotenv import load_dotenv
import json
import os
import re
import anthropicModule
import openaiModule
import toolsModule

class reader:
    """this is a class used to read .csv files for the anthropic pipeline"""

    def read_csv(self, file):
        with open(file, 'r') as file:
            return file.read()


if __name__ == "__main__":
    load_dotenv()

    anthropic_client = anthropicModule.anthropicLLM()
    openai_client = openaiModule.openaiLLM()
    prompt_tools = toolsModule.tools()
    csv_reader = reader()

    # read the csv file
    file = "Hours of operation.csv"
    data = csv_reader.read_csv(file)

    with open("output.json", "w") as file:
        file.write("[\n")
        for idx, line in enumerate(data.split("\n")):
            if idx > 4:
                break

            response = anthropic_client.get_response(prompt_tools.create_prompt(line, prompt_tools.hoursOfOpperationRequirements))
            # print(response)
            # print(response[0].text)
            result = re.search(r'\{(.|\n)*\}', response[0].text)

            # Extract and print the content if found
            if result:
                removed_result = result.group(0)

                # validate removed_result is a valid JSON string
                try:
                    reformated_response = json.loads(removed_result)
                except:
                    try:
                        reformated_response = anthropic_client.get_response(prompt_tools.validate_json_prompt(removed_result))
                        # print(reformated_response)
                        reformated_response = json.loads(re.search(r'\{(.|\n)*\}', reformated_response[0].text).group(0))
                    except Exception as e:
                        print(e)
                        break
            else:
                print("No outermost curly braces found.")

            # print(reformated_response)

            print(reformated_response["original"])


            # Write the reformated_response to the output file
            file.write(json.dumps(reformated_response, indent=4))
            file.write(",\n")
        # on close of the loop, remove the last comma and add the closing curly brace
        file.seek(file.tell()-2)
        file.write("\n]")
        file.close()