class tools:
    """this is a class used to store the prompts for the anthropic pipeline"""

    def __init__(self):
        self.hoursOfOpperationRequirements = """
Days of the week are abbreviated as follows: {Mon, Tues, Wed, Thurs, Fri, Sat, Sun}

The opening or closing hour of the day includes hour and minute, separated by a colon, followed

by “am” or “pm” designation after a space. The “am” and “pm” designations are always lower

case and never include a period:

* 8:00 am



Hours of Operation is almost always expressed as a period of time. Hence, an “[Hour] space dash

space [Hour]” format is used. The long-form dash is used, which is auto-formatted when typing a

dash, followed by a space, then one or more characters, and finally another space:

* 9:30 am - 5:00 pm



Hours of Operation must include one or more days of the week. For consecutive days of the week,

use a hyphen. Days come first, then hours.

* Mon - Thurs 8:00 am - 5:00 pm



Use commas to separate non-consecutive days with the same hours, and gaps in time on the same

days. Use semicolons to separate days of the week.

* Mon, Wed, Fri 6:00 am - 12:00 pm, 1:00 pm - 5:00 pm; Sat 10:00 am - 12:00 pm



24-hour services provided 7 days a week are formatted as:

* 24 hours a day, 7 days a week



For services with the same hours each day of the week, start with Sunday and end with Saturday:

* Sun - Sat 9:00 am - 5:00 pm



For services with differing weekend and weekday hours, start with Monday:

* Mon - Fri 7:00 am - 7:00 pm; Sat 8:00 am - 5:00 pm; Sun 8:30 am - 3:00 pm



For differing hours within a Program, such as multiple services, use a line break:

* Application Hours: Mon - Fri 8:00 am - 1:00 pm

Service Hours: Mon - Wed 7:00 pm - 9:00 pm
"""
        self.disabilitiesAccessRequirements = """
Lists specific accessibility features that the location has, lacks, separated by a line return. If no information is known, use “Call for information”. If some information is entered but some is not known, add “Call for more information”. Do not state that a location lacks a non-applicable feature. For example, braille directories are not applicable if the location houses just one entity (i.e. single- unit). Do not just indicate “Yes” or “Accessible”. Always characterize the accessibility features that are present.

-Location has bathroom grab bars, wheelchair ramps.

-Location lacks braille directories.

-Call for more information
"""

    def create_prompt(self, fieldValue, requirements):
        return f"""
        Your task is to validate whether a data field value meets a set of requirements. And return a JSON object with the format shown below.

        The field value is:
        <field_value>
        {fieldValue}
        </field_value>

        The requirements for the field are:
        <requirements>
        {requirements}
        </requirements>

        Carefully compare the provided field value to the stated requirements.
        Return a response JSON object shown below.
        - In the resoning feild of the response object, explain in detail how the value does or does not meet each requirement.
        - If the value does not meet the requirements, provide a corrected value that does in the corrected field. If the value meets the requirements, the corrected field should be the same as the field value.
        - In the isValid field of the response object, return true if the value meets the requirements and false if it does not.
        - In the original_score field of the response object, score field of the response object, return a number between 0 and 1 that represents the confidence level that the original value meets the requirements. A score of 1 means the value meets the requirements with 100% confidence. A score of 0 means the value does not meet the requirements with 0% confidence.
        - In the corrected_score field of the response object, return a number between 0 and 1 that represents the confidence level that the corrected value meets the requirements. A score of 1 means the corrected value meets the requirements with 100% confidence. A score of 0 means the corrected value does not meet the requirements with 0% confidence.

        Only return the response obhect and make sure it is formatted-as-JSON-safe-string!

        {{
            "original": "{fieldValue}",
            "isValid": "Boolean",
            "original_score": "Number",
            "corrected_score": "Number",
            "corrected": "String",
            "reasoning": "String"
        }}
        """

    def create_evaluation_prompt(self, original, corrected, reasoning, original_score, corrected_score, isValid, requirements):
        return f"""
        your task is to evaluate a peer response to a data validation task. The peer has been asked to validate whether a data field value meets a set of requirements.

        The original field value is:
        <original>
        {original}
        </original>

        The requirements for the field are:
        <requirements>
        {requirements}
        </requirements>

        The peer has given the following corrected field value:
        <corrected>
        {corrected}
        </corrected>

        The peer has given the following reasoning for their correction:
        <reasoning>
        {reasoning}
        </reasoning>

        The peer has given the following scores for their original and corrected values:
        <scores>
        Original Score: {original_score}
        Corrected Score: {corrected_score}
        </scores>

        The peer has given the following evaluation of the corrected value:
        <evaluation>
        {isValid}
        </evaluation>

        Your task is to evaluate the peer's task. Return a JSON object with the format shown below.

        {{
            "original": "fieldValue",
            "isValid": "Boolean",
            "original_score": "Number",
            "corrected_score": "Number",
            "corrected": "String",
            "reasoning": "String"
            "your_evaluation": "Boolean"
            "your_score": "Number"
            "your_reasoning": "String"
        }}

        - In the your_evaluation field of the response object, return true if the corrected value meets the requirements and false if it does not.
        - In the your_score field of the response object, return a number between 0 and 1 that represents the confidence level that the corrected value meets the requirements. A score of 1 means the corrected value meets the requirements with 100% confidence. A score of 0 means the corrected value does not meet the requirements with 0% confidence.
        - In the your_reasoning field of the response object, explain in detail how the corrected value does or does not meet each requirement.
        """



    def validate_json_prompt(self, responseToFomat):
        return f"""
You will be given a string in JSON format like this:

<json>
{{
    "original": "fieldValue",
    "isValid": "Boolean",
    "original_score": "Number",
    "corrected_score": "Number",
    "corrected": "String",
    "reasoning": "String"
}}
</json>

Your task is to first check if this JSON string is "safe" (hint it is not). A "safe" JSON string has the following
properties:
- All keys are enclosed in double quotes
- All string values are enclosed in double quotes
- Double quotes within string values are properly escaped with a backslash (\)
- Special characters like newlines, tabs, siglequotes and backslashes within string values are properly escaped
with a backslash (\)

For example, this is an unsafe JSON string because the keys are not in quotes and the string values are not properly escaped:
<unsafe_example>
{{name: "Bob", age: 25, city: 'New York'}}
</unsafe_example>
...
Here is the JSON string to process:
<json>
{responseToFomat}
</json>

If the JSON string is safe, return the original string (hint it is not). If the JSON string is not safe, return a corrected version of the string that is safe.
"""


def validate_json_evaluation_prompt(self, responseToFomat):
        return f"""
You will be given a string in JSON format like this:

<json>
{{
    "original": "fieldValue",
    "isValid": "Boolean",
    "original_score": "Number",
    "corrected_score": "Number",
    "corrected": "String",
    "reasoning": "String",
    "your_evaluation": "Boolean",
    "your_score": "Number",
    "your_reasoning": "String"
}}
</json>

Your task is to first check if this JSON string is "safe" (hint it is not). A "safe" JSON string has the following
properties:
- All keys are enclosed in double quotes
- All string values are enclosed in double quotes
- Double quotes within string values are properly escaped with a backslash (\)
- Special characters like newlines, tabs, siglequotes and backslashes within string values are properly escaped
with a backslash (\)

For example, this is an unsafe JSON string because the keys are not in quotes and the string values are not properly escaped:
<unsafe_example>
{{name: "Bob", age: 25, city: 'New York'}}
</unsafe_example>
...
Here is the JSON string to process:
<json>
{responseToFomat}
</json>

If the JSON string is safe, return the original string (hint it is not). If the JSON string is not safe, return a corrected version of the string that is safe.
"""
