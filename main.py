import ollama
llm = "qwen2.5"

stream = ollama.generate(
    model=llm,
    prompt='what time is it?',
    stream=True
)

for chunk in stream:
    print(chunk['response'], end='', flush=True)
    
    
from langchain_community.tools import DuckDuckGoSearchResults 

def search_web(query:str) -> str: 
    return DuckDuckGoSearchResults(backend='news').run(query)


tool_search_web = {
    'type':'function',
    'function':{
        'name':'search_web',
        'description':'search the web for the given query',
        'parameters':{
            'type':'object',
            'properties':{
                'query':{
                    'type':'string',
                    'description':'the query to search for'
                }
            },
            'required':['query']
        }
    }
}

result = search_web(query='nvidia')
print(result)

def search_yf(query:str) -> str:
    engine = DuckDuckGoSearchResults(backend='news')
    return engine.run(f"site:finance.yahoo.com {query}")

tool_search_yf = {
    'type':'function',
    'name':'search_yf',
    'description': 'Search for specific financial news',
  'parameters': {'type': 'object',
                'required': ['query'],
                'properties': {
                    'query': {'type':'str', 'description':'the financial topic or subject to search'},
                
}
                }
}

search_yf(query='nvidia')

prompt = '''You are an assistant with access to tools, you must decide when to use tools to answer user message.''' 
messages = [{"role":"system",
             "content":prompt}]

while True:
    
    try:
        q = input('hey enter inputs > ')
    except EOFError:
        break
    
    if q == 'quit':
        break 
    if q.strip() == "":
        continue
    
    messages.append( {"role":"user",
                      "content":q})
    
    agent_res = ollama.chat(
        model=llm,
        stream=False,
        tools=[tool_search_web,tool_search_yf],
        messages=messages
    )
    
    dic_tools = {'search_web':search_web, 'search_yf':search_yf}

    if hasattr(agent_res["message"], "tool_calls") and agent_res["message"].tool_calls:
        for tool in agent_res["message"].tool_calls:
            t_name, t_inputs = tool["function"]["name"], tool["function"]["arguments"]
            if f := dic_tools.get(t_name):
                ### calling tool
                print('🔧 >', f"\x1b[1;31m{t_name} -> Inputs: {t_inputs}\x1b[0m")
                messages.append( {"role":"user", "content":"use tool '"+t_name+"' with inputs: "+str(t_inputs)} )
                ### tool output
                t_output = f(**tool["function"]["arguments"])
                print(t_output)
                ### final res
                p = f'''Summarize this to answer user question, be as concise as possible: {t_output}'''
                res = ollama.generate(model=llm, prompt=q+". "+p)["response"]
            else:
                print('🤬 >', f"\x1b[1;31m{t_name} -> NotFound\x1b[0m")
 
    if agent_res['message']['content'] != '':
        res = agent_res["message"]["content"]
     
    print("👽 >", f"\x1b[1;30m{res}\x1b[0m")
    messages.append( {"role":"assistant", "content":res} )
            
            
    