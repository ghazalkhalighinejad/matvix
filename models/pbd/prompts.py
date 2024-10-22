
def get_prompt_dict(sample_compositions):
    
    prompt_dict = {
        "only-text":
            """Please read the following paragraphs, find all the polymer samples, and then fill out the given JSON template for each one of those samples. Please do not merge samples in the same JSON template. Every attribute (polymer type, DS/Modification/type, value of DS or Modification, Degree of hydrolysis, Molecular weight) should be filled out with one single value. If the value is not mentioned in the text, please fill it with null.

            {
                "Polymer Type": "",
                "Substitution Type": "",
                "Degree of Substitution": "",
                "Comonomer Type": "",
                "Degree of Hydrolysis": "",
                "Molecular Weight": "",
                "Molecular Unit": "",
                "Biodegradation":{
                    "headers": ["", ""],
                    "data": [],
                }
            }

            Biodegradation header should be filled out with the x and y labels which are the names of the conditions (e.g. time, temperature) and the names of the properties (e.g. biodegradation percentage, biodegradation rate). The data should be a list of (x, y) tuples. For example, if the biodegradation percentage is 50% at 10 days and 80% at 20 days, the data should be [(10, 50), (20, 80)]. If no biodegradation data is mentioned, please fill it with null.
            """,
        "only-image_single-image":
            f"""Given the image and the following polymer sample compositions, first identify which sample composition is present in the image then extract its properties.
                    
                Sample Compositions:
                {sample_compositions}

                For those sample compositions that are present in the image, extract the information about the property. The extracted information should be in JSON format as follows:

                Biodegradation: {{ 
                    "headers": ["", ""],
                    "data": [],
                }}

                Biodegradation header should be filled out with the x and y labels which are the names of the conditions (e.g. time, temperature) and the names of the properties (e.g. biodegradation percentage, biodegradation rate). The data should be a list of (x, y) tuples. For example, if the biodegradation percentage is 50% at 10 days and 80% at 20 days, the data should be [(10, 50), (20, 80)]. If no biodegradation data is mentioned, please fill it with null.
                
                Expand the sample composition JSONs to include the property information and return all the expanded JSONs."""
    }
    
    return prompt_dict