import os
import signal
import sys
from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import successText, errorText


def cleanup_and_exit(signum, frame):
    """Remove the chat history file and exit."""
    try:
        if os.path.exists('.current_chat.txt'):
            os.remove('.current_chat.txt')
            print(successText(f"\n✅ Removed chat history file: {'.current_chat.txt'}"))
    except Exception as e:
        print(errorText(f"Error cleaning up chat file: {str(e)}"))
    sys.exit(0)

 
signal.signal(signal.SIGINT, cleanup_and_exit)    
signal.signal(signal.SIGTERM, cleanup_and_exit)  

def startCodeSession(firstPrompt: str):
    try:
        

        
       
        model_response = modelInteraction(firstPrompt)
        
   
        if model_response:
            with open('.current_chat.txt', "a") as f:
                f.write('YOU(MODEL): ' + model_response + '\n')
            
            print(model_response)
            continueChat()
        
    except PermissionError:
        print('Could not start a chat session - permission error')
    except Exception as e:
        print(f'Error starting chat session: {str(e)}')
    

def continueChat():
    newPrompt = input('> ')
    
    try:
       
        with open('.current_chat.txt', 'r') as f:
            chatHistory = f.read()
        
         
        model_response = modelInteraction(chatHistory + "USER: " + newPrompt)
        
      
        if model_response:
            with open('.current_chat.txt', 'a') as f:
                f.write('USER: ' + newPrompt + '\n')
                f.write('YOU(MODEL): ' + model_response + '\n')
            
            print(model_response)
            continueChat()
        
    except FileNotFoundError:
        print('Error: Chat history file not found')
        print('Exiting now, please start a new session')
        quit()
    except Exception as e:
        print(f'Error continuing chat: {str(e)}')
        print('Exiting now, please start a new session')
        quit()