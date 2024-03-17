from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain

@tool
def get_columns(file_name: str) -> list:
    """Get columns from xlsx file. Output list of column name"""
    import pandas as pd

    dataframe = pd.read_excel(file_name)
    return dataframe.columns.tolist()

@tool
def generate_cleaning_code(actions:str, cols:list) -> str:
    """Generate cleaning code using open ai. Input is the actions to perform and the available list of columns in the excel file. Output is a string of code."""
        
    openai = ChatOpenAI( model="gpt-4-0125-preview", temperature = 0) # Add your openai api key here
    template = """The excel has the following columns {cols}.

    Write a react code to do the following cleaning operations:

    {question}

    Use the following code template:

    ```typescript
    {code}
        ```

    make sure to convert the types of item to the appropriate type before performing any operations on them.
    Also handle any null values with ? operator.
        
    Provide only the code without any explanations.     
    """


    prompt = PromptTemplate.from_template(template)
    prompt = prompt.partial(code = """ <NuvoImporter
    licenseKey="Your License Key"
    settings={\{
        developerMode: true,
        identifier: "customer_data",
        columns: [
        {
            label: "Customer Code",
            key: "customer_code",
            columnType: "string",
        },
        {
            label: "Phone Number",
            key: "phone_number",
            columnType: "string",
        },
        ],
    }}
    columnHooks={{
        phoneNumber: (values) => {
        values.map(([item, index]) => {
            let phoneNumber = item;
            if (/^[0]{{2}}/.test(phoneNumber)) {
            phoneNumber = `+${item.slice(2, item.length)}`;
            }
            return [
            {
                value: phoneNumber,
                info: [
                {
                    message:
                    'We have automatically transformed your input into the correct format by converting "00" to "+".',
                    level: "info",
                },
                ],
            },
            index,
            ];
        });
        },
    }}
    >
    Import data
    </NuvoImporter>""")
    prompt = prompt.partial(cols= cols)
    llm_chain = LLMChain(llm=openai, prompt=prompt)
    output = llm_chain.invoke(actions)
    return output["text"]


