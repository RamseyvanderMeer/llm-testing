import json
import os
import re
import anthropicModule
import openaiModule
import toolsModule
from dotenv import load_dotenv
import jsonpickle

class reader:
    """this is a class used to read .csv files for the anthropic pipeline"""

    def read_csv(self, file):
        with open(file, 'r') as file:
            return file.read()


class evaluator:
    def calculateTotalScore(self, file, feild):
        with open(file, 'r') as f:
            data = json.load(f)
            total_score = 0
            potential_score = 0
            for item in data:
                total_score += float(item[feild])
                potential_score += 1
            return (total_score, potential_score)

    def evaluate(self, input_file, client, output_file="output.json", max_lines=100):
        # read the csv file
        # file = "Hours of operation.csv"
        data = csv_reader.read_csv(input_file)

        num_completed = 0
        if os.path.exists(output_file):
            try:
                f = open(output_file, "r")
                data = json.loads(f.read())
                print("File already exists")
                return
            except:
                # count number of json objects in the file to determine how many have been completed
                # file contains a list of json objects
                with open(output_file, "r") as file:

                    prev_data = file.read()
                    # remove the last comma and add a closing square bracket to prev_data
                    prev_data = prev_data[:len(prev_data)-2] + "\n]"
                    print(prev_data)
                    prev_data = json.loads(prev_data)
                    num_completed = len(prev_data)
                    # print(prev_data)
                    print("Number of completed evaluations: " + str(num_completed))
                    file.close()

        with open(output_file, "a") as file:
            if num_completed == 0:
                file.write("[\n")
            for idx, line in enumerate(data.split("\n")):
                if idx < num_completed:
                    continue
                print(str(idx + 1) + " of " + str(max_lines) + " file length: " + str(len(data.split("\n"))))

                if input_file == "Hours of operation.csv":
                    response = client.get_response(prompt_tools.create_prompt(line, prompt_tools.hoursOfOpperationRequirements))
                elif input_file == "Disabilities Access.csv":
                    response = client.get_response(prompt_tools.create_prompt(line, prompt_tools.disabilitiesAccessRequirements))
                # print(response)
                # print(response[0].text)
                # if client.name == "anthropic":
                #     res = response[0].text
                # else:
                #     res = response.choices[0].message

                result = re.search(r'\{(.|\n)*\}', response)

                # Extract and print the content if found
                if result:
                    removed_result = result.group(0)

                    # validate removed_result is a valid JSON string
                    try:
                        reformated_response = json.loads(removed_result)
                    except:
                        try:
                            reformated_response = client.get_response(prompt_tools.validate_json_prompt(removed_result))
                            # print(reformated_response)
                            reformated_response = json.loads(re.search(r'\{(.|\n)*\}', reformated_response).group(0))
                        except Exception as e:
                            reformated_response = {"original": line, "corrected": "llm provided borken formatting in response", "reasoning": jsonpickle.encode(e), "original_score": 0, "corrected_score": 0, "isValid": False}
                else:
                    reformated_response = {"original": line, "corrected": "llm provided borken formatting in response", "reasoning": "No reasoning provided", "original_score": 0, "corrected_score": 0, "isValid": False}

                # print(reformated_response)

                print(reformated_response["original"])


                # Write the reformated_response to the output file
                file.write(json.dumps(reformated_response, indent=4))
                file.write(",\n")
            file.close()
        with open(output_file, "r+") as file:
            # Move to the end of the file
            file.seek(0, 2)
            # Go back two characters from the end
            file.seek(file.tell() - 2)
            # Truncate the file at the new position, effectively deleting the last two characters
            file.truncate()
            # file.seek(file.tell()-2)
            file.write("\n]")
            file.close()

    def evaluate_llm(self, client, input_file, output_file="evaluation.json", max_lines=100, req_file="Hours of operation.csv"):
        print(output_file)
        num_completed = 0
        if os.path.exists(output_file):
            try:
                f = open(output_file, "r")
                data = json.loads(f.read())
                print("File already exists")
                return
            except:

                # count number of json objects in the file to determine how many have been completed
                # file contains a list of json objects
                with open(output_file, "r") as file:

                    prev_data = file.read()
                    # remove the last comma and add a closing square bracket to prev_data
                    prev_data = prev_data[:len(prev_data)-2] + "\n]"
                    print(prev_data)
                    prev_data = json.loads(prev_data)
                    num_completed = len(prev_data)
                    # print(prev_data)
                    print("Number of completed evaluations: " + str(num_completed))
                    file.close()

        f = open(input_file, "r")
        print(input_file)
        data = json.loads(f.read())

        with open(output_file, "a") as file:
            if num_completed == 0:
                file.write("[\n")
            for idx, item in enumerate(data):

                if idx < num_completed:
                    continue
                if req_file == "Hours of operation.csv":
                    response = client.get_response(prompt_tools.create_evaluation_prompt(item["original"], item["corrected"], item["reasoning"], item["original_score"], item["corrected_score"], item["isValid"], prompt_tools.hoursOfOpperationRequirements))
                elif req_file == "Disabilities Access.csv":
                    response = client.get_response(prompt_tools.create_evaluation_prompt(item["original"], item["corrected"], item["reasoning"], item["original_score"], item["corrected_score"], item["isValid"], prompt_tools.disabilitiesAccessRequirements))
                result = re.search(r'\{(.|\n)*\}', response)

                # Extract and print the content if found
                if result:
                    removed_result = result.group(0)
                    try:
                        file.write(json.dumps(json.loads(removed_result), indent=4))
                    except:
                        try:
                            reformated_response = client.get_response(prompt_tools.validate_json_evaluation_prompt(removed_result))
                            print(reformated_response)
                            reformated_response = json.loads(re.search(r'\{(.|\n)*\}', reformated_response).group(0))
                            file.write(json.dumps(reformated_response, indent=4))
                        except Exception as e:
                            fail_response = {"original": item["original"], "isValid": False, "original_score": item["original_score"], "corrected_score": 0, "corrected": item["corrected"], "reasoning": item["reasoning"], "your_score": 0, "your_reasoning": "llm provided borken formatting in response", "your_evaluation": False}
                            file.write(json.dumps(fail_response, indent=4))
                else:
                    fail_response = {"original": item["original"], "isValid": False, "original_score": item["original_score"], "corrected_score": 0, "corrected": item["corrected"], "reasoning": item["reasoning"], "your_score": 0, "your_reasoning": "llm provided borken formatting in response", "your_evaluation": False}
                    file.write(json.dumps(fail_response, indent=4))
                file.write(",\n")
                print(str(idx + 1) + " of " + str(len(data)))
            file.close()
        with open(output_file, "r+") as file:
            # Move to the end of the file
            file.seek(0, 2)
            # Go back two characters from the end
            file.seek(file.tell() - 2)
            # Truncate the file at the new position, effectively deleting the last two characters
            file.truncate()
            # file.seek(file.tell()-2)
            file.write("\n]")
            file.close()

    def run_llms(self, llm1, llm2, input_file):

        num_lines = sum(1 for line in open(input_file))
        # print(num_lines)
        # print(str(llm1.name) + " " + str(llm2.name) + " " + input_file)
        score_evaluator.evaluate(input_file, llm1, llm1.name + "_output_" + input_file + ".json", num_lines)
        score_evaluator.evaluate_llm(llm2, llm1.name + "_output_" + input_file + ".json", llm2.name + "_evaluation_of_" + llm1.name + "_" + input_file + ".json", num_lines, input_file)

        # calculate the scores
        total_original_score, potential_original_score = score_evaluator.calculateTotalScore(llm2.name + "_evaluation_of_" + llm1.name + "_" + input_file + ".json", "original_score")
        total_corrected_score, potential_corrected_score = score_evaluator.calculateTotalScore(llm2.name + "_evaluation_of_" + llm1.name + "_" + input_file + ".json", "corrected_score")
        llm_evaluation_score, llm_evaluation_potential_score = score_evaluator.calculateTotalScore(llm2.name + "_evaluation_of_" + llm1.name + "_" + input_file + ".json", "your_score")

        with open(llm2.name + "_evaluation_scores_of_" + llm1.name + ".json", "w") as file:
            file.write("Scores for " + str(llm1.name) + " correcting the data and " + str(llm2.name) + " evaluating the corrections" + "\n")
            file.write("Total Original Score: " + str(total_original_score) + " out of " + str(potential_original_score) + "\n")
            file.write("Total Corrected Score: " + str(total_corrected_score) + " out of " + str(potential_corrected_score) + "\n")
            file.write("LLM Evaluation Score: " + str(llm_evaluation_score) + " out of " + str(llm_evaluation_potential_score) + "\n")
            print("Scores for " + str(llm1.name) + " correcting the data and " + str(llm2.name) + " evaluating the corrections")
            print("Total Original Score: " + str(total_original_score) + " out of " + str(potential_original_score))
            print("Total Corrected Score: " + str(total_corrected_score) + " out of " + str(potential_corrected_score))
            print("LLM Evaluation Score: " + str(llm_evaluation_score) + " out of " + str(llm_evaluation_potential_score))

        with open("scores.csv", "a") as file:
            file.write(str(llm1.name) + "," + str(llm2.name) + "," + input_file + "," + str(total_original_score) + "," + str(potential_original_score) + "," + str(total_corrected_score) + "," + str(potential_corrected_score) + "," + str(llm_evaluation_score) + "," + str(llm_evaluation_potential_score) + "\n")
            file.close()

