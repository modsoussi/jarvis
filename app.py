import kernel
import os
import prompts.sys
from playwright.sync_api import sync_playwright

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
  action_agent = kernel.CompletionAgent(
    config=kernel.Config(
      openai_key=os.getenv("OPENAI_API_KEY"),
      model="gpt-4",
      system_prompt=prompts.sys.action_gen
    )
  )

  with sync_playwright() as p:
    try:
      user_input = input(">> ")
      if user_input == ":q":
        exit(0)
      
      browser = kernel.Browser(p)
      context = []
      
      while True:
        action = kernel.Action(action_agent.get_completion(user_input, context), browser=browser)
        print(action.desc())
        result = action.exec()
        
        if action.action_type == kernel.ACTION_TYPE_FINAL:
          print(result)
          browser.close()
          exit(0)
        
        context.append((action.desc(), result))
    
    except EOFError:
      if browser is not None:
        browser.close()
      exit(0)
    except KeyboardInterrupt:
      if browser is not None:
        browser.close()
      exit(0)
