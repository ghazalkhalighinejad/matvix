
def get_prompt_dict(sample_compositions):
    
    prompt_dict = {
        "allin_single-image":
            """
            Please read the following paragraphs, find all the nano-composite samples, along with their properties that can be presented in the image, and then fill out the given JSON template for each one of those nanocomposite samples. Please do not merge samples of different compositions. If an attribute is not mentioned in the paragraphs fill that section with "null". Mass and Volume Composition should be followed by a %.

            {{
                "Matrix Chemical Name": "chemical_name",
                "Matrix Chemical Abbreviation": "abbreviation",
                "Filler Chemical Name": "chemical_name",
                "Filler Chemical Abbreviation": "abbreviation",
                "Filler Composition Mass": "mass_value",
                "Filler Composition Volume": "volume_value",
                "Filler Particle Surface Treatment Chemical Name": "chemical_name",
                "Properties": [
                    {{
                        "property name": "property_name", 
                        "headers": ["", ""],
                        "data": []
                    }}
                ]
            }}  

            Properties is a list of dictionaries where each dictionary represents a property of the nanocomposite. The property name should be filled out with the name of the property where the choicese are: electrical, mechanical, viscoealstic, thermal, volumetric, rheological.
            The headers should be filled out with the x and y labels which are the names of the conditions or the labels of the data (e.g. time, temperature, frequency, strain, conductivity, dielectric strength, etc.). The data should be a list of (x, y) tuples. For example, if the property is 24 MPa at temperature 25°C and 30 MPa at temperature 50°C, the data should be [(25, 24), (50, 30)]. If no data is mentioned, please fill it with null.
        """,
        "allin_multi-image":
            """
            Please read the following paragraphs, find all the nano-composite samples, along with their properties that can be presented in the images, and then fill out the given JSON template for each one of those nanocomposite samples. Please do not merge samples of different compositions. If an attribute is not mentioned in the paragraphs fill that section with "null". Mass and Volume Composition should be followed by a %.

            {{
                "Matrix Chemical Name": "chemical_name",
                "Matrix Chemical Abbreviation": "abbreviation",
                "Filler Chemical Name": "chemical_name",
                "Filler Chemical Abbreviation": "abbreviation",
                "Filler Composition Mass": "mass_value",
                "Filler Composition Volume": "volume_value",
                "Filler Particle Surface Treatment Chemical Name": "chemical_name",
                "Properties": [
                    {{
                        "property name": "property_name", 
                        "headers": ["", ""],
                        "data": []
                    }}
                ]
            }}

            Properties is a list of dictionaries where each dictionary represents a property of the nanocomposite. The property name should be filled out with the name of the property where the choicese are: electrical, mechanical, viscoealstic, thermal, volumetric, rheological.
            The headers should be filled out with the x and y labels which are the names of the conditions or the labels of the data (e.g. time, temperature, frequency, strain, conductivity, dielectric strength, etc.). The data should be a list of (x, y) tuples. For example, if the property is 24 MPa at temperature 25°C and 30 MPa at temperature 50°C, the data should be [(25, 24), (50, 30)]. If no data is mentioned, please fill it with null.

            """,
        "only-text":
            """Please read the following paragraphs, find all the nano-composite samples, and then fill out the given JSON template for each one of those nanocomposite samples. Please do not merge samples of different compositions. If an attribute is not mentioned in the paragraphs fill that section with "null". Mass and Volume Composition should be followed by a %. 

            {{
                "Matrix Chemical Name": "chemical_name",
                "Matrix Chemical Abbreviation": "abbreviation",
                "Filler Chemical Name": "chemical_name",
                "Filler Chemical Abbreviation": "abbreviation",
                "Filler Composition Mass": "mass_value",
                "Filler Composition Volume": "volume_value",
                "Filler Particle Surface Treatment Chemical Name": "chemical_name",
                "Properties": [
                    {{
                        "property name": "property_name", 
                        "headers": ["", ""],
                        "data": []
                    }}
                ]
            }}

            Properties is a list of dictionaries where each dictionary represents a property of the nanocomposite. The property name should be filled out with the name of the property where the choicese are: electrical, mechanical, viscoealstic, thermal, volumetric, rheological.
            The headers should be filled out with the x and y labels which are the names of the conditions or the labels of the data (e.g. time, temperature, frequency, strain, conductivity, dielectric strength, etc.). The data should be a list of (x, y) tuples. For example, if the property is 24 MPa at temperature 25°C and 30 MPa at temperature 50°C, the data should be [(25, 24), (50, 30)]. If no data is mentioned, please fill it with null.
            """,
        "only-image_single-image":
            f"""Given the image and the following polymer nanocomposite sample compositions, first identify which sample composition is present in the image then extract its properties.
                    
                    Sample Compositions:
                    {sample_compositions}

                    For those sample compositions that are present in the image, extract the information about the property. The extracted information should be in JSON format as follows:

                    {{
                        "property name": "property_name",
                        "headers": ["", ""],
                        "data": []
                    }}

                     Properties is a list of dictionaries where each dictionary represents a property of the nanocomposite. The property name should be filled out with the name of the property where the choicese are: electrical, mechanical, viscoealstic, thermal, volumetric, rheological.
                    The headers should be filled out with the x and y labels which are the names of the conditions or the labels of the data (e.g. time, temperature, frequency, strain, conductivity, dielectric strength, etc.). The data should be a list of (x, y) tuples. For example, if the property is 24 MPa at temperature 25°C and 30 MPa at temperature 50°C, the data should be [(25, 24), (50, 30)]. If no data is mentioned, please fill it with null.
                    
                    Expand the sample composition JSONs to include the property information and return all the expanded JSONs.""",
        "only-image_multi-image":
            f"""Given the images and the following polymer nanocomposite sample compositions, first identify which sample compositions are present in the images then extract their properties.

                    Sample Compositions:
                    {sample_compositions}

                    For those sample compositions that are present in the images, extract the information about the property. The extracted information should be in JSON format as follows:

                    {{
                        "property name": "property_name",
                        "headers": ["", ""],
                        "data": []
                    }}

                    Properties is a list of dictionaries where each dictionary represents a property of the nanocomposite. The property name should be filled out with the name of the property where the choicese are: electrical, mechanical, viscoealstic, thermal, volumetric, rheological.
                    The headers should be filled out with the x and y labels which are the names of the conditions or the labels of the data (e.g. time, temperature, frequency, strain, conductivity, dielectric strength, etc.). The data should be a list of (x, y) tuples. For example, if the property is 24 MPa at temperature 25°C and 30 MPa at temperature 50°C, the data should be [(25, 24), (50, 30)]. If no data is mentioned, please fill it with null.
                    
                    Expand the sample composition JSONs to include the property information and return all the expanded JSONs."""
    }
    
    return prompt_dict