if __name__ == "__main__":
    load_dotenv()

    anthropic_client = anthropicModule.anthropicLLM()
    openai_35_client = openaiModule.openai35LLM()
    openai_4_client = openaiModule.openai4LLM()
    openai_4o_client = openaiModule.openai4oLLM()
    prompt_tools = toolsModule.tools()
    csv_reader = reader()
    score_evaluator = evaluator()

    with open("scores.csv", "w") as file:
        file.write("llm1,llm2,input_file,total_original_score,potential_original_score,total_corrected_score,potential_corrected_score,llm_evaluation_score,llm_evaluation_potential_score\n")
        file.close()

    score_evaluator.run_llms(openai_4o_client, openai_35_client, "Hours of operation.csv")
    score_evaluator.run_llms(openai_4o_client, openai_4_client, "Hours of operation.csv")
    # score_evaluator.run_llms(openai_35_client, openai_4_client, "Hours of operation.csv")
    # score_evaluator.run_llms(openai_4_client, openai_35_client, "Hours of operation.csv")
    # score_evaluator.run_llms(openai_35_client, anthropic_client, "Hours of operation.csv")
    # score_evaluator.run_llms(openai_4_client, anthropic_client, "Hours of operation.csv")

    score_evaluator.run_llms(openai_4o_client, openai_35_client, "Disabilities Access.csv")
    score_evaluator.run_llms(openai_4o_client, openai_4_client, "Disabilities Access.csv")

    score_evaluator.run_llms(openai_4o_client, anthropic_client, "Hours of operation.csv")
    score_evaluator.run_llms(openai_4o_client, anthropic_client, "Disabilities Access.csv")
    # score_evaluator.run_llms(openai_35_client, openai_4_client, "Disabilities Access.csv")
    # score_evaluator.run_llms(openai_4_client, openai_35_client, "Disabilities Access.csv")
    # score_evaluator.run_llms(openai_35_client, anthropic_client, "Disabilities Access.csv")
    # score_evaluator.run_llms(openai_4_client, anthropic_client, "Disabilities Access.csv")